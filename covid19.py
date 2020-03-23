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
##             'Ireland',
             'United_Kingdom',
##             'France',
             'Germany',
##             'United_States',
##             'Iran',
             'Spain',
##             'South_Korea',
##             'COUNTRY',
##             'OTHER_COUNTRY',
              ]

###############
#Inputs

              
'''Enter 'logistic' to fit logistic, enter None for no fit
    and 'exp' (or anything else!) to get exponential'''
fit = 'logistic'#None


#The minimum number of cases to start from (the first few points might be more noise)
# Use 15 if using US data, 30 for South Korea
min_cases = 10


#Extend fit this many days to see the trajectory
fit_pred = 5


#Normalise by population
''' Enter True to normalise by population and show per million'''
norm = False#True


''' Change death to true to plot deaths instead of number of cases'''
# Currently no death column in the Irish dataset on wikipedia
death = False#True


#Start fitting from this point (early values might not be accurate)
fit_start = 2


'''TIME defaults to the number of days since min_cases infections,
 put in 'date' to plot from a certain date abd then choose that date below'''
# Note that starting from a specific date, the fits won't be accurate
# as it will use the number of days for the x value
TIME = False#'date'

#if TIME is 'date', need to choose the date to start plotting from
date = datetime.datetime(2020,2,1)


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
#Change values associated with figsize to change figure dimensions
plt.figure(figsize=(7,6))

#Shows gridlines with some transparency
plt.grid(alpha=0.5)
ax = plt.gca()


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

        #Get the x and y for the fit
        x = np.arange(time[fit_start],max(time)+1+fit_pred,1)
        y_fit = exp(x,np.exp(linear_fit[0][0]),linear_fit[0][1])
        if fit == 'logistic':
            y_fit = logistic(x,logistic_fit[0][0],logistic_fit[0][1],logistic_fit[0][2])
            #Prints the country, the last number of cases, the
            # logistic cutoff and the growth parameter
            print(country,cases[-1],logistic_fit[0],y_fit[-1])
        else:
            #Prints the country, the last number of cases and the
            # exponential growth parameter
            print(country,cases[-1],y_fit[-1])

    #Cycles through colours
    color=next(ax._get_lines.prop_cycler)['color']

    #Keeps Ireland green!!
    if color == '#2ca02c' and country != 'Ireland' and 'Ireland' in countries:
        color=next(ax._get_lines.prop_cycler)['color']
    if country == 'Ireland':
        color = '#2ca02c'

    #Plot the data
    plt.plot(time,cases, 'o', label=country, color=color, ms=ms)#+' ('+str(b)+')',color=color)
    if fit != None:
        #Plot the fit
        plt.plot(x,y_fit, ':',color=color)



##################
#Figure details


plt.xlim(-1)
#plt.ylim(8,100000)
plt.legend()

#Show the y-axis on a log scale
plt.yscale('log')


#Axis labels under various conditions
if norm == True:
    plt.ylabel('Number of cases per million',fontsize=17)
else:
    if death == True:
        plt.ylabel('Number of deaths',fontsize=16)
    else:
        plt.ylabel('Number of cases',fontsize=16)

if TIME == 'date':
    plt.xlabel('Number of days since 1st February',fontsize=16)
else:
    plt.xlabel('Number of days since 10 cases',fontsize=16)


#Display the figure
plt.show()

