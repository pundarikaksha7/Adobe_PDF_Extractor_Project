# Adobe_PDF_Extractor_Project
This project uses PDF Extract API by Adobe to read transaction bills given in .pdf format and store the extracted data in a .csv format.


# How to use it?

1: Install dependencies by running requirements.txt

2: Input the Test Data path location and the resultant zip files path location inside PDF_Extractor.py. This algorithm would convert the PDFs into zip files and store them in the assigned path location for zip files.

3: Use ZipExtractor.py to unzip all zipped files in the zip files folder to another folder containing all unzipped .json files

4: Use Processing_Code.py to process all .json files to return .csv files to your desired path location, and done!

PS: Right now my path locations are stored in the file, you will have to replace those with yours for the code to rum.


