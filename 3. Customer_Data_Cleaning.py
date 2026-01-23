# First Part of this Data Analysis is to make some cleaning and preparation with
# the data so we can, later, perform some more complex activities


# We start importing the things we going to use it, in this case its a very simples
# analysis so only pandas its going to be necessary 
import pandas as pd

# Just opening the .csv file
df = pd.read_csv("THIS PART I'M GOING TO CENSURATE IT")

# Some easy and useful information here
df.head()
df.info()
df.describe(include = 'all')


# Lets check the null values
df.isnull().sum()

# We find it all of them in this only variable, so I will change them all to the
# median value (not the mean value because its highly affected by outliers)
df['Review Rating'] = df.groupby('Category')['Review Rating'].transform(lambda x: x.fillna(x.median()))

# Just cheking the null values again and its fine
df.isnull().sum()


# Now we need to change the columns to make it easier for ourselves in the future
# dealing with this data
df.columns = df.columns.str.lower()
df.columns = df.columns.str.replace(' ','_')
df = df.rename(columns = {'purchase_amount_(usd)':'purchase_amount'})
df.columns


# Let's create 'age_groups' column to gather more information
labels = ['Young Adult', 'Adult', 'Middle Aged', 'Senior']
df['age_group'] = pd.qcut(df['age'], q=4, labels = labels)
df[['age', 'age_group']].head(10)


# Changing the purchase_frequency_days column to numeric, because its very annoying
# to work with these kind of values in variables
frequency_mapping = {
    'Fortnightly': 14,
    'Weekly': 7,
    'Monthly': 30,
    'Quarterly':90,
    'Bi-Weekly':14,
    'Annually': 365,
    'Every 3 Months': 90
}

df['purchase_frequency_days'] = df['frequency_of_purchases'].map(frequency_mapping)
df[['purchase_frequency_days','frequency_of_purchases']].head(10)



# I realized that 'discount_applied' and 'promo-code-used' provide us with the 
# exact same information, so we dont need it both.
df[['discount_applied','promo_code_used']].head(10)
(df['discount_applied'] == df['promo_code_used']).all()
df = df.drop('promo_code_used', axis=1)


# By the end, just checking things again
df.columns
df.head()
df.info()



# And last but not least, let's go to the MySQL so we can work with other questions
# in this Analysis
from sqlalchemy import create_engine
username = "Example"
password = "Example"
host = "Example"
port = "Example"
database = "Example"

engine = create_engine(f"mysql+pymysql://{username}:{password}@{host}:{port}/{database}")

table_name = "mytable"
df.to_sql(table_name, engine, if_exists="replace", index=False)

pd.read_sql("SELECT * FROM mytable LIMIT 5;", engine)






