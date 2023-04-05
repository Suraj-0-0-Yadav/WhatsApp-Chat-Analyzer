import numpy as np
import pandas as pd
import re

def get_date_and_time(x):
  date , time = x.split(",")
  time = time.split()[0]

  return date+" "+time

def get_string(text):
  return text.split("\n")[0]

def preprocess(data):

    text_data = data.split("\n")

    pattern = "\d{1,2}/\d{1,2}/\d{2,4},\s\d{1,2}:\d{2}\s[AMP]{2}\s-\s"
    messages = re.split(pattern,data)[1:]
    dates = re.findall(pattern,data)

    df = pd.DataFrame(data={"messages":messages,
                        'message_date':dates})
    df['message_date'] = df['message_date'].apply(lambda text : get_date_and_time(text))

    user=[]
    messages=[]

    for msg in df['messages']:

        entry = re.split(':\s',msg)
        if len(entry)>1:
        # if entry[1:]:
            user.append(entry[0])
            messages.append(entry[1])
        else:
            user.append("Group Notification")
            messages.append(entry[0])

    df['user'] = user
    df['message'] = messages

    df['message'] = df['message'].apply(lambda text : get_string(text))

    df.drop(columns=['messages'],inplace=True)
    df.rename(columns={'message_date':'Date',
                   'user':'User',
                   'message':'Message'},inplace=True)

    df['Only date'] = pd.to_datetime(df['Date']).dt.date

    df['Year'] = pd.to_datetime(df['Date']).dt.year

    df['Month_no'] = pd.to_datetime(df['Date']).dt.month

    df['Month'] = pd.to_datetime(df['Date']).dt.month_name()

    df['Day'] = pd.to_datetime(df['Date']).dt.day

    df['Day_name'] = pd.to_datetime(df['Date']).dt.day_name()

    df['Hour'] = pd.to_datetime(df['Date']).dt.hour

    df['Minute'] = pd.to_datetime(df['Date']).dt.minute

    return df

    