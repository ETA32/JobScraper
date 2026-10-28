"""Scraping data from Job List links (salaries, requirements, descriptions, ?)"""
from asyncio import tasks

from selenium.webdriver.common.devtools.v148.fetch import continue_request
from seleniumbase import sb_cdp
from playwright.sync_api import sync_playwright
from bs4 import BeautifulSoup, ResultSet
import csv
import time
import random
import copy
import re
import os
from dotenv import load_dotenv

"""Link Types"""
ziprecruiterbase = "https://www.ziprecruiter.com/Salaries/"
ziprecruiterbrowse = "https://www.ziprecruiter.com/browse/salaries/"
# salaryexpert = ""  # can't access rn...
indeed = "https://www.indeed.com/"
career_explorer = "https://www.careerexplorer"
salary_com_base = "https://www.salary.com"

"""Files"""
load_dotenv()
JOB_FOLDER = os.getenv("JOB_FOLDER")

all_good_jobs = f"{JOB_FOLDER}all good jobs base.txt"
bio_data_file = f"{JOB_FOLDER}scrapable_sorted_bio_and_data_new_jobs.txt"
# test_bio_data_file = f"{JOB_FOLDER}scrapable_sorted_bio_and_data_new_jobs copy.txt"
other_file = f"{JOB_FOLDER}scrapable_sorted_other_new_good_check.txt"
# other_recheck_file = f"{JOB_FOLDER}salaryexpert_other_new_good_check copy.txt"
salary_exp_bio_data_file = f"{JOB_FOLDER}salaryexpert_bio_and_data_new_jobs.txt"
salary_exp_other_file = f"{JOB_FOLDER}salaryexpert_other_new_good_check.txt"
salary_exp_test_file = f"{JOB_FOLDER}salaryexpert_bio_and_data_new_jobs copy.txt"

all_good_jobs_R2 = f"{JOB_FOLDER}all_new_jobs_R2.txt"
bio_data_file_R2 = f"{JOB_FOLDER}bio_and_data_new_jobs_R2.txt"
other_file_R2 = f"{JOB_FOLDER}refined_other_new_good_check_R2.txt"
# retry_file = f"{JOB_FOLDER}refined_other_new_good_check_R2 RETRY.txt"
ce_missed = f"{JOB_FOLDER}Full Data (scraped)/CE Missed jobs SCRAPE.txt"

"""Dicts (^)"""
test_dict = {"test": "https://www.scrapethissite.com/pages/forms/"}
test_dict2 = {"wavicle data solutions": "https://www.ziprecruiter.com/Salaries/wavicle-data-solutions-Salary#TableView",
              "cancer genetic counselor": "https://www.ziprecruiter.com/Salaries/cancer-genetic-counselor-Salary#TableView"}
test_dict3 = {
              "biological scientist": "https://www.careerbuilder.com/colab/biological-scientist",
              # "agronomist": "https://www.careerexplorer.com/careers/agronomist/salary/",
              # "biologist v": "https://www.salary.com/research/salary/benchmark/biologist-v-salary",
              }

id_test_dict4 = {
                 "agronomist": "https://www.salary.com/research/salary/benchmark/agronomist-salary",
                 "biologist": "https://www.salary.com/research/salary/listing/biologist-salary",
                 # "agronomist ce1": "https://www.careerexplorer.com/careers/agronomist/salary/",
                 # "agronomist ce2": "https://www.careerexplorer.com/careers/agronomist/overview/",
                 # "agronomist ce3": "https://www.careerexplorer.com/careers/agronomist/ai-impact/",
                 # "agronomist ce4": "https://www.careerexplorer.com/careers/agronomist/education-and-training-requirements/",
                 # "administrator cloud systems se": "https://www.salaryexpert.com/salary/job/administrator-cloud-systems/united-states"
                }

test_dict5 = {
              'biofuel engineer ce2': 'https://www.careerexplorer.com/careers/biofuel-engineer/overview/',
              'biofuel engineer ce4': 'https://www.careerexplorer.com/careers/biofuel-engineer/education-and-training-requirements/',
                }

bio_and_data_dict = {}
other_dict = {}

# with open (salary_exp_bio_data_file, "r") as f:
with open (bio_data_file_R2, "r") as f:
    bio_data_list = f.readlines()
    for line in bio_data_list:
        try:
            job = (line.split(": ")[0])
            link = (line.split(": ")[1]).strip("\n")
            if link.startswith(ziprecruiterbrowse):
                link = ziprecruiterbase + (link.split("salaries/")[1])[2:] + "-Salary#TableView"
                bio_and_data_dict[job + " zp"] = link
            elif link.startswith(ziprecruiterbase):
                link = link + "#TableView"
                bio_and_data_dict[job + " zp"] = link
            if link.startswith(career_explorer):
                link1 = link + "salary/"
                link2 = link + "overview/"
                link3 = link + "ai-impact/"
                link4 = link + "education-and-training-requirements/"
                bio_and_data_dict[job + " ce1"] = link1
                bio_and_data_dict[job + " ce2"] = link2
                bio_and_data_dict[job + " ce3"] = link3
                bio_and_data_dict[job + " ce4"] = link4
            # if link.startswith(salary_com_base):
            #     bio_and_data_dict[job] = link
            # bio_and_data_dict[job] = link
        except IndexError:
            # print(line)
            continue
