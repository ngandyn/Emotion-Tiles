# Code originally by TA Payam Jome Yazdian from CMPT 419
# Modified for project use

import json
import requests
import urllib.parse
from pathlib import Path
import os

print("Replace intended downloaded GIF emotions in python script's \"target_metrics\".")
API_ENDPOINT = 'https://www.qnt.io/api/displaymetrics?pID=gifgif&mode=all&key=54a309ac1c61be23aba0da3f'
#Make a request: 
r=requests.get(API_ENDPOINT)

#Parse the response using JSON
output_json = json.loads(r.text)

Dic = []
print("=========================================")
print("Metrics and mID from enpoint:")
for obj in output_json:
  Dic.append( [obj[('metric')], obj[('mID')]] )
  print("Metric: " + obj[('metric')] + '______' + " mID: " + obj[('mID')])
print("=========================================")

BaseFolder = './dataset' # Where the downloaded GIFs will be saved
sample_count = 100  # Number of GIFs to download for a specific metric
target_metrics = ["happiness", "sadness", "fear", "surprise"] # Only metrics specified in the array will be downloaded

print("Target GIFs: " + ", ".join(target_metrics))
print("GIF count for each metric: " + str(sample_count))
for obj in Dic:

  Metric, mID = obj
  if str(Metric) in target_metrics:
    
    # Check if the metric folder does not exist in the base folder, then create it.
    directory = str(BaseFolder) + '/' + str(Metric)
    print("Downloading " + str(Metric) +
           " GIFs into " + directory)
    if not os.path.exists(directory):
      os.makedirs(directory)

    # Create request URL 
    API_ENDPOINT = "https://www.qnt.io/api/results?pID=gifgif&mID={}&limit={}&key=54a309ac1c61be23aba0da3f".format(mID, sample_count)
    r=requests.get(API_ENDPOINT)
    output_json = json.loads(r.text)

    # Download gif file
    for result in output_json['results']:
      embedLink = result['content_data']['embedLink']
      r = requests.get(embedLink, allow_redirects=True)
      open(directory + '/' + f"{result['rank']}.{result['content_type']}", 'wb').write(r.content)

print("Finished")
