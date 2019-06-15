import time
import pandas as pd
import numpy as np

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }

months = ['january','february','march','april','may','june']
days = ['sunday','monday','tuesday','wednesday','thursday','friday','saturday']

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

    while True:
        city = input('Enter the city to filter on (chicago, new york city, or washington): ').lower()
        if CITY_DATA.get(city,False):
            break
        else:
            print('That is not a valid city.')

    # get user input for month (all, january, february, ... , june)
    while True:
        month = input('Enter the month to filter on (January through June), or "all" for no filter: ').lower()
        if month == 'all':
            break
        elif month in months:
            break
        else:
            print('That is not a valid month.')

    # get user input for day of week (all, monday, tuesday, ... sunday)
    while True:
        day = input('Enter the day of the week to filter on, or "all" for no filter: ').lower()
        if day == 'all':
            break
        elif day in days:
            break
        else:
            print('That is not a valid weekday.')

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
        df - Pandas DataFrame containing city data filtered by month and day
    """
    # load data file into a dataframe
    df = pd.read_csv(CITY_DATA[city])

    # convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    # extract month and day of week from Start Time to create new columns
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.weekday_name

        # filter by month if applicable
    if month != 'all':
        # use the index of the months list to get the corresponding int
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
    # display the most common month
    df['month'] = df['Start Time'].dt.month
    common_month = df['month'].mode()[0]
    print('\nMost common month: ', months[common_month-1].title())

    # display the most common day of week
    df['day_of_week'] = df['Start Time'].dt.weekday_name
    common_weekday = df['day_of_week'].mode()[0]
    print('\nMost common day of week: ', common_weekday)

    # display the most common start hour
    df['hour'] = df['Start Time'].dt.hour
    common_hour = df['hour'].mode()[0]
    print('\nMost common start hour: ', common_hour)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    start_stations = df['Start Station'].mode()[0]
    print('\nMost common start station: ', start_stations)

    # display most commonly used end station
    end_stations = df['End Station'].mode()[0]
    print('\nMost common end station: ', end_stations)

    # display most frequent combination of start station and end station trip
    df['Start-End'] = df['Start Station'] + ' to ' + df['End Station']
    common_trip = df['Start-End'].mode()[0]
    print('\nMost frequent combination of start station and end station trip: ', common_trip)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    total_travel_time = df['Trip Duration'].sum() / 60
    print('\nTotal travel time in this period in minutes: ', int(total_travel_time))

    # display mean travel time
    mean_travel_time = df['Trip Duration'].mean() / 60
    print('\nAverage (mean) travel time in this period in minutes: ', int(mean_travel_time))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    user_types = df['User Type'].value_counts()
    print('\nCount of users by type: \n\n',user_types)
    # Display counts of gender
    try:
        gender = df['Gender'].value_counts()
        print('\nCount of users by gender: \n\n',gender)
    except:
        pass

    # Display earliest, most recent, and most common year of birth
    try:
        earliest_birth_year = int(df['Birth Year'].min())
        recent_birth_year = int(df['Birth Year'].max())
        common_birth_year = int(df['Birth Year'].mode()[0])

        print('\nEarliest birth year: \n\n',earliest_birth_year)
        print('\nMost recent birth year: \n\n',recent_birth_year)
        print('\nMost common birth year: \n\n',common_birth_year)
    except:
        pass

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def raw_data(df):
    """Displays 5 lines of raw data. Queries user to repeat."""

    while True:
        raw_data = input('\nWould you like to see 5 rows of raw data? Enter yes or no.\n')
        #Prints 5 rows of data if the user enters 'yes', then prompts if user wants to see more data
        if raw_data.lower() =='yes':
            start_time = time.time()
            print('Preparing 5 random rows of data...\n')
            print(df.sample(n=5))
            print("\nThis took %s seconds." % (time.time() - start_time))
            print('-'*40)
        #Response if user enters something other than 'yes' or 'no'
        elif raw_data.lower() !='no':
            print('\nYou entered an invalid response.\n')
            continue
        #Exits if 'no' is entered
        else:
            break

def main():
    """Executes the program"""
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        raw_data(df)

        #Checks if the user wants to restart the program.
        while True:
            restart = input('\nWould you like to restart? Enter yes or no.\n')
            if restart.lower() == 'no':
                return False
            elif restart.lower() == 'yes':
                print('\n\n\n')
                break
            #Response if user enters something other than 'yes' or 'no'
            else:
                print('\nYou entered an invalid response.')
                continue
if __name__ == "__main__":
	main()
