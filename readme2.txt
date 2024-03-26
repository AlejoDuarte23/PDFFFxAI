1.Preprocesing.py


Requires Base path for the folder twith the images 
infodict is created based on the metadata 
create a json file path to save the info dict (output_file_path)
output_file_path = 'grout_damage.json'
--
example with grouting 


    # create the folder 
    base_path = "E:\Grouting_damage"
    info_dict = create_info_dict(base_path)
    print(json.dumps(info_dict, indent=4))

    output_file_path = 'grout_damage.json'
    save_info_dict(info_dict,output_file_path)



2. Extraction_images.py

requires json output file path from Preprocesing , in this case "grout_damage.json"
the runs: processed_inspection_data = process_inspection_data(filepath,500) process the images of the inspections and returns a dictionary with {id:{Location,Images}} whe Location and Images are pydantic model classess
--
example with grouting

filepath = 'grout_damage.json'  # Ensure this is the correct path to your JSON file
processed_inspection_data = process_inspection_data(filepath,500)
output_file_path = 'grout_damage_processed_inspection_data.pkl'  # The file to save to
save_processed_data_pickle(processed_inspection_data, output_file_path)

3. Factory 

requires the input file of the pickle crated in extraction images 
and a json file direction of the outpt

the modify cost function , and assign the sturctural assessment report information 

---
Examples

    input_file_path = 'grout_damage_processed_inspection_data.pkl'
    output_file_path = 'grouting_final_inspection_reports.json'

    actions_example = Actions(action_type='Concrete Cracking', action_code='CC', action_level='3')
    likelihood_rating_example = LikelihoodRating(rating='D')
    moderate_consequence_example = Moderate()
    risk_ranking_example = RiskRanking(likelihood=likelihood_rating_example, consequence=moderate_consequence_example)
    reqs_example = requirements(shutdown_req='NO', eng_req='NO', overdue='NO')
    info_example = Info()

    inspection_report_factory(
        input_file_path = input_file_path,
        potential_incident="Improper load redistribution from the structure to the foundation element leading to instability and/or overloading.",
        stru_failure_mech="The failure mechanism is a combination of mechanical overload, aging, and wear due to the harsh operating conditions.",
        action_methodology="Remove existing grout and clean the surface thoroughly. Drill a hole on the anchoring plate to pump the grout in the cavity. Follow the grout instructions from the OEM and build an adequate roll off angle.",
        struc_issue_description="Significant damage in the grouting between the structure base and the concrete support has been observed...",
        recomended_act='REPAIR (Actionable)',
        actions=actions_example,
        likelihood_rating=likelihood_rating_example,
        moderate_consequence=moderate_consequence_example,
        risk_ranking=risk_ranking_example,
        reqs=reqs_example,
        info=info_example,
        output_file_path = 'output_file_path'

    )



4. FFPDF.PY
pdf creations 
requires de ouptu of the previous section filepath = 'grouting_final_inspection_reports.json'
the inspection report are loaded 
load_inspection_reports_from_json

a new folder is created and the template for the pdf creations is selsctes
the magic happend with : process_reports_and_generate_pdfs(

---
 example with grouting




if __name__ == '__main__':
    # Assuming the file is named 'final_inspection_reports.json'
    filepath = 'grouting_final_inspection_reports.json'
    final_reports_data = load_inspection_reports_from_json(filepath)
    output_folder = r'grout_damges'
    template_dir = r"Templates\moderate_template.pdf"  # Assuming the template directory is fixed

    process_reports_and_generate_pdfs(final_reports_data, output_folder,template_dir)






