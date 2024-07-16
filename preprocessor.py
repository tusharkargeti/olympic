import pandas as pd


def preprocess():
    df = pd.read_csv(r'athlete_events.csv')
    region_df = pd.read_csv(r'noc_regions.csv')

    # Filter for Summer Olympics
    df = df[df['Season'] == 'Summer']

    # Merge with region data
    df = df.merge(region_df, on='NOC', how='left')
    df.drop_duplicates(inplace=True)

    # Create dummy variables for medals
    df = pd.concat([df, pd.get_dummies(df['Medal']).astype(int)], axis=1)

    return df

