import os
from dotenv import load_dotenv

load_dotenv()

JOB_FOLDER = os.getenv("JOB_FOLDER")

"""Job List Consolidation"""
# test_list = ["biology teacher", "volunteer", "nurse volunteer", "biology", "data", "biology data"]
with open(f"{JOB_FOLDER}Scrape Filtering Files/good_word_list.txt", "r") as good_word_list:
    good_list = good_word_list.readlines()  # 1-item list (string with all words in doc)
    good_words = (good_list[0].split(", "))
with open(f"{JOB_FOLDER}Scrape Filtering Files/job_words_4.txt", "r") as words_to_remove:
    bad_list = words_to_remove.readlines()  # 1-item list (string with all words in doc)
    bad_words = (bad_list[0].split(", "))
#
full_list = []
refined_list = []
new_list = []
#
#
# with open (f"{JOB_FOLDER}Ziprecruiter_new_jobs.txt", "r") as zipjobs:
#     zip_job_list = zipjobs.readlines()
#     for line in zip_job_list:
#         job = (line.split(":")[0])
#         full_list.append(job)
#         if any(item in job for item in good_words) and not any(item in job for item in bad_words):
#             refined_list.append(line)
#         elif not any(item in job for item in good_words) and not any(item in job for item in bad_words):
#             new_list.append(line)
# with open (f"{JOB_FOLDER}Ziprecruiter_new_salaries.txt", "r") as zipsalaries:
#     zip_salary_list = zipsalaries.readlines()
#     for line in zip_salary_list:
#         salary = (line.split(":")[0])
#         full_list.append(salary)
#         if any(item in salary for item in good_words) and not any(item in salary for item in bad_words):
#             refined_list.append(line)
#         elif not any(item in salary for item in good_words) and not any(item in salary for item in bad_words):
#             new_list.append(line)
# with open (f"{JOB_FOLDER}BLS A-Z copy2.txt", "r") as bls:
#     bls_job_list = bls.readlines()
#     for line in bls_job_list:
#         job = (line.split("\n")[0])
#         full_list.append(job)
#         if any(item in job for item in good_words) and not any(item in job for item in bad_words):
#             refined_list.append(line)
#         elif not any(item in job for item in good_words) and not any(item in job for item in bad_words):
#             new_list.append(line)
# with open (f"{JOB_FOLDER}careercom_new_jobs.txt", "r") as cc:
#     cc_job_list = cc.readlines()
#     for line in cc_job_list:
#         job = (line.split(":")[0])
#         full_list.append(job)
#         if any(item in job for item in good_words) and not any(item in job for item in bad_words):
#             refined_list.append(line)
#         elif not any(item in job for item in good_words) and not any(item in job for item in bad_words):
#             new_list.append(line)
# with open (f"{JOB_FOLDER}indeed_new_jobs.txt", "r") as indeed_new_jobs:
#     indeed_job_list = indeed_new_jobs.readlines()
#     for line in indeed_job_list:
#         job = (line.split(":")[0])
#         full_list.append(job)
#         if any(item in job for item in good_words) and not any(item in job for item in bad_words):
#             refined_list.append(line)
#         elif not any(item in job for item in good_words) and not any(item in job for item in bad_words):
#             new_list.append(line)
"""Round 2: """
with open (f"{JOB_FOLDER}career_exp_new_new_jobs.txt", "r") as career_exp_new_new_jobs:
    career_exp_job_list = career_exp_new_new_jobs.readlines()
    for line in career_exp_job_list:
        job = (line.split(":")[0])
        full_list.append(job)
        if any(item in job for item in good_words) and not any(item in job for item in bad_words):
            refined_list.append(line)
        elif not any(item in job for item in good_words) and not any(item in job for item in bad_words):
            new_list.append(line)
with open (f"{JOB_FOLDER}career_builder_new_new_jobs.txt", "r") as career_builder_new_new_jobs:
    career_b_job_list = career_builder_new_new_jobs.readlines()
    for line in career_b_job_list:
        job = (line.split(":")[0])
        full_list.append(job)
        if any(item in job for item in good_words) and not any(item in job for item in bad_words):
            refined_list.append(line)
        elif not any(item in job for item in good_words) and not any(item in job for item in bad_words):
            new_list.append(line)
