#!/usr/bin/env python
# coding: utf-8

# In[1]:


#importing libraries
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt


# In[2]:


#reading data which is csv file in this case and saving in df which will be dataframe, 
#inside "" is directory in which csv file is in
df = pd.read_csv("C:\\Users\\harsh\\Downloads\\netflix1.csv\\netflix1.csv")


# In[3]:


#checking how many rows and columns the dataset is
print('number of rows: ', len(df.axes[0]))
print('number of columns: ', len(df.axes[1]))


# In[4]:


#how data looks like:
df.head(10)


# In[5]:


#more info on data
df.info()
#Things to clean,
#1)date_added column is object type: changing it to datetime dtype


# In[6]:


#seeing if there are any duplicate values in df
df.duplicated().value_counts()


# In[7]:


#seeing if I can use groupby to sort tv shows and movies based on their duration:
df.groupby('duration').count().sort_values(by='show_id',ascending=False)


# In[8]:


#2)things to clean:
#for a given duration, there are 2 kinds of values: Seasons and minutes, I need to filter out 
#int values in these elements.

#upon furthur inspection, I found that seasons are for duration of tv_series
#and minutes for movies.

#3)So, I need to first separate the df into 2: one with tv_series and other one
#with movies.then I can separate their duration that is mins and seasons

#I'll create a copy of df and try to clean the copy:
df_clean = df.copy()


# In[9]:



df_clean.head()
#4)there are multiple genre per row in listed_in in some cases, these genres are repeating values in the rows
#for ease of looking and analysis, ill convert the rows having multiple genres into 3 seperate columns,
#namely genre column 1, 2 and 3. i will disregard the rest and consider only the starting 3 genres as top 3
#genres for that tv series or movie.


# In[10]:


#ANS1)this .to_datetime will convert date_added column to datetime dtype
df_clean.date_added = pd.to_datetime(df_clean.date_added)


# In[11]:


df_clean.info()


# In[12]:


#ans 4) for seperating genres, I will iterate through every row in listed_in column and 
#and will select out the 3 genres ( if there are 3) to 3 different columns
#make 3 seperate columns for top 3 genres
#creating 3 seperate columns:
df_clean['listed_in1'] = 0
df_clean['listed_in2'] = 0
df_clean['listed_in3'] = 0
#temp_cat will denote which row we are in out of 8790 rows
temp_cat = df_clean.listed_in.str.split(',')
i=0
for i in range (8790):
    t_cat = temp_cat[i]
    #if there is only one genre
    if len(t_cat) == 1:
        df_clean['listed_in1'][i] = temp_cat[i][0]
        df_clean['listed_in2'][i] = 0
        df_clean['listed_in3'][i] = 0
    #if there are two genres
    if len(t_cat) == 2:
        df_clean['listed_in1'][i] = temp_cat[i][0]
        df_clean['listed_in2'][i] = temp_cat[i][1]
        df_clean['listed_in3'][i] = 0
    #if there are 3 genres
    if len(t_cat) == 3:
        df_clean['listed_in1'][i] = temp_cat[i][0]
        df_clean['listed_in2'][i] = temp_cat[i][1]
        df_clean['listed_in3'][i] = temp_cat[i][2]


# In[13]:


df_clean
#this represents df with 3 seperate columns for 3 genres


# In[14]:


#ANS 3) creating df_tv and df_movies to seperate out df_clean into 2 dfs based on tv show or movie 
df_tv = df_clean[df_clean.type == 'TV Show']
df_movie = df_clean[df_clean.type == 'Movie']


# In[15]:


df_tv.head(50)


# In[16]:


df_movie.head()


# In[17]:


#ANS2)create a column named df_tv.duration_seasons.
#first we will split the values in duration column at ' ' and 
# will store a list of all sub-values that are splitted with ' '
#and then chose the very first value out of these sub values in any row
temp_dur = df_tv.duration.str.split(' ',expand=True)
df_tv['duration_seasons'] = temp_dur[0]
df_tv.duration_seasons = pd.to_numeric(df_tv.duration_seasons)


# In[18]:


df_tv.head()


# In[19]:


#same for movie
temp_dur = df_movie.duration.str.split(' ',expand=True)
df_movie['duration_minutes'] = temp_dur[0]
df_movie.duration_minutes = pd.to_numeric(df_movie.duration_minutes)


# In[20]:


df_movie.head()


# In[21]:


#we created 3 database from the original one, ill save all these 3
df_clean.to_csv('Netflix_DF_clean.csv')
df_tv.to_csv('Netflix_TV_cleaned.csv')
df_movie.to_csv('Netflix_Movie_cleaned.csv')


# In[22]:


#Suppose we wanted to know what kind of media has been produced in netflix per year (movie and tvshow)
#specifying the size of chart
plt.figure(figsize=[20,6])
#specifying color with seaborn
base_color = sns.color_palette('coolwarm',n_colors=5)
#showing counts of dates in form of bar and setting up color that is in base_color, setting 
#hue as 'type' because we wanna know number of --tvshows or movies-- per year.
tv_movie = sns.countplot(x=df_clean.date_added.dt.year, data=df_clean, hue='type', palette = base_color)
#title
tv_movie.set_title("Number of TV Shows and Movies Netflix has released per Year",fontsize = 20)
#x & Y axis name
tv_movie.set_xlabel('Year',fontsize = 15)
tv_movie.set_ylabel('Number of Movies/TV Shows',fontsize = 15)
for container in tv_movie.containers:
    tv_movie.bar_label(container)


# In[23]:


#Inference --> more movies than tv show every year, there is increasing number of media till 2019 then
#gradual decrline possibly because of COVID
df_clean.date_added.dt.year


# In[24]:


df_clean.date_added.dt.year.count()


# In[25]:


len(df_tv.groupby('country').count().index)


# In[26]:


df_tv.head()
#Q2)suppose Rajiv from pakistan is looking for tvseries from pakistan.
#he is only looking for series to bingewatch(series having 4 or more seasons)
# and only TV-14 or TV-MA rating movies
#country - pakistan
# duration_seasons >= 4


# In[27]:


df_tv.rating.unique()
#df_tv.listed_in1.unique()


# In[28]:


df_tv.info()


# In[29]:


pakistani_tv_shows = df_tv.loc[(df_tv['country']== 'Pakistan') & (df_tv['duration_seasons'] >= 4) ]
pakistani_tv_shows


# In[30]:


pakistani_tv_shows


# In[31]:


pakistani_tv_shows['title']


# In[33]:



pakistani_tv_shows.to_csv('2nd_outputpakistani_tv_show.csv')


# In[ ]:




