import pandas as pd
import numpy as np
from collections import Counter
from wordcloud import WordCloud
from emoji import UNICODE_EMOJI
import re

#################################################################
def fetchstats(user,df):
  if user != "Overall":
    df = df[df['User'] == user]

  num_msg = df.shape[0]

  words=[]
  for msg in df['Message']:
    words.extend(msg.split())
    
  media_omitted = df[df['Message'] == '<Media omitted>'].shape[0]

  links=[]
  for msg in df['Message']:
    links.extend(re.findall('https:\S+',msg)) # links.extend(extract.find_urls(msg))
  
  return num_msg , len(words) , media_omitted , len(links)
#################################################################


def fetch_busy_user(df):

  df = df[df['User'] != "Group Notification"]

  count = df['User'].value_counts()

  new_df = pd.DataFrame(data=(df['User'].value_counts()/df.shape[0])*100)

  return count , new_df


#################################################################


def create_word_cloud(user,df):

  if user != 'Overall':
    df = df[df['User'] == user]

  wc = WordCloud(width=500 , height=500 , min_font_size=10 , background_color = 'white')

  wc_img = wc.generate(df['Message'].str.cat(sep=" "))

  return wc_img

#################################################################

def get_common_words(user,data):

  with open("stop_hinglish.txt",'r') as f:
    stopwords = f.read()
  
  stopwords = stopwords.split("\n")

  if user != "Overall":
    data = data[data['User'] == user]

  temp_df = data[(data['Message'] !='<Media omitted>')]
  temp_df = temp_df[(temp_df['User'] !='Group Notification')]

  words=[]

  for msg in temp_df['Message']:
    for word in msg.lower().split():
      if word not in stopwords and word[0] not in UNICODE_EMOJI:
        words.append(word)


  return pd.DataFrame(data=Counter(words).most_common(20),columns=['words','counts'])
  # return Counter(words)
#################################################################

def get_emoji_stats(user,df):

  if user != 'Overall':
    df = df[df['User'] == user]
  
  emojis=[]

  for msg in df['Message']:
    emojis.extend([c for c in msg if c in UNICODE_EMOJI['en']])
  
  return pd.DataFrame(data=Counter(emojis).most_common(10),columns=["Emojis","Counts"])

#################################################################


def month_time_line(user,df):
  if user != 'Overall':
    df = df[df['User'] == user]
  
  temp=df.groupby(['Year','Month_no','Month']).count()['Message'].reset_index()

  time=[]

  for i in range(temp.shape[0]):
    time.append(temp['Month'][i] + "-" + str(temp['Year'][i]))
  
  temp['time'] = np.array(time)

  return temp

#################################################################

def week_activity(user,df):
  if user != 'Overall':
    df = df[df['User'] == user]
  
  return df['Day_name'].value_counts()

#################################################################

def month_activity(user,df):
  if user != 'Overall':
    df = df[df['User'] == user]
  
  return df['Month'].value_counts()