# print(bio_and_data_dict)

# with open (salary_exp_other_file, "r") as o:
with open (other_file_R2, "r") as o:
    other_list = o.readlines()
    for line in other_list:
        try:
            job = (line.split(": ")[0])
            link = (line.split(": ")[1]).strip("\n")
            # if link.startswith(ziprecruiterbrowse):
            #     link = ziprecruiterbase + (link.split("salaries/")[1])[2:] + "-Salary#TableView"
            #     bio_and_data_dict[job + " zp"] = link
            # elif link.startswith(ziprecruiterbase):
            #     link = link + "#TableView"
            #     bio_and_data_dict[job + " zp"] = link
            # if link.startswith(career_explorer):
            #     link1 = link + "salary/"
            #     link2 = link + "overview/"
            #     link3 = link + "ai-impact/"
            #     link4 = link + "education-and-training-requirements/"
            #     other_dict[job + " ce1"] = link1
            #     other_dict[job + " ce2"] = link2
            #     other_dict[job + " ce3"] = link3
            #     other_dict[job + " ce4"] = link4
            if link.startswith(salary_com_base):
                other_dict[job] = link
            # other_dict[job] = link
        except IndexError:
            # print(line)
            continue
# print(other_dict)

scraped_dict = {}

final_dict = {}

retry_dict = {}

retry_spec_dict = {}

"""Scraper"""
def block_ads(route):
    # Match Google ads or leads domain/path
    if 'googleads' in route.request.url or 'g.doubleclick.net' in route.request.url:
        route.abort()
    else:
        route.continue_()

sb = sb_cdp.Chrome()  # Activate "stealthy" Chromium browser via SeleniumBase
endpoint_url = sb.get_endpoint_url()

timeout_times = [3000]
def stealth_scrape(key, value):
    try:
        with sync_playwright() as p:
            browser = p.chromium.connect_over_cdp(endpoint_url)
            default_context = browser.contexts[0]
            page = default_context.pages[0] if default_context.pages else default_context.new_page()
            page.route("**/cookie_push_onload*", lambda route: route.abort())
            page.route("**/pagead2.googlesyndication.com/**", lambda route: route.abort())
            page.route("**googleads**", lambda route: route.abort())
            page.route("**adtrafficquality**", lambda route: route.abort())
            page.route('**/*', block_ads)
            """website link here"""
            page.goto(f"{value}", wait_until="domcontentloaded")
            timeout_wait = random.choice(timeout_times)
            page.wait_for_timeout(timeout_wait)
            html_content = page.content()
            browser.close()
        soup = BeautifulSoup(html_content, "html.parser")
        return soup
    except Exception as e:
        retry_dict[key] = value
        print(e)
    # print (soup)

def retry_scraping(retry_dict, scrape_dict):
    # print(retry_dict)
    retry_count = len(retry_dict)
    # print(retry_count)
    retries = retry_dict
    attempts_counter = {}
    while retry_count > 0:
        finished_keys = []
        print("about to start retry loop", retries)
        for key, value in retries.items():
            print("starting retry loop", key)
            if type(scrape_dict[key]) == list:
                print("done with:", key)
                retry_count -= 1
                finished_keys += [key]
                pass
            else:
                if key not in attempts_counter:
                    print("new key:", key)
                    soup = stealth_scrape(key, value)
                    zip_refining(soup, scrape_dict)
                    attempts_counter[key] = 1
                elif key in attempts_counter and 0 < attempts_counter[key] < 5:
                    print("reretrying", key)
                    soup = stealth_scrape(key, value)
                    zip_refining(soup, scrape_dict)
                    attempts_counter[key] += 1
                else:
                    print("missed:", key)
                    finished_keys += [key]
                    retry_count -= 1
                    pass
        print("attempts counter:", attempts_counter)
        for item in finished_keys:
            # print(item)
            if item in retries:
                del retries[item]
            if item in attempts_counter:
                del attempts_counter[item]
        print(retry_dict)
        print(retry_count)


"""Soup refining"""
def zip_refining(soup, dict):
    try:
        top_earner = soup.find(string="Top Earners")
        top_salary = top_earner.find_next("td")
        # print(top_earner_salary.text)
        p75 = soup.find(string="75th Percentile")
        p75_salary = p75.find_next("td")
        # print(p75_salary.text)
        avg = soup.find(string="Average")
        avg_salary = avg.find_next("td")
        # print(avg_salary.text)
        p25 = soup.find(string="25th Percentile")
        p25_salary = p25.find_next("td")
        # print(p25_salary.text)
        if key in scraped_dict:
            scraped_dict[key + ": zip"] = [value, top_salary.text, p75_salary.text, avg_salary.text, p25_salary.text]
        else:
            scraped_dict[key] = [value, top_salary.text, p75_salary.text, avg_salary.text, p25_salary.text]
    except Exception as e:
        retry_dict[key + ": zp"] = value
        # print(e)

