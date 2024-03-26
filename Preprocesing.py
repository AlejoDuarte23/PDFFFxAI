import os
import json
import shutil
from PIL import Image


from typing import Dict, List, Tuple
from fuzzywuzzy import process

def find_matching_keys(json_data: Dict, search_term: str, fuzziness_threshold: int = 90) -> Dict:
    """
    Searches for matching keys in a JSON structure based on a fuzzy search term for description,
    with adjustable fuzziness control.
    
    Args:
    - json_data: The JSON structure containing the data.
    - search_term: The search term to find matching descriptions.
    - fuzziness_threshold: The minimum match score from 0 to 100 to consider a match (default is 90).
    
    Returns:
    - A dictionary with the structure:
      {key: {'location': str, 'description': str, 'latitude': float, 'longitude': float, 'images': {int: str}}}
    """
    final_dict = {}
    for key, value in json_data.items():
        for item in value:
            match_ratio = process.extractOne(search_term, [item['description']], score_cutoff=fuzziness_threshold)
            if match_ratio:
                if key not in final_dict:
                    final_dict[key] = {'location': item['location'], 'description': item['description'],
                                       'latitude': item['latitude'], 'longitude': item['longitude'], 'images': {}}
                img_count = len(final_dict[key]['images']) + 1
                final_dict[key]['images'][img_count] = item['path']
    return final_dict



def get_decimal_from_dms(dms, ref):
    degrees, minutes, seconds = dms
    decimal = degrees + (minutes / 60.0) + (seconds / 3600.0)
    if ref in ['S', 'W']:
        decimal = -decimal
    return decimal

def get_comments_info(image_path:str) -> dict:
    with Image.open(image_path) as img:
        info = img._getexif()
        if 37510 not in info:
            return {}

        decoded_string = info[37510].decode('ascii')
        cleaned_string = decoded_string.replace('ASCII', '').replace('\x00', '').strip()
        parts = cleaned_string.split(',', 1)
        location = parts[0].strip()
        description = parts[1].strip() if len(parts) > 1 else ''

        date = info.get(36867, None)

        gps_info = info.get(34853)
        if gps_info:
            latitude = get_decimal_from_dms(gps_info[2], gps_info[1])
            longitude = get_decimal_from_dms(gps_info[4], gps_info[3])
        else:
            latitude, longitude = None, None
        
        return {
            'location': location,
            'description': description,
            'date': date,
            'latitude': latitude,
            'longitude': longitude,
            'path': image_path
        }

def create_info_dict(base_path):
    final_dict = {}
    subfolders = [f.path for f in os.scandir(base_path) if f.is_dir()]
    for folder_path in subfolders:
        folder_name = os.path.basename(folder_path)
        images = [os.path.join(folder_path, img) for img in os.listdir(folder_path) if img.upper().endswith('.JPG')]
        for image_path in images:
            info = get_comments_info(image_path)
            if info:
                key = info['location']
                if key not in final_dict:
                    final_dict[key] = {'location': info['location'], 'description': info['description'],
                                       'latitude': info['latitude'], 'longitude': info['longitude'], 'images': {}}
                img_count = len(final_dict[key]['images']) + 1
                final_dict[key]['images'][img_count] = info['path']
    return final_dict


def save_info_dict(info_dict:Dict,output_file_path:str):
        with open(output_file_path, 'w') as json_file:
            json.dump(info_dict, json_file, indent=4)


if False:
    base_path = "E:\\Damage_in_protective_coating"
    info_dict = create_info_dict(base_path)
    print(json.dumps(info_dict, indent=4))

    output_file_path = 'damage_in_pc.json'
    with open(output_file_path, 'w') as json_file:
        json.dump(info_dict, json_file, indent=4)

    base_path = "E:\\Damage_in_protective_coating"
    info_dict = create_info_dict(base_path)
    print(json.dumps(info_dict, indent=4))

    output_file_path = 'damage_in_pc.json'
    with open(output_file_path, 'w') as json_file:
        json.dump(info_dict, json_file, indent=4)


if False:
    # create the folder 
    base_path = "E:\Grouting_damage"
    info_dict = create_info_dict(base_path)
    print(json.dumps(info_dict, indent=4))

    output_file_path = 'grout_damage.json'
    save_info_dict(info_dict,output_file_path)
