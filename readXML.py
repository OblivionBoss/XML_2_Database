import os
import pandas as pd
import xml.etree.ElementTree as ET

def parse_xml(file_path):
    """Parse a single XML file and return its data in a flattened dictionary."""
    tree = ET.parse(file_path)
    root = tree.getroot()
    
    # Initialize a dictionary to hold the data
    data_dict = {}
    
    # Recursive function to parse XML tree
    def parse_element(element, parent_key=''):
        """Recursively parse the XML element and populate the data_dict."""
        for child in element:
            # Create the key for the child element
            child_key = f"{parent_key}.{child.tag}" if parent_key else child.tag
            
            # If the child has sub-elements, recurse
            if len(child) > 0:
                parse_element(child, child_key)
            else:
                # If the child has no sub-elements, assign the text value to data_dict
                if child_key in data_dict:
                    # If key already exists, append the new value (handle multiple entries)
                    data_dict[child_key] += f";{child.text.strip()}" if child.text else ''
                else:
                    data_dict[child_key] = child.text.strip() if child.text else ''
    
    # Start parsing from root element
    parse_element(root)
    
    return data_dict

def main(xml_directory, output_csv):
    """Main function to convert XML files to a DataFrame and save to CSV."""
    # List to hold the parsed data from each XML file
    parsed_data = []
    
    # Iterate through each file in the XML directory
    for filename in os.listdir(xml_directory):
        if filename.endswith(".xml"):
            file_path = os.path.join(xml_directory, filename)
            # Parse the XML file
            data_dict = parse_xml(file_path)
            # Add the parsed data to the list
            parsed_data.append(data_dict)
    
    # Convert the list of dictionaries to a DataFrame
    df = pd.DataFrame(parsed_data)
    
    # Save the DataFrame to a CSV file
    df.to_csv(output_csv, index=False)
    
    print(f"Data saved to {output_csv}")

# Usage
xml_directory = '.\\XML_files'  # Specify the path to your XML files directory
output_csv = 'XML_files\\output.csv'  # Specify the path for the output CSV file
main(xml_directory, output_csv)
