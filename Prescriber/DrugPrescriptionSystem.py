from matplotlib.backends.backend_agg import RendererAgg
import streamlit as st
import numpy as np
import pandas as pd
import xmltodict
from pandas import json_normalize
import urllib.request
import seaborn as sns
import matplotlib
from matplotlib.figure import Figure
from PIL import Image
import gender_guesser.detector as gender
from streamlit_lottie import st_lottie
import requests

st.set_page_config(layout="wide")

def load_lottieurl(url: str):
    r = requests.get(url)
    if r.status_code != 200:
        return None
    return r.json()

lottie_book = load_lottieurl('https://assets4.lottiefiles.com/temp/lf20_aKAfIn.json')
st_lottie(lottie_book, speed=1, height=200, key="initial")


matplotlib.use("agg")

_lock = RendererAgg.lock


sns.set_style('darkgrid')
row0_spacer1, row0_1, row0_spacer2, row0_2, row0_spacer3 = st.columns(
    (.1, 2, .2, 1, .1))

row0_1.title('Analyzing your Drugs')


with row0_2:
    st.write('')

row0_2.subheader(
    'A Streamlit web app by [Raghav Somani & Aryaman Mishra & Siddharth Mehta] Prescribing you top 5 drugs on the basis of the disease which the patient is suffering from.')

row1_spacer1, row1_1, row1_spacer2 = st.columns((.1, 3.2, .1))
with row1_1:
    st.markdown("Hey there! Welcome to Drug Analysis and Recommender App. This app scrapes (and never keeps or stores!) the drugs you've used and analyzes data about your drug list, including estimating the gender breakdown, and looking at the distribution of the age and amount of drug used. After some nice graphs, it tries to recommend a curated drug list to you, if you're on a mobile device, switch over to landscape for viewing ease. Give it a go!")
    st.markdown(
        "**To begin, please enter the link.** 👇")

row2_spacer1, row2_1, row2_spacer2 = st.columns((.1, 3.2, .1))
with row2_1:
    default_username = st.selectbox("Select one of our sample Conditions", (
        "89659767-tyler-richards", "diabetes", "depression", "pain"))
    st.markdown("**or**")
    user_input = st.text_input(
        "Input your own symptoms.")
    need_help = st.expander('Need help? 👉')
    with need_help:
        st.markdown(
            "Having trouble finding your Goodreads profile? Head to the [Goodreads website](https://www.goodreads.com/) and click profile in the top right corner.")

    if not user_input:
        user_input = f"https://www.goodreads.com/user/show/{default_username}"

user_id = ''.join(filter(lambda i: i.isdigit(), user_input))
user_name = user_input.split(user_id, 1)[1].split('-', 1)[1].replace('-', ' ')


@st.cache
def get_user_data(user_id, key='ZRnySx6awjQuExO9tKEJXw', v='2', shelf='read', per_page='200'):
    api_url_base = 'https://www.goodreads.com/review/list/'
    final_url = api_url_base + user_id + '.xml?key=' + key + \
        '&v=' + v + '&shelf=' + shelf + '&per_page=' + per_page
    contents = urllib.request.urlopen(final_url).read()
    return(contents)


user_input = str(user_input)
contents = get_user_data(user_id=user_id, v='2', shelf='read', per_page='200')
contents = xmltodict.parse(contents)

line1_spacer1, line1_1, line1_spacer2 = st.columns((.1, 3.2, .1))

with line1_1:
    if int(contents['GoodreadsResponse']['reviews']['@total']) == 0:
        st.write("Add Drugs.")
        st.stop()

    st.header('Analyzing the History of Drugs')

df = json_normalize(contents['GoodreadsResponse']['reviews']['review'])
u_books = len(df['book.id.#text'].unique())
u_authors = len(df['book.authors.author.id'].unique())
df['read_at_year'] = [i[-4:] if i != None else i for i in df['read_at']]
has_records = any(df['read_at_year'])

st.write('')
row3_space1, row3_1, row3_space2, row3_2, row3_space3 = st.columns(
    (.1, 1, .1, 1, .1))


