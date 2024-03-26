
import pandas as pd
import json
import numpy as np
import pickle
from typing import Dict, Any
from Classes import Structural_info, Actions, LikelihoodRating, Moderate, RiskRanking, requirements, Info, Location, Images, InspectionReport,CompleteReport,Major,Minor


def save_final_reports_to_json(final_reports_data: Dict[str, Any], output_file_path: str) -> None:
    with open(output_file_path, 'w') as f:
        json.dump(final_reports_data, f, ensure_ascii=False, indent=4)

def load_processed_data_pickle(input_file_path: str) -> Dict[str, Any]:
    with open(input_file_path, 'rb') as file:
        return pickle.load(file)
    

if __name__ == '__main__':
    # Load the DataFrame
    excel_path = r'C:\Users\aleja\Documents\PDFFF\complete_inspection_report.xlsx'
    df = pd.read_excel(excel_path)
    output_file_path = 'grouting_final_inspection_reports_excel.json'
    # Initialize an empty list to hold all the created objects, if needed
    all_objects = []
    complete_report = CompleteReport()
    final_reports_data = {}
    for index, row in df.iterrows():
        # Create instances of your classes based on the current row
        actions = Actions(action_type=row['Action Type'], action_code=row["Action Code"], action_level=str(row["Action Level"]))
        likelihood_rating = LikelihoodRating(rating=row['Likelyhood'])
        
        # Assuming you have predefined classes for consequences based on their severity
        consequence_map = {'Major': Major(), 'Moderate': Moderate(), 'Minor': Minor()}
        risk_consequence = consequence_map.get(row['Risk consequence'])  # Defaulting to Moderate if not found
        
        risk_ranking = RiskRanking(likelihood=likelihood_rating, consequence=risk_consequence)
        reqs = requirements(shutdown_req=row['Shutdown Requirement'], eng_req=row['Engineering Requirement'], overdue=row['Requirements Overdue'])
        info = Info()


        potential_incident=row['Potential Incident']
        stru_failure_mech= row['Failure Mechanism']
        action_methodology= row['Action Methodology']
        struc_issue_description=row['Issue Description']
        recomended_act=row['Recommended Action']

        image_dict = {'1': row.get('Image 1', None), '2': row.get('Image 2', None), '3': row.get('Image 3', None)}
        images = Images(images_dict=image_dict)

        location = Location(facility=row['Facility'],location=row['Location'],component=row['Component'],area=row['Area'])
        
        _cost = str(row['Repair Cost'])
        _ID = row['Seq Number']

        _structural_info = Structural_info(
        struc_issue_description=struc_issue_description,
        potential_incident=potential_incident,
        stru_failure_mech=stru_failure_mech,
        action_methodology=action_methodology,
        recomended_act=recomended_act,
        cost=_cost
        )

        inspection_report = InspectionReport(
        id=_ID,
        seq_number= row['Seq Number']
        actions=actions,
        location=location,
        risk_ranking=risk_ranking,
        info=info,
        requirements=reqs,
        structural_info=_structural_info,
        images=images)


        report_dict = inspection_report.to_custom_dict()
        image_dict = images.json()

        combined_data = {
            "report": report_dict,
            "images": json.loads(image_dict)['images_dict']
        }
        

        complete_report.append_report(inspection_report)
        final_reports_data[_ID] = combined_data
        



        save_final_reports_to_json(final_reports_data, output_file_path)
        complete_report.compute_ids()


