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
    print('Hello! Let\'s explore some US bikeshare data!\n')
    # get user input for city (chicago, new york city, washington).
    #HINT: Use a while loop to handle invalid inputs
    city_name =''
    while city_name not in CITY_DATA :
        print('We can only process data for Chicago, New Your City and Washington.\n')
        print('Please pick Chicago, New York City (NYC) or Washington.\n')
        city_name = input('Please enter the city of your choice: \n')
        if str(city_name).lower() in CITY_DATA :
            city = str(city_name).lower()
            break
        elif str(city_name).lower() == 'nyc':
            city = 'new york city'
            break
    # get user input for month (all, january, february, ... , june)
    months = ['all', 'january', 'february', 'march', 'april', 'may', 'june']
    month =''
    while month not in months:
        print('Would you like to filter data based on month.\n')
        print('Please pick a month betwen January and June or \"all\" for no filters.\n')
        month = input('Please enter your choice of month:\n')
        if month.lower() in months:
            month=month.lower()
            break

    # get user input for day of week (all, monday, tuesday, ... sunday)
    days = ['all', 'monday', 'tuesday', 'wednesday', 'thursday', 'friday','saturday', 'sunday']
    day = ''
    while day not in days:
        print('Would you like to filter data based on a specific day.\n')
        print('Please pick a day or \"all\" for no filters.\n')
        day = input('Please enter your day:\n')
        if day.lower() in days:
            day=day.lower()
            break

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
    df = pd.read_csv(CITY_DATA[city])
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    # extract month and day of week from Start Time to create new columns
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.day_name() #weekday_name
##SOURCE --> https://stackoverflow.com/questions/60214194/error-in-reading-stock-data-datetimeproperties-object-has-no-attribute-week

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

    # display the most common month
    popular_month = df['month'].mode()[0]
    month_list = ['january', 'february', 'march', 'april', 'may', 'june']
    print('The Most Popular Travel Month is: ', month_list[popular_month-1].upper())

    # display the most common day of week
    popular_day = df['day_of_week'].mode()[0]
    print('The Most Popular Travel Day is: ', popular_day.upper())

    # display the most common start hour
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    df['hour'] = df['Start Time'].dt.hour
    popular_hour = df['hour'].mode()[0]
    print('The Most Popular Travel Start Hour is: ', popular_hour)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    popular_start_station = df['Start Station'].mode()[0]
    print('The Most Popular Start Station is: ', popular_start_station)
    # display most commonly used end station
    popular_end_station = df['End Station'].mode()[0]
    print('The Most Popular End Station is: ', popular_end_station)
    pd.set_option('max_columns', None)
    #print(df.head())
    # display most frequent combination of start station and end station trip
    #Source --> http://net-informations.com/ds/pd/comb.htm
    df['start_to_end'] = df['Start Station'] + ' -TO- ' + df['End Station']
    #print(df['start_to_end'].head())
    print('The most popular route is from', df['start_to_end'].mode()[0])
    count=0
    for i in df['start_to_end']:
        if i == "Lake Shore Dr & Monroe St -TO- Lake Shore Dr & Monroe St":
            count+=1

    print("count is", count)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

#New function to split seconds into hours, minutes and seconds
def seconds_to_hour_mins(total_trip_duration):
    hours=int(total_trip_duration / 3600)
    minutes=int((total_trip_duration - hours*3600) / 60)
    seconds = int(total_trip_duration - hours*3600 - minutes*60)
    return hours, minutes, seconds

def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    total_trip_duration=df['Trip Duration'].sum()
    hours, minutes, seconds = seconds_to_hour_mins(total_trip_duration)
    print("Total Trip duration is {} hours : {} minutes : {} seconds.".format({hours},{minutes},{seconds}))

    # display mean travel time
    mean_travel_time = df['Trip Duration'].mean()
    hours, minutes, seconds = seconds_to_hour_mins(mean_travel_time)
    print("Mean Travel time is  {} hours : {} minutes : {} seconds.".format({hours},{minutes},{seconds}))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    print('Break down of users:\n', df['User Type'].value_counts())

    # Display counts of gender
    try:
        print('\nBreak down of gender:\n', df['Gender'].value_counts())
    except KeyError:
        print("There is no Gender data available in this case")

    # Display earliest, most recent, and most common year of birth
    try:
        earliest_year = int(df['Birth Year'].min())
        print("\nThe earliest Birth Year is: ", earliest_year)

        recent_year = int(df['Birth Year'].max())
        print("The most recent Birth Year is: ", recent_year)

        common_year = int(df['Birth Year'].mode())
        print("The most common Birth Year is: ", common_year)
    except KeyError:
        print("There is no Birth Year data available in this case")

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def wait_for_next_stats():
    for i in [1,2,3,4]:
        print(".",end='')
        time.sleep(1)

def disaply_raw_data(df):
    print('We can display 5 lines of raw data at a time.')
    print('Would you like to display 5 lines of raw data?')
    yes_no =input('Answer with YES or NO:').lower()
    line_count = 0

    while line_count < len(df):
        if yes_no not in ['yes', 'no']:
            print('Please answer with only YES or NO!!')
            yes_no =input('Answer with YES or NO:').lower()
        elif yes_no == 'yes':
            pd.set_option('max_columns', None)
            if line_count+5 < len(df):
                print(df[line_count: line_count+5])
            else:
                print(df[line_count: line_count+(len(df) - line_count)])
                print('These were the last lines of data.')
                break
            line_count+=5
            yes_no =input('\n5 more line of raw data?\nYES or NO:').lower()
        elif yes_no == 'no':
            print('Got it!')
            break



def main():
    while True:
        #city, month, day = get_filters()
        city='nyc'
        month='june'
        day = 'monday'
        df = load_data(city, month, day)

        disaply_raw_data(df)
        time_stats(df)
        #wait_for_next_stats()
        #station_stats(df)
        #wait_for_next_stats()
        #trip_duration_stats(df)
        #wait_for_next_stats()
        #user_stats(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
