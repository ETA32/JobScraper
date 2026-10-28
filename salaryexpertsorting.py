import os
from dotenv import load_dotenv

load_dotenv()

JOB_FOLDER = os.getenv("JOB_FOLDER")
FILTER_FILES = os.getenv("FILTER_FILES")

with open(f"{FILTER_FILES}good_word_list.txt", "r") as good_word_list:
    good_list = good_word_list.readlines()  # 1-item list (string with all words in doc)
    good_words = (good_list[0].split(", "))
    # for word in words:
    #     print(word)
with open(f"{FILTER_FILES}job_words_4.txt", "r") as words_to_remove:
    bad_list = words_to_remove.readlines()  # 1-item list (string with all words in doc)
    # print(bad_list)
    bad_words = (bad_list[0].split(", "))


full_list = []
refined_list = []
new_list = []
bad_list = []
for file in os.listdir(f"{JOB_FOLDER}SALARYEXPERT NEW/"):
    if file.endswith(".txt"):
        print(file)
        with open (f"{JOB_FOLDER}SALARYEXPERT NEW/{file}", "r") as salaryexpertletter:
            salaryexpertjobs = salaryexpertletter.readlines()
            # zip_jobs = (zip_job_list[0].split(", "))
            for line in salaryexpertjobs:
                job = (line.split(":")[0])
                full_list.append(job)
                if any(item in job for item in good_words) and not any(item in job for item in bad_words):
                    refined_list.append(line)
                elif not any(item in job for item in good_words) and not any(item in job for item in bad_words):
                    new_list.append(line)
                if any(item in job for item in bad_words):
                    # print(job)
                    bad_list.append(line)

print(len(full_list))
print(len(bad_list))
print(len(refined_list))
print(len(new_list))
refined_set = set(refined_list)
new_set = set(new_list)
print(len(refined_set))
print(len(new_set))

with open(f"{JOB_FOLDER}sorted_salaryexpert_good_jobs.txt", "a") as sorted_salaryexpert_good:
    for job in sorted(refined_set):
        sorted_salaryexpert_good.write(f"{job}")
with open(f"{JOB_FOLDER}sorted_salaryexpert_new_jobs.txt", "a") as sorted_salaryexpert_new_jobs:
    for job in sorted(new_set):
        sorted_salaryexpert_new_jobs.write(f"{job}")