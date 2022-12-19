from fileinput import filename
import requests
import json
import zipfile
import time
import pandas as pd

def start_response_export(format, surveyId):
    data = {'format': format}
    headers = {
        'Content-Type': 'application/json',
        'X-API-TOKEN' :  'oxbF4ldtte5658O36Bt6hany8MKC4b8tk5V4Cmcm'
    }
    url = f"https://stanforduniversity.ca1.qualtrics.com/API/v3/surveys/{surveyId}/export-responses"

    resp = requests.post(url, data = json.dumps(data), headers=headers).json()
    return resp

def get_export_progress(exportProgressId, surveyId):
    headers = {
        'Content-Type': 'application/json',
        'X-API-TOKEN' :  'oxbF4ldtte5658O36Bt6hany8MKC4b8tk5V4Cmcm'
    }
    url = f"https://stanforduniversity.ca1.qualtrics.com/API/v3/surveys/{surveyId}/export-responses/{exportProgressId}"

    resp = requests.get(url, headers=headers).json()
    return resp

def get_file(fileId, surveyId, folder_name):
    headers = {
        'Content-Type': 'application/json',
        'X-API-TOKEN' :  'oxbF4ldtte5658O36Bt6hany8MKC4b8tk5V4Cmcm'
    }
    url = f"https://stanforduniversity.ca1.qualtrics.com/API/v3/surveys/{surveyId}/export-responses/{fileId}/file"

    resp = requests.get(url, headers=headers)
    filename = f'{folder_name}/response.zip'
    with open(filename, 'wb') as f:
        f.write(resp.content)

    return filename

def get_qualtrics_data(surveyID, folder_name, file_name, format = 'csv'):
    export_resp = start_response_export(format, surveyID)
    status = 'inProgress'
    while status == 'inProgress':
        progress_resp = get_export_progress(export_resp['result']['progressId'], surveyID)
        status = progress_resp['result']['status']
        time.sleep(1)
    fileId = progress_resp['result']['fileId']
    zipfile_path = get_file(fileId, surveyID, folder_name)
    with zipfile.ZipFile(zipfile_path, 'r') as zip_ref:
        zip_ref.extractall(folder_name)
    with open(file_name) as csv_file:
        df = pd.read_csv(csv_file)
        return df

if __name__ == "__main__":
    get_qualtrics_data()