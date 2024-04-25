import instructor 
import os 

from openai import OpenAI
from typing import Dict,Iterable
from Classes import Location

os.environ["OPENAI_API_KEY"] = ""
client = instructor.patch(OpenAI())


def gextraction(image_metada:Dict)->Location:
    return client.chat.completions.create(
        model="gpt-3.5-turbo-0125",
        messages=[

            {
                "role": "user",
                "content": f"Help me extracting the locations and components from the image metada. the metada of the image is /n :  {image_metada} ",
            },
            
        ],
    temperature=0.1,
    response_model=Iterable[Location],
    stream = True,
    max_retries = 6
    ) 