def sal_exp_refining_simple(soup, dict):
    try:
        """Salary"""
        # <div class="salary-range-graph" id="salaryRangeGraph" role="img" aria-label="Salary range by experience for this job and location" style="--exp-range-mid-pct: 66.37826833768051%;"
        #       data-entry="33801" data-senior="49520" data-mid-mean="44719" data-mid-median="44235" data-hours-per-year="2080">
        table = soup.find(id="salaryRangeGraph")
        salary_entry = table.get('data-entry')
        salary_median = table.get('data-median')
        salary_mean = table.get('data-mean')
        salary_senior = table.get('data-senior')

        salary_other_locs = soup.get('')
        if key in scraped_dict:
            scraped_dict[key + ": se"] = [value, "", ]
        else:
            scraped_dict[key] = [value, "", ]
    except Exception as e:
        retry_dict[key + ": se"] = value
def sal_exp_refining_complete(soup, dict):  # FINISH... figure out how to acrape all pages
    """FINISHED: Salary"""
    try:
#         # <div class="salary-range-graph" id="salaryRangeGraph" role="img" aria-label="Salary range by experience for this job and location" style="--exp-range-mid-pct: 66.37826833768051%;"
#         #       data-entry="33801" data-senior="49520" data-mid-mean="44719" data-mid-median="44235" data-hours-per-year="2080">
        table = soup.find(id="salaryRangeGraph")
        salary_entry = table.get('data-entry')
        salary_median = table.get('data-median')
        salary_mean = table.get('data-mean')
        salary_senior = table.get('data-senior')
        print(salary_entry, salary_median, salary_mean, salary_senior)
    except Exception as e:
        salary_entry = "Retry"
        salary_median = "Retry"
        salary_mean = "Retry"
        salary_senior = "Retry"
        print(e)
        if [key] not in retry_dict:
            retry_dict[key + ": se"] = value

    """FINISHED: Salary: Other locations"""
    try:
        loc_list = []
        locations = soup.find(id="salaryByLocation")
        salary_other_locs = locations.find_all(class_="item")
        for location in salary_other_locs:
            salary_loc = location.find(class_="value")
            full_loc_info = f"{location.text}: {salary_loc.text})"
            loc_list.append(full_loc_info)
        print(loc_list)
        all_locs = ", ".join(loc_list)
        print(all_locs)
    except Exception as e:
        all_locs = "Retry"
        print(e)
        if [key] not in retry_dict:
            retry_dict[key+ ": se"] = value

    """Education:  COPY SKILLS SECTION WHEN FINISHED"""
    try:
        education = soup.find_all(class_="legend")
        # for level in education:
        bhs = education[0].text
        hs = education[1].text
        ass = education[2].text
        bs = education[3].text
        ms = education[4].text
        phd = education[5].text
        print("education:", bhs.strip(), hs.strip(), ass.strip(), bs.strip(), ms.strip(), phd.strip(), "\n")
        fos = soup.find(class_="link", string="See how education can impact your salary")
        field_of_study = fos.find_previous_sibling()
        print("field of study:", field_of_study.text.strip(), "\n")
    except Exception as e:
        education = "Retry"
        print(e)
        if [key+ ": se"] not in retry_dict:
            retry_dict[key+ ": se"] = value

    """Skills"""
    try:
        skills = soup.find_all(class_="skill-card")
        print(type(skills))
        skill1 = skills[0].get_text(separator=": ", strip=True)
        skill2 = skills[1].get_text(separator=": ", strip=True)
        skill3 = skills[2].get_text(separator=": ", strip=True)
        skill4 = skills[3].get_text(separator=": ", strip=True)
        skill5 = skills[4].get_text(separator=": ", strip=True)
        skill6 = skills[5].get_text(separator=": ", strip=True)
        skill7 = skills[6].get_text(separator=": ", strip=True)
        skill_list = [skill1, skill2, skill3, skill4, skill5, skill6]
        print("skills:", skill_list, "\n")
    except Exception as e:
        if isinstance(skills, ResultSet):
            print("It is a ResultSet!")
            skill_list = []
            for skill in skills:
                skill_list.append(skill.get_text(separator=": ", strip=True), )
            if len(skill_list) != 7:
                vals_needed = 7 - len(skill_list)
                for i in range(vals_needed):
                    skill_list.append("Retry")
        else:
            skill_list = ["Retry", "Retry", "Retry", "Retry", "Retry", "Retry"]
        print(skill_list)
        print(e)
        print([key])
        if key + ": se" not in retry_dict:
            retry_dict[key+ ": se"] = value

    """FINISHED: What they do"""
    try:
        faqs = soup.find("h2", string="Frequently Asked Questions")
        faqelem_ = faqs.parent
        task_card = faqelem_.find(class_="card item")
        tasks = task_card.get_text(separator=" ", strip=True)
        print("tasks:", tasks, "\n")
    except Exception as e:
        task_card = "Retry"
        print(e)
        if key+ ": se" not in retry_dict:
            retry_dict[key+ ": se"] = value

    """FINISHED: Similar Job Titles"""
    try:
        similar_jobs_list = []
        similar_jobs = soup.find("h2", string="Salaries for Similar Job Titles in the United States")
        similar_jobs_whole = similar_jobs.parent
        # print(similar_jobs, similar_jobs_whole, "\n")
        jobs = similar_jobs_whole.find_all(class_="item")
        for job in jobs:
            # print("similar jobs:", job.get_text(separator=": ", strip=True), "\n")
            similar_jobs_list.append(job.get_text(separator=" ", strip=True))
        print(similar_jobs_list)
        sim_jobs_string = ", ".join(similar_jobs_list)
        print(sim_jobs_string)
    except Exception as e:
        similar_jobs_list = "Retry"
        print(e)
        if [key+ ": se"] not in retry_dict:
            retry_dict[key+ ": se"] = value

    # if key in scraped_dict:
    #     scraped_dict[key + ": se"] = [value, salary_senior, salary_median, salary_mean, salary_entry, all_locs,
    #                                   bhs, hs, ass, bs, ms, phd, tasks,
    #                                   skill_list[0], skill_list[1], skill_list[2], skill_list[3], skill_list[4], skill_list[5], sim_jobs_string]
    # else:
    #     scraped_dict[key] = [value, salary_senior, salary_median, salary_mean, salary_entry, all_locs,
    #                                   bhs, hs, ass, bs, ms, phd, tasks,
    #                                   skill_list[0], skill_list[1], skill_list[2], skill_list[3], skill_list[4], skill_list[5], sim_jobs_string]

