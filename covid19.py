# -*- coding: utf-8 -*-
#
# Created by Pádraig Mac Carron
#
#################
#Import Libraries
import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit
import datetime
from read_wiki_data import read_wiki
from read_wiki_data import get_population
###############




###############
#Countries

'''Add the name of any country as it appears on Wikipedia
    to this list in the same format'''

countries = ['Italy',
             'Ireland',
             'United_Kingdom',
##             'France',
##             'Germany',
##             'United_States',
##             'Iran',
             'Spain',
##             'South_Korea',
##             'COUNTRY',
##             'OTHER_COUNTRY',
##             'Japan',
##             'Netherlands',
              ]

###############
#Inputs

              
'''Enter 'logistic' to fit logistic, enter None for no fit
    and 'exp' (or anything else!) to get exponential'''
fit = 'logistic'#None


#The minimum number of cases to start from (the first few points might be more noise)
# Use 15 if using US data, 30 for South Korea or Japan
min_cases = 10


#Start fitting from this point (early values might not be accurate)
fit_start = 3


#Extend fit this many days to see the trajectory
fit_pred = 5


#Normalise by population
''' Enter True to normalise by population and show per million'''
norm = False


''' Change death to true to plot deaths instead of number of cases'''
# Currently no death column in the Irish dataset on wikipedia
death = False#True


'''Change to False for linear scale, 'log' for log scale'''
yscale = 'log'


###############
#Less important

'''TIME defaults to the number of days since min_cases infections,
 put in 'date' to plot from a certain date abd then choose that date below'''
# Note that starting from a specific date, the fits won't be accurate
# as it will use the number of days for the x value
TIME = False#'date'

#if TIME is 'date', need to choose the date to start plotting from
date = '2020-02-01'


#The marker size for the plot
ms = 5


#Fraction of population that can be infected in logistic model
# (i.e. cut-off parameter), this just bounds the cut-off so it can't
# go above that when fitting (not really necessary)
frac = 0.6



############
#Functions

#Exponential
def exp(x,a,b):
    return a*np.exp(b*x)

#Linear
def linear(x,a,b):
    return a + b*x

#Logistic
def logistic(x,a,b,c):
    return c/(1 + a*np.exp(-b*x))


############
#Get Data

#Use ggplot style
#plt.style.use('ggplot')

#Change values associated with figsize to change figure dimensions
plt.figure(figsize=(7,6))
ax = plt.gca()


case = 'cases' if death!=True else 'deaths'
date = datetime.datetime.strptime(date,'%Y-%m-%d')


