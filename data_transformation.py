import pandas as pd
#load df
raw_climate_data = pd.read_csv('climate_data.csv')
#check df info
print("Raw dataframe info:")
print(raw_climate_data.info)
# check if there are NaN values and its count
na_count =  raw_climate_data.isna().sum().sum()
print( "Null values : ", na_count)
#copy df
climate_data = raw_climate_data.copy()
#replase all symbols in temp and precipation columns
# and change datatype to float
climate_data["Precipitation"] = (climate_data["Precipitation"]
                                 .str.replace('"',"").astype(float))

temp_columns = ['High Temp', 'Low Temp', 'Mean Temp']
for column in temp_columns:
    climate_data[column] = (climate_data[column]
                            .str.replace(' °F','').astype(float))

#check modified df info

print("Modified dataframe info:")
print(climate_data.info)