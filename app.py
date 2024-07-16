import streamlit as st
import pandas as pd
import plotly.express as px
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.figure_factory as ff

import preprocessor
import helper


st.sidebar.title('Olympic analysis')
st.sidebar.image(r"https://th.bing.com/th/id/OIP.OuMqmAa-IN26pYjjO3TqbwAAAA?w=272&h=181&c=7&r=0&o=5&dpr=1.3&pid=1.7")
df = preprocessor.preprocess()
user_menu = st.sidebar.radio('Select an option',
                             ('Medal tally', 'Overall Analysis', 'Country-wise Analysis', 'Athlete-wise Analysis'))

# Check if 'region' column exists
if 'region' not in df.columns:
    st.error("The 'region' column is missing. Please check the preprocessing step.")
else:
    if user_menu == 'Medal tally':
        st.sidebar.header('Medal_Tally')
        Year, country = helper.country_Year_list(df)
        selected_Year = st.sidebar.selectbox("Select Year", Year)
        selected_country = st.sidebar.selectbox("Select country", country)
        medal_tally = helper.fetch_medal_tally(df, selected_Year, selected_country)
        if selected_Year == 'overall' and selected_country == 'overall':
            st.title('Overall Tally')
        if selected_Year != 'overall' and selected_country == 'overall':
            st.title('Medal Tally in ' + str(selected_Year))
        if selected_Year == 'overall' and selected_country != 'overall':
            st.title(selected_country + ' overall performance')
        if selected_Year != 'overall' and selected_country != 'overall':
            st.title(selected_country + ' performance in ' + str(selected_Year))
        st.table(medal_tally)

    if user_menu == 'Overall Analysis':
        editions = df['Year'].unique().shape[0] - 1
        cities = df['City'].unique().shape[0]
        sports = df['Sport'].unique().shape[0]
        events = df['Event'].unique().shape[0]
        athletes = df['Name'].unique().shape[0]
        nations = df['region'].unique().shape[0]

        st.title("Top Statistics")
        col1, col2, col3 = st.columns(3)

        with col1:
            st.header("Edition")
            st.title(editions)

        with col2:
            st.header("Cities")
            st.title(cities)

        with col3:
            st.header("Sport")
            st.title(sports)

        col1, col2, col3 = st.columns(3)

        with col1:
            st.header("Event")
            st.title(events)

        with col2:
            st.header("Athlete")
            st.title(athletes)

        with col3:
            st.header("Nation")
            st.title(nations)

        nations_over_time = helper.participating_nations_over_time(df)
        fig = px.line(nations_over_time, x='Year', y='Number_of_Countries')
        st.title('Participating nation over the years')
        st.plotly_chart(fig)

        events_over_time = helper.data_over_time(df, 'Event')
        fig = px.line(events_over_time, x='Year', y='Event')
        st.title('Events over the years')
        st.plotly_chart(fig)

        athletes_over_time = helper.data_over_time(df, 'Name')
        fig = px.line(athletes_over_time, x='Year', y='Name')
        st.title('Athletes over the years')
        st.plotly_chart(fig)

        st.title("No of event over time(Every sport)")
        fig, ax = plt.subplots(figsize=(15, 15))
        x = df.drop_duplicates(['Year', 'Sport', 'Event'])
        ax = sns.heatmap(
            x.pivot_table(index='Sport', columns='Year', values='Event', aggfunc='count').fillna(0).astype('int'),
            annot=True)
        st.pyplot(fig)

    if user_menu == 'Country-wise Analysis':
        st.title('Country-wise Analysis')
        country_list = df['region'].dropna().unique().tolist()
        country_list.sort()
        selected_country = st.selectbox("Select a Country", country_list)
        country_df = helper.yearwise_medal_tally(df, selected_country)
        fig = px.line(country_df, x='Year', y='Medal')
        st.title(selected_country + ' Medal Tally over the years')
        st.plotly_chart(fig)

        st.title(selected_country + ' Excels in following sports')
        pt = helper.country_event_heatmap(df, selected_country)
        fig, ax = plt.subplots(figsize=(15, 15))
        ax = sns.heatmap(pt, annot=True)
        st.pyplot(fig)
    if user_menu == 'Athlete-wise Analysis':
        athlete_df = df.drop_duplicates(subset=['Name', 'region'])
        x1 = athlete_df['Age'].dropna()
        x2 = athlete_df[athlete_df['Medal'] == 'Gold']['Age'].dropna()
        x3 = athlete_df[athlete_df['Medal'] == 'Silver']['Age'].dropna()
        x4 = athlete_df[athlete_df['Medal'] == 'Bronze']['Age'].dropna()

        fig = ff.create_distplot([x1, x2, x3, x4],
                                 ['overall age', 'Gold medalist', 'silver medalist', 'bronze medalist'],

                                 show_hist=False, show_rug=False)
        fig.update_layout(autosize=False, height=600, width=1000)
        st.title('Distribution of Age')
        st.plotly_chart(fig)

        sport_list = df['Sport'].unique().tolist()
        sport_list.sort()
        sport_list.insert(0, 'overall')

        st.title('Height vs Weight')

        selected_sport = st.selectbox('select sport', sport_list)
        temp_df = helper.weight_height(df, selected_sport)
        fig, ax = plt.subplots()

        ax = sns.scatterplot(x=temp_df['Weight'], y=temp_df['Height'], hue=temp_df['Medal'], style=temp_df['Sex'], s=60)
        st.pyplot(fig)

        st.title("Men Women participation over a year")
        final = helper.men_vs_women(df)
        fig = px.line(final,x='Year',y=['Male','Female'])
        fig.update_layout(autosize=False, height=600, width=1000)
        st.plotly_chart(fig)
