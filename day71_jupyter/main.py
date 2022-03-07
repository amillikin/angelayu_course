import pandas as pd


df = pd.read_csv('./salaries_by_college_major.csv')

# display first 5 rows
df.head()

# last 5
df.tail()

# row / col count
df.shape # (51, 6) => (row, col)

# column labels
df.columns

# Index(['Undergraduate Major', 'Starting Median Salary',
#        'Mid-Career Median Salary', 'Mid-Career 10th Percentile Salary',
#        'Mid-Career 90th Percentile Salary', 'Group'],
#       dtype='object')

# missing values / bad data
df.isna()

# new clean df
clean_df = df.dropna()


# specific column
clean_df['Starting Median Salary']

# max Salary
clean_df['Starting Median Salary'].max() # => 74,300

# index of max?

clean_df['Starting Median Salary'].idxmax() # => 43

# Undergraduate Major at 43
clean_df['Undergraduate Major'].loc[43]
clean_df['Undergraduate Major'][43] # => Physician Assistant

# Full row with column headers
clean_df.loc[43]

# What college major has the highest mid-career salary? 
# How much do graduates with this major earn? (Mid-career is defined as having 10+ years of experience).
clean_df['Mid-Career Median Salary'].max() # => 107k
clean_df['Mid-Career Median Salary'].idxmax() # => 8
clean_df['Undergraduate Major'][8] # => Chemical Engineering


# Which college major has the lowest starting salary
# and how much do graduates earn after university?
clean_df['Starting Median Salary'].min() # => 34k
clean_df['Starting Median Salary'].idxmin() # => 49
clean_df['Undergraduate Major'][49] # => Spanish

# Which college major has the lowest mid-career salary
# and how much can people expect to earn with this degree?
clean_df.loc[clean_df['Mid-Career Median Salary'].idxmin()] # => Education

# variance/risk
spread_col = clean_df['Mid-Career 90th Percentile Salary'] - clean_df['Mid-Career 10th Percentile Salary']

# Add as column
clean_df.insert(1, 'Spread', spread_col)

# least risk
clean_df.loc[clean_df['Spread'].idxmin()]

# sort
low_risk = clean_df.sort_values('Spread')
low_risk[['Undergraduate Major', 'Spread']].head()

# highest potential
hp = clean_df.sort_values('Mid-Career 90th Percentile Salary', ascending=False)
hp[['Undergraduate Major', 'Mid-Career 90th Percentile Salary']].head()

# high risk
high_risk = clean_df.sort_values('Spread', ascending=False)
high_risk[['Undergraduate Major', 'Spread']].head()

# Grouping
clean_df.groupby('Group').count() # => counts by col by Business, HASS, STEM
clean_df.groupby('Group').mean() # => mean by col by Group row

# set precision
pd.options.display.float_format = '{:,.2f}'.format
