import pandas as pd
import numpy as np
import time

CITY_DATA = {'chicago': 'chicago.csv',
             'new york': 'new_york_city.csv',
             'washington': 'washington.csv'}

restart = '\n Type \'r\' to restart or \'yes\' to continue. '


def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """

    print('Hello! Let\'s explore some US bikeshare data!',
          'Would you like to see data for Chicago, New York, or Washington?', sep='\n')
    # Get user input for city (chicago, new york city, washington).
    city = input().lower()
    # While loop to handle invalid inputs
    while city not in ['chicago', 'new york', 'washington']:
        print('Try again.',
              'Would you like to see data for Chicago, New York, or Washington? ', sep='\n')
        city = input().lower()
    print('Would you like to filter the data by month, day, both or not at all? Type \'n\' for no time filter.')
    filter = input().lower()
    # While loop to handle invalid inputs
    while filter != 'month' and filter != 'day' and filter != 'both' and filter != 'n':
        print('Incorrect answer.',
              'Please type \'month\', \'day\', \'both\' or \'n\'.', sep='\n')
        filter = input().lower()
    if filter == 'month':
        # Choose month
        print('Which month? Please type your response as an integer (with January=1, February=2, etc.)')
        month = int(input())
        # While loop to handle invalid inputs
        while month not in [n for n in range(1, 7)]:
            print('Please type your response as an integer (with January=1, February=2, ..., June=6)')
            month = int(input())
        day = 'all'
    elif filter == 'day':
        # Choose day
        print('Which day? Please type your response as an integer (with Monday=0, Sunday=6).')
        day = int(input())
        # While loop to handle invalid inputs
        while day not in [n for n in range(7)]:
            print(
                'Please choose an integer (\'Mon\' = 0,\'Tue\' = 1,\'Wed\' = 2,\'Thu\' = 3,\'Fri\' = 4,\'Sat\' = 5,\'Sun\' = 6).')
            day = int(input())
        month = 'all'
    elif filter == 'both':
        # Choose month
        print('Which month? Please type your response as an integer (with January=1, February=2, etc.)')
        month = int(input())
        # While loop to handle invalid inputs
        while month not in [n for n in range(1, 7)]:
            print('Please type your response as an integer (with January=1, February=2, ..., June=6)')
            month = int(input())
        # Choose day
        print('Which day? Please type your response as an integer (with Monday=0, Sunday=6).')
        day = int(input())
        # While loop to handle invalid inputs
        while day not in [n for n in range(7)]:
            print(
                'Please choose an integer (\'Mon\' = 0,\'Tue\' = 1,\'Wed\' = 2,\'Thu\' = 3,\'Fri\' = 4,\'Sat\' = 5,\'Sun\' = 6).')
            day = int(input())

    else:
        month = 'all'
        day = 'all'
    # Check if user choose the right parameters

    dict_months = {1: 'January', 2: 'February', 3: 'March', 4: 'April', 5: 'May', 6: 'June', 'all': 'All'}
    dict_days = {0: 'Monday', 1: 'Tuesday', 2: 'Wednesday', 3: 'Thursday', 4: 'Friday', 5: 'Saturday', 6: 'Sunday',
                 'all': 'All'}
    day = dict_days.get(day)
    print(' Is it a right statistical parameters:\n city - {},\n month - {},\n day - {}?'.format(city.title(),
                                                                                                 dict_months.get(month),
                                                                                                 day),
          restart)
    test = input()
    if test == 'r':
        main()
    print('-' * 40)
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
    # Load the data into a pandas DataFrame
    df = pd.read_csv(CITY_DATA[city])
    print("Accessing data from: ", city.title())
    # Convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(arg=df['Start Time'], format='%Y-%m-%d %H:%M:%S')
    # Filter by month if applicable
    if month != 'all':
        # extract month from Start Time to create new columns
        df['month'] = df['Start Time'].dt.month

        # Update dataframe with month filter
        df = df.loc[df['month'] == month]
    # Filter by day if applicable
    if day.lower() != 'all':
        # extract day of week from Start Time to create new columns
        df['day_of_week'] = df['Start Time'].dt.weekday_name

        # Update dataframe with day filter
        df = df.loc[df['day_of_week'] == day]

    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # Convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(arg=df['Start Time'], format='%Y-%m-%d %H:%M:%S')
    # Create new columns for month, day, hour
    month = df['Start Time'].dt.month
    day_name = df['Start Time'].dt.weekday_name
    hour = df['Start Time'].dt.hour

    # Display the most common month
    most_common_month = month.mode()[0]
    print('Most common month: ', most_common_month)
    # Display the most common day of week
    most_common_day_of_week = day_name.mode()[0]
    print('Most common day of week: ', most_common_day_of_week)

    # Display the most common start hour
    common_start_hour = hour.mode()[0]
    print('Most popular start hour: ', common_start_hour)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-' * 40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # Ddisplay most commonly used start station
    top_start_station = df['Start Station'].describe()
    print('Most commonly used start station: {}. Count: {}.'.format(top_start_station[2], top_start_station[3]))
    # Display most commonly used end station
    top_end_station = df['End Station'].value_counts().idxmax()
    count_top_end_station = df['End Station'].describe()[3]
    print('Most commonly used end station: {}. Count: {}.'.format(top_end_station, count_top_end_station))
    # Display most frequent combination of start station and end station trip
    combination_stations = 'from ' + df['Start Station'] + ' to ' + df['End Station']
    most_popular_trip = combination_stations.describe()
    print('Most popular trip:\n{}. Count: {}.'.format(most_popular_trip[2], most_popular_trip[3]))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-' * 40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # Display total travel time
    total_travel_time = df['Trip Duration'].sum()
    # Convert seconds to years, months, days, minutes, seconds
    sec_to_year = total_travel_time // (365 * 86400)
    sec_to_day = total_travel_time // 86400 - 365 * sec_to_year
    sec_to_hour = total_travel_time // 3600 - sec_to_day * 24 - sec_to_year * 365 * 24
    sec_to_minute = (total_travel_time // 60) % 60
    seconds = total_travel_time % 60
    print(
        'Years: {}, Days: {}, Hours: {}, Mins: {}, Secs: {}'.format(sec_to_year, sec_to_day, sec_to_hour, sec_to_minute,
                                                                    seconds))
    # Display mean travel time
    mean_travel_time = df['Trip Duration'].mean()
    print('\nMean travel time: {} seconds'.format(mean_travel_time))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-' * 40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    count_types = df['User Type'].value_counts()
    print('\nUser Type\t\tCount', count_types, sep='\n')
    # Display counts of gender
    if 'Gender' not in df:
        print('No gender data for this city.')
    else:
        count_gender = df.groupby('Gender', as_index=False).count()
        print('\nGender\tCount', count_gender, sep='\n')
    # Display earliest, most recent, and most common year of birth
    if 'Birth Year' not in df:
        print('No birth year data for this city.')
    else:
        birth_year = df['Birth Year'].describe()
        common_birth_year = df['Birth Year'].mode()[0]
        print("\nEarliest year of birth: {} ".format(birth_year[3]),
              "Most recent year of birth: {} ".format(birth_year[7]),
              "Most common year of birth: {} ".format(common_birth_year),
              sep='\n')

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-' * 40)


def raw_data(df):
    user_input = input('\nDo you want to see raw data? Enter yes or no.\n')
    line_number = 0

    while True:
        if user_input.lower() != 'no':
            line_number += 5
            print(df.head(line_number))
            user_input = input('\nDo you want to see more raw data? Enter yes or no.\n')
        else:
            break


def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        raw_data(df)

        restart2 = input('\nWould you like to restart? Enter yes or no.\n')
        if restart2.lower() != 'yes':
            break


if __name__ == "__main__":
    main()
