# Adobe_PDF_Extractor_Project
This project uses PDF Extract API by Adobe to read transaction bills given in .pdf format and store the extracted data in a .csv format.


# How to use it?

1: Install dependencies by running
 
    pip install -r requirements.txt

2: Input the Test Data path location and the resultant zip files path location inside PDF_Extractor.py. This algorithm would extract data from the PDFs into zip files and store them in the assigned path location for zip files.

3: Use ZipExtractor.py to unzip all zipped files in the zip files folder to another folder containing all unzipped .json files

4: Use Processing_Code.py to process all .json files to return .csv files to your desired path location, and done!

# Files structure

TestDataSet contains all the test data in .pdf format.

ResultZipSet contains all the .zip files obtained by extracting data from the test data using Adobe PDF Extract API.

ResultJSONSet contains all the .json files obtained by unzipping data from ResultZipSet.

ResultSet contains all .csv files containing extracted data in the required format for each of the 100 files. An ExtractedData.csv is also present in the main directory containing a combined .csv file of all the .csv files.

PS: Right now my path locations are stored in the files, you will have to replace those with yours for the code to run. The codes do not delete any zip file or .json files after extraction to prevent loss of data due to any code defects.


