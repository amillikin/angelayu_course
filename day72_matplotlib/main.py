import pandas as pd
import matplotlib.pyplot as plt

# header=0 allows col name substitution
df = pd.read_csv(
    'QueryResults.csv',
    names=['DATE', 'TAG', 'POSTS'],
    header=0)

df.head() #  first 5 rows
df.tail() # last 5 rows
df.shape # (rows, cols)
df.count() # count of non-NaN in each column

df.groupby('TAG').sum() # sum of posts by TAG category
df.groupby('TAG').count() # count of months TAG is seen

df['DATE'][1] == df.DATE[1] # access elements in column DATE
type(df.DATE) # check type
df.DATE = pd.to_datetime(df.DATE) # convert column from str to datetime

# pivot table with language (TAG) for columns, split by DATE, values POST count
reshaped_df = df.pivot(index='DATE', columns='TAG', values='POSTS')
reshaped_df.fillna(0, inplace=True) # fill NaN with 0
reshaped_df.isna().values.any() # returns bool if any values NaN.

# plot java [pst count by date]
plt.plot(reshaped_df.index, reshaped_df.java)

"""
.figure() - allows us to resize our chart

.xticks() - configures our x-axis

.yticks() - configures our y-axis

.xlabel() - add text to the x-axis

.ylabel() - add text to the y-axis

.ylim() - allows us to set a lower and upper bound
"""

# 16 width, 10 height
plt.figure(figsize=(16,10))
# adjust axis tick size
plt.xticks(fontsize=14)
plt.yticks(fontsize=14)
# axis labels
plt.xlabel('Date', fontsize=14)
plt.ylabel('Number of Posts', fontsize=14)
# set y axis limits
plt.ylim(0, 35000)
plt.plot(reshaped_df.index, reshaped_df.java) # or reshaped_df[['java','python']]
plt.plot(reshaped_df.index, reshaped_df.python)

# plot each column on same graph w/ legend
for column in reshaped_df.columns:
    plt.plot(reshaped_df.index,
             reshaped_df[column],
             linewidth=3,
             label=reshaped_df[column].name)
plt.legend(fontsize=16)

# rolling average
rolling_df = reshaped_df.rolling(window=6).mean() # avg over 6 periods



