import google_play_scraper as gps
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st


# Title
st.markdown("<h1 style='color:yellow;'> Live Play Store App's Analysis </h1>", unsafe_allow_html=True)

# Set Image
st.image("playstore.png", width=60)
st.markdown("<br>",unsafe_allow_html=True)

# Input text
n = st.text_input("Enter for what you want search: ")

# Getting AppIds
result = gps.search(
    n,
    lang="en",  # defaults to 'en'
    country='in',  # defaults to 'us'
    n_hits=30  # defaults to 30 (= Google's maximum)
    
)

app_id = []
for i in range(len(result)): 
    app_id.append(result[i]['appId'])

# Getting other parameters 
icon = []
title = []
version = [] 
minInstalls = []
realInstalls = []
score = []
ratings = []
reviews = []
lastUpdatedOn = []
developer = []
video_link = []
summary = []

for i in range(len(app_id)): 
    result1 = gps.app(
        app_id[i],
        lang = 'en',
        country = 'in'
    )
    icon.append(result1['icon'])
    title.append(result1['title'])
    version.append(result1['version'])
    minInstalls.append(result1['minInstalls'])
    realInstalls.append(result1['realInstalls'])
    score.append(result1['score'])
    ratings.append(result1['ratings'])
    reviews.append(result1['reviews'])
    lastUpdatedOn.append(result1['lastUpdatedOn'])
    developer.append(result1['developer'])
    video_link.append(result1['video'])
    summary.append(result1['summary'])

# Making dictionary
dic = {
    'AppId':app_id,
    'Icon':icon,
    'Title':title, 
    'Version':version,
    'MinInstalls':minInstalls, 
    'RealInstalls':realInstalls, 
    'RatingScore':score, 
    'Ratings':ratings, 
    'Reviews':reviews, 
    'LastUpdatedOn':lastUpdatedOn,
    'Developer':developer,
    'VideoLink':video_link,
    'Summary':summary
}

# Creating dataframe and correct the data of RatingScore column
df = pd.DataFrame(dic)

df['RatingScore'] = df['RatingScore'].apply(lambda x: f"{x:.1f}")

# Changing the datatype of RatingScore from object to float
df['RatingScore'] = df['RatingScore'].astype(float)

# Showing Dataframe
st.dataframe(df)

# Separation Markdown
st.markdown("----")

# Subheader
st.markdown("<h2 style='color:orange;'>Graphical Analysis</h2>",unsafe_allow_html=True)

# 4 Visulaization's
x = df['Title']
y = df['RatingScore']     
fig, ax = plt.subplots()         
ax.plot(x,y,"-o", color='red')
plt.title('Based on Rating Score')
plt.xlabel("Title --->")
plt.ylabel('Rating Score --->')
plt.xticks(rotation=90)
st.pyplot(fig)

 
x = df['Title']
y = df['RealInstalls']     
fig, ax = plt.subplots()         
ax.plot(x,y,"-o", color='green')
plt.title("Based on Real Installs")
plt.xlabel("Title --->")
plt.ylabel('RealInstalls --->')
plt.xticks(rotation=90)
st.pyplot(fig)

 
x = df['Title']
y = df['Ratings']     
fig, ax = plt.subplots()         
ax.plot(x,y,"-o", color="blue")
plt.title("Based on No. of Ratings")
plt.xlabel("Title --->")
plt.ylabel('Ratings --->')
plt.xticks(rotation=90)
st.pyplot(fig)

 
x = df['Title']
y = df['Reviews']     
fig, ax = plt.subplots()         
ax.plot(x,y,"-o", color="magenta")
plt.title("Based on No. of Review")
plt.xlabel("Title --->")
plt.ylabel('Reviews --->')
plt.xticks(rotation=90)
st.pyplot(fig)

st.markdown("----")

# Subheader
st.markdown("<h2 style='color:orange;'>Choose Your App</h2>",unsafe_allow_html=True)

# Range with two Columns
r1 = st.slider("Start Rating From", 1.0, 5.0, 3.0,step=0.5)
r2 = st.slider("End Rating To", 1.0, 5.0 ,4.0,step=0.5)

# Ranged Dataframe
st.dataframe(df[['Title', 'Version', 'RatingScore', 'LastUpdatedOn', 'Developer', 'Summary']][(df['RatingScore']>=r1) & (df['RatingScore']<=r2)])

#Break 
st.markdown("<br>", unsafe_allow_html=True)

# Input Label
ti = st.text_input("Enter The Index of the App")
st.markdown("---")


# Markdown, Url Generation
if ti: 
    st.markdown("<h2 style='color:orange;'>Download Your App</h2>",unsafe_allow_html=True)
    ti = int(ti)
    appid = df.iloc[ti,0]
    st.markdown(
        f"<a href='https://play.google.com/store/apps/details?id={appid}&hl=en_IN' style='color:blue; text-decoration:none;'>https://play.google.com/store/apps/details?id={appid}&hl=en_IN</a>",
        unsafe_allow_html=True
    )


