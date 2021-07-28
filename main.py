from azure.cognitiveservices.vision.computervision import ComputerVisionClient
from azure.cognitiveservices.vision.computervision.models import OperationStatusCodes
from azure.cognitiveservices.vision.computervision.models import VisualFeatureTypes
from msrest.authentication import CognitiveServicesCredentials

from array import array
import os
from PIL import Image
import sys
import time

#Script is currently non functional 

subscription_key = "#Commented out for security"
endpoint = "#Commented out for security"

computervision_client = ComputerVisionClient(endpoint, CognitiveServicesCredentials(subscription_key))


for filename in os.listdir("./Images"): #Directory currently used to store test images
    with open(os.path.join(os.getcwd(), filename), 'r') as f:
        read_response = computervision_client.read(f.name,  raw=True)

        read_operation_location = read_response.headers["Operation-Location"]

        operation_id = read_operation_location.split("/")[-1]
        
        while True:
            read_result = computervision_client.get_read_result(operation_id)
            if read_result.status not in ['notStarted', 'running']:
                break
            time.sleep(1)
        finalStr = ""
        if read_result.status == OperationStatusCodes.succeeded:
            for text_result in read_result.analyze_result.read_results:
                for line in text_result.lines:
                    finalStr += line.text
        with open("Output.txt", "w") as text_file:
            text_file.write(finalStr)
            

            