def car_build_refining(soup, dict):
        try:
            """Salary"""
            avg = soup.find(class_="SalaryTool_averageValue__zen7E")
            # print(avg.text)
            low = soup.find_all(class_="SalaryTool_barLabel__lhUWE")[0]
            # print(low.text)
            avg2 = soup.find(class_="SalaryTool_barLabelStrong__mFJwS")
            # print(avg2.text)
            high = soup.find_all(class_="SalaryTool_barLabel__lhUWE")[1]
            # print(high.text)
            # dict[key] = [value, "", high.text, avg.text[:-6], low.text]
            if key in scraped_dict:
                scraped_dict[key+": cb"] = [value, "Unknown %s ->", high.text, avg.text[:-6], low.text]
            else:
                scraped_dict[key] = [value, "Unknown %s ->", high.text, avg.text[:-6], low.text]
        except Exception as e:
            print(e)
            retry_dict[key + ": cb"] = value

def car_exp_refining_simple(soup, dict):
    try:
        bar = soup.find_all(class_="AverageSalaryGraph__graph-data__datum")
        high = bar[2]
        avg = bar[1]
        low = bar[0]
        if key in scraped_dict:
            scraped_dict[key + ": ce"] = [value, "T20, med, L20 ->", high.text[:-8], avg.text[:-7], low.text[:-11]]
        else:
            scraped_dict[key] = [value, "T20, med, L20 ->", high.text[:-8], avg.text[:-7], low.text[:-11]]
    except Exception as e:
        print(e)
        retry_dict[key + ": ce"] = value
