import time
import pandas as pd
import numpy as np

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')
    # get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    
    city = input('What city would you like to explore? We can look at New York City, Chicago, or Washington. \n').lower()
    while city not in ['chicago', 'new york city', 'washington']:
        city = input('Please input either New York City, Chicago, or Washington. \n').lower()

    # get user input for month (all, january, february, ... , june)
    month = input('What month would you like to focus on? You can put "all" if you want to see every month. Please note that I only have data from January to June. \n').lower()
    
    while month not in ['january', 'february', 'march', 'april', 'may', 'june', 'all']:
        month = input('Please put in a valid month or "all" to see every month. \n').lower()
        
    # get user input for day of week (all, monday, tuesday, ... sunday)
    day = input('What day of the week would you like to focus on? You can put "all" if you want to see each day. \n').lower()
    
    while day not in ['monday', 'tuesday', 'wednesday', 'thrusday', 'friday', 'saturday', 'sunday', 'all']:
        
        day = input('Please put in a valid day of the week or "all" to see each day. \n').lower()
    print('-'*40)
    
    return city, month, day


def load_data(city, month, day):
    """
    Loads data for the specified city and filters by month and day if applicable.

    Args:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    Returns:
        df - pandas DataFrame containing city data filtered by month and day
    """
    
    # load data file into a dataframe
    df = pd.read_csv(CITY_DATA[city])

    # convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    # extract month and day of week from Start Time to create new columns
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.day_name()


    # filter by month if applicable
    if month != 'all':
        # use the index of the months list to get the corresponding int
        months = ['january', 'february', 'march', 'april', 'may', 'june']
        month = months.index(month) + 1
    
        # filter by month to create the new dataframe
        df = df[df['month'] == month]

    # filter by day of week if applicable
    if day != 'all':
        # filter by day of week to create the new dataframe
        df = df[df['day_of_week'] == day.title()]
    
    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    df['End Time'] = pd.to_datetime(df['End Time'])
    # display the most common month
    df['month'] = df['Start Time'].dt.month
    popular_month = df['month'].mode()[0]
    list_of_months = ['January', 'February', 'March', 'April', 'May', 'June']
    popular_month_name = list_of_months[(popular_month - 1)]
    print('The most common month of travel is',  popular_month_name)


    # display the most common day of week
    
    df['day'] = df['Start Time'].dt.day_name()
    popular_day = df['day'].mode()[0]
    print('The most common day of travel is',  popular_day)
    
    # display the most common start hour
    df['hour'] = df['Start Time'].dt.hour
    popular_hour = df['hour'].mode()[0]
    hour_number = 0
    if popular_hour <= 12:
        hour_number = popular_hour
    else:
        hour_number = popular_hour - 12
    am_pm = ""
    if popular_hour / 12 < 1:
        am_pm = "A.M."
    else:
        am_pm = "P.M."
    
    print('Most Popular Start Hour: ', hour_number, am_pm)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    mode_start = df['Start Station'].mode()[0]
    print('The most commonly used start station is ' + mode_start)
    
    # display most commonly used end station
    mode_end = df['End Station'].mode()[0]
    print('The most commonly used end station is ' + mode_end)

    # display most frequent combination of start station and end station trip
    df['End to End Trip'] = df['Start Station'] + " to " + df['End Station']
    mode_e2e = df['End to End Trip'].mode()[0]
    print('The most frequent combination of start station and end station trip is ' + mode_e2e)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    total_travel_sec = df['Trip Duration'].sum()
    print('The total travel to for all trips is ',  total_travel_sec , " seconds." )
    time_converter(total_travel_sec)
    # display mean travel time
    mean_travel_time = df['Trip Duration'].mean()
    print('The mean travel time is ', mean_travel_time, "seconds.")
    time_converter(mean_travel_time)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def time_converter(time_in_sec):
    """takes a length of time in seconds and converts it into a time in years, days, hours, minutes, and seconds"""
    time_counter = time_in_sec 
    years = 0
    days = 0
    hours = 0
    minutes = 0
    seconds = 0
    # Determine if the number of seconds is greater than the total in one year; 
    # if so, find out how many years' worth of seconds there are and assign that 
    # value to the years variable. Then, deduct the number of seconda already 
    # accounted for by years and repeat for months, days, and hours
    if time_counter >= (365 * 24 * 60 * 60):
        years = int(time_counter / (365 * 24 * 60 * 60))
        time_counter = time_counter - (years * (365 * 24 * 60 * 60))
    if time_counter >= (24 * 60 * 60):
        days = int(time_counter / (24 * 60 * 60))
        time_counter = time_counter - (days * (24 * 60 * 60))
    if time_counter >= (60 * 60):
        hours = int(time_counter / (60 * 60))
        time_counter = time_counter - (hours * (60 * 60))
    if time_counter >= 60:
        minutes = int(time_counter / 60)
        time_counter = time_counter - (minutes * 60)
    seconds = round(time_counter, 2)
        
    print("That's equivalent to", years, "year(s),", days, "day(s),", hours, "hour(s),", minutes, "minute(s), and", seconds, "seconds." )
    
    
    
    
def user_stats(df):
    """Displays statistics on bikeshare users."""
    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    user_types = df['User Type'].value_counts().to_frame()
    print(user_types)

    # Display counts of gender
    try:
        gender_count = df['Gender'].value_counts().to_frame()
        print(gender_count)
    except: 
        print("Sorry, I don't have info on user gender right now")
    # Display earliest, most recent, and most common year of birth
    try:
        earliest_birth = df['Birth Year'].min()
        latest_birth = df['Birth Year'].max()
        mode_birth = df['Birth Year'].mode()[0]
        print('The oldest rider was born in ' + str(int(earliest_birth)))
        print('The youngest rider was born in ' + str(int(latest_birth)))
        print('The most common birth year for all riders is ' + str(int(mode_birth)))
    except:
        print("Sorry, I don't have info on user age right now")

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def call_rows(df): 
    """Allows the user to view the raw data, five rows at a time"""
   
    answer = input('Would you like to view 5 rows of the data?')
    index_start = 0
    index_stop = 5
    while answer == 'yes':
        print(df.iloc[index_start:index_stop])
        index_start = index_start + 5
        index_stop = index_stop + 5
        answer = input('Would you like to view 5 more rows of the data? \n')
    

def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)
        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        call_rows(df)
                  
                
        restart = input('\nWould you like to restart? Enter yes or no.\n')
        while restart.lower() not in ['yes', 'no']:
            restart = input("Sorry, I don't understand. Would you like to restart? Enter yes or no. \n")
        if restart.lower() != 'yes':
            break

if __name__ == "__main__":
	main()