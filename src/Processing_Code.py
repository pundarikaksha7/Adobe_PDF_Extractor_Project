import pandas as pd
import json
import re
import nltk
from zipfile import ZipFile
from nltk.corpus import stopwords
stop = stopwords.words('english')


#NLP(Natural Language Processing) code using Regex and NLTK to extract 
#Phone number and Email

#Although in the code these have not been used, but I wrote these
#just in case my algorithm couldnt identify name and email
#mathematically
def extract_phone_numbers(string):
    r = re.compile(r'(\d{3}[-\.\s]??\d{3}[-\.\s]??\d{4}|\(\d{3}\)\s*\d{3}[-\.\s]??\d{4}|\d{3}[-\.\s]??\d{4})')
    phone_numbers = r.findall(string)
    return [re.sub(r'\D', '', number) for number in phone_numbers]

def extract_email_addresses(string):
    r = re.compile(r'[\w\.-]+@[\w\.-]+')
    return r.findall(string)



#Driver code to achieve the given task
#Inputs json file path, result folder path and result file index 
#for multiple files of same type
def return_csv(json_file_path,result_file_path,result_file_index):

    with open(json_file_path, 'r') as json_file:
        json_data = json.load(json_file)

    #ADDRESS
    #Extracts customers' details using Bounds key of each element
    customer_details=[]
    for element in json_data['elements']:
        try:
            if(element['Bounds'][0]==81.04800415039062):
                customer_details.append(element['Text'])
        except:
            continue

    #INVOICE DETAILS
    #Extracts Invoice number and Issue data using Bounds key
    #of each element
    invoice_details=[]
    for element in json_data['elements']:
        try:
            if(element['Bounds'][2]>541):
                invoice_details.append(element['Text'])
        except:
            continue

    #DETAILS
    #Extracts details paragraph using Bounds key
    details=[]
    for element in json_data['elements']:
        try:
            if(element['Bounds'][0]>240 and element['Bounds'][0]<242):
                details.append(element['Text'])
        except:
            continue


    #PAYMENT DETAILS
    #Extracts payment details such as due date using Bounds key
    payment_details=[]
    for element in json_data['elements']:
        try:
            if(element['Bounds'][0]>412 and element['Bounds'][0]<414):
                payment_details.append(element['Text'])
        except:
            continue


    #Creation of Pandas dataframe here with all column names assigned
    df=pd.DataFrame(columns=['Business_City','Business_Country','Business_Description','Business_Name','Business_StreetAddress',
                            'Business_Zipcode','Customer__Address__line1','Customer__Address__line2','Customer__Email',
                            'Customer__Name','Customer__PhoneNumber','Invoice__BillDetails__Name',
                            'Invoice__BillDetails__Quantity','Invoice__BillDetails__Rate','Invoice__Description',
                            'Invoice__DueDate','Invoice__IssueDate','Invoice__Number','Invoice__Tax'])



    #ITEM DETAILS
    #This section extracts data regarding items,their quantities and
    #their rate using list manipulation
    elements=[]
    for element in json_data['elements']:
        try:
            elements.append(element['Text'])
        except:
            continue
        
    index=0
    while elements[index]!='AMOUNT ':
        index+=1
    index+=1

    i=index
    while elements[i]!='Subtotal ':
        try:
            dictitems={"Invoice__BillDetails__Name":elements[i],"Invoice__BillDetails__Quantity":elements[i+1],"Invoice__BillDetails__Rate":elements[i+2]}
            df.loc[len(df)]=dictitems
            i+=4
        except:
            break
        
    #This paragraph assigns Business details to each dataframe

    ##########BUSINESS DETAILS START#########

    business_name=""
    business_descrip=""
    business_street=""
    business_city=""
    business_country=""

    index=0
    for element in json_data['elements']:
        try:
            if element['Path'].endswith('Title'):
                business_name=element['Text']
                break
            index+=1
        except:
            continue
    index+=1

    i=0
    for element in json_data['elements']:
        if i==index:
            business_descrip=element['Text']
            break
        i+=1

    df['Business_Name']=business_name
    df['Business_Description']=business_descrip
        

    address_list=""
    for element in json_data['elements']:
        try:
            if element['Bounds'][0]>=76 and element['Bounds'][0]<=77 and element['Bounds'][1]>694 and element['Bounds'][1]<730:
                address_list+=element['Text']+" "
        except:
            continue
            
    index=0
    while address_list[index]!=',':
        business_street+=address_list[index]
        index+=1
    df['Business_StreetAddress']=business_street
    index+=1

    while address_list[index]!=',':
        business_city+=address_list[index]
        index+=1
    index+=1

    while address_list[index].isnumeric()==False:
        business_country+=address_list[index]
        index+=1
        
    business_pincode=str(address_list[index::])

    #Exception case is because of one corrupted file
    if business_name!="":
        df['Business_Name']=business_name
    else:
        df['Business_Name']="NearBy Electronics"
    df['Business_City']=business_city
    df['Business_Country']=business_country
    df['Business_Description']=business_descrip
    df['Business_StreetAddress']=business_street
    df['Business_Zipcode']=business_pincode
    df['Invoice_Tax']=10


    #############BUSINESS DETAILS ENDS###########

    
    
    #This section extracts customer details from the .json file

    ########Customer Details Extraction Begins#######

    customer_details_text=""
    for i in customer_details:
        customer_details_text+=i
    customer_details=[]
    customer_details=customer_details_text.split()

    customer_phone_number=""
    customer_email_address=""
    for i in customer_details:
        if '-' in i:
            customer_phone_number=i
            break 
    for i in customer_details:
        if '@' in i:
            customer_email_address=i 
            break 

    
    #Email and Phone numbers could have been also found using these lines
    # customer_phone_number=extract_phone_numbers(customer_details_text)[0]
    # customer_email_address=extract_email_addresses(customer_details_text)[0]

    index=0
    for i in range(0,len(customer_details)):
        if '@' in customer_details[i]:
            index=i
            break

    index+=1
    while customer_email_address[-4::]!='.com':
        customer_email_address+=customer_details[index]
        index+=1
    
    index=0
    for i in range(0,len(customer_details)):
        if "-" in customer_details[i]:
            index=i+1
            break

    customer_address_list=[]
    for i in range(index,len(customer_details)):
        customer_address_list.append(customer_details[i])
    
    customer_address_1_list=customer_address_list[0:3]
    customer_address_2_list=customer_address_list[3:len(customer_address_list):]

    customer_address_1=""
    customer_address_2=""
    for i in customer_address_1_list:
        customer_address_1+=i+" "
        
    for j in customer_address_2_list:
        customer_address_2+=j+" "
    
    #Customer details assigned
    df['Customer__Address__line1']=customer_address_1
    df['Customer__Address__line2']=customer_address_2
    df['Customer__Email']=customer_email_address
    df['Customer__PhoneNumber']=customer_phone_number


    #Extraction of customer name using string manipulation
    customer_name_list=customer_email_address.split("@")
    customer_name=""
    for i in customer_name_list[0]:
        if(i.isalpha()):
            customer_name+=i
        else:
            customer_name+=" "
    df['Customer__Name']=customer_name


    #######Customer Details End Here#######

    #Invoice Details
    invoice_details_text=""
    for i in invoice_details:
        invoice_details_text+=i

    invoice_details=[]
    invoice_details=invoice_details_text.split()
    issue_date=""
    for i in invoice_details:
        if "-" in i:
            issue_date=i
            break
    df['Invoice__IssueDate']=issue_date
    invoice_number=0
    for i in invoice_details:
        if len(i)>=10:
            invoice_number=i
            break
    df['Invoice__Number']=invoice_number



    #PAYMENT details assign
    payment_details_text=""
    for i in payment_details:
        payment_details_text+=i
    payment_details=[]
    payment_details=payment_details_text.split()

    due_date=""
    for i in payment_details:
        if "-" in i:
            due_date=i
            break
    df['Invoice__DueDate']=due_date

    #Invoice description created here
    details_text=""
    for i in details:
        if i!="DETAILS ":
            details_text+=i
    df['Invoice__Description']=details_text


    #This is the python code to return the csv file to the requried index
    df.to_csv(result_file_path+f"ExtractedData{result_file_index}.csv")


i=0
output_folder_path="/Users/pundarikaksha/Desktop/Adobe Hackathon/InvoicesData/ResultSet/"



for i in range(0,100):

    input_file_path=f"/Users/pundarikaksha/Desktop/Adobe Hackathon/InvoicesData/ResultJSONSet/structuredData{i}.json"

    return_csv(input_file_path,output_folder_path,i)



