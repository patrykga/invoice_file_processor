import re
import dateparser

def create_safe_filename(*strings):
    combined_string = '_'.join(strings)

    # Replace special characters and newlines with '_'
    safe_filename = re.sub(r'[\n\/:*?"<>| ]', '_', combined_string)

    # Remove underscore at the beginning if it exists
    safe_filename = re.sub(r'^_', '', safe_filename)

    return safe_filename

def remove_special_characters(input_string):
    cleaned_string = re.sub(r'[^a-zA-Z0-9_]', '', input_string)
    return cleaned_string
    
def convert_date(date_string):
    try:
        parsed_date = dateparser.parse(date_string)

        formatted_date = parsed_date.strftime("%Y.%m.%d")

        return formatted_date
    except ValueError:
        print(f"Error: Unable to parse date '{date_string}'")
        return date_string