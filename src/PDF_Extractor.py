

import os
import csv
import logging
from zipfile import ZipFile
from adobe.pdfservices.operation.auth.credentials import Credentials
from adobe.pdfservices.operation.exception.exceptions import ServiceApiException, ServiceUsageException, SdkException
from adobe.pdfservices.operation.pdfops.options.extractpdf.extract_pdf_options import ExtractPDFOptions
from adobe.pdfservices.operation.pdfops.options.extractpdf.extract_element_type import ExtractElementType
from adobe.pdfservices.operation.execution_context import ExecutionContext
from adobe.pdfservices.operation.io.file_ref import FileRef
from adobe.pdfservices.operation.pdfops.extract_pdf_operation import ExtractPDFOperation


logging.basicConfig(level=logging.INFO)


credentials_path = 'pdfservices-api-credentials.json'


for i in range(0,100):
    pdf_file_path=f"/Users/pundarikaksha/Desktop/Adobe Hackathon/InvoicesData/TestDataSet/output{i}.pdf"


    zip_file_path = f'/Users/pundarikaksha/Desktop/Adobe Hackathon/InvoicesData/ResultZipSet/extracted_dataoutput{i}.zip'

    try:
        #Initial setup, create credentials instance.
        credentials = Credentials.service_account_credentials_builder()\
            .from_file("/Users/pundarikaksha/Desktop/Adobe Hackathon/PDFServicesSDK-Python (Extract, Auto-Tag)Samples/adobe-dc-pdf-services-sdk-python-samples/pdfservices-api-credentials.json") \
            .build()

        #Create an ExecutionContext using credentials and create a new operation instance.
        execution_context = ExecutionContext.create(credentials)
        extract_pdf_operation = ExtractPDFOperation.create_new()

        #Set operation input from a source file.
        source = FileRef.create_from_local_file(pdf_file_path)
        extract_pdf_operation.set_input(source)

        #Build ExtractPDF options and set them into the operation
        extract_pdf_options: ExtractPDFOptions = ExtractPDFOptions.builder() \
            .with_element_to_extract(ExtractElementType.TEXT) \
            .build()
        extract_pdf_operation.set_options(extract_pdf_options)

        #Execute the operation.
        result: FileRef = extract_pdf_operation.execute(execution_context)

        result.save_as(zip_file_path)


    except (ServiceApiException, ServiceUsageException, SdkException) as e:
        logging.exception("Exception encountered while executing operation: %s", str(e))
