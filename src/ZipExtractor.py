from zipfile import ZipFile
import os

resultant_json_folder="/Users/pundarikaksha/Desktop/Adobe Hackathon/InvoicesData/ResultJSONSet/"

for i in range(0,100):
    with ZipFile(f'/Users/pundarikaksha/Desktop/Adobe Hackathon/InvoicesData/ResultZipSet/extracted_dataoutput{i}.zip', 'r') as a:
        a.extractall(resultant_json_folder)
        old_name=resultant_json_folder+"structuredData.json"
        new_name=resultant_json_folder+f"structuredData{i}.json"
        os.rename(old_name,new_name)