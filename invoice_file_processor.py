import os
import shutil
import json
import converters

from azure.core.credentials import AzureKeyCredential
from azure.ai.documentintelligence import DocumentIntelligenceClient
from azure.ai.documentintelligence.models import AnalyzeDocumentRequest

endpoint = os.environ["DOCUMENT_INTELLIGENCE_ENDPOINT"]
key = os.environ["DOCUMENT_INTELLIGENCE_SUBSCRIPTION_KEY"]

def process_field(field_name, new_file_name, all_conditions_met, invoice, convert_function=None):
    field = invoice.fields.get(field_name)
    if field:
        field_content = field.get('content')
        if convert_function:
            field_content = convert_function(field_content)
        new_file_name = new_file_name + "_" + field_content
        print(f"{field_name}: {field.get('content')} has confidence: {field.get('confidence')}")
    else:
        all_conditions_met = False
    return new_file_name, all_conditions_met

    
def analyze_invoices():

    for filename in os.listdir("in"):
        filepath = os.path.join("in", filename)

        if os.path.isfile(filepath):
            print(filepath)

            document_intelligence_client = DocumentIntelligenceClient(
                endpoint=endpoint, credential=AzureKeyCredential(key)
            )

            try:
                with open(filepath, "rb") as f:
                    file_content = f.read()

                    if not file_content:
                        print("Error: The file is empty.")
                    else:
                        poller = document_intelligence_client.begin_analyze_document(
                            "prebuilt-invoice", analyze_request=file_content, content_type="application/octet-stream"
                        )
                        invoices = poller.result()

                        new_file_name = ""

                        all_conditions_met = True

                        for idx, invoice in enumerate(invoices.documents):
                            print(f"--------Analyzing invoice --------")

                            new_file_name, all_conditions_met = process_field("InvoiceDate", new_file_name, all_conditions_met, invoice, converters.convert_date)
                            new_file_name, all_conditions_met = process_field("VendorName", new_file_name, all_conditions_met, invoice, converters.remove_special_characters)
                            new_file_name, all_conditions_met = process_field("VendorTaxId", new_file_name, all_conditions_met, invoice, converters.remove_special_characters)
                            new_file_name, all_conditions_met = process_field("InvoiceId", new_file_name, all_conditions_met, invoice, converters.remove_special_characters)
                            new_file_name, all_conditions_met = process_field("CustomerName", new_file_name, all_conditions_met, invoice, converters.remove_special_characters)
                            new_file_name, all_conditions_met = process_field("CustomerTaxId", new_file_name, all_conditions_met, invoice, converters.remove_special_characters)

                            print("----------------------------------------")

                            file_name = converters.create_safe_filename(new_file_name)

                            print(file_name)

                            output = invoices.as_dict()

                            out_directory = "out" if all_conditions_met else "error"


                            with open(os.path.join(out_directory, file_name + '.json'), 'w') as json_file:
                                json.dump(output, json_file)
                        
                            file, file_extension = os.path.splitext(filepath)
                            shutil.copy(filepath, os.path.join(out_directory, file_name + file_extension))

            except FileNotFoundError:
                print(f"Error: File not found at {filepath}")

            except Exception as e:
                print(f"An error occurred: {e}")

            

if __name__ == "__main__":
    analyze_invoices()