with open (f"{JOB_FOLDER}salary_com_middle_new_new_jobs.txt", "r") as salary_com_middle_new_new_jobs:
    salary_com_middle_job_list = salary_com_middle_new_new_jobs.readlines()
    for line in salary_com_middle_job_list:
        job = (line.split(":")[0])
        full_list.append(job)
        if any(item in job for item in good_words) and not any(item in job for item in bad_words):
            refined_list.append(line)
        elif not any(item in job for item in good_words) and not any(item in job for item in bad_words):
            new_list.append(line)
with open (f"{JOB_FOLDER}salary_com_upper_new_new_jobs.txt", "r") as salary_com_upper_new_new_jobs:
    salary_com_upper_job_list = salary_com_upper_new_new_jobs.readlines()
    for line in salary_com_upper_job_list:
        job = (line.split(":")[0])
        full_list.append(job)
        if any(item in job for item in good_words) and not any(item in job for item in bad_words):
            refined_list.append(line)
        elif not any(item in job for item in good_words) and not any(item in job for item in bad_words):
            new_list.append(line)
with open (f"{JOB_FOLDER}salary_com_high_new_new_jobs.txt", "r") as salary_com_high_new_new_jobs:
    salary_com_high_job_list = salary_com_high_new_new_jobs.readlines()
    for line in salary_com_high_job_list:
        job = (line.split(":")[0])
        full_list.append(job)
        if any(item in job for item in good_words) and not any(item in job for item in bad_words):
            refined_list.append(line)
        elif not any(item in job for item in good_words) and not any(item in job for item in bad_words):
            new_list.append(line)
with open (f"{JOB_FOLDER}salary_com_six_new_new_jobs.txt", "r") as salary_com_six_new_new_jobs:
    salary_com_six_job_list = salary_com_six_new_new_jobs.readlines()
    for line in salary_com_six_job_list:
        job = (line.split(":")[0])
        full_list.append(job)
        if any(item in job for item in good_words) and not any(item in job for item in bad_words):
            refined_list.append(line)
        elif not any(item in job for item in good_words) and not any(item in job for item in bad_words):
            new_list.append(line)

print(len(full_list))
print(len(refined_list))
print(len(new_list))
#
with open (f"{JOB_FOLDER}new_good_check_R2.txt", "a") as all_good_check_R2:
    for job in refined_list:
        all_good_check_R2.write(f"{job}")
# with open (f"{JOB_FOLDER}all_new_check.txt", "a") as all_new_check:
with open(f"{JOB_FOLDER}all_new_check_R2.txt", "a") as all_new_check_R2:
    for job in new_list:
        all_new_check_R2.write(f"{job}")


"""Unique Words + Counts"""
# all_unique_words = ()
# word_count = {}
# counter = 0
# with open (f"{JOB_FOLDER}all_new_check.txt", "r") as jobs:
#     for line in jobs.readlines():
#         # print(line)
#         line_no_url = line.split(":")[0]
#         counter += 1
#         words = line_no_url.lower().split()
#         # print(words)
#         unique_words = set(words)
#         for word in unique_words:
#             if word not in all_unique_words:
#                 all_unique_words += (word,)
#                 word_count[word] = 0
#             if word in all_unique_words:
#                 word_count[word] = word_count.get(word, 0) + 1
# print(len(all_unique_words))
# print(sorted (all_unique_words))
# print(word_count)
# sorted_data = dict(sorted(word_count.items(), key=lambda item: item[1]))
# print(sorted_data)
# for k, v in sorted_data.items():
#     print(k)
# print(counter)

# words = []
# string = ""
# with open (f"{JOB_FOLDER}new_good_check_words.txt", "r") as zipjobs:
#     doc = zipjobs.readlines()
#     lines = doc[0].split(",")
#     # print(lines)
#     for line in lines:
#         print(line.strip().split(":")[0])
#         words.append(line.strip().split(":")[0])
#         string += f'{line.strip().split(":")[0]}, '
#     print(words)
#     print(string)
#     print(len(words))