def car_exp_refining_complete(soup, dict):
    try:
        nonexistent = soup.find(class_="page-header large").find("h1").get_text().strip() == "Page Not Found"
        print("Nonexistent:", nonexistent)
        retry_dict[key] = [value, "page doesn't exist"]
    except Exception as e:
        dashkey = key.replace(" ", "-")
        print(dashkey[:-4])
        if value.endswith("salary/"):
            """FINISHED: Salary"""
            try:
                bar = soup.find_all(class_="AverageSalaryGraph__graph-data__datum")
                high = bar[2].text[:-8]
                med = bar[1].text[:-7]
                low = bar[0].text[:-11]
                other_ps = soup.find(id="salary-percentiles-container")
            except Exception as e:
                print(e)
                high = med = low = "Retry"
                if key not in retry_dict:
                    retry_dict[key] = value
            try:
                other_cards = other_ps.find_all(class_="SalaryPercentileCard__rate")
                T10 = other_cards[1].text
                T75 = other_cards[3].text
                L25 = other_cards[7].text
                L10 = other_cards[9].text
            except Exception as e:
                print(e)
                T10 = T75 = L25 = L10 = "Retry"
                if key not in retry_dict:
                    retry_dict[key] = value
            """FINISHED: Similar Job Titles"""
            try:
                similar_jobs = soup.find(id="compare-salary")
                table_rows = similar_jobs.find_all("td")
                similar_titles_list = []
                similar_sal_list =[]
                for index, row in enumerate(table_rows[::2]):
                    similar_titles_list.append(row.get_text(strip=True))
                for index, row in enumerate(table_rows[1::2]):
                    similar_sal_list.append(row.get_text(strip=True))
                similar_job_list = [t + ": " + s for t, s in zip(similar_titles_list, similar_sal_list)]
                sim_jobs_string = ",  ".join(similar_job_list)
                # print(sim_jobs_string)
            except Exception as e:
                print(e)
                sim_jobs_string = "Retry"
                if key not in retry_dict:
                    retry_dict[key] = value
            if key in scraped_dict:
                scraped_dict[key + " ce1"] = [value, T10, high, T75, med, L25, low, L10, sim_jobs_string]
            else:
                scraped_dict[key] = [value, T10, high, T75, med, L25, low, L10, sim_jobs_string]

        elif value.endswith("overview/"):
            """Full scrape"""
            desc_full = tasks_refd = sub_types = workplace_full = rel_tits_string = "Retry"
            try:
                if soup.find(id=f"what-is-an-{dashkey[:-4]}") != None:
                    print("desc is here")
                    desc_find = soup.find(id=f"what-is-an-{dashkey[:-4]}")
                elif soup.find(id=f"what-is-a-{dashkey[:-4]}") != None:
                    print("desc is here")
                    desc_find = soup.find(id=f"what-is-a-{dashkey[:-4]}")
                desc_full = desc_find.parent.get_text(strip=True)
            except Exception as e:
                print(e, ": description scrape failed")
                if key not in retry_dict:
                    retry_dict[key] = value
            try:
                if soup.find(id=f"what-does-an-{dashkey[:-4]}-do") != None:
                    print("tasks are here")
                    tasks_find = soup.find(id=f"what-does-an-{dashkey[:-4]}-do")
                elif soup.find(id=f"what-does-a-{dashkey[:-4]}-do") != None:
                    print("tasks are here")
                    tasks_find = soup.find(id=f"what-does-a-{dashkey[:-4]}-do")
                tasks_full = tasks_find.parent
                tasks_refd = tasks_full.get_text(strip=True).split(".Types of ")[0]
                sub_types = tasks_full.get_text(strip=True).split(".Types of ")[1]
            except Exception as e:
                print(e, ": tasks/subtypes scrape failed")
                if key not in retry_dict:
                    retry_dict[key] = value
            try:
                if soup.find(id=f"what-is-the-workplace-of-an-{dashkey[:-4]}-like") != None:
                    print("workplace is here")
                    workplace_find = soup.find(id=f"what-is-the-workplace-of-an-{dashkey[:-4]}-like")
                elif soup.find(id=f"what-is-the-workplace-of-a-{dashkey[:-4]}-like") != None:
                    print("workplace is here")
                    workplace_find = soup.find(id=f"what-is-the-workplace-of-a-{dashkey[:-4]}-like")
                workplace_full = workplace_find.parent.get_text(strip=True)
            except Exception as e:
                print(e, "workplace scrape failed")
                if key not in retry_dict:
                    retry_dict[key] = value
            try:
                rel_tits_find = soup.find(id="science-related-careers-and-degrees")
                if rel_tits_find:
                    rel_tits_full = rel_tits_find.parent.next_sibling.next_sibling
                    rel_tits_refined = rel_tits_full.find("p", string="Careers").next_sibling.next_sibling
                    rel_tits_list = [el.get_text(strip=True) for el in rel_tits_refined if el.get_text(strip=True)]
                    rel_tits_string = ", ".join(rel_tits_list)
                else:
                    rel_tits_string = "None Found"
            except Exception as e:
                print(e, "rel tits scrape failed")
                if key not in retry_dict:
                    retry_dict[key] = value
            # print(desc_full, "\n", tasks_refd, "\n", sub_types, "\n", workplace_full, "\n", rel_tits_string)
            if key in scraped_dict:
                scraped_dict[key + " ce2"] = [value, desc_full, tasks_refd, sub_types, workplace_full, rel_tits_string]
            else:
                scraped_dict[key] = [value, desc_full, tasks_refd, sub_types, workplace_full, rel_tits_string]

        elif value.endswith("ai-impact/"):
            """Skills to build for the AI era""" #  Replace html  /salary/ with /ai-impact/
            summary = new_skills_string = timeless_string = today_string = y2030_string = "retry"
            try:
                summary = soup.find(class_="ai-impact-full-picture__conclusion").get_text(strip=True)
            except Exception as e:
                print(e, "AI Summary failed")
                if key not in retry_dict:
                    retry_dict[key] = value
            try:
                skills = soup.find_all(class_="ai-impact-skills__column")
                new_skills_list = []
                new_skills = skills[0].find_all(class_="ai-impact-skills__cards")
                for skill in new_skills:
                    new_skills_list.append(skill.get_text(strip=True))
                if new_skills_list:
                    new_skills_string = ", ".join(new_skills_list)
            except Exception as e:
                print(e, "new skills failed")
                if key not in retry_dict:
                    retry_dict[key] = value
            try:
                timeless_list = []
                timeless = skills[1].find_all(class_="ai-impact-skills__cards")
                for skill in timeless:
                    timeless_list.append(skill.get_text(strip=True))
                if timeless_list:
                    timeless_string = ", ".join(timeless_list)
            except Exception as e:
                print(e, "timeless Skills failed")
                if key not in retry_dict:
                    retry_dict[key] = value
            """AI Job Outlook (table)""" #  ^
            try:
                today_list = []
                today = soup.find_all(class_="ai-impact-job-outlook__cell ai-impact-job-outlook__cell--data ai-impact-job-outlook__cell--today-data")
                for outlook in today:
                    today_list.append(outlook.get_text(strip=True))
                if today_list:
                    today_string = ", ".join(today_list)
            except Exception as e:
                print(e, "ai today failed")
                if key not in retry_dict:
                    retry_dict[key] = value
            try:
                y2030_list = []
                y2030 = soup.find_all(class_="ai-impact-job-outlook__cell ai-impact-job-outlook__cell--data ai-impact-job-outlook__cell--future-data")
                for outlook in y2030:
                    y2030_list.append(outlook.get_text(strip=True))
                if y2030_list:
                    y2030_string = ", ".join(y2030_list)
            except Exception as e:
                print(e, "y2030 failed")
                if key not in retry_dict:
                    retry_dict[key] = value
            # print(summary, "\n", new_skills_string, "\n", timeless_string, "\n", today_string, "\n", y2030_string, "\n")
            if key in scraped_dict:
                scraped_dict[key + " ce3"] = [value, summary, new_skills_string, timeless_string, today_string, y2030_string]
            else:
                scraped_dict[key] = [value, summary, new_skills_string, timeless_string, today_string, y2030_string]

        elif value.endswith("education-and-training-requirements/"):
            """How to become one"""  # Replace html  /salary/ with /education-and-training-requirements/
            steps_string = "Retry"
            certs_string = "Retry"
            try:
                if soup.find(id=f"how-to-become-an-{dashkey[:-4]}") != None:
                    print("training is here")
                    training_all = soup.find(id=f"how-to-become-an-{dashkey[:-4]}").parent
                elif soup.find(id=f"how-to-become-a-{dashkey[:-4]}") != None:
                    print("training is here")
                    training_all = soup.find(id=f"how-to-become-a-{dashkey[:-4]}").parent
                steps = training_all.find_all("ul")[0]
                step_list = []
                for step in steps:
                    clean_step = step.get_text(strip=True)
                    if clean_step:
                        step_list.append(clean_step)
                steps_string = ", ".join(step_list)
                certs = training_all.find_all("ul")[1]
                cert_list = []
                for cert in certs:
                    clean_cert = cert.get_text(strip=True)
                    if clean_cert:
                        cert_list.append(clean_cert)
                certs_string = ", ".join(cert_list)
            except Exception as e:
                print(e, " education and training requirements failed")
                if key not in retry_dict:
                    retry_dict[key] = value
            # print(steps_string, "\n", certs_string, "\n")
            if key in scraped_dict:
                scraped_dict[key + " ce4"] = [value, steps_string, certs_string ]
            else:
                scraped_dict[key] = [value, steps_string, certs_string]
        else:
            print(value)

