"""
==========================================================================
Project: IMDb Data Analysis 

Objective:
Analyze the IMDb Top 1000 movies dataset to explore trends in movie ratings across genres, popularity (number of votes), and runtime. The goal is to identify patterns and relationships that influence movie ratings using data analysis and visualization
==========================================================================

"""

# -------------- Import Libraries -------------- 
import pandas as pd
import matplotlib.pyplot as plt

# -------------- Display Settings --------------  
pd.set_option('display.max_columns', None)

# -------------- Load Dataset -------------- 
df = pd.read_csv("imdb_top_1000.csv")

# -------------- Initial Exploration -------------- 
print(df.head())
print("\nmissing values: \n ",df.isnull().sum())
print("\nbasic statistics: \n",df.describe())

# -------------- Basic Analysis -------------- 
print("\naverage imdb rating: ",df['IMDB_Rating'].mean())

# -------------- Visualisation: Rating Distribution -------------- 
top_movies = df.sort_values(by='IMDB_Rating', ascending=False).head(10)
print("\n top 10 movies:")
print(top_movies[['Series_Title','IMDB_Rating']])

# plot distribution of IMDb ratings 
plt.hist(df['IMDB_Rating'],bins=30)   #increasing bins gives a more detailed distribution 
plt.title("IMDb Rating distribution")
plt.xlabel('IMDb Rating')
plt.ylabel('Number of Movies')
plt.savefig('images/Rating_Distribution.png')
plt.show()

# -------------- Genre Analysis -------------- 

df['Genre'] = df['Genre'].str.split(',')  
df_exploded = df.explode('Genre')  #Expand rows so each genre gets its own row 
df_exploded['Genre'] = df_exploded['Genre'].str.strip()  #strip is used to remove the extra spaces so 'Drama' and ' Drama' are treated the same 
genre_rating = df_exploded.groupby('Genre')['IMDB_Rating'].mean().sort_values(ascending=False)  #calculate average rating per genre 
print('\nAverage rating by Genre: ')
print(genre_rating.head(10))

# -------------- Visualisation: Genre Trend --------------
 
df['Released_Year']= pd.to_numeric(df['Released_Year'],errors='coerce')  #errors='coerce' converts year to numeric; invalid values (eg: 'unknown' , 'N/A' ) becomes NaN
year_rating = df.groupby('Released_Year')['IMDB_Rating'].mean()
print('\nRecent Year ratings:\n',year_rating.tail())

# plot trend of IMDb Ratings 
genre_rating.head(10).plot(kind='bar')
plt.title('Top Genres by Average Rating ')
plt.xlabel('Genre')
plt.ylabel('Average Rating')
plt.xticks( rotation = 45 )
plt.tight_layout()  #adjust layout to prevent overlapping of labels and titles 
plt.savefig('images/Genre_Trend.png')
plt.show()

# -------------- Visualisation: Rating Trend Over Years -------------- 

year_rating.plot()
plt.title('IMDb Rating Trend Over Years')
plt.xlabel('Year')
plt.ylabel('Average Rating')
plt.xticks( rotation = 45 )
plt.tight_layout()
plt.savefig('images/Rating_Trend_Over_Years.png')
plt.show()

# -------------- Visualisation: Runtime vs Rating -------------- 
df['Runtime']=df['Runtime'].str.replace(' min','')  #remove ' min' from runtime values before converting to numeric
df['Runtime'] = pd.to_numeric(df['Runtime'],errors='coerce')

plt.scatter(df['Runtime'], df["IMDB_Rating"])
plt.title('Runtime vs IMDb Rating')
plt.xlabel('Runtime (minutes)')
plt.xticks(rotation=0)
plt.ylabel('IMDb Rating')
plt.savefig('images/Runtime_vs_Rating.png')
plt.grid(alpha=0.4)  #alpha controls the transparency of the grid lines
plt.show()
corr = df['Runtime'].corr(df['IMDB_Rating'])
print('Correlation between runtime and rating', corr)  #correlation measures how strongly two variables move together 

# -------------- Visualisation: Votes vs Rating -------------- 
plt.scatter(df['No_of_Votes'],df['IMDB_Rating'])
plt.xscale('log')  #use log scale to handle large range of vote values (eg: 1000-> 10^3)
plt.title('Votes vs IMDb Rating ')
plt.xlabel('Number of Votes')
plt.ylabel('IMDb Rating')
plt.savefig('images/Votes_vs_Rating.png')
plt.grid(alpha=0.3)
plt.show()