with row3_1, _lock:
    st.subheader('Drugs Used')
    if has_records:
        year_df = pd.DataFrame(
            df['read_at_year'].dropna().value_counts()).reset_index()
        year_df = year_df.sort_values(by='index')
        fig = Figure()
        ax = fig.subplots()
        sns.barplot(x=year_df['index'],
                    y=year_df['read_at_year'], color='goldenrod', ax=ax)
        ax.set_xlabel('Year')
        ax.set_ylabel('Books Read')
        st.pyplot(fig)


with row3_2, _lock:
    st.subheader("Drug Age")
    fig = Figure()
    ax = fig.subplots()
    sns.histplot(pd.to_numeric(df['book.publication_year'], errors='coerce').dropna(
    ).astype(np.int64), kde_kws={'clip': (0.0, 2020)}, ax=ax, kde=True)
    ax.set_xlabel('Drug')
    ax.set_ylabel('Density')
    st.pyplot(fig)

    avg_book_year = str(
        int(np.mean(pd.to_numeric(df['book.publication_year']))))
    row = df.sort_values(by='book.publication_year', ascending=False).head(1)
    oldest_book = row['book.title_without_series'].iloc[0]
    row_young = df.sort_values(by='book.publication_year').head(1)
    youngest_book = row_young['book.title_without_series'].iloc[0]


st.write('')
row4_space1, row4_1, row4_space2, row4_2, row4_space3 = st.columns(
    (.1, 1, .1, 1, .1))

with row4_1, _lock:
    st.subheader("How Do You Rate Your Reviews?")
    rating_df = pd.DataFrame(pd.to_numeric(df[df['rating'].isin(
        ['1', '2', '3', '4', '5'])]['rating']).value_counts(normalize=True)).reset_index()
    fig = Figure()
    ax = fig.subplots()
    sns.barplot(x=rating_df['index'],
                y=rating_df['rating'], color="goldenrod", ax=ax)
    ax.set_ylabel('Percentage')
    ax.set_xlabel('Your Drug Ratings')
    st.pyplot(fig)

    df['rating_diff'] = pd.to_numeric(df['book.average_rating']) - pd.to_numeric(
        df[df['rating'].isin(['1', '2', '3', '4', '5'])]['rating'])

    difference = np.mean(df['rating_diff'].dropna())
    row_diff = df[abs(df['rating_diff']) == abs(df['rating_diff']).max()]
    title_diff = row_diff['book.title_without_series'].iloc[0]
    rating_diff = row_diff['rating'].iloc[0]
    pop_rating_diff = row_diff['book.average_rating'].iloc[0]

with row4_2, _lock:
    st.subheader("How do Users Rate Your Reviews?")
    fig = Figure()
    ax = fig.subplots()
    sns.histplot(pd.to_numeric(df['book.average_rating'], errors='coerce').dropna(
    ), kde_kws={'clip': (0.0, 5.0)}, ax=ax, kde=True)
    ax.set_xlabel('Drug Ratings')
    ax.set_ylabel('Density')
    st.pyplot(fig)
    st.markdown("Here is the distribution of average rating.")
st.write('')
row5_space1, row5_1, row5_space2, row5_2, row5_space3 = st.columns(
    (.1, 1, .1, 1, .1))

with row5_1, _lock:
    # page breakdown
    st.subheader('Drug Amount Distribution')
    fig = Figure()
    ax = fig.subplots()
    sns.histplot(pd.to_numeric(df['book.num_pages'].dropna()), ax=ax, kde=True)
    ax.set_xlabel('Number of Drugs')
    ax.set_ylabel('Density')
    st.pyplot(fig)

    book_len_avg = round(np.mean(pd.to_numeric(df['book.num_pages'].dropna())))
    book_len_max = pd.to_numeric(df['book.num_pages']).max()
    row_long = df[pd.to_numeric(df['book.num_pages']) == book_len_max]
    longest_book = row_long['book.title_without_series'].iloc[0]