#Iterate through countries list
for country in countries:

    #Ireland is actaully down as 'Republic_of_Ireland' so fix that
    if country == 'Ireland':
        #Calls the functions from the other script to get the data
        dates, cases, deaths, death_dates = read_wiki('Republic_of_'+country)
        population = get_population('Republic_of_'+country)
    else:
        dates, cases, deaths, death_dates = read_wiki(country)
        population = get_population(country)

    #If plotting deaths instead of number of cases
    if death == True:
        cases = deaths
        dates = death_dates

    #Create an empty list for time to get number of days rather than dates
    time = []
    
    #Iterate through the dates
    for i,l in enumerate(dates):
        if cases[i] >= min_cases:
            #Check how to plot
            if TIME == 'date':
                #This subtracts the number of days from each date
                # from the date chosen at the start
                time += [(datetime.datetime.strptime(l,'%Y-%m-%d') - date).days]
            else:
                #This adds the first day to the list and gets the date
                # associated with that t0
                if len(time) == 0:
                    time += [0]
                    t0 = datetime.datetime.strptime(l,'%Y-%m-%d')
                else:
                    #For dates after the first date, subtract number
                    # of days from t0 to get the number of days since
                    time += [(datetime.datetime.strptime(l,'%Y-%m-%d')-t0).days]


    #Get the cases list for above the minimum number chosen
    cases = [u for u in cases if u >= min_cases]

    #Check if wanted to normalise
    if norm == True:
        #Normalise by population per million
        # (change 1e6 to say 1e5 if want 100,000 instead of million
        cases = [u/(population/1e6) for u in cases]

            
    #Fits a line to the semi-log data
    linear_fit = curve_fit(linear,time[fit_start:],  np.log(cases[fit_start:]),p0=[1,0.1])

    #Gets the exponential growth parameter
    b = round(linear_fit[0][1],2)

    #If fit is selected
    if fit != None:
        if fit == 'logistic':
            #This factor is for the bounds when fitting
            factor = 1
            if norm == True:
                factor = 1e-3
            #Logistic fit, p0 are the initial estimates, I put bounds in to confine the parameter space a little
            logistic_fit = curve_fit(logistic,time[fit_start:],  cases[fit_start:], method='trf',
                                 p0=[2,0.1,max(cases)],bounds=(0,(1000000,1,frac*population*factor)))

        #b = round(logistic_fit[0][1],2)

        print('\n\n=================')
        print('Country:',country)
        print('Population:',population)
        print('Total',case+': ',cases[-1],'(',
              cases[-1]-cases[-2],'on',dates[-1],')')
        print('Percentage infected:',round(cases[-1]/population,4))

        #Get the x and y for the fit
        x = np.arange(time[fit_start],max(time)+1+fit_pred,1)
        y_fit = exp(x,np.exp(linear_fit[0][0]),linear_fit[0][1])
        exp_pred = y_fit[-fit_pred]
        if fit == 'logistic':
            y_fit = logistic(x,logistic_fit[0][0],logistic_fit[0][1],logistic_fit[0][2])
            #Prints the country, the last number of cases, the
            # logistic cutoff and the growth parameter
            print('\nLogistic Growth fit:')
            if fit_pred>0:
                print('Predicted tomorrow:',int(y_fit[-fit_pred]),
                  '(',int(y_fit[-fit_pred]-cases[-1])
                      ,'new cases )')
                guess_log = int(y_fit[-fit_pred]-cases[-1])

            b_log = round(logistic_fit[0][1],2)
            print('Cutoff parameter:',round(logistic_fit[0][2],1),'   Growth parameter:',b)
        if fit != None:
            if fit != 'logistic' or int(y_fit[-fit_pred]-cases[-1]) < cases[-1]-cases[-2]:
                #Prints the country, the last number of cases and the
                # exponential growth parameter
                print('\nExponential Growth fit:')
                if fit_pred > 0:
                    print('Predicted tomorrow:',int(exp_pred),
                      '(',int(exp_pred-cases[-1]),'new cases )')
                    guess_exp = int(exp_pred-cases[-1])
                print('Exponential growth parameter:',b)

    
    #Keeps Ireland green!!
    if country == 'Ireland':
        color = '#2ca02c'
    else:
        #Cycles through colours
        color=next(ax._get_lines.prop_cycler)['color']

    if color == '#2ca02c' and country != 'Ireland':# and 'Ireland' in countries:
        color=next(ax._get_lines.prop_cycler)['color']


    #Plot the data
    plt.plot(time,cases, 'o', label=country, color=color, ms=ms,alpha=0.9)#+' ('+str(b)+')',color=color)
    if fit != None:
        #Plot the fit
        plt.plot(x,y_fit, ':',color=color,alpha=0.6)



##################
#Figure details


#Shows gridlines with some transparency
plt.grid(True,which='both',linestyle=':',alpha=0.7)

plt.xlim(-1)#,34)
#plt.ylim(8,100000)
plt.legend()

#Show the y-axis on a log scale
plt.yscale(yscale)


#Axis labels under various conditions
if norm == True:
    plt.ylabel('Number of '+case+' per million',fontsize=17)
else:
    plt.ylabel('Number of '+case,fontsize=16)

if TIME == 'date':
    plt.xlabel('Number of days since '+str(date).split()[0],fontsize=16)
elif death == True:
    plt.xlabel('Number of days since '+str(min_cases)+' deaths recorded',fontsize=15)
else:
    plt.xlabel('Number of days since '+str(min_cases)+' cases',fontsize=16)


#Display the figure
plt.show()


