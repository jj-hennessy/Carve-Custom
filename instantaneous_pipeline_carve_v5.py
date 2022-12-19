from multiprocessing.dummy import current_process
import time
import os
import stat
import pandas as pd
from pathlib import Path
from create_instantaneous_emails import send_email
from pull_qualtrics_data import get_qualtrics_data
import requests
import shutil
import tqdm

all_going_well = True
survey_id = 'SV_byGGKBGOjkP2rT8'
send_email_a = False
csv_with_records = 'record_responses_study_v5.csv'

while all_going_well:
    survey_df = get_qualtrics_data(survey_id, 'qualtrics_resp_v5', 'qualtrics_resp_v5/Trust Carve_v5.csv')
    survey_df.fillna('', inplace=True)
    survey_df_dict = survey_df.to_dict('records')
    image_links = ['B48','E48','H48','K48','N48','Q48']
    sent_emails = "".join(open(csv_with_records, 'r').readlines()).replace("\n", "")
    for row in tqdm.tqdm(survey_df_dict[2:]):

        first_name = row['Q35_7'].lower().capitalize().strip(" ")
        email = row['Q35_42']
        if email not in sent_emails and len(email) > 0:
            try:
                name, receiver_email, sent_email_a, cost_option_index = send_email(first_name, email, send_email_a)
                print(f'Just sent an email to {name} on {receiver_email} with cost option {cost_option_index}')
                record_file = open(csv_with_records, 'a')
                record_file.write(f'{name},{receiver_email},{sent_email_a},{cost_option_index}\n')
                record_file.close()
            except Exception as e:
                print(f'Error sending email for {name} is {str(e)}')
                record_file = open(csv_with_records, 'a')
                record_file.write(f'{first_name},{email},{str(e)},\n')
                record_file.close()
