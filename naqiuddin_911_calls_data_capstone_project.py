# -*- coding: utf-8 -*-
"""NAQIUDDIN- 911 Calls Data Capstone Project

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1X686WM64V-qjaRNI5AQvI87wGJC2hVXk

# 911 Calls Capstone Project

For this capstone project we will be analyzing some 911 call data from [Kaggle](https://www.kaggle.com/mchirico/montcoalert). The data contains the following fields:

* lat : String variable, Latitude
* lng: String variable, Longitude
* desc: String variable, Description of the Emergency Call
* zip: String variable, Zipcode
* title: String variable, Title
* timeStamp: String variable, YYYY-MM-DD HH:MM:SS
* twp: String variable, Township
* addr: String variable, Address
* e: String variable, Dummy variable (always 1)

Just go along with this notebook and try to complete the instructions or answer the questions in bold using your Python and Data Science skills!

## Data and Setup

____
** Import numpy and pandas **
"""

import numpy as np
import pandas as pd

"""** Import visualization libraries  **"""

import seaborn as sns
import matplotlib.pyplot as plt

"""** Read in the csv file as a dataframe called df **"""

df = pd.read_csv("/content/911.csv")

"""** Check the info() of the df **"""

df.info()

"""** Check the head of df **"""

df.head()

"""## Basic Questions

** What are the top 5 zipcodes for 911 calls? **
"""

df['zip'].value_counts().head()

#Answer

"""** What are the top 5 townships (twp) for 911 calls? **"""

df['twp'].value_counts().head()

#answer

"""** Take a look at the 'title' column, how many unique title codes are there? **"""

df['title'].nunique()

#Answer

"""## Creating new features

** In the titles column there are "Reasons/Departments" specified before the title code. These are EMS, Fire, and Traffic. Use .apply() with a custom lambda expression to create a new column called "Reason" that contains this string value.** 

**For example, if the title column value is EMS: BACK PAINS/INJURY , the Reason column value would be EMS. **
"""

df['Reason'] = df['title'].apply(lambda reason: reason.split(":")[0])

df.head()

"""** What is the most common Reason for a 911 call based off of this new column? **"""

df['Reason'].value_counts()

"""** Now use seaborn to create a countplot of 911 calls by Reason. **"""

sns.countplot(x='Reason', data=df)

"""___
** Now let us begin to focus on time information. What is the data type of the objects in the timeStamp column? **
"""

df.info()
df['timeStamp']

"""** You should have seen that these timestamps are still strings. Use [pd.to_datetime](http://pandas.pydata.org/pandas-docs/stable/generated/pandas.to_datetime.html) to convert the column from strings to DateTime objects. **"""

#df['timeStamp'] = pd.to_datetime(df['timeStamp'])

df['timeStamp']=pd.to_datetime(df['timeStamp'],format = '%Y-%m-%d %H:%M:%S')
 df['timeStamp']

"""** You can now grab specific attributes from a Datetime object by calling them. For example:**

    time = df['timeStamp'].iloc[0]
    time.hour

**You can use Jupyter's tab method to explore the various attributes you can call. Now that the timestamp column are actually DateTime objects, use .apply() to create 3 new columns called Hour, Month, and Day of Week. You will create these columns based off of the timeStamp column, reference the solutions if you get stuck on this step.**
"""

time = df['timeStamp'].iloc[0]
time.hour

df['Hour']=df['timeStamp'].apply(lambda findhour: findhour.hour)

df['Month']=df['timeStamp'].apply(lambda findmonth: findmonth.month)

df['Day']=df['timeStamp'].apply(lambda findday: findday.dayofweek)

df.info()

"""** Notice how the Day of Week is an integer 0-6. Use the .map() with this dictionary to map the actual string names to the day of the week: **

    dmap = {0:'Mon',1:'Tue',2:'Wed',3:'Thu',4:'Fri',5:'Sat',6:'Sun'}
"""

df['Day']

dmap = {0:'Mon',1:'Tue',2:'Wed',3:'Thu',4:'Fri',5:'Sat',6:'Sun'}

df['Day'] = df['Day'].apply(lambda x: dmap[x])
#df['Day'] = df['Day'].map(dmap)

