
import json 
import numpy as np
import pickle
from Classes import Structural_info,Actions,LikelihoodRating,Minor,RiskRanking,requirements,Info,Location,Images,InspectionReport
from Extraction_test import  gextraction
from pydantic import ValidationError

def cost()->str:
    #  Cost
    mean_cost = 10000 
    std_dev_cost = 2000  
    cost = np.random.normal(mean_cost, std_dev_cost)
    return f"{cost:.2f}"


def save_final_reports_to_json(final_reports_data, output_file_path):
    with open(output_file_path, 'w') as f:
        json.dump(final_reports_data, f, ensure_ascii=False, indent=4)


def load_processed_data_pickle(input_file_path):
    with open(input_file_path, 'rb') as file:
        return pickle.load(file)
    
input_file_path = 'processed_inspection_data.pkl'  # The file to load from
loaded_data = load_processed_data_pickle(input_file_path)
final_reports_data = {}
for id_counter,combine_dict in loaded_data.items():

    location = combine_dict['Location']
    images = combine_dict['Images']
        

            
    potential_incident = '''Continued coating degradation leading to corrosive attack.'''

    stru_failure_mech = '''Material loss associated with corrosion.'''

    action_methodology = '''Pressure blast cleaning of the structure to remove all dirt and debris.
    Apply surface protectant.'''

    struc_issue_description = '''The protective coating on the structural elements have some damage that could lead to ineffectiveness of corrosion protection. It is expected that corrosive attacks will increase on these areas as the coating continues to deteriorate.'''

    recomended_act = 'REPAIR (Actionable)'



    actions = Actions(
        action_type='Protective Coating', 
        action_code='PC',  
        action_level='2'  
    )


    likelihood_rating = LikelihoodRating(rating='D')
    moderate_consequence = Minor()
    risk_ranking = RiskRanking(likelihood=likelihood_rating, consequence=moderate_consequence)

    reqs = requirements(
        shutdown_req='NO',
        eng_req='NO',
        overdue='NO'
    )

    info = Info()


    # we add  the location adn images hre 
    _structural_info = Structural_info(struc_issue_description=struc_issue_description,
    potential_incident=potential_incident,  
    stru_failure_mech=stru_failure_mech,
    action_methodology=action_methodology,
    recomended_act=recomended_act,
    cost=cost()
    )


    inspection_report = InspectionReport(
    actions=actions,
    location=location,
    risk_ranking=risk_ranking,
    info=info,
    requirements=reqs,
    structural_info=_structural_info,
    images=images
)


    report_dict = inspection_report.to_custom_dict()
    # dump current images 
    image_dict = images.json()
    # Combine the report dict and images dict for storage
    combined_data = {
        "report": report_dict,
        "images": json.loads(image_dict)['images_dict']
    }

    # Store the combined data in the final reports data dict with an unique ID
    final_reports_data[id_counter] = combined_data

    id_counter += 1  # Increment the ID for the next report

    # create a dict and store each iteration with {id,report_dict,images dict}

def save_final_reports_to_json(final_reports_data, output_file_path):
    with open(output_file_path, 'w') as f:
        json.dump(final_reports_data, f, ensure_ascii=False, indent=4)


output_file_path = 'final_inspection_reports2.json'
save_final_reports_to_json(final_reports_data, output_file_path)



# with open('damage_in_pc.json', 'r') as json_file:
#     filtered_results = json.load(json_file)

# # Iterate over the keys and values in the loaded JSON data
# Location_instance = []
# processed_entries = 0

# for key, value in filtered_results.items():

#     if processed_entries >= 50:
#         break

#     image_metadata = {
#         "location": value['location'],
#         "description": value['description']
#     }
#     # Call the gextraction function with the image metadata
#     response2 = gextraction(image_metadata)
#     if response2:
#         for location in response2:
#             assert isinstance(location, Location)
#             Location_instance.append(location)
#             # Depending on your actual code, process the location instances as needed
#             print(location)
            
#     processed_entries += 1  # Placeholder for actual processing




