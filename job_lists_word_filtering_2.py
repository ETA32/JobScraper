import os
from dotenv import load_dotenv

load_dotenv()

JOB_FOLDER = os.getenv("JOB_FOLDER")

"""Filtering New Good Job List"""
bio_substrings = ['bio', 'enviro', 'water', 'hydro', 'geo', 'gene', 'natural', 'conserv',
                   'sustain', 'climat', 'forest', 'silvi', 'ocean', 'water', 'renew', "agri", "agro", ]
data_substrings = ['data', 'stat', 'research', 'info']
manag_substrings = ['manag', 'direct', 'design', 'anal', 'prog', 'proj', 'plan', 'consult', 'coord', 'advis']


full_list = []
# refined_list = []
bio_list = []
data_list = []
manage_list = []
no_substrings = []
with open (f"{JOB_FOLDER}new_good_check_R2.txt", "r") as new_good_check:
    new_good_check_list = new_good_check.readlines()
    for line in new_good_check_list:
# with open (f"{JOB_FOLDER}sorted_salaryexpert_good_jobs.txt") as salary_expert_good_jobs:
#     salary_expert_good_jobs_list = salary_expert_good_jobs.readlines()
#     for line in salary_expert_good_jobs_list:
        job = (line.split(":")[0])
        full_list.append(job)
        # if not any(item in job for item in manag_substrings):
        #     refined_list.append(job)
        if any(item in job for item in bio_substrings) and not any(item in job for item in data_substrings) and not any(item in job for item in manag_substrings):
            bio_list.append(line)
        elif not any(item in job for item in bio_substrings) and any(item in job for item in data_substrings) and not any(item in job for item in manag_substrings):
            data_list.append(line)
        elif not any(item in job for item in bio_substrings) and not any(item in job for item in data_substrings) and any(item in job for item in manag_substrings):
            manage_list.append(line)
        elif not any(item in job for item in bio_substrings) and not any(item in job for item in data_substrings) and not any(item in job for item in manag_substrings):
            no_substrings.append(line)
        else:
            no_substrings.append(line)

# """originals"""
#     """Only bio_substrings:  7617 """
#     """Only data_substrings:  7860 """
#     """Only manag_substrings:  44105 """
#     """None of the above:  14848 """

"""Only bio_substrings:  360 """
"""Only data_substrings:  436 """
"""Only manag_substrings:  4532 """
"""None of the above:  1260 """

# print(refined_list)
print(len(full_list))
# print(len(refined_list))
print(len(bio_list))
print(len(data_list))
print(len(manage_list))
print(len(no_substrings))
# print(len(no_substrings))

with open(f"{JOB_FOLDER}bio_and_data_new_jobs_R2.txt", "a") as bio_and_data_new_jobs:
# with open(f"{JOB_FOLDER}salaryexpert_bio_and_data_new_jobs.txt", "a") as bio_and_data_new_jobs:
    bio_and_data_new_jobs.write("Bio:\n\n")
    for job in bio_list:
        bio_and_data_new_jobs.write(f"{job}")
    bio_and_data_new_jobs.write("Data:\n\n")
    for job in data_list:
        bio_and_data_new_jobs.write(f"{job}")

with open(f"{JOB_FOLDER}other_new_good_check_R2.txt", "a") as other_new_good_check:
# with open(f"{JOB_FOLDER}salaryexpert_other_new_good_check.txt", "a") as other_new_good_check:
    other_new_good_check.write("Other:\n\n")
    for job in no_substrings:
        other_new_good_check.write(f"{job}")
    other_new_good_check.write("Management:\n\n")
    for job in manage_list:
        other_new_good_check.write(f"{job}")