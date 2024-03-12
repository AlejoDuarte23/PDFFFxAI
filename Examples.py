



from pydantic import BaseModel , Field
from typing import Literal,Union

# %% Model for AI training 


class Actions(BaseModel):
    action_type: Literal['Protective Coating', 'Steel Corrosion', 'Steel Damage', 'Structural Bolts', 'Structural Welds', 'Design', 'Safety Machinery', 'Concrete Finish', 'Concrete Cracking', 'Concrete Drummy', 'Concrete Spalling', 'Reinforcement Corrosion', 'Embankments', 'Retaining Walls', 'Cathodic Protection', 'Facing Panels', 'Soil Reinforcement', 'Earth Wall Drainage']
    action_code: Literal['PC', 'SC', 'ST', 'SB', 'SW', 'DE', 'SM', 'CF', 'CC', 'CD', 'CS', 'CR', 'EMB', 'RW', 'CP', 'EWF', 'EWS', 'EWD']
    action_level: Literal['1','2','3','4','5']


class Location(BaseModel):
    facility: Literal['Gregory Crinum Mine'] = 'Gregory Crinum Mine'
    area: Literal[
        'CHPP Building', 'Foundations', 'Centrifuges Floor', 'Mezzanine Floor',
        'Vibrating Screens Floor', 'Top Floor', 'Belt Filter Building', 'Access Structures',
        'Rotary Breaker Station 5205', '5179 Rotary Breaker', 'Crinum 5128 Breaker',
        'Crinum 5127 Vibrating Feeder', 'ROM Structure', 'Conveyors', 'Conveyor CV805',
        'Conveyor CV802', 'Conveyor CV801', 'Conveyor CV330', 'Conveyor CV715',
        'Conveyors CV231 to CV233', 'Conveyor CV231', 'Conveyor CV232', 'Conveyor CV233',
        'Conveyor CV216', 'Conveyor CV207', 'Conveyor CV206', 'Conveyor CV204',
        'Conveyor Crinum CV129', 'Conveyor Crinum CV112', 'Conveyor Crinum CV113',
        'Conveyor Crinum East Ovland', 'Conveyor Crinum East Ramp', 'Conveyor Crinum Tunnel',
        'Stacker Crinum Mine', 'Transfer Station CV815Y-CV805', 'Clean Coal Sampling Tower',
        'Tailings Thickener', 'Froth Thickener', 'Microcell Building', 'Fire Control System Shed',
        'Compressors Shed', 'Storage Bins', 'TLO Bin', '300 Tonne Bin Structure', 'Rejects Bin',
        '1000 Tonne Bin', 'Cranes', 'Tunnels', 'Tunnel CV206', 'Tunnel CV5156', 'Clarifier Tunnel',
        'Tunnel CV815Y', 'Buildings', 'Maintenance Workshop Building', 'CHPP Lab',
        'CHPP Control Building', 'Gregory Main Workshop', 'Mining Engineers Office',
        'Water Treatment Plant (WTP)', 'Storage Sheds'
    ]
    component: str = Field(default='component of the structure where the defect is found')
    location: str = Field(default='short location of the component')



class Major(BaseModel):
    des_health_sft: str = Field(default='''Permanent total disabilities; single fatality''')
    des_damage: str = Field(default='''Major damage to facility requiring corrective action
Loss of production < six months''')
    des_financial: str = Field(default='''AUD $50,000 - $500,000''')

class Moderate(BaseModel):
    des_health_sft: str = Field(default='''Major injury or health effects: >1 work day lost case; permanent disability''')
    des_damage: str = Field(default='''Moderate damage to equipment and / or facility Loss of production < one week''')
    des_financial: str = Field(default='''AUD $10,000 - $50,000''')

class Minor(BaseModel):
    des_health_sft: str = Field(default='''Minor injuries or health effects: minor medical, restricted work; or <1 work day lost case''')
    des_damage: str = Field(default='''Minor or superficial damage to equipment and / or facility No loss of production''')
    des_financial: str = Field(default='''AUD $1,000 - $10,000''')


class LikelihoodRating(BaseModel):
    rating: Literal['A', 'B', 'C', 'D', 'E']
    description: str = Field(default_factory=str)

    def __init__(self, **data):
        super().__init__(**data)
        descriptions = {
            'A': 'The event is expected to occur in most circumstances [once per week]',
            'B': 'Will probably occur in most circumstances [once per month]',
            'C': 'Might occur at some time [once per year]',
            'D': 'Could occur at some time [once per 10 years]',
            'E': 'May occur only in exceptional circumstances [once per life of facility >20 years]',
        }
        self.description = descriptions[self.rating]


