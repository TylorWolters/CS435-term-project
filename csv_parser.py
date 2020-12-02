#Tylor Wolters, siu853377382

#Objective-2 will be to create a UI where a user can select/define the parameters on which to search this database 
#(e.g., specific date, county, state, number of cases/deaths more/less than N, etc.). 
#Based on the specified user parameters, your tool will create a visualization of the data on a county-level map of the US.
#imports
from datetime import date
import pandas as pd
import numpy as np
from dateutil.relativedelta import relativedelta



#initializers
death_data = pd.read_csv('covid_deaths_usafacts.csv', delimiter = ',')
death_data.columns.values[1] = "county_name"

case_data = pd.read_csv('covid_confirmed_usafacts.csv', delimiter = ',')
case_data.columns.values[1] = "county_name"

population_data = pd.read_csv('covid_county_population_usafacts.csv', delimiter = ',')
population_data.columns.values[1] = "county_name"



#[[GOAL]] EXAMPLE_CALL:
#   [[Today's date, searchable in the csv files]] make_working_date("today",0)
#   [[the date from 2 weeks ago, '' ]] make_working_date("week",2)

#functions
#data: population_data, death_data, or case_file csv file.
#option: today, week, month
#time: (if using week or month, give how many weeks or months back you are pulling from.)
def make_working_date(data,option,time): 
    def zero_slayer(usable_current_date): #removes leading zeros from date. EXAMPLE: 11/04/20 -> 11/4/20 || 02/05/21 -> 2/5/21 http://y2u.be/3EPeyOiicvU
        if(usable_current_date[0] == '0'):
            usable_current_date = usable_current_date[1:]
            if(usable_current_date[2] == '0'):
                usable_current_date = usable_current_date[:2] + usable_current_date[3:]
        if(usable_current_date[3] == '0'):
            usable_current_date = usable_current_date[:3] + usable_current_date[4:] 
        return usable_current_date      
    header_length =len(list(data.columns.values))
    most_recent = data.columns.values[header_length-1]
    today = most_recent
    if option == "today": #returns todays date, formatted for csv file use.
        return zero_slayer(today)
    
    else: #if a date a month or a week back (however long specified, can be several of either)
        if option == "week":
            usable_date = date.today() + relativedelta(weeks=-time)
        if option == "month":
            usable_date = date.today() + relativedelta(months=-time)
        return zero_slayer(((str(usable_date)[5:7] + "/" +str(usable_date)[8:10]+"/"+str(usable_date)[2:4]))) 


#[[GOAL]] EXAMPLE_CALL:
#   [[Covid cases from today from Illinois]] working_title("today",0,"state","Illinois","none")
#   [[Change in cases from today compared to 3 months ago from Illinois]] working_title("month",3,"state","Illinois","none")
#   [[Covid cases change from 2 weeks ago in Cook County, Illinois]] working_title("week",2,"county","Illinois","Cook County")

#data: population_data, death_data, or case_file csv file.
#time_size: today, week, month. 
#time_distance: (if using week or month for time size, give how many weeks or months back you are pulling from.)
#size_option: state, county, nationwide.
#state: IL, AL, KY, WI etc...
def working_title(data,time_size,time_distance,size_option,state,county):

    if size_option == "state": #Takes a state and returns either: the total cases/death in that state today, or compares cases from a week or more back in time.
        state_counties = data[data.State==state]

        if time_size == "today":#cases, deaths, or total population for a given state, with most recent data.
            return sum(state_counties.loc[:,make_working_date(data,time_size,time_distance)])
        
        if (time_size == "week") or (time_size == "month"):#cases, deaths, or total population for a given state, with most recent data compared to however far back.
            current_state_data = sum(state_counties.loc[:,make_working_date(data,"today",0)])
            previous_state_data = sum(state_counties.loc[:,make_working_date(data,time_size,time_distance)])
            change = current_state_data - previous_state_data
            return change
    
    if size_option == "county":
            county = data[data.county_name == county] 
            final_county = county[county.State ==state]

        if time_size == "today": #cases, deaths, or total population for given county in a given state, with most recent data.
            return sum(final_county.loc[:,make_working_date(data,"today",0)])
        
        if (time_size == "week") or (time_size == "month"):#cases, deaths, or total population for a given state, with most recent data compared to however far back.
            current_county_data = sum(final_county.loc[:,make_working_date(data,"today",0)])
            previous_county_data = sum(final_county.loc[:,make_working_date(data,time_size,time_distance)])
            return (current_county_data - previous_county_data)