"""** Now use seaborn to create a countplot of the Day of Week column with the hue based off of the Reason column. **"""

sns.countplot(x="Day", data=df, hue="Reason", palette= "rainbow")

"""**Now do the same for Month:**"""

dmonth = {1:'January',2:'February',3:'March',4:'April',5:'May',6:'June',7:'July',8:'August',9:'September',10:'October', 11:'November', 12:'December'}

df['Month'] = df['Month'].apply(lambda x: dmonth[x])

plt.figure(figsize=(13,6))
sns.countplot(x="Month", data=df, hue="Reason", palette= "rainbow")

"""**Did you notice something strange about the Plot?**

_____

** You should have noticed it was missing some Months, let's see if we can maybe fill in this information by plotting the information in another way, possibly a simple line plot that fills in the missing months, in order to do this, we'll need to do some work with pandas... **

** Now create a gropuby object called byMonth, where you group the DataFrame by the month column and use the count() method for aggregation. Use the head() method on this returned DataFrame. **
"""

byMonth=df.groupby('Month').count()
byMonth.head()

byMonth['lat'].plot()

"""** Now create a simple plot off of the dataframe indicating the count of calls per month. **

** Now see if you can use seaborn's lmplot() to create a linear fit on the number of calls per month. Keep in mind you may need to reset the index to a column. **
"""

byMonth.head()

byMonth.reset_index(inplace=True)

byMonth.head()

sns.jointplot( x='Month', y='lat', data=byMonth, kind="reg")

"""**Create a new column called 'Date' that contains the date from the timeStamp column. You'll need to use apply along with the .date() method. ** """

df['Date'] = df['timeStamp'].apply(lambda time:time.date())

df.head()

"""** Now groupby this Date column with the count() aggregate and create a plot of counts of 911 calls.**"""

df.groupby('Date').count()

plt.figure(figsize=(9,5))
df.groupby('Date').count()['lat'].plot()

"""** Now recreate this plot but create 3 separate plots with each plot representing a Reason for the 911 call**"""

df['Reason']

plt.figure(figsize=(9,5))
df[df['Reason']=='Traffic'].groupby('Date').count()['lat'].plot()
plt.title("Month wise Traffic Call Counts")

plt.figure(figsize=(9,5))
df[df['Reason']=='Fire'].groupby('Date').count()['lat'].plot()
plt.title("Month wise Fire Call Counts")

plt.figure(figsize=(9,5))
df[df['Reason']=='EMS'].groupby('Date').count()['lat'].plot()
plt.title("Month wise EMS Call Counts")

"""____
** Now let's move on to creating  heatmaps with seaborn and our data. We'll first need to restructure the dataframe so that the columns become the Hours and the Index becomes the Day of the Week. There are lots of ways to do this, but I would recommend trying to combine groupby with an [unstack](http://pandas.pydata.org/pandas-docs/stable/generated/pandas.DataFrame.unstack.html) method. Reference the solutions if you get stuck on this!**
"""

df2= df.groupby(['Day','Hour']).count()['lat'].unstack() 
#becomin multi index dataframe , then index will become column because unstack

df2.head()

"""** Now create a HeatMap using this new DataFrame. **"""

plt.figure(figsize=(13,6))
sns.heatmap(df2, cmap='coolwarm',linewidths=1, linecolor='white', annot= True, fmt='g')

"""** Now create a clustermap using this DataFrame. **"""

plt.figure(figsize=(13,6))
sns.clustermap(df2, cmap='coolwarm',linewidths=1, linecolor='white', annot= True, fmt='g')

"""** Now repeat these same plots and operations, for a DataFrame that shows the Month as the column. **"""

df3= df.groupby(['Day','Month']).count()['lat'].unstack()

df3.head()

plt.figure(figsize=(13,6))
sns.heatmap(df3, cmap='coolwarm',linewidths=1, linecolor='white', annot= True, fmt='g')

plt.figure(figsize=(13,6))
sns.clustermap(df2, cmap='coolwarm',linewidths=1, linecolor='white', annot= True, fmt='g')

"""**Continue exploring the Data however you see fit!**
# Great Job!
"""