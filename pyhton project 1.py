#!/usr/bin/env python
# coding: utf-8

# In[275]:


import time
import pandas as pd
import numpy as np

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }

months = ['January', 'February', 'March', 'April', 'May', 'June']
    
days = ['Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday']

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')
    # TO DO: get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    city = input('please enter the name of city you want to know about\n 1-chicago\n 2-new york city\n 3-washington\n').lower()
    while city not in CITY_DATA.keys():
        city = input('\n pleas enter a valid city name \n').lower()
        for c in city :
            if c[:3]==city[:3] :
                city=c
    filter_time = input('how would you want to get the data filtered by month,day,both or not at all type "none" for no time filter.\n')
    while filter_time.lower() not in ['month', 'day', 'both', 'none']:
        filter_time = input('please enter a valid value.\nhow would you want to get the data filtered by month,day,both or not at all type "none" for no time.\n')
        
    month, day = '', ''
        
    # TO DO: get user input for month (all, january, february, ... , june)
    if filter_time == 'month' or filter_time == 'both':
         
        month = input('what month would you like to choose? Jan, Feb, Mar, Apr, May, or Jun? Type "all" for all months.\n').title()
        
        while month[:3] not in [month[:3] for month in months] and month != 'All': 
            month = input("please enter a valid month name like written in previous line.\n").title()
        for m in months :
            if m[:3]==month[:3] :
                month=m
                
    # TO DO: get user input for day of week (all, monday, tuesday, ... sunday)


    if filter_time == 'day' or filter_time == 'both':
        day = input('what day?? Sun, Mon, Tue, Wed, Thur, or Fri? Type "all" for all days.\n').title()
        
        while day[:3] not in [day[:3] for day in days] and day != 'All': 
            day = input("please enter a vaild day name .\n").title()
    for d in days :
        if d[:3]==day[:3] :
            day=d

    print('-'*40)
    return city, month, day


# In[ ]:





# In[276]:



def load_data(city, month, day):
    """
    Loads data for the specified city and filters by month and day if applicable.

    Args:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    Returns:
        df - Pandas DataFrame containing city data filtered by month and day
    """

    # load data file into a dataframe
    df = pd.read_csv(CITY_DATA[city],parse_dates=["Start Time","End Time"])
                     
    # extract month and day of week from Start Time to create new columns
    df['hour'] = df['Start Time'].dt.hour
    df['day_of_week'] = df['Start Time'].dt.day_name()
    df['month'] = df['Start Time'].dt.month

    # filter by month if applicable
    if month.lower() != 'all'and month.lower()!="":
        # use the index of the months list to get the corresponding int
        month = months.index(month) + 1

        # filter by month to create the new dataframe

        df =df.query("month==@month")

    # filter by day of week if applicable
    if day.lower() != 'all'and day.lower()!="":
        # filter by day of week to create the new dataframe
        df =df.query("day_of_week==@day")
    return df


# In[277]:


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()
    common_month = df['month'].mode()
    common_month = common_month[0]
    common_day = df['day_of_week'].mode()
    common_day =common_day [0]
    common_hour = df['hour'].mode()
    common_hour=common_hour[0]

    # display the most common month
    print('The most common month: {}'.format(common_month))
    
    # display the most common day of week
    print('The most common day: {}'.format(common_day))

    # display the most common start hour
    print(f'The most common hour: {common_hour}')

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


# In[278]:


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()
    common_start_station = df['Start Station'].mode()
    common_start_station =common_start_station[0]
    common_end_station = df['End Station'].mode()
    common_end_station =common_end_station [0]
    common_trip = df[['Start Station', 'End Station']].mode()

    print('Most common Station...\n')
    # display most commonly used start station
    print(f'Start station: {common_start_station}')
    
    # display most commonly used end station
    print(f'End Station: {common_end_station}')
    


    # display most frequent combination of start station and end station trip
    print(' the Most common Trip...\n')
    trips = df['Start Station'] + " to " + df['End Station']
    print('Trip: {}'.format(trips.mode()[0]))



    print("\n it takes %s seconds." % (time.time() - start_time))
    print('-'*40)


# In[279]:


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    total_trip_Duration= df['Trip Duration'].sum()
    print("Total Duration: {}".format(total_trip_Duration))


    # display mean travel time
    mean_trip_Duration = df['Trip Duration'].mean()
    print('Average trip_Duration: {}'.format(mean_trip_Duration))


    print("\nit takes %s seconds." % (time.time() - start_time))
    print('-'*40)


# In[280]:



def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    counts_types = df['User Type'].value_counts()
    for user_type, Count in dict(counts_types).items():
        print(f'{user_type}: {Count}',"\n")


    # Display counts of gender
    if 'Gender' in df.columns:
        GenderCount = df['Gender'].value_counts()
        for Gender, Count in dict(GenderCount).items():
            print(f'{Gender}: {Count}','\n')
        


    # Display earliest, most recent, and most common year of birth
    if 'Birth Year' in df.columns:
        OldestYear = df['Birth Year'].min()
        YoungestYear = df['Birth Year'].max()
        MostPopular = df['Birth Year'].mode()
        MostPopular=MostPopular[0]
        print('The OLdest, YONGEST, and most popular year of birth...')
        print("OldestYear is {}" .format(OldestYear) )
        print('YoungestYear is {}'.format(YoungestYear))
        print('Most popular year is {}'.format(MostPopular))
        


    print("\n it takes %s seconds." % (time.time() - start_time))
    print('-'*40)


# In[281]:


def show_five_rows(df):
    """ showing 5 rows """
    decision = input("do you want to view any trip data???////type yes or no.\n").upper()

    
    Counter = 0
    if decision.lower() == 'yes':    
        for row in df.iterrows():
            for column, value in dict(row[1]).items():
                print('{}: {}'.format(column,value))
            print('-' * 40)
            
            Counter += 1
            if Counter % 5 == 0:
                decision = input("do you want to view any trip data type Type yes or no.\n")
            
            if decision.lower() != 'yes':
                break
    


# In[ ]:


def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        show_five_rows(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        print('-' * 80)
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()


# In[ ]:




