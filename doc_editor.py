import os
from dotenv import load_dotenv

load_dotenv()

JOB_FOLDER = os.getenv("JOB_FOLDER")

# refremove = [", see", ":", " -", ' "good']
# final_good_jobs = []
# with open (f"{JOB_FOLDER}jobs_checked_2x.txt", "r") as f:
#     good_checked_jobs = f.readlines()
#     # good_checked_jobs[8] = good_checked_jobs[8][14:]
#     # print(len(good_checked_jobs))
#     for line in good_checked_jobs:
#         # print(f"line {line}")
#         if line[0] == " ":
#             line = line[1:]
#         for item in refremove:
#             if item in line:
#                 # print(line)
#                 result = line.split(item)[0]
#                 # print(result)
#                 final_good_jobs.append(result)
#                 break
#             elif not any(item in line for item in refremove):
#                 final_good_jobs.append(line)
#                 break
#                 # print(item)
# print(len(good_checked_jobs))
# # print(type(good_checked_jobs))
# # for line in good_checked_jobs:
# #     print(line)
# print(len(final_good_jobs))
# # for line in final_good_jobs:
# #     print(line)


# with open (f"{JOB_FOLDER}jobs_checked_refined.txt", "w") as f2:
#     for item in final_good_jobs:
#         f2.write(item + "\n")
#     print(f2)

good_jobs = []
# with open (f"{JOB_FOLDER}goodjobs_final.txt", "r") as f2:
#     for line in f2.readlines():
#         good_jobs.append(line)
# print(len(good_jobs))
# for line in final_good_jobs:
#     if line not in good_jobs:
#         print(line)

checked_jobs = []
# with open (f"{JOB_FOLDER}checked_jobs_careerplanner.txt", "r") as f2:
#     for line in f2.readlines():
#         checked_jobs.append(line)
# #         print(line)
#     print(len(checked_jobs))
# bad_checked_jobs = [item for item in checked_jobs if item not in good_jobs]
# print(len(bad_checked_jobs))

bad_jobs = []
# with open (f"{JOB_FOLDER}bad_checked_jobs.txt", "w") as f3:
#     for job in bad_checked_jobs:
#         f3.write(job + "\n")
#     print(f3)
# with open (f"{JOB_FOLDER}bad_checked_jobs.txt", "r") as f3:
#     for line in f3.readlines():
#         # print(line)
#         if line.strip():
#             bad_jobs.append(line)
#     print(len(bad_jobs))

cleaned_bad_jobs = []
# with open (f"{JOB_FOLDER}bad_checked_jobs.txt", "r") as og, open(f"{JOB_FOLDER}bad_checked_jobs_clean.txt", "w", encoding="utf-8") as cleaned:
#     for line in og:
#         if line.strip():
#             cleaned.write(line)
# with open (f"{JOB_FOLDER}bad_checked_jobs_clean.txt", "r") as clean:
#     for line in clean.readlines():
#         # print(line)
#         if line.strip():
#             cleaned_bad_jobs.append(line)
#     print(len(cleaned_bad_jobs))

cleaned_all_new_jobs_words = []
with open (f"{JOB_FOLDER}Job Lists/all_new_check_filter_by_words.txt", "r") as all_new_jobs:
    allnew = all_new_jobs.readlines()
    allnew_words = (allnew[0].split(", "))
    for word in allnew_words:
        word_clean = word.split(':')[0]
        # print(word_clean.strip())
        cleaned_all_new_jobs_words.append(word_clean.strip())

with open (f"{JOB_FOLDER}Job Lists/all_new_check_filter_by_words_clean2.txt", "a") as all_new_job_words:
    for word in cleaned_all_new_jobs_words:
        all_new_job_words.write(word + ", ")


