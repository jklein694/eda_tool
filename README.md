# eda_tool
A pandas OOP tool for helping clean data
Three tools:
-  eda helper()
  - This function returns a dataframe of the following:
    * Null count
    * Unique count
    * Data Types
    * Mean
    * Standard Deviation
    * Peak to Peak
    * Min
    * Max
    * Kurtosis
- remove column name spaces()
  - This will remove all spaces with "_". 
  
- to Float 
  - This function will check the ratio of numbers to words, you can change this parameter to fit your dataset, if it meets the ratio criteria the columns will be changed to floats. The removed data will be added to the column name to preserve lost information. This function will ignore ".", obviously still important for floats. In addition, there is a prameter to add stop words. 

### Example:
```python
eda = Eda(df)
empty_df = eda.remove_full_null_cols()
eda.remove_full_null_cols()
eda.to_float(num_ratio=.20, stop_words=['important'])
eda.eda_helper(sort=True)
data = eda.df
data.head()
```
