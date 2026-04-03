"""
==========================================================================  
Project: IMDb Data Analysis  

Objective:
Analyze the IMDb Top 1000 movies dataset to explore trends in movie ratings  
across genres, popularity (number of votes), runtime, and revenue.  
The goal is to identify patterns and relationships using data analysis  
and visualization techniques.
==========================================================================
"""

# ---------------- Import Libraries ----------------
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Set visualization style
sns.set(style="whitegrid")

# ---------------- Display Settings ----------------
pd.set_option('display.max_columns', None)

# ---------------- Load Dataset ----------------
df = pd.read_csv("imdb_top_1000.csv")

# ---------------- Initial Exploration ----------------
print(df.head())
print("\nMissing values:\n", df.isnull().sum())
print("\nBasic statistics:\n", df.describe())

# ---------------- Basic Analysis ----------------
print("\nAverage IMDb rating:", df['IMDB_Rating'].mean())

# ---------------- Top Movies ----------------
top_movies = df.sort_values(by='IMDB_Rating', ascending=False).head(10)
print("\nTop 10 movies:")
print(top_movies[['Series_Title', 'IMDB_Rating']])

# ---------------- Visualization: Rating Distribution ----------------
sns.histplot(df['IMDB_Rating'], bins=30, kde=True)
# KDE adds a smooth curve to show the distribution pattern

plt.title("IMDb Rating Distribution")
plt.xlabel("IMDb Rating")
plt.ylabel("Number of Movies")

plt.savefig("images/Rating_Distribution.png")
plt.show()

# ---------------- Genre Analysis ----------------
df['Genre'] = df['Genre'].str.split(',')

df_exploded = df.explode('Genre')  # Expand rows so each genre gets its own row
df_exploded['Genre'] = df_exploded['Genre'].str.strip()

genre_rating = (
    df_exploded.groupby('Genre')['IMDB_Rating']
    .mean()
    .sort_values(ascending=False)
)

print("\nAverage rating by Genre:")
print(genre_rating.head(10))

# ---------------- Year Trend ----------------
df['Released_Year'] = pd.to_numeric(df['Released_Year'], errors='coerce')
year_rating = df.groupby('Released_Year')['IMDB_Rating'].mean()

print("\nRecent year ratings:\n", year_rating.tail())

# ---------------- Visualization: Genre Trend ----------------
genre_rating.head(10).plot(kind='bar')

plt.title("Top Genres by Average Rating")
plt.xlabel("Genre")
plt.ylabel("Average Rating")
plt.xticks(rotation=45)

plt.tight_layout()  # Prevent label overlap
plt.savefig("images/Genre_Trend.png")
plt.show()

# ---------------- Visualization: Rating Trend Over Years ----------------
year_rating.plot()

plt.title("IMDb Rating Trend Over Years")
plt.xlabel("Year")
plt.ylabel("Average Rating")
plt.xticks(rotation=45)

plt.tight_layout()
plt.savefig("images/Rating_Trend_Over_Years.png")
plt.show()

# ---------------- Visualization: Runtime vs Rating ----------------
df['Runtime'] = df['Runtime'].str.replace(' min', '')
df['Runtime'] = pd.to_numeric(df['Runtime'], errors='coerce')

sns.scatterplot(x=df['Runtime'], y=df['IMDB_Rating'])

plt.title("Runtime vs IMDb Rating")
plt.xlabel("Runtime (minutes)")
plt.ylabel("IMDb Rating")

plt.grid(alpha=0.4)  # Light grid for readability
plt.savefig("images/Runtime_vs_Rating.png")
plt.show()

# Correlation analysis
corr = df['Runtime'].corr(df['IMDB_Rating'])
print("Correlation between runtime and rating:", corr)

# ---------------- Visualization: Votes vs Rating ----------------
plt.scatter(df['No_of_Votes'], df['IMDB_Rating'])

plt.xscale('log')  # Handle large vote values
plt.title("Votes vs IMDb Rating")
plt.xlabel("Number of Votes")
plt.ylabel("IMDb Rating")

plt.grid(alpha=0.3)
plt.savefig("images/Votes_vs_Rating.png")
plt.show()

# ---------------- Visualization: Revenue vs Rating ----------------
df['Gross'] = df['Gross'].str.replace(',', '')
df['Gross'] = pd.to_numeric(df['Gross'], errors='coerce')

sns.regplot(
    x=df['Gross'],
    y=df['IMDB_Rating'],
    scatter_kws={'alpha': 0.4}
)
# Add regression line + transparent points to show trend clearly

plt.xscale('log')
plt.title("Gross Revenue vs IMDb Rating")
plt.xlabel("Gross Revenue (log scale)")
plt.ylabel("IMDb Rating")

plt.savefig("images/Gross_vs_Rating.png")
plt.show()
