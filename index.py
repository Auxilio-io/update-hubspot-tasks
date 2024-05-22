from dotenv import load_dotenv
import os
import requests
import pandas as pd
import json

df = pd.read_csv('/Users/louischausse/Documents/GitHub/update-hubspot-tasks/tasks-to-update.csv') # add the link to your csv file here

load_dotenv()

token = os.getenv('ACCESS_TOKEN')

def update_tasks(url,headers,payload):
    try:
        response = requests.request("POST", url, headers=headers, data=payload)
        print(f"Response Status Code: {response.status_code}")
        print(response.json())
    except requests.exceptions.RequestException as e:
        print(f"A Requests error occurred: {e}")
    except Exception as e:
        print(f"An error occurred: {e}")

tasks_ids_to_update = []

for index, row in df.iterrows():
    task_id = str(row['Task ID'])
    owner_id = str(row['Task owner'])
    tasks_ids_to_update.append({"id":task_id,"properties":{"hubspot_owner_id":owner_id}})

url = "https://api.hubapi.com/crm/v3/objects/tasks/batch/update"

headers = {
  'Authorization': f'Bearer {token}',
  'Content-Type': 'application/json'
}

tasks_batch_size = 100
for i in range(0, len(tasks_ids_to_update), tasks_batch_size):
    tasks_batch = tasks_ids_to_update[i:i+tasks_batch_size]
    tasks_ids_to_update_inputs_batch = [item for item in tasks_batch]
    payload = json.dumps({
        "inputs": tasks_ids_to_update_inputs_batch
    })
    update_tasks(url,headers,payload)

