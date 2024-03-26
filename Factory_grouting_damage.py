
# import json 
# import numpy as np
# import pickle
# from Classes import Structural_info,Actions,LikelihoodRating,Minor,RiskRanking,requirements,Info,Location,Images,InspectionReport,Moderate
# # from Extraction_test import  gextraction
# from pydantic import ValidationError

# def cost()->str:
#     #  Cost
#     mean_cost = 12000 
#     std_dev_cost = 1000  
#     cost = np.random.normal(mean_cost, std_dev_cost)
#     return f"{cost:.2f}"


# def save_final_reports_to_json(final_reports_data, output_file_path):
#     with open(output_file_path, 'w') as f:
#         json.dump(final_reports_data, f, ensure_ascii=False, indent=4)


# def load_processed_data_pickle(input_file_path):
#     with open(input_file_path, 'rb') as file:
#         return pickle.load(file)
    
# input_file_path = 'grout_damage_processed_inspection_data.pkl'  # The file to load from
# loaded_data = load_processed_data_pickle(input_file_path)
# final_reports_data = {}
# for id_counter,combine_dict in loaded_data.items():

#     location = combine_dict['Location']
#     images = combine_dict['Images']
        

            
#     potential_incident = '''Improper load redistribution from the structure to the foundation element leading to instability and/or overloading.'''

#     stru_failure_mech = '''The failure mechanism is a combination of mechanical overload, aging, and wear due to the harsh operating conditions.'''

#     action_methodology = '''Remove existing grout and clean the surface thoroughly. Drill a hole on the anchoring plate to pump the grout in the cavity. Follow the grout instructions from the OEM and build an adequate roll off angle.'''

#     struc_issue_description = '''Significant damage in the grouting between the structure base and the concrete support has been observed. The most probable causes are mechanical overload, aging, and wear, or even poor application practices during construction or material incompatibility. The damaged grouting will not be able to distribute the loads uniformly to the foundation elements and will fail to brace the anchor bolts properly, generating bending stress in the bolts.'''

#     recomended_act = 'REPAIR (Actionable)'



#     actions = Actions(
#         action_type='Concrete Cracking', 
#         action_code='CC',  
#         action_level='3'  
#     )


#     likelihood_rating = LikelihoodRating(rating='D')
#     moderate_consequence = Moderate()
#     risk_ranking = RiskRanking(likelihood=likelihood_rating, consequence=moderate_consequence)

#     reqs = requirements(
#         shutdown_req='NO',
#         eng_req='NO',
#         overdue='NO'
#     )

#     info = Info()


#     # we add  the location adn images hre 
#     _structural_info = Structural_info(struc_issue_description=struc_issue_description,
#     potential_incident=potential_incident,  
#     stru_failure_mech=stru_failure_mech,
#     action_methodology=action_methodology,
#     recomended_act=recomended_act,
#     cost=cost()
#     )


#     inspection_report = InspectionReport(
#     actions=actions,
#     location=location,
#     risk_ranking=risk_ranking,
#     info=info,
#     requirements=reqs,
#     structural_info=_structural_info,
#     images=images
# )


#     report_dict = inspection_report.to_custom_dict()
#     # dump current images 
#     image_dict = images.json()
#     # Combine the report dict and images dict for storage
#     combined_data = {
#         "report": report_dict,
#         "images": json.loads(image_dict)['images_dict']
#     }

#     # Store the combined data in the final reports data dict with an unique ID
#     final_reports_data[id_counter] = combined_data

#     id_counter += 1  # Increment the ID for the next report

#     # create a dict and store each iteration with {id,report_dict,images dict}

# def save_final_reports_to_json(final_reports_data, output_file_path):
#     with open(output_file_path, 'w') as f:
#         json.dump(final_reports_data, f, ensure_ascii=False, indent=4)


# output_file_path = 'grouting_final_inspection_reports.json'
# save_final_reports_to_json(final_reports_data, output_file_path)



# # with open('damage_in_pc.json', 'r') as json_file:
# #     filtered_results = json.load(json_file)

# # # Iterate over the keys and values in the loaded JSON data
# # Location_instance = []
# # processed_entries = 0

# # for key, value in filtered_results.items():

# #     if processed_entries >= 50:
# #         break

# #     image_metadata = {
# #         "location": value['location'],
# #         "description": value['description']
# #     }
# #     # Call the gextraction function with the image metadata
# #     response2 = gextraction(image_metadata)
# #     if response2:
# #         for location in response2:
# #             assert isinstance(location, Location)
# #             Location_instance.append(location)
# #             # Depending on your actual code, process the location instances as needed
# #             print(location)
            
