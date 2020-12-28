import time
import pandas as pd
import numpy as np
import sys
from os import system, name

# included 'new york' and 'new york city' on purpose
CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv',
              'new york': 'new_york_city.csv' }

MONTH_DATA = { 1 : 'january', 2: 'february',
              3 : 'march', 4 : 'april',
              5 : 'may', 6 : 'june' }

DAY_DATA = {0: 'monday', 1 : 'tuesday', 2: 'wednesday',
            3 : 'thursday', 4 : 'friday', 5: 'saturday', 6: 'sunday'}


# clear helper function - needs os module
def clear():
    # win
    if name == 'nt': _ = system('cls')
    # mac/linux
    else: _ = system('clear')

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    #print('\n')
    print('\n'+'-'*50)
    print('Hello! Let\'s explore some US bikeshare data!')
    print('-'*50+'\n\n')
    # get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    city=None
    while city not in CITY_DATA:
        city=input("Enter the city you would like to investigate. Enter city name (Chicago, New York, Washington) or number (1, 2, 3).\n\tEnter city ['quit' to exit]: "'").lower()
        if city.isnumeric() and 1 <= int(city) <= 3:
            city=list(CITY_DATA.keys())[int(city)-1]
        if city=='quit':
            sys.exit()
    # get user input for month (all, january, february, ... , june)
    month=None
    while month not in MONTH_DATA.values() and month != 'all':
        month=input("Filter data by month? Enter full month name (January...June), month number (1...6) or'all' to include all months.\n\tEnter month ['quit' to exit]: ").lower()
        if month.isnumeric():
            month=MONTH_DATA.get(int(month),None)
        if month=='quit':
            sys.exit()

    # get user input for day of week (all, monday, tuesday, ... sunday)
    day=None
    while day not in DAY_DATA.values() and day != 'all':# day not in MONTH_DATA.values() and month != 'all':
        day=input("Filter data by weekday? Enter full day name (Monday...Sunday), day number (0...6) or'all' to include all weekdays.\n\tEnter weekday ['quit' to exit]: ").lower()
        if day.isnumeric():
            day=DAY_DATA.get(int(day),None)
        if day=='quit':
            sys.exit()

    print('-'*50+'\n')

    return city, month, day


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
    df = pd.read_csv(CITY_DATA[city])

    # convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    # extract month and day of week from Start Time to create new columns
    df['month'] = df['Start Time'].dt.month
    df['dayofweek'] = df['Start Time'].dt.dayofweek
    # also extract start hour for time_stats functions
    df['hour'] = df['Start Time'].dt.hour

    # set default values for month and day num (used for pretty output)
    month_num='all'
    day_num='all'
    # filter by month if applicable
    if month != 'all':
        month_num = dict(zip(MONTH_DATA.values(), MONTH_DATA.keys()))[month]
        df = df[df['month']==month_num]

    # filter by day of week if applicable
    if day != 'all':
        day_num = dict(zip(DAY_DATA.values(), DAY_DATA.keys()))[day]
        df = df[df['dayofweek']==day_num]

    # set col and index names
    df.rename(columns={'Unnamed: 0' : 'id'},inplace=True)
    df.rename_axis('index',inplace=True)

    print('\nData loaded for {} and filtered by month={}/{} and weekday={}/{}'.format(city.title(), month, month_num, day, day_num))
    print('-'*50+'\n')

    return df


def time_stats(df):
    """
    Displays statistics on the most frequent times of travel.

    Args:
        df - Pandas DataFrame containing city data filtered by month and day
    """

    print('Calculating The Most Frequent Times of Travel:\n')
    start_time = time.time()

    # Note: i know this can be done using the mode() method, however i wanted to try grouping as well

    # display the most common month
    # create temp data series of month number and count
    temp=df.groupby(['month'])['month'].count()
    print('\tMost common month: {}/{}'.format(MONTH_DATA[temp.idxmax()].title(), temp.idxmax()))
    # display the most common day of week
    # create temp data series of day of week and count
    temp=df.groupby(['dayofweek'])['dayofweek'].count()
    print('\tMost common day of week: {}/{}'.format(DAY_DATA[temp.idxmax()].title(), temp.idxmax()))
    # display the most common start hour
    # create temp data series of start hour and count
    temp=df.groupby(['hour'])['hour'].count()
    print('\tMost common start hour: {}'.format(temp.idxmax()))

    print('\nThis took %s seconds.' % (time.time() - start_time))
    print('-'*50+'\n')


def station_stats(df):
    """
    Displays statistics on the most popular stations and trip.

    Args:
        df - Pandas DataFrame containing city data filtered by month and day
    """

    print('Calculating The Most Popular Stations and Trip:\n')
    start_time = time.time()

    # display most commonly used start station
    print('\tMost common start station: {}'.format(df['Start Station'].mode()[0]))

    # display most commonly used end station
    print('\tMost common end station: {}'.format(df['End Station'].mode()[0]))

    # display most frequent combination of start station and end station trip
    # Note: i know this can be done using the value_counts() method, however i wanted to try grouping and selecting the top-most result
    temp=df.groupby(['Start Station', 'End Station']).size().sort_values(ascending=False)
    print('\tMost common trip is: {} -> {} ({} rides) '.format(*temp.index[0], temp[0]))

    print('\nThis took %s seconds.' % (time.time() - start_time))
    print('-'*50+'\n')


def trip_duration_stats(df):
    """
    Displays statistics on the total and average trip duration.

    Args:
        df - Pandas DataFrame containing city data filtered by month and day
    """

    print('Calculating Trip Duration:\n')
    start_time = time.time()

    # display total travel time
    print('\tTotal travel time: {}'.format(pd.Timedelta(df['Trip Duration'].sum(), unit='seconds')))

    # display mean travel time
    print('\tMean travel time: {}'.format(pd.Timedelta(df['Trip Duration'].mean(), unit='seconds')))

    print('\nThis took %s seconds.' % (time.time() - start_time))
    print('-'*50+'\n')


def user_stats(df):
    """
    Displays statistics on bikeshare users.

    Args:
        df - Pandas DataFrame containing city data filtered by month and day
    """

    print('Calculating User Stats:\n')
    start_time = time.time()

    # Display counts of user types
    print('\tUsers by type:')
    for i,v in df.value_counts('User Type').items():
        print('\t\t{}: {}'.format(i,v))

    # Check if gender col is present in data. If yes, display counts of gender
    if 'Gender' in df.columns:
        print('\tUsers by gender:')
        for i,v in df.value_counts('Gender').items():
            print('\t\t{}: {}'.format(i,v))
    # Check if birth date col is present in data. If yes, display earliest, most recent, and most common year of birth
    if 'Birth Year' in df.columns:
        print('\tUser's YOB stats:')
        print('\t\tearliest: {:.0f}\n\t\tmost recent: {:.0f}\n\t\tmost common: {:.0f}'.format(
            df['Birth Year'].min(),
            df['Birth Year'].max(),
            df['Birth Year'].mode()[0] ))


    print('\nThis took %s seconds.' % (time.time() - start_time))
    print('-'*50+'\n')

def print_data(df, city, month, day):
    """
    Prints filtered data. 5 rows per user input.

    Args:
        df - Pandas DataFrame containing city data filtered by month and day
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """

    # display all columns using continuation symbol \ in terminal
    pd.options.display.max_columns = None
    # init local vars
    pos=0
    showdata=None

    # loop through data frame
    while pos<df.index.size:
        # query input from user
        while showdata==None or showdata not in ['yes', 'y', 'no', 'n']:
            showdata = input('Would you like to view {} raw data? Enter yes/y or no/n.\n\t'.format('some' if pos==0 else 'more')).lower()
        # quit if user does not want to show more data
        if showdata in ['no', 'n']:
            return
        # print raw data as well as current index position and applied filter
        print('\nShowing rows {} to {} of {} total rows.\nFilter applied: city={}, month={}, day={}:\n'.format(pos+1,pos+5 if pos+5<=df.index.size else df.index.size, df.index.size,city.title(),month,day))
        print(df.iloc[pos:pos+5 , :df.columns.size-3])
        print('-'*50+'\n')
        # setup local vars for next loop
        pos+=5
        showdata=None
    else:
        # let user know if data frome is output completely and there is no more data to show
        print('Reached end of file. No more data to show.')
        print('-'*50+'\n')



def main():
    """
    This is the main entry point of the script.
    """

    while True:

        clear()
        # get user input
        city, month, day = get_filters()
        # calculate stats and display data
        df = load_data(city, month, day)
        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        print_data(df, city, month, day)

        # query input from user asking to restart or quit
        restart=None
        while restart==None or restart not in ['yes', 'y', 'no', 'n']:
            restart = input('Would you like to restart? Enter yes/y or no/n.\n\t').lower()
        if restart in ['no', 'n']:
            break

# the "pythonic way" of C-like main(), yikes
if __name__ == "__main__":
	main()