def sal_com_refining_simple(soup, dict):
    try:
        div = soup.find(class_="salary-overview-main-intro")
        avg = div.find("b")
        rest = div.find_all("li")
        high = rest[0]
        p25_75 = rest[1]
        low = rest[2]
        # print(high.text, avg.text, p25_75.text, low.text)
        if key in scraped_dict:
            scraped_dict[key + ": sc"] = [value, high.text[31:], p25_75.text[39:], avg.text, low.text[31:]]
        else:
            scraped_dict[key] = [value, high.text[31:], p25_75.text[39:], avg.text, low.text[31:]]
    except Exception as e:
        print(e)
        retry_dict[key + ": sc"] = value
def sal_com_refining_complete(soup, dict):
    # try:
        if soup == None:
            retry_dict[key] = value
            high = p25_75 = low = entry = inter = senior = special = expert = education_gen = education_string = skill_string = \
                industry_gen = industry_string = state_string = city_string = tasks_string = rel_jobs_string = "retry FULL"
        elif soup.find(id="human-check"):
            retry_dict[key] = value
            high = p25_75 = low = entry = inter = senior = special = expert = education_gen = education_string = skill_string = \
                industry_gen = industry_string = state_string = city_string = tasks_string = rel_jobs_string = "retry FULL"
        else:
            high = p25_75 = low = entry = inter = senior = special = expert = education_gen = education_string = skill_string = \
                industry_gen = industry_string = state_string = city_string = tasks_string = rel_jobs_string = "retry"
            """Salary:"""
            try:
                div = soup.find(class_="salary-overview-main-intro")
                avg = div.find("b")
                rest = div.find_all("li")
                high = rest[0].get_text(strip=True)
                p25_75 = rest[1].get_text(strip=True)
                low = rest[2].get_text(strip=True)
                # print(high.text, avg.text, p25_75.text, low.text)
            except Exception as e:
                print(e, key, "general salary retry")
                if key not in retry_spec_dict:
                    retry_spec_dict[key] = value
            """Salary by Exp"""
            try:
                exp_table = soup.find(class_="salary-by-experience-table")
                exp_data = exp_table.find_all("td")
                entry = exp_data[1].get_text(strip=True)
                inter = exp_data[3].get_text(strip=True)
                senior = exp_data[5].get_text(strip=True)
                special = exp_data[7].get_text(strip=True)
                expert = exp_data[9].get_text(strip=True)
            except Exception as e:
                print(e, key, "exp retry")
                if key not in retry_spec_dict:
                    retry_spec_dict[key] = value
            """Salary by Education"""
            try:
                education_list = []
                education_gen_txt = soup.find(class_="salary-by-education-intro").get_text(strip=True)
                education_gen = " ".join(education_gen_txt.split())
                educ_salary_table = soup.find(class_="salary-by-education-table")
                educations = educ_salary_table.find("tbody").find_all("tr")
                for education in educations:
                    education_list.append(education.get_text(strip=True))
                education_string = ", ".join(education_list)
            except Exception as e:
                print(e, key, "education retry")
                if key not in retry_spec_dict:
                    retry_spec_dict[key] = value
            """Skills"""
            try:
                skill_list = []
                skills = soup.find_all(class_="salary-boosting-skills-list")
                for skill in skills:
                    skill_txt = skill.get_text(strip=True)
                    skill_list.append(skill.get_text(strip=True))
                skill_string = ", ".join(skill_list)
            except Exception as e:
                print(e, key, "skills retry")
                if key not in retry_spec_dict:
                    retry_spec_dict[key] = value
            """Salary by Industry"""
            try:
                industry_list = []
                industry_gen_txt = soup.find(class_="highest-paying-industries-intro").get_text(strip=True)
                industry_gen = " ".join(industry_gen_txt.split())
                top_industries = soup.find(class_="highest-paying-industries-table")
                industries = top_industries.find("tbody").find_all("tr")
                for industry in industries:
                    industry_txt = industry.get_text(strip=True)
                    industry_txt2 = industry_txt.replace(".0", "/hr.")
                    industry_list.append(industry_txt2.translate({ord('$'): ': $', ord('.'): '; ', ord(','): ''}))
                industry_string = ", ".join(industry_list)
            except Exception as e:
                print(e, key, "industry retry")
                if key not in retry_spec_dict:
                    retry_spec_dict[key] = value
            """Salary by State"""
            state_list = []
            try:
                state_salaries = soup.find(class_="slide layout-carousel salary-state")
                states = state_salaries.find_all(class_="salary-state-card")
                for state in states:
                    state_txt = state.get_text(strip=True)
                    state_list.append(state_txt.translate({ord(','): '', ord('$'): ': $'}))
                state_string = ", ".join(state_list)
            except Exception as e:
                print(e, key, "state retry")
                if key not in retry_spec_dict:
                    retry_spec_dict[key] = value
            """Salary by City"""
            city_list = []
            try:
                city_salaries = soup.find(class_="slide layout-carousel top-paying")
                cities = city_salaries.find_all(class_="cursor-pointer top-paying-card")
                for city in cities:
                    city_txt = city.get_text(strip=True)
                    city_list.append(city_txt.translate({ord(','): '', ord('$'): ': $'}))
                city_string = ", ".join(city_list)
            except Exception as e:
                print(e, key, "city retry")
                if key not in retry_spec_dict:
                    retry_spec_dict[key] = value
            """Tasks and Responsibilities"""  # FAQ Section
            try:
                tasks = soup.find(class_="faq-question", string=re.compile(f"What are the responsibilities"))
                tasks_string = tasks.next_element.next_element.next_element.get_text(strip=True)
            except Exception as e:
                print(e, key, "Tasks retry")
                if key not in retry_spec_dict:
                    retry_spec_dict[key] = value
            """Related Jobs + Sals"""
            try:
                rel_jobs_list = []
                related_jobs = soup.find(class_="slide layout-carousel jobs-related")
                jobs = related_jobs.find_all(class_="jobs-related-card")
                for job in jobs:
                    job_txt = job.get_text(strip=True)
                    rel_jobs_list.append(job_txt.translate({ord(','): '', ord('$'): ' $'}))
                rel_jobs_string = ", ".join(rel_jobs_list)
            except Exception as e:
                print(e, key, "related jobs retry")
                if key not in retry_spec_dict:
                    retry_spec_dict[key] = value

        if key in scraped_dict:
            scraped_dict[key + ": sc"] = [value, high, p25_75, low, expert, special, senior, inter, entry, education_string, education_gen,
                                          skill_string, industry_gen, industry_string, state_string, city_string, tasks_string, rel_jobs_string]
        else:
            scraped_dict[key] = [value, high, p25_75, low, expert, special, senior, inter, entry, education_string, education_gen,
                                          skill_string, industry_gen, industry_string, state_string, city_string, tasks_string, rel_jobs_string]
    # except Exception as e:
    #     print(e, key, "scraped retry")
    #     retry_dict[key] = value
    #     high = p25_75 = low = entry = inter = senior = special = expert = education_gen = education_string = skill_string = \
    #         industry_gen = industry_string = state_string = city_string = tasks_string = rel_jobs_string = "retry FULL"
    #     if key in scraped_dict:
    #         scraped_dict[key + ": sc"] = [value, high, p25_75, low, expert, special, senior, inter, entry, education_string, education_gen,
    #                                       skill_string, industry_gen, industry_string, state_string, city_string, tasks_string, rel_jobs_string]
    #     else:
    #         scraped_dict[key] = [value, high, p25_75, low, expert, special, senior, inter, entry, education_string, education_gen,
    #                                       skill_string, industry_gen, industry_string, state_string, city_string, tasks_string, rel_jobs_string]

    # You can just make your script wait when the Captcha is detected, and play a sound when it's shown so you can manually do the captcha yourself,
    #    <div class="hv-title">Human Check Required</div>
    #       <div class="hv-cbox-wrapper">
    #             <label class="hv-label" id="hv-checkbox" style="display: flex;">
    #                 <input type="checkbox" name="isChecked" id="human-check">
    #                 I am not a robot
    #             </label>
    #             <div class="verifying-container" id="token-loader" style="display: none;">
    #                 <div class="verifying">
    #                     <svg id="verifying-i" viewBox="0 0 30 30" xmlns="http://www.w3.org/2000/svg">
    #                         <path class="circle" d="M15 1.5 L15 5.5 M24.5459 5.4541 L21.7175 8.2825 M28.5 15 L24.5 15 M24.5459 24.5459 L21.7175 21.7175 M15 28.5 L15 24.5 M5.4541 24.5459 L8.2825 21.7175 M1.5 15 L5.5 15 M5.4541 5.4541 L8.2825 8.2825"></path>
    #                 <div class="verifying-msg">
    #                     <span id="verifying-text">verifying…</span>

