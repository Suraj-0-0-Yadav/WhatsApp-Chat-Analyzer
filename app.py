from os import link
import streamlit as st
import preprocess
import stats
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import re

st.set_page_config(page_title="WhatsApp Chat Analyser")
st.sidebar.title("WhatsApp Chat Analyzer")

text_file = st.sidebar.file_uploader("Chose a file")

if text_file is not None:
    bytes_data = text_file.getvalue()

    data = bytes_data.decode("utf-8")

    df = preprocess.preprocess(data)

    all_user = df['User'].unique().tolist()
    all_user.remove("Group Notification")
    all_user.sort()
    all_user.insert(0,"Overall")

    user_name = st.sidebar.selectbox(
        "Show analysis with",
        all_user
    )

    st.title("WhatsApp Chat Analysis for "+user_name)

    if st.sidebar.button("Show Analysis"):

        no_msg,no_words,media_omiited,links=stats.fetchstats(user_name,df)

        col1,col2,col3,col4 = st.columns(4)

        with col1:
            st.header("Total Message")
            st.title(no_msg)
        with col2:
            st.header("Total no. of words")
            st.title(no_words)
        with col3:
            st.header("Media Shared")
            st.title(media_omiited)
        with col4:
            st.header("Total Links Shared")
            st.title(links)
        
        if user_name == "Overall":

            st.title("Most Busy User")
            busy_count , new_df = stats.fetch_busy_user(df)

            col1,col2 = st.columns(2)

            with col1:
                fig,ax = plt.subplots()
                ax.bar(busy_count.index,busy_count.values,color='red')
                plt.xticks(rotation='vertical')
                st.pyplot(fig)
            with col2:
                st.dataframe(new_df)
        
        # Word Cloud
        st.title("Word Cloud")
        img = stats.create_word_cloud(user_name,df)
        fig,ax = plt.subplots()
        ax.imshow(img)
        st.pyplot(fig)

        # Most common words
        st.title("Most Common Words")
        mc_words = stats.get_common_words(user_name,df)
        fig,ax = plt.subplots()
        ax.barh(mc_words['words'],mc_words['counts'])
        plt.xticks(rotation='vertical')
        ax.set_xlabel("Number of words")
        ax.set_ylabel("Most Common words")
        st.pyplot(fig)

        # Most Common Wmoji
        st.title("Most Common Emoji")
        mc_emoji_df = stats.get_emoji_stats(user_name,df)
        st.dataframe(mc_emoji_df)
        
        # Monthly time line
        st.title("Monthly Timeline")
        mt_df = stats.month_time_line(user_name,df)
        fig, ax = plt.subplots()
        ax.plot(mt_df['time'], mt_df['Message'], color='green')
        plt.xticks(rotation='vertical')
        plt.tight_layout()
        st.pyplot(fig)

        # Activity Map
        st.title("Activity Maps")

        col1, col2 = st.columns(2)

        with col1:

            st.header("Most Busy Day")

            busy_day = stats.week_activity(user_name,df)

            fig, ax = plt.subplots()
            ax.bar(busy_day.index, busy_day.values, color='purple')
            plt.xticks(rotation='vertical')
            plt.tight_layout()
            st.pyplot(fig)
        with col2:

            st.header("Most Busy Month")
            busy_month = stats.month_activity(user_name,df)

            fig, ax = plt.subplots()
            ax.bar(busy_month.index, busy_month.values, color='orange')
            plt.xticks(rotation='vertical')
            plt.tight_layout()
            st.pyplot(fig)