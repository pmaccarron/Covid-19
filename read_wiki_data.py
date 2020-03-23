# -*- coding: utf-8 -*-
#
# Created by Pádraig Mac Carron
#
################################
#Import Libraries
import urllib.request
import urllib.error
import urllib.parse
import time
################################



########################
#Gets page data

user = "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/29.0.1547.66 Safari/537.36"
def connect(url):    
    req = urllib.request.Request(url, data=payload, headers={'User-Agent' : user})
    try:
        con = urllib.request.urlopen(req)
    except urllib.error.HTTPError:
        time.sleep(10)
        try:
            con = urllib.request.urlopen(req)
        except urllib.error.HTTPError:
            return 0
    except urllib.error.URLError:
        time.sleep(120)
        try:
            con = urllib.request.urlopen(req)
        except urllib.error.HTTPError:
            return 0
                    
    return con

#####################

payload = b'"DSCOVERYDATA"="[{\"datasources\":[{\"ischecked\":true,\"hitcount\":642,\"searchstate\":-1,\"page\":1,\"pagelength\":10,\"fields\":[\"RefNo\",\"Title\",\"Description\"],\"name\":\"Catalog\",\"fullname\":\"DServe.Catalog\",\"description\":\"Catalog\",\"record\":{\"datasourcename\":\"\",\"position\":0,\"id\":null,\"fields\":null,\"xmlstring\":null},\"xmlstring\":\"\",\"htmlstring\":\"\",\"elementset\":\"DC\",\"expression\":\"((Description=rector)OR(Title=rector))\",\"keyfield\":\"RefNo\",\"searchcommand\":\"rector\"},{\"ischecked\":false,\"hitcount\":-1,\"searchstate\":-1,\"page\":0,\"pagelength\":10,\"fields\":[\"Code\",\"PersonName\",\"Dates\"],\"name\":\"Persons\",\"fullname\":\"DServe.Persons\",\"description\":\"Persons\",\"record\":{\"datasourcename\":\"\",\"position\":0,\"id\":null,\"fields\":null,\"xmlstring\":null},\"xmlstring\":\"\",\"htmlstring\":\"\",\"elementset\":\"DC\",\"expression\":\"\",\"keyfield\":\"Code\",\"searchcommand\":\"\"},{\"ischecked\":false,\"hitcount\":-1,\"searchstate\":-1,\"page\":0,\"pagelength\":10,\"fields\":[\"Code\",\"Set\",\"Notes\"],\"name\":\"Places\",\"fullname\":\"DServe.Places\",\"description\":\"Places\",\"record\":{\"datasourcename\":\"\",\"position\":0,\"id\":null,\"fields\":null,\"xmlstring\":null},\"xmlstring\":\"\",\"htmlstring\":\"\",\"elementset\":\"DC\",\"expression\":\"\",\"keyfield\":\"Code\",\"searchcommand\":\"\"}],\"name\":\"DServe\",\"ischecked\":\"True\"}]"&"__EVENTTARGET"=""&"__EVENTARGUMENT"=""&"__"DSCoveryPagerBar1"="{\"id\":\"ctl00$main$DSCoveryPagerBar1\",\"classAttribute\":\"\",\"visible\":\"\",\"value\":\"\",\"datasource\":\"DServe.Catalog\",\"start\":1,\"end\":642,\"size\":10,\"current\":1}"&"__VIEWSTATE"="/wEPDwUKMjEyNjA5OTI3Ng9kFgJmD2QWAgIDD2QWCgIBDw8WCh4RTWVkaXVtRm9udFRvb2xUaXBlHhBMYXJnZUZvbnRUb29sVGlwZR4STGFyZ2VzdEZvbnRUb29sVGlwZR4IQ3NzQ2xhc3MFGUZvbnRTaXplU3dpdGNoZXJDb250YWluZXIeBF8hU0ICAmRkAgMPDxYEHwMFFlN0eWxlU3dpdGNoZXJDb250YWluZXIfBAICZGQCBQ9kFgICAQ9kFgRmD2QWAmYPDxYGHghJbWFnZVVybAXKAS9TdFBhdHJpY2tzQ29sbGVnZS9DYWxtVmlldy9XZWJSZXNvdXJjZS5heGQ/ZD0tcG54TVZSSjJ6azFGQ1g3V3lMTk9zTGhnTmNqSklaRHpROER3NWFxOVo1MFNjZ1BqLVZ5c1RUbW8taHRIMGhoTGIwd3NKYk0tZWNLNlQ0OFdocGhNUmNmSGF2QkVaWlJtUTJZZEEzVWhXSlNvUE4wYzlsUm5oLWlaVXd4QmlvMWZjMzdRQTImdD02MzM4NzkyODU2MjAwMDAwMDAeDUFsdGVybmF0ZVRleHQFCVNlYXJjaGluZx4HVG9vbFRpcAUJU2VhcmNoaW5nZGQCAg9kFgJmDw8WBB4RVXNlU3VibWl0QmVoYXZpb3JoHg1PbkNsaWVudENsaWNrBRR2b2lkKG51bGwpOzsgcmV0dXJuO2RkAgkQPCsADQIADxYCHgtfIURhdGFCb3VuZGdkDBQrAAIFAzA6MBQrAAIWDh4EVGV4dAUPQWR2YW5jZWQgU2VhcmNoHgVWYWx1ZQUPQWR2YW5jZWQgU2VhcmNoHwcFFEFkdmFuY2VkIFNlYXJjaCBNZW51HgdFbmFibGVkZx4KU2VsZWN0YWJsZWgeCERhdGFQYXRoBSRkNGJkNjY0Zi0xNmQ2LTRjNjMtYjJjZi1hZjc4MzU0NTgzYjQeCURhdGFCb3VuZGcUKwACBQMwOjAUKwACFhAfCwUJQ2F0YWxvZ3VlHwwFCUNhdGFsb2d1ZR4LTmF2aWdhdGVVcmwFPC9TdFBhdHJpY2tzQ29sbGVnZS9DYWxtVmlldy9hZHZhbmNlZC5hc3B4P3NyYz1EU2VydmUuQ2F0YWxvZx8HBRVTZWFyY2ggb3VyIGNhdGFsb2d1ZS4fDWcfDmcfDwU8L3N0cGF0cmlja3Njb2xsZWdlL2NhbG12aWV3L2FkdmFuY2VkLmFzcHg/c3JjPWRzZXJ2ZS5jYXRhbG9nHxBnZGRkAhMPZBYCAgEPFgIfCwUOU2VhcmNoIFJlc3VsdHNkGAEFHl9fQ29udHJvbHNSZXF1aXJlUG9zdEJhY2tLZXlfXxYBBQ1jdGwwMCR0dndNZW51yOFj5WSAPgBAvvHtiq0BJOZ+KEA="&"__VIEWSTATEGENERATOR"="BC890391"&"DS__SystemStateBag"=""&"ctl00$search$DSCoverySearch1$ctl00$SearchText"="rector"&"__CALLBACKID"="ctl00$main$DSCoveryContainer1"&"__CALLBACKPARAM"=""'                 


def read_wiki(country):
    url = 'https://en.wikipedia.org/wiki/Template:2019%E2%80%9320_coronavirus_pandemic_data/'+country+'_medical_cases_chart'

    dates, cases, deaths, death_dates = [], [], [], []
    used_date = []
    flag = 0
    con = connect(url)
    for line in con:
        if b'<b>Date<' in line:
            flag = 1
        if flag == 1:
            if b'style="padding-left:0.4em' in line:
                l = line.strip().split(b':center">')[1]
                if b'block' in line:
                    l = l.split(b'block">')[1].split(b'<')[0].decode('utf-8').replace(',','')
                else:
                    l = l.split(b'<')[0].decode('utf-8')

                if '-' in l:
                    dates += [l]
                    
                else:
                    if len(cases) < len(dates):
                        cases += [int(l)]
                    if len(cases) == len(dates) and l.isnumeric() and int(l) < int(cases[-1]):
                        deaths += [int(l)]
                        death_dates += [dates[-1]]

    return [dates,cases,deaths,death_dates]

#date,cases,deaths,death_dates = read_wiki('Republic_of_Ireland')

def get_population(country):
    url = 'https://en.wikipedia.org/wiki/' + country

    con = connect(url)

    for line in con:
        if b'Population' in line:
            try:
                pop = int(line.split(b'data-file-width="300" data-file-height="300" />')[1].strip().split(b'<')[0].replace(b',',b''))
            except ValueError:
                pop = int(line.split(b'estimate</div></th><td>')[1].strip().split(b'<')[0].replace(b',',b''))
                
            #pop = int(line.split(b'Population</th><td>')[1].split()[0].replace(b',',b''))
            break
    return pop

