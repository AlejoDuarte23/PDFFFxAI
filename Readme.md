
PHASE I : Pydantic Models Definition
Base Models: Defined base models (Actions, Location, LikelihoodRating, RiskRanking, Info, requirements, Structural_info) to encapsulate various aspects of inspection data such as actions, locations, risk assessments, and structural issues.

Usage
Instantiate the InspectionReport with validated data from Pydantic models, then call to_custom_dict() to generate a dictionary ready for report generation or further processing.

inspection_report = InspectionReport(
    actions=actions,
    location=location,
    risk_ranking=risk_ranking,
    info=info,
    requirements=reqs,
    structural_info=structural_info
)

report_dict = inspection_report.to_custom_dict()

* Pending create Union Literals for repair methods and consequence of failure for AI to select them

PHASE II: Feature Extraction
* Allow AI to access Literal and Field Type to extract relevant features such as location Area Component 
* test Fuzzy finder instead of GPT3.5 for data extraction
* DB for cost based on @(repair , component , area )

PHASE III: GPT V and desicion making 
- Extract visual features 
- Fine Tune the model for desicion making and automation

--------

Instalation:
pip install pdfrw
pip install reportlab
pip install pydantic