with row5_2, _lock:
    # length of time until completion
    st.subheader('How Quickly do you complete your dose?')
    if has_records:
        df['days_to_complete'] = (pd.to_datetime(
            df['read_at']) - pd.to_datetime(df['started_at'])).dt.days
        fig = Figure()
        ax = fig.subplots()
        sns.histplot(pd.to_numeric(
            df['days_to_complete'].dropna()), ax=ax, kde=True)
        ax.set_xlabel('Days')
        ax.set_ylabel('Density')
        st.pyplot(fig)
        days_to_complete = pd.to_numeric(df['days_to_complete'].dropna())
        time_len_avg = 0
        if len(days_to_complete):
            time_len_avg = round(np.mean(days_to_complete))
        st.markdown("On average, it takes you **{} days** between you drug schedules.")


st.write('')
row6_space1, row6_1, row6_space2, row6_2, row6_space3 = st.columns(
    (.1, 1, .1, 1, .1))


with row6_1, _lock:
    st.subheader('Gender Breakdown')
    # gender algo
    d = gender.Detector()
    new = df['book.authors.author.name'].str.split(" ", n=1, expand=True)

    df["first_name"] = new[0]
    df['author_gender'] = df['first_name'].apply(d.get_gender)
    df.loc[df['author_gender'] == 'mostly_male', 'author_gender'] = 'male'
    df.loc[df['author_gender'] == 'mostly_female', 'author_gender'] = 'female'

    author_gender_df = pd.DataFrame(
        df['author_gender'].value_counts(normalize=True)).reset_index()
    fig = Figure()
    ax = fig.subplots()
    sns.barplot(x=author_gender_df['index'],
                y=author_gender_df['author_gender'], color="goldenrod", ax=ax)
    ax.set_ylabel('Percentage')
    ax.set_xlabel('Gender')
    st.pyplot(fig)
    st.markdown('To get the gender breakdown of the drugs.')
with row6_2, _lock:
    st.subheader("Gender Distribution Over Time")

    if has_records:
        year_author_df = pd.DataFrame(df.groupby(['read_at_year'])[
            'author_gender'].value_counts(normalize=True))
        year_author_df.columns = ['Percentage']
        year_author_df.reset_index(inplace=True)
        year_author_df = year_author_df[year_author_df['read_at_year'] != '']
        fig = Figure()
        ax = fig.subplots()
        sns.lineplot(x=year_author_df['read_at_year'], y=year_author_df['Percentage'],
                     hue=year_author_df['author_gender'], ax=ax)
        ax.set_xlabel('Year')
        ax.set_ylabel('Percentage')
        st.pyplot(fig)
        st.markdown(
            "Here you can see the gender distribution over time to see how you must consume your drugs.")
st.write('')
row7_spacer1, row7_1, row7_spacer2 = st.columns((.1, 3.2, .1))

with row7_1:
    st.header("**Drug List Recommendation**")

    reco_df = pd.read_csv('recommendations_df.csv')
    unique_list_books = df['book.title'].unique()
    reco_df['did_user_read'] = reco_df['goodreads_title'].isin(
        unique_list_books)
    most_in_common = pd.DataFrame(reco_df.groupby('recommender_name').sum(
    )).reset_index().sort_values(by='did_user_read', ascending=False).iloc[0][0]
    avg_in_common = pd.DataFrame(reco_df.groupby('recommender_name').mean(
    )).reset_index().sort_values(by='did_user_read', ascending=False).iloc[0][0]
    most_recommended = reco_df[reco_df['recommender_name'] == most_in_common]['recommender'].iloc[0]
    avg_recommended = reco_df[reco_df['recommender_name'] == avg_in_common]['recommender'].iloc[0]

    def get_link(recommended):
        if '-' not in recommended:
            link = 'https://bookschatter.com/books/' + recommended
        elif '-' in recommended:
            link = 'https://www.mostrecommendedbooks.com/' + recommended + '-books'
        return(link)


    st.markdown('For one last bit of analysis, we scraped a few hundred drug lists from famous hospitals and medical healthcare institutes. We took your list of drugs used by patients earlier and tried to recommend the top 5 drugs based on overall reviews and their usefulness.')

    st.markdown('***')
    st.markdown(
        "Thanks for going through this mini-analysis with me! I'd love feedback on this, so if you want to reach out you can find me on [twitter] (https://twitter.com/tylerjrichards) or my [website](http://www.tylerjrichards.com/).")