"""Activation: Salary-specific"""
# for key, value in other_dict.items():
# for key, value in bio_and_data_dict.items():
#     soup = stealth_scrape(key, value)
#     print(soup)
#     if value.startswith("https://www.ziprecruiter"):
#         zip_refining(soup, other_dict)
    # elif value.startswith("https://www.careerbuilder.com"):
    #     car_build_refining(soup, other_dict)
    # elif value.startswith("https://www.careerexplorer.com"):
    #     car_exp_refining_simple(soup, other_dict)
    # elif value.startswith("https://www.salary.com"):
    #     sal_com_refining_simple(soup, other_dict)


"""Activation: In-Depth"""
for key, value in bio_and_data_dict.items():
# for key, value in bio_and_data_dict.items():
    soup = stealth_scrape(key, value)
    # if value.startswith("https://www.salaryexpert.com/"): # FINISH... figure out how to acrape all pages
    #     sal_exp_refining_complete(soup, bio_and_data_dict)
    if value.startswith("https://www.careerexplorer.com"):
        car_exp_refining_complete(soup, bio_and_data_dict)
    # if value.startswith("https://www.salary.com"):
    #     sal_com_refining_complete(soup, retry)

"""Career Explorer dict combining"""
final_dict = copy.deepcopy(scraped_dict)
for key, value in scraped_dict.items():
    try:
        if key[:-4] in final_dict:
            refvalue = final_dict[key][1:]
            final_dict[key[:-4]].extend(refvalue)
        else:
            final_dict[key[:-4]] = final_dict[key]
        del final_dict[key]
    except Exception as e:
        print(e, key)
