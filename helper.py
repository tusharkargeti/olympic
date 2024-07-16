import pandas as pd

def men_vs_women(df):
    athlete_df = df.drop_duplicates(subset=['Name', 'region'])
    men_athlete = athlete_df[athlete_df['Sex'] == 'M'].groupby('Year').count()['Name'].reset_index()
    women_athlete = athlete_df[athlete_df['Sex'] == 'F'].groupby('Year').count()['Name'].reset_index()

    final = men_athlete.merge(women_athlete, on='Year', how='left')
    final.rename(columns={"Name_x": 'Male', 'Name_y': 'Female'}, inplace=True)

    final.fillna(0, inplace=True)
    return final

def weight_height(df, sport):
    athlete_df = df.drop_duplicates(subset=['Name', 'region'])
    athlete_df['Medal'].fillna('No medal', inplace=True)
    if sport != 'overall':
        temp_df = athlete_df[athlete_df['Sport'] == sport]
        return temp_df
    else:
        return athlete_df

def yearwise_medal_tally(df, country):
    temp_df = df.dropna(subset=['Medal'])
    temp_df = temp_df.drop_duplicates(subset=['Team', 'NOC', 'Year', 'City', 'Sport', 'Event', 'Medal'])
    new_df = temp_df[temp_df['region'] == country]
    final_df = new_df.groupby('Year').count()['Medal'].reset_index()
    return final_df

def country_event_heatmap(df, country):
    temp_df = df.dropna(subset=['Medal'])
    temp_df = temp_df.drop_duplicates(subset=['Team', 'NOC', 'Year', 'City', 'Sport', 'Event', 'Medal'])
    new_df = temp_df[temp_df['region'] == country]
    pt = new_df.pivot_table(index='Sport', columns='Year', values='Medal', aggfunc='count').fillna(0).astype('int')
    return pt

def preprocess():
    df = pd.read_csv('path_to_athlete_events.csv')
    region_df = pd.read_csv('path_to_noc_regions.csv')

    # Filter for Summer Olympics
    df = df[df['Season'] == 'Summer']

    # Merge with region data
    df = df.merge(region_df, on='NOC', how='left')
    df.drop_duplicates(inplace=True)

    # Create dummy variables for medals
    df = pd.concat([df, pd.get_dummies(df['Medal']).astype(int)], axis=1)

    return df

def participating_nations_over_time(df):
    if 'region' in df.columns:
        nations_over_time = df.drop_duplicates(['Year', 'region'])['Year'].value_counts().reset_index()
        nations_over_time.columns = ['Year', 'Number_of_Countries']
        nations_over_time = nations_over_time.sort_values('Year')
        return nations_over_time
    else:
        raise KeyError("The 'region' column is missing in the DataFrame.")

def data_over_time(df, col):
    if 'region' in df.columns:
        data_over_time = df.drop_duplicates(['Year', col])['Year'].value_counts().reset_index()
        data_over_time.columns = ['Year', col]
        data_over_time = data_over_time.sort_values('Year')
        return data_over_time
    else:
        raise KeyError("The 'region' column is missing in the DataFrame.")

def country_Year_list(df):
    years = df['Year'].unique().tolist()
    years.sort()
    years.insert(0, 'overall')

    countries = df['region'].dropna().unique().tolist()
    countries.sort()
    countries.insert(0, 'overall')

    return years, countries

def fetch_medal_tally(df, year, country):
    medal_df = df.drop_duplicates(subset=['Team', 'NOC', 'Year', 'City', 'Sport', 'Event', 'Medal'])

    flag = 0
    if year == 'overall' and country == 'overall':
        temp_df = medal_df
    if year == 'overall' and country != 'overall':
        flag = 1
        temp_df = medal_df[medal_df['region'] == country]
    if year != 'overall' and country == 'overall':
        temp_df = medal_df[medal_df['Year'] == int(year)]
    if year != 'overall' and country != 'overall':
        temp_df = medal_df[(medal_df['Year'] == int(year)) & (medal_df['region'] == country)]

    if flag == 1:
        x = temp_df.groupby('Year').sum()[['Gold', 'Silver', 'Bronze']].sort_values('Year').reset_index()
    else:
        x = temp_df.groupby('region').sum()[['Gold', 'Silver', 'Bronze']].sort_values('Gold', ascending=False).reset_index()

    x['total'] = x['Gold'] + x['Silver'] + x['Bronze']

    return x
