import os
from dotenv import load_dotenv

load_dotenv()

JOB_FOLDER = os.getenv("JOB_FOLDER")

"""checking docs/__"""
full_list = []

ziprecruiter_list = []
with open (f"{JOB_FOLDER}Ziprecruiter_good_jobs.txt", "r") as zipjobraw, open ("~/Desktop/Job Lists/Ziprecruiter_good_salaries.txt", "r") as zipsalaryraw:
    zipjoblines = zipjobraw.readlines()
    for line in zipjoblines:
        print(line)
        job = line.split(":")[0]
        print(job)
        full_list.append(job)
        ziprecruiter_list.append(job)
    zipsallines = zipsalaryraw.readlines()
    for line in zipsallines:
        print(line)
        job = line.split(":")[0]
        print(job)
        full_list.append(job)
        ziprecruiter_list.append(job)
print(ziprecruiter_list.sort())

indeedlist = []
with open (f"{JOB_FOLDER}indeed_good_jobs.txt", "r") as indeedraw:
    indeedlines = indeedraw.readlines()
    for line in indeedlines:
        print(line)
        job = line.split(":")[0]
        print(job)
        full_list.append(job)
        indeedlist.append(job)
print(indeedlist)

careercomlist = []
with open (f"{JOB_FOLDER}careercom_good_jobs.txt", "r") as careercomraw:
    careercomlines = careercomraw.readlines()
    for line in careercomlines:
        print(line)
        job = line.split(":")[0]
        print(job)
        full_list.append(job)
        careercomlist.append(job)
print(careercomlist)

bio_and_data_new_jobs_file = []
with open (f"{JOB_FOLDER}bio_and_data_new_jobs.txt", "r") as bio_and_data_new_jobs:
    bio_and_data_new_list = bio_and_data_new_jobs.readlines()
    for line in bio_and_data_new_list:
        print(line)
        job = line.split(":")[0]
        print(job)
        full_list.append(job)
        bio_and_data_new_jobs_file.append(job)
print(bio_and_data_new_jobs_file)

other_new_jobs_file = []
with open (f"{JOB_FOLDER}other_new_good_check.txt", "r") as other_new_jobs:
    other_new_list = other_new_jobs.readlines()
    for line in other_new_list:
        print(line)
        job = line.split(":")[0]
        print(job)
        full_list.append(job)
        other_new_jobs_file.append(job)
print(other_new_jobs_file)

print(full_list)
print(f"Zip Good:  {len(ziprecruiter_list)}")
print(f"Indeed Good:  {len(indeedlist)}")
print(f"CC Good:  {len(careercomlist)}")
print(f"B/D likely:  {len(bio_and_data_new_jobs_file)}")
print(f"Other likely:  {len(other_new_jobs_file)}")