print("final refined:", final_dict)

print(scraped_dict)
print("retry = ", retry_dict)
print("spec retry = ", retry_spec_dict)

# retry_scraping(retry_dict, bio_and_data_dict)

"""Writing to CSV:"""
with open(f"{JOB_FOLDER}scraped_jobs.csv", "w", newline="") as csvfile:
    writer = csv.writer(csvfile)
#     # writer.writerow(["Title", "Link", "Top Earners", "75th Percentile", "Average", "25th Percentile"])
#     # writer.writerow(["Title", "Link", "Top 10%", "25-75%", "Average", "Bottom 10%"])
#    """Career Explorer"""
    writer.writerow(["Title", "Link", "Top 10%", "Top 20%", "Top 25%", "Median", "Low 25%", "Low 20%", "Low 10%", "Similar Jobs",
                     "desc_full", "tasks_refd", "sub_types", "workplace_full", "rel_tits_string",
                     "summary", "new_skills_string", "timeless_string", "today_string", "y2030_string",
                     "steps_string", "certs_string", ])
    for key, values in final_dict.items():  # Combine key and the list of values into one flat list
    # """Salary_com"""
    # writer.writerow(["Title", "Link", "Top 10%", "25%-75%", "Low 10%", "Expert (>8)", "Senior (5-8)", "Mid (2-4)", "Early (1-2)", "Entry (<1y)",
    #                  "% with Education Lvl:", "Education Overview", "Skills", "Industry Overview", "Salary by Industry; % >/< Avg",
    #                  "By State", "By City", "Tasks", "Related Jobs", ])
    # for key, values in scraped_dict.items():  # Combine key and whole list of values into a list
        row = [key, *values]
        writer.writerow(row)