# #     processed_entries += 1  # Placeholder for actual processing

import json
import numpy as np
import pickle
from typing import Dict, Any
from Classes import Structural_info, Actions, LikelihoodRating, Moderate, RiskRanking, requirements, Info, Location, Images, InspectionReport,CompleteReport

def cost() -> str:
    mean_cost = 12000
    std_dev_cost = 1000
    cost_value = np.random.normal(mean_cost, std_dev_cost)
    return f"{cost_value:.2f}"

def save_final_reports_to_json(final_reports_data: Dict[str, Any], output_file_path: str) -> None:
    with open(output_file_path, 'w') as f:
        json.dump(final_reports_data, f, ensure_ascii=False, indent=4)

def load_processed_data_pickle(input_file_path: str) -> Dict[str, Any]:
    with open(input_file_path, 'rb') as file:
        return pickle.load(file)

def inspection_report_factory(input_file_path:str,potential_incident: str, stru_failure_mech: str, action_methodology: str, struc_issue_description: str, recomended_act: str, actions: Actions, likelihood_rating: LikelihoodRating, moderate_consequence: Moderate, risk_ranking: RiskRanking, reqs: requirements, info: Info,output_file_path:str , excel_output_path:str) -> None:
    loaded_data = load_processed_data_pickle(input_file_path)
    complete_report = CompleteReport()
    final_reports_data = {}

    for id_counter, combine_dict in loaded_data.items():
        location = combine_dict['Location']
        images = combine_dict['Images']
        # print(images)

        _structural_info = Structural_info(
            struc_issue_description=struc_issue_description,
            potential_incident=potential_incident,
            stru_failure_mech=stru_failure_mech,
            action_methodology=action_methodology,
            recomended_act=recomended_act,
            cost=cost()
        )

        inspection_report = InspectionReport(
            id=id_counter,
            seq_number = id_counter,
            actions=actions,
            location=location,
            risk_ranking=risk_ranking,
            info=info,
            requirements=reqs,
            structural_info=_structural_info,
            images=images
        )
        
        report_dict = inspection_report.to_custom_dict()
        print(inspection_report.images.images_dict.keys())
        image_dict = images.json()

        combined_data = {
            "report": report_dict,
            "images": json.loads(image_dict)['images_dict']
        }

        complete_report.append_report(inspection_report)
        final_reports_data[id_counter] = combined_data
    



    save_final_reports_to_json(final_reports_data, output_file_path)
    complete_report.compute_ids()

    complete_report.export_to_xlsx(excel_output_path)




if __name__ == "__main__":
    # Example of calling the modified function with parameters
    input_file_path = 'grout_damage_processed_inspection_data.pkl'
    output_file_path = 'grouting_final_inspection_reports.json'

    actions_example = Actions(action_type='Concrete Cracking', action_code='CC', action_level='3')
    likelihood_rating_example = LikelihoodRating(rating='D')
    moderate_consequence_example = Moderate()
    risk_ranking_example = RiskRanking(likelihood=likelihood_rating_example, consequence=moderate_consequence_example)
    reqs_example = requirements(shutdown_req='NO', eng_req='NO', overdue='NO')
    info_example = Info()

    excel_output_path = 'complete_inspection_report.xlsx'

    inspection_report_factory(
        input_file_path = input_file_path,
        potential_incident="Improper load redistribution from the structure to the foundation element leading to instability and/or overloading.",
        stru_failure_mech="The failure mechanism is a combination of mechanical overload, aging, and wear due to the harsh operating conditions.",
        action_methodology="Remove existing grout and clean the surface thoroughly. Drill a hole on the anchoring plate to pump the grout in the cavity. Follow the grout instructions from the OEM and build an adequate roll off angle.",
        struc_issue_description='''Significant damage in the grouting between the structure base and the concrete support has been observed. The most probable causes are mechanical overload, aging, and wear, or even poor application practices during construction or material incompatibility. The damaged grouting will not be able to distribute the loads uniformly to the foundation elements and will fail to brace the anchor bolts properly, generating bending stress in the bolts.'''
,
        recomended_act='REPAIR (Actionable)',
        actions=actions_example,
        likelihood_rating=likelihood_rating_example,
        moderate_consequence=moderate_consequence_example,
        risk_ranking=risk_ranking_example,
        reqs=reqs_example,
        info=info_example,
        output_file_path =output_file_path,
        excel_output_path = excel_output_path

    )


