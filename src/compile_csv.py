import os
import glob
import pandas as pd

path = '/Users/pundarikaksha/Desktop/Adobe Hackathon/InvoicesData/ResultSet/'
extension = 'csv'
os.chdir(path)
result = glob.glob('*.{}'.format(extension))

final_dataframe=pd.DataFrame()

for csv in result:
    df=pd.read_csv(csv)
    final_dataframe=final_dataframe._append(df,ignore_index=True)

print(final_dataframe)

final_dataframe.to_csv(path+"ExtractedData.csv")