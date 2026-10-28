import os
from dotenv import load_dotenv

load_dotenv()

JOB_FOLDER = os.getenv("JOB_FOLDER")

"""Refiltering Other New Good Job List..."""

bio_substrings = ['bio', 'enviro', 'water', 'hydro', 'geo', 'gene', 'natural', 'conserv',
                   'sustain', 'climat', 'forest', 'silvi', 'ocean', 'water', 'renew', "agri", "agro"]
data_substrings = ['data', 'stat', 'research', 'info']
#
full_list = []
bio_list = []
data_list = []
all_list = []
# with open (f"{JOB_FOLDER}other_new_good_check_R2.txt", "r") as new_good_check:
#     new_good_check_list = new_good_check.readlines()
#     for line in new_good_check_list:
#         job = (line.split(":")[0])
#         full_list.append(job)
#         if any(item in job for item in bio_substrings):
#             bio_list.append(job)
#         elif any(item in job for item in data_substrings):
#             data_list.append(job)
#         if any(item in job for item in bio_substrings) and any(item in job for item in data_substrings):
#             all_list.append(line)
#         elif any(item in job for item in bio_substrings) and not any(item in job for item in data_substrings):
#             all_list.append(line)
#         elif any(item in job for item in data_substrings) and not any(item in job for item in bio_substrings):
#             all_list.append(line)
#
# print(len(bio_list))
# print(len(data_list))
# print(len(all_list))
#
# with open(f"{JOB_FOLDER}bio_and_data_new_jobs.txt", "a") as bio_and_data_new_jobs:
#     bio_and_data_new_jobs.write("\n\nBoth:\n\n")
#     for job in all_list:
#         bio_and_data_new_jobs.write(f"{job}")


"""Creating new 'Other New Good Job List' w/o ^"""

# with open(f"{JOB_FOLDER}bio_and_data_new_jobs_R2.txt", "r") as bio_and_data:
#     bio_and_data_ref = bio_and_data.readlines()
#     for line in bio_and_data_ref:
#         job = (line.split(":")[0])
#         bio_list.append(job)
# #
# new_good_list = []
# remove_list = []
# with open(f"{JOB_FOLDER}other_new_good_check_R2.txt", "r") as new_good_check:
#     new_good_check_list = new_good_check.readlines()
#     for line in new_good_check_list:
#         job = (line.split(":")[0])
#         full_list.append(job)
#         if job not in bio_list:
#             new_good_list.append(line)
#         if job in bio_list:
#             remove_list.append(line)
#
# print(f"Full: {len(full_list)}")
# print(f"Other: {len(new_good_list)}")
# print(f"Bio: {len(remove_list)}") #R2 should be 654?
#
#
# with open(f"{JOB_FOLDER}refined_other_new_good_check_R2.txt", "a") as refined_other_new_good_check:
#     for job in new_good_list:
#         refined_other_new_good_check.write(f"{job}")


"""Removing Duplicates"""

# sorted_set = []
# with open(f"{JOB_FOLDER}refined_other_new_good_check_R2.txt", "r") as refined_other_new_good_check:
#     other_new_good_check_list = refined_other_new_good_check.readlines()
#     # print(type(other_new_good_check_list))
#     print(len(other_new_good_check_list))
#     # print(other_new_good_check_list)
#     other_new_good_check_set = set(other_new_good_check_list)
#     # print(type(other_new_good_check_set))
#     # print(len(other_new_good_check_set))
#     # print(other_new_good_check_set)
#     sorted_set = sorted(other_new_good_check_set)
#     # print(type(sorted_set))
#     print(len(sorted_set))
    # print(sorted_set)
# with open(f"{JOB_FOLDER}sorted_other_new_good_check_R2.txt", "a") as sorted_other_new_good_check:
#     for job in sorted_set:
#         sorted_other_new_good_check.write(f"{job}")

# sorted_bd_list = []
# with open(f"{JOB_FOLDER}bio_and_data_new_jobs_R2.txt", "r") as bio_and_data_new_jobs:
#     bio_and_data_new_jobs_list = bio_and_data_new_jobs.readlines()
#     print(len(bio_and_data_new_jobs_list))
#     bio_and_data_new_jobs_set = set(bio_and_data_new_jobs_list)
#     sorted_bd_list = sorted(bio_and_data_new_jobs_list)
#     print(len(sorted_bd_list))
# with open(f"{JOB_FOLDER}sorted_bio_and_data_new_jobs_R2.txt", "a") as sorted_bio_and_data_new_jobs:
#     for job in sorted_bd_list:
#         sorted_bio_and_data_new_jobs.write(f"{job}")

"""Duplicate ^ Checking:"""
# with (open(f"{JOB_FOLDER}refined_other_new_good_check.txt", "r") as refined_other_new_good_check,
#       open(f"{JOB_FOLDER}sorted_other_new_good_check.txt", "r") as sorted_other_new_good_check):
#     other_new_good_check_list = refined_other_new_good_check.readlines()
#     other_new_good_check_set = set(other_new_good_check_list)
#     sorted_other_new_good_check_list = sorted_other_new_good_check.readlines()
#     print(len(sorted_other_new_good_check_list))
#     for job in other_new_good_check_set:
#         if job not in sorted_other_new_good_check_list:
#             print(job)
#
# with (open(f"{JOB_FOLDER}bio_and_data_new_jobs.txt", "r") as bio_and_data_new_jobs,
#       open(f"{JOB_FOLDER}sorted_bio_and_data_new_jobs.txt", "r") as sorted_bio_and_data_new_jobs):
#     bio_and_data_new_list = bio_and_data_new_jobs.readlines()
#     bio_and_data_new_set = set(bio_and_data_new_list)
#     sorted_bio_and_data_new_jobs_list = sorted_bio_and_data_new_jobs.readlines()
#     print(len(sorted_bio_and_data_new_jobs_list))
#     for job in bio_and_data_new_set:
#         if job not in sorted_bio_and_data_new_jobs_list:
#             print(job)
