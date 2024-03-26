import json 
import numpy as np
import pickle
from Classes import Structural_info,Actions,LikelihoodRating,Minor,RiskRanking,requirements,Info,Location,Images,InspectionReport
from Extraction_test import  gextraction
from pydantic import ValidationError,BaseModel
from instructor import llm_validator



#%%  extract :


def cost()->str:
    #  Cost
    mean_cost = 10000 
    std_dev_cost = 2000  
    cost = np.random.normal(mean_cost, std_dev_cost)
    return f"{cost:.2f}"
 


def save_processed_data_pickle(processed_data, output_file_path):
    with open(output_file_path, 'wb') as file:
        pickle.dump(processed_data, file)

def load_processed_data_pickle(input_file_path):
    with open(input_file_path, 'rb') as file:
        return pickle.load(file)

def process_inspection_data(filepath: str, threshold: int = 500):
    with open(filepath, 'r') as json_file:
        filtered_results = json.load(json_file)

    processed_data = {}
    problematic_entries = {}
    id_counter = 1  # Monotonically increasing ID

    for key, value in filtered_results.items():
        try:
            # Extract and prepare image metadata
            image_metadata = {
                "description1": value['location'],
                "description2": value['description']
            }
            print(image_metadata)
            # Call the gextraction function with the image metadata
            response = gextraction(image_metadata)
            if response:
                for location_instance in response:
                    assert isinstance(location_instance, Location), "gextraction must return a Location instance"
                    
                    # Create Images instance from images dict in value
                    images_instance = Images(images_dict=value['images'])

                    # Store the Location instance and Images instance together using id_counter as the key
                    processed_data[id_counter] = {
                        "Location": location_instance,
                        "Images": images_instance
                    }
                    print(location_instance)  # Assuming you want to print the location instances processed
                    id_counter += 1  # Increment ID for the next entry

                    if id_counter > threshold:  # Adjust as needed
                        break
        except (AssertionError, ValidationError, KeyError) as e:
            print(f"Problem processing entry {key}: {str(e)}")
            problematic_entries[key] = value
        except Exception as e:
            print(f"Unexpected error with entry {key}: {str(e)}")
            problematic_entries[key] = value

        if id_counter > threshold:
            break

    # Optionally, save the problematic entries to a file
    with open('problematic_entries.json', 'w') as outfile:
        json.dump(problematic_entries, outfile, indent=4)

    return processed_data


if  False:
    filepath = 'damage_in_pc.json'  # Ensure this is the correct path to your JSON file
    processed_inspection_data = process_inspection_data(filepath,500)
    output_file_path = 'processed_inspection_data.pkl'  # The file to save to
    save_processed_data_pickle(processed_inspection_data, output_file_path)
    
if False:
    filepath = 'grout_damage.json'  # Ensure this is the correct path to your JSON file
    processed_inspection_data = process_inspection_data(filepath,500)
    output_file_path = 'grout_damage_processed_inspection_data.pkl'  # The file to save to
    save_processed_data_pickle(processed_inspection_data, output_file_path)




