import os
import json

from PIL import Image
from typing import Dict


def get_decimal_from_dms(dms, ref):
    degrees, minutes, seconds = dms
    decimal = degrees + (minutes / 60.0) + (seconds / 3600.0)
    if ref in ['S', 'W']:
        decimal = -decimal
    return decimal

def get_comments_info(image_path:str) -> dict:
    with Image.open(image_path) as img:
        info = img._getexif()
        print(image_path)
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

def create_info_dict_path(base_path):
    final_dict = {}
    subfolders = [f.path for f in os.scandir(base_path) if f.is_dir()]
    for folder_path in subfolders:
        folder_name = os.path.basename(folder_path)
        images = [os.path.join(folder_path, img) for img in os.listdir(folder_path) if img.upper().endswith('.JPG')]
        description_key = folder_name.split()[-1]  # Use last word in folder name to distinguish keys
        for image_path in images:
            info = get_comments_info(image_path)
            if info:
                base_key = info['location']
                full_key = f"{base_key}.{description_key}"
                if full_key not in final_dict:
                    final_dict[full_key] = {'location': info['location'], 'description': info['description'],
                                            'latitude': info['latitude'], 'longitude': info['longitude'], 'images': {}}
                img_count = len(final_dict[full_key]['images']) + 1
                final_dict[full_key]['images'][str(img_count)] = info['path']
    return final_dict

def save_info_dict(info_dict:Dict,output_file_path:str):
        with open(output_file_path, 'w') as json_file:
            json.dump(info_dict, json_file, indent=4)


if False:
    # create the folder 
    base_path = r"D:\YLY Defect Groups\Grouting_damage"
    info_dict = create_info_dict(base_path)
    print(json.dumps(info_dict, indent=4))

    output_file_path = r'C:\Users\ADMIN\Documents\PDFFFxAI\Grouting_damage\grout_damage.json'
    save_info_dict(info_dict,output_file_path)


