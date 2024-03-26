from openai import OpenAI
import instructor 
import json 
import os 
from typing import Dict,Iterable
from Classes import Location

with open('oai_api_key.json', 'r') as file:
    data = json.load(file)

os.environ["OPENAI_API_KEY"] = data["OPENAI_API_KEY"]
client = instructor.patch(OpenAI())


def gextraction(image_metada:Dict)->Location:
    return client.chat.completions.create(
        model="gpt-4-0125-preview",
        messages=[
            {
                "role": "system",
                "content": f" the metada of the image is  : {image_metada}",
            },
            {
                "role": "user",
                "content": f"Help me extracting the locations and components from the image metada",
            },
            
        ],
    response_model=Iterable[Location],
    stream = True,
    max_retries = 2
    ) 
