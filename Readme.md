# Invoice File Processor

## Overview
Invoice File Processor is an application designed to automate the processing of invoice files. It sends invoices to the Azure Document Intelligence Service to extract relevant data and renames the files based on specific data points such as date, vendor name, vendor tax ID, invoice ID, customer name, and customer tax ID. Processed files are moved to an output directory, and extracted data is saved in a JSON format.

## Requirements
- Python 3.8
- azure-core version 1.30.0
- azure-ai-documentintelligence version 1.0.0b1

## Installation

### Set up a Conda environment
To set up the required environment for this application, follow these steps:

1. Create a new Conda environment:

conda create --name myenv python=3.8

2. Activate the environment:

conda activate myenv

3. Install the required packages:

pip install azure-core==1.30.0
pip install azure-ai-documentintelligence==1.0.0b1


## Usage

### Directory Structure
Before running the application, ensure that your directory structure is as follows:

```
/invoice_processor/
│
├── in/ # Directory containing invoices to process
├── out/ # Directory where processed invoices will be saved
├── error/ # Directory where processed with some issue invoices will be saved (to manual review)
└── invoice_file_processor.py # Main script to run the application
``````

## Running the Application

### Setting Up Azure Document Intelligence
Before running the application, it's crucial to set up Azure Document Intelligence correctly. Follow these steps:

1. **Create Azure Document Intelligence Resource**: 
   - Navigate to the Azure portal and create a new resource for Azure Document Intelligence.
   - Ensure that you are using a compatible Azure region. As of the current version (2023-10-31-preview) of the SDK, Azure Document Intelligence sdk support is only available in the following regions:
     - East US
     - West US 2
     - West Europe

2. **Read Official SDK Documentation**: 
   - It is essential to read the [official documentation](https://learn.microsoft.com/en-us/azure/ai-services/document-intelligence/quickstarts/get-started-sdks-rest-api?view=doc-intel-4.0.0&preserve-view=true&pivots=programming-language-python) of the Azure Document Intelligence SDK.
   - Ensure that you are familiar with the features and limitations of the SDK, particularly the version requirements and regional availability.

3. **Environment Variables Configuration**: 
   - After creating your Azure Document Intelligence resource, you will receive an endpoint configuration and an access key.
   - Set these as environment variables on the system where the application will run (or hardcode it in your script ;)):
     - `DOCUMENT_INTELLIGENCE_ENDPOINT` for the endpoint configuration.
     - `DOCUMENT_INTELLIGENCE_SUBSCRIPTION_KEY` for the access key.

### Executing the Application
Once the Azure setup is complete and environment variables are configured, you can run the application:

1. **Prepare Invoice Files**:
   - Place the invoice files (format: PDF, JPEG/JPG, PNG, BMP, TIFF, HEIF) in the `in/` directory.

2. **Run the Script**:
   - Execute the `invoice_file_processor.py` script:
     ```shell
     python invoice_file_processor.py
     ```

3. **Check Processed Files**:
   - Processed files will be moved to the `out/` directory, and files with incomplete details will be in the `error/` directory.


### Output
Processed invoices will be moved to the `out/` directory and renamed in the following format:

invoice_date_vendor_name_vendor_tax_id_invoice_id_customer_name_customer_tax_id.extension


Additionally, the extracted invoice data will be saved in a JSON file within the `out/` directory.

## Configuration

### Customizing File Naming
The application allows for customization of the output file naming structure. By editing the `invoice_file_processor.py` script, users can modify how the processed invoice files are named.

To change the file naming structure, locate the section in the code where the `new_file_name, all_conditions_met = process_field("InvoiceDate", new_file_name, all_conditions_met, invoice, converters.convert_date)` variable is constructed.

Example:
```python
new_file_name, all_conditions_met = process_field("InvoiceDate", new_file_name, all_conditions_met, invoice, converters.convert_date)
new_file_name, all_conditions_met = process_field("VendorName", new_file_name, all_conditions_met, invoice, converters.remove_special_characters)
new_file_name, all_conditions_met = process_field("VendorTaxId", new_file_name, all_conditions_met, invoice, converters.remove_special_characters)
new_file_name, all_conditions_met = process_field("InvoiceId", new_file_name, all_conditions_met, invoice, converters.remove_special_characters)
new_file_name, all_conditions_met = process_field("CustomerName", new_file_name, all_conditions_met, invoice, converters.remove_special_characters)
new_file_name, all_conditions_met = process_field("CustomerTaxId", new_file_name, all_conditions_met, invoice, converters.remove_special_characters)
```

You can extract simple this fields:

``` 
InvoiceDate
VendorName
VendorAddress
VendorAddressRecipient
VendorTaxId
InvoiceId
InvoiceTotal
CustomerName
CustomerId
CustomerAddress
CustomerAddressRecipient
CustomerTaxId
DueDate
PurchaseOrder
BillingAddress
BillingAddressRecipient
ShippingAddress
ShippingAddressRecipient
SubTotal
TotalTax
PreviousUnpaidBalance
AmountDue
ServiceStartDate
ServiceEndDate
ServiceAddress
ServiceAddressRecipient
RemittanceAddress
RemittanceAddressRecipient
```

Users can add, remove or rearange details in the file name


## License

This project is open source and available under the [MIT License](LICENSE).