class RiskRanking(BaseModel):
    likelihood: LikelihoodRating
    consequence: Union[Major, Moderate, Minor]
    rank_code: str = Field(default_factory=str)

    class Config:
        arbitrary_types_allowed = True

    def __init__(self, **data):
        super().__init__(**data)
        # Define a mapping from likelihood to row and consequence to column
        likelihood_map = {'A': 0, 'B': 1, 'C': 2, 'D': 3, 'E': 4}
        consequence_map = {Major: 3, Moderate: 2, Minor: 1}
        consequence_map_str = { 3:'Major', 2:'Moderate', 1:'Minor'}

                
        risk_matrix = [
            ['H11', 'H16', 'E20', 'E23', 'E25'],
            ['M7', 'H12', 'H17', 'E21', 'E24'],
            ['L4', 'M8', 'H13', 'E18', 'E22'],
            ['L2', 'L5', 'M9', 'H14', 'E19'],
            ['L1', 'L3', 'L6', 'M10', 'H15']
        ]
                
        row = likelihood_map[self.likelihood.rating]
        col = consequence_map[type(self.consequence)]
        self.rank_code = f"{risk_matrix[row][col]} - {consequence_map_str[col]}"
        print(self.rank_code) 


class Info(BaseModel):
    PO: str = 'PO-93356'
    date: str = '22/02/2024'
    res_person: str = 'Jodie Belleville'
    rep_ref: str = 'Structural Integrity Audit 2024'
    action_status: str = 'Incomplete'

class requirements(BaseModel):
    shutdown_req:str = Literal['YES','NO']
    eng_req: str = Literal['YES','NO']
    overdue: str = Literal['YES','NO']


class Structural_info(BaseModel):
    struc_issue_description: str= Field(description="description of the structural issue , expalining the cause and  structural and operational cosecuente of the defect ")
    potential_incident:str= Field(description="description of potencial incident the defect can cause ")
    stru_failure_mech:str= Field(description="what is the damage mechanism causing the defect ")
    action_methodology:str= Field(description="explenation of the repair method ")
    recomended_act:str = Literal['REPAIR (Actionable)','FIT FOR SERVICE (Informative)','REPLACE (Actionable)','BARRICADE (Actionable)','DECOMISSION (Actionable)'] 
    cost:str =  Field(description="cost of the repair method or strategies ")

class InspectionReport(BaseModel):
    actions: Actions
    location: Location
    risk_ranking: RiskRanking
    info: Info
    requirements: requirements
    structural_info: Structural_info

    def to_custom_dict(self) -> dict:
        return {
            "Cost_r": self.structural_info.cost,
            "Overdue": self.requirements.overdue,
            "Description": self.structural_info.struc_issue_description,
            "Incident": self.structural_info.potential_incident,  
            "Failure": self.structural_info.stru_failure_mech,
            "Rec_Action": self.structural_info.recomended_act,
            "Shutdown": self.requirements.shutdown_req,
            "GI1": self.info.date,
            "eng": self.requirements.eng_req,
            "Responsible": self.info.res_person,
            "Report_ref": self.info.rep_ref,
            "Methodology": self.structural_info.action_methodology,
            "L_ACTION": self.actions.action_level,
            "Code": self.actions.action_code,
            "action": self.actions.action_type,
            "FACILITY_1": self.location.component,
            "lookuplistpicker_13": self.location.area,
            "FACILITY": self.location.facility,
            "LOCATION_add": self.location.location,
            "ACTION_STATUS": self.info.action_status,
            "Financial": self.risk_ranking.consequence.des_financial,
            "Health": self.risk_ranking.consequence.des_health_sft,
            "JOB_NUM": self.info.PO,
            "DAMAGE2": self.risk_ranking.consequence.des_damage,
            "Risk_Ranking": self.risk_ranking.rank_code,
            "Description_L": self.risk_ranking.likelihood.description,
        }



# %% Example 

struc_issue_description = '''There is significant section loss on the web of the column, most likely caused by corrosion, coupled with overloading at the connection to the guardrail’s bottom support. This loss of material reduces the column’s ability to resist axial, shear, and bending forces, compromising the structural strength.
'''
# data extraction
potential_incident = 'Material loss due to corrosive effects.'# needs to be a list 

stru_failure_mech = 'Peak bending and shear stress associated with loss of cross sectional area.'

action_methodology = '''RPEQ Engineer to develop repair procedure. In general, the repair is the following: Pressure/Blast clean affected area.
Weld reinforcement plate to the affected area. Clean the remaining area of foreign materials.
Follow Sojitz' standard for protective coating application.'''

recomended_act = 'REPAIR (Actionable)'

cost = '7860'


structural_info = Structural_info(
    struc_issue_description=struc_issue_description,
    potential_incident=potential_incident,  # Assuming you want this to be a single item list. Pydantic will validate this.
    stru_failure_mech=stru_failure_mech,
    action_methodology=action_methodology,
    recomended_act=recomended_act,
    cost=cost
)


actions = Actions(
    action_type='Steel Corrosion', 
    action_code='SC',  
    action_level='3'  
)

location = Location(
    facility='Gregory Crinum Mine',
    area='Water Treatment Plant (WTP)',
    component='column',
    location='' 
)

likelihood_rating = LikelihoodRating(rating='D')
moderate_consequence = Moderate()
risk_ranking = RiskRanking(likelihood=likelihood_rating, consequence=moderate_consequence)

reqs = requirements(
    shutdown_req='NO',
    eng_req='NO',
    overdue='NO'
)


info = Info()

inspection_report = InspectionReport(
    actions=actions,
    location=location,
    risk_ranking=risk_ranking,
    info=info,
    requirements=reqs,
    structural_info=structural_info
)


PDF_dict2 = inspection_report.to_custom_dict()

