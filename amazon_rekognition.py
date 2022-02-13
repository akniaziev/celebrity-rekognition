import csv
import boto3 
import pickle
import os
import shutil
from time import sleep

rekog_results_dir = '/results/'
rekog_images_dir = '/data/'
personal_access_key = ""
secret_access_key = ""
client=boto3.client('rekognition','us-east-1', 
    aws_access_key_id = personal_access_key, 
    aws_secret_access_key = secret_access_key) 
local_images = os.listdir(rekog_images_dir)
holder_content_celeb = []
for imageFile in local_images:
    with open(rekog_images_dir + imageFile, 'rb') as image:
        response = client.recognize_celebrities(Image={'Bytes': image.read()})
    print('Detecting faces for ' + imageFile)
    if len(response['CelebrityFaces']) == 0:
        print ("No Celebrities Detected")
        temp_dict = {}
        temp_dict["image_id"] = imageFile
        temp_dict["celeb_full_response"] = ""
        temp_dict["celeb_num"] = ""
        temp_dict["celeb_urls"] = ""
        temp_dict["celeb_name"] = ""
        temp_dict["celeb_id"] = ""
        temp_dict["celeb_face_data"] = ""
        temp_dict["celeb_face_conf"] = ""
        temp_dict["celeb_match_conf"] = ""
        temp_dict['celeb_metadata'] = response['ResponseMetadata']    
        holder_content_celeb.append(temp_dict)
    else:
        celeb_counter = 1
        for face in response['CelebrityFaces']:
            print (face['Name'] + ' : ' + str(face['MatchConfidence']))
            temp_dict = {}
            temp_dict["image_id"] = imageFile
            temp_dict["celeb_full_response"] = face 
            temp_dict["celeb_num"] = celeb_counter
            temp_dict["celeb_urls"] = face['Urls']
            temp_dict["celeb_name"] = face['Name']
            temp_dict["celeb_id"] = face['Id']
            temp_dict["celeb_face_data"] = face['Face']
            temp_dict["celeb_face_conf"] = face['Face']['Confidence']
            temp_dict["celeb_match_conf"] = face['MatchConfidence']
            temp_dict['celeb_metadata'] = response['ResponseMetadata']
            celeb_counter += 1
            holder_content_celeb.append(temp_dict)
with open(rekog_results_dir + 'awsrekognition_celeb_detect.csv', 'w', newline = '') as csvfile:
    fieldnames = ['image_id', 'celeb_full_response',
                  'celeb_num', 'celeb_urls',
                  'celeb_name', 'celeb_id',
                  'celeb_face_data', 'celeb_face_conf', 
                  'celeb_match_conf', 'celeb_metadata']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    writer.writeheader()
    for entry in holder_content_celeb:
        writer.writerow(entry)
dir = '/data/'
for f in os.listdir(dir):
    os.remove(os.path.join(dir, f))