from seleniumbase import sb_cdp
from playwright.sync_api import sync_playwright
from bs4 import BeautifulSoup
import os
from dotenv import load_dotenv

load_dotenv()

"""File Locations"""
JOB_FOLDER = os.getenv("JOB_FOLDER")
FILTER_FILES = os.getenv("FILTER_FILES")

"""Links"""
test = "https://www.scrapethissite.com/pages/forms/"

# ziprecruiterbase = "https://www.ziprecruiter.com"
# ziprecruiterjobs = "https://www.ziprecruiter.com/browse/titles/"
# ziprecruitersalaries = "https://www.ziprecruiter.com/browse/salaries/"
# indeedjobs = "https://www.indeed.com/browsejobs/Titles/"
# indeedbase = ("https://www.indeed.com")
# salaryexpert = "https://www.salaryexpert.com/salary/browse/jobs/"
# salaryexpertbase = ("https://www.salaryexpert.com")
# career_com = "https://www.career.com/jobs/-by-title/?c="
# # career_com_page = f"https://www.career.com/jobs/-by-title/{number}?c="
# career_com_base = "https://www.career.com/jobs/"
# bls = "https://www.bls.gov/ooh/a-z-index.htm"
"""FINISH"""
# careerexplorer = f"https://www.careerexplorer.com/careers/?page=" # 10j per "page" ;  get num of pgs from: "x of 1,673 results" (=168 pgs)
# careerexplore_base = "https://www.careerexplorer.com"
# careerbuilder = "https://www.careerbuilder.com/browse/titles/" #{letter}
# careerbuilder_base = "https://www.careerbuilder.com"
# salary_com_middle = f"https://www.salary.com/research/middle-income-salary?view=compact&pageno="
# salary_com_upper = f"https://www.salary.com/research/upper-middle-income-salary?view=compact&pageno="
# salary_com_high = f"https://www.salary.com/research/high-income-salary?view=compact&pageno="
salary_com_six = f"https://www.salary.com/research/six-figure-income-salary?view=compact&pageno="
salarycom_base = '' #"https://www.salary.com/research"

def block_ads(route):
    # Match Google ads or leads domain/path
    if 'googleads' in route.request.url or 'g.doubleclick.net' in route.request.url:
        route.abort()
    else:
        route.continue_()


letters = ("A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M", "N", "O", "P", "Q", "R", "S", "T", "U", "V", "W", "X", "Y", "Z")
lettertest = ("A")
pagenumbers = 1190  # final page+1
pagenumbertest = 2

sb = sb_cdp.Chrome()
endpoint_url = sb.get_endpoint_url()

job_dict = {}
# for letter in letters:
for pagenumber in range(1, pagenumbers):
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
            # page.goto(f"{careerbuilder}{letter}", wait_until="domcontentloaded")
            page.goto(f"{salary_com_six}{pagenumber}", wait_until="load")
            page.wait_for_timeout(3000)
            # page.locator("id=main-content").wait_for()
            # print(f"Successfully bypassed! Page title: {page.title()}")
            html_content = page.content()
            browser.close()
        soup = BeautifulSoup(html_content, "html.parser")
    except Exception as e:
        print(e, f"\nSKIPPED: {salary_com_six}{pagenumber}")
        continue
    # print (soup)
    # print(f"{careerbuilder}{letter}")
    print(f"{salary_com_six}{pagenumber}")
    """website-specific tag for each job listing here"""
    jobs = soup.find_all("a", class_="font-semibold text-size18")
    # job_table = soup.find("ul", class_="JobTitlesList_list__A6bG7")
    # if job_table:
    #     jobs = job_table.find_all("li")
    # # print(len(jobs))
    for job in jobs:
        # print(job)
        title = job.get_text().strip()
        if title[-1] == " ":
            title = title[:-1]
        # link = job.find("a", string="Salary").get('href')
        link = job.get('href')
        # print(title, link)

        """website base link here, for link creation"""
        # job_dict[((job.h3.get_text()).lower()).strip("\n")] = f"{career_com_base}{job.get('href')}"
        # job_dict[((job.get_text()).lower()).strip("\n")] = f"{careerexplore_base}{job.get('href')}"
        job_dict[(title.lower()).strip("\n")] = f"{salarycom_base}{link}"

    """Pagination  | put site-specific class here"""
    # pagelist = []
    # # pages = soup.find_all("a", class_="pagination_item")
    # # for page in pages:
    # #     pagelist.append(page.get_text())
    # # print(pagelist)
    # if pagelist:
    #     finalpage = int(pagelist[-2]) + 1
    #     """Pages 2-X"""
    #     for number in range(2, finalpage): #scrape last pagenumber from ^
    #         with sync_playwright() as p:
    #             browser = p.chromium.connect_over_cdp(endpoint_url)
    #             default_context = browser.contexts[0]
    #             page = default_context.pages[0] if default_context.pages else default_context.new_page()
    #             """website link here"""
    #             page.goto(f"https://www.career.com/jobs/-by-title/{number}?c={letter}")
    #             page.wait_for_timeout(3000)
    #             html_content = page.content()
    #             browser.close()
    #         soup = BeautifulSoup(html_content, "html.parser")
    #         jobs = soup.find_all("td")
    #         for job in jobs:
    #             """website base link here, for link creation"""
    #             job_dict[(job.get_text()).lower()] = f"{career_com_base}{job.a.get('href')}"
    #     print(len(job_dict))
    # else:
    #     print(len(job_dict))
    #     continue
    """Pagination 2:  Hidden Final Page Number (use 'Next' button"""
    # try:
    #     nextpage = (soup.find(attrs={"aria-label": "Next"})).get("href")
    #     while nextpage:
    #         # print("bing bong")
    #         print(nextpage)
    #         with sync_playwright() as p:
    #             browser = p.chromium.connect_over_cdp(endpoint_url)
    #             default_context = browser.contexts[0]
    #             page = default_context.pages[0] if default_context.pages else default_context.new_page()
    #             page.route("**/cookie_push_onload*", lambda route: route.abort())
    #             page.route("**/pagead2.googlesyndication.com/**", lambda route: route.abort())
    #             page.route("**googleads**", lambda route: route.abort())
    #             page.route("**adtrafficquality**", lambda route: route.abort())
    #             page.route('**/*', block_ads)
    #             """website link here"""
    #             page.goto(f"https://www.career.com{nextpage}", wait_until="domcontentloaded")
    #             # page.wait_for_timeout(2000)
    #             html_content = page.content()
    #             browser.close()
    #         soup = BeautifulSoup(html_content, "html.parser")
    #         """website-specific tag for each job listing here"""
    #         jobs = soup.find_all("a", class_="crr-card-item")
    #         for job in jobs:
    #             job_dict[((job.h3.get_text()).lower()).strip("\n")] = f"{career_com_base}{job.get('href')}"
    #         nextpage = (soup.find(attrs={"aria-label": "Next"})).get("href")
    #     # else:
    #     #     # print("Womp womp")
    #     print(len(job_dict))
    #     continue
    # except AttributeError:
    #     continue


# first_item = next(iter(job_dict.items()))
# print(first_item)
# for k, v in job_dict.items():
#     print(k, v)
    # print(type(k))


"""Adding Scraped jobs (Dict) matching Good jobs (List) to new dict"""
good_jobs_dict = {}
with open (f"{FILTER_FILES}goodjobs_finalX.txt", "r") as f:
    good_checked_jobs = f.readlines()
    good_checked_jobs_clean =  [item.replace("\n", "") for item in good_checked_jobs]
    good_jobs_dict = {k: v for k, v in job_dict.items() if k in good_checked_jobs_clean}
print(len(good_jobs_dict))

with open (f"{JOB_FOLDER}salary_com_six_new_good_jobs.txt", "w") as g:
    for k, v in good_jobs_dict.items():
        g.write(f"{k}: {v}\n")


"""Filtering Scraped jobs using Bad & Good jobs"""
new_jobs_dict = {}
with (open (f"{FILTER_FILES}goodjobs_finalX.txt", "r") as good,
      open (f"{FILTER_FILES}bad_checked_jobs_cleanX.txt", "r") as bad):
    good_jobs = good.readlines()
    bad_jobs = bad.readlines()
    all_jobs = good_jobs + bad_jobs
    all_jobs_clean = [item.replace("\n", "") for item in all_jobs]
    # print(all_jobs_clean)
    new_jobs_dict = {k: v for k, v in job_dict.items() if k not in all_jobs_clean}
    print(len(new_jobs_dict))

with open (f"{JOB_FOLDER}salary_com_six_new_new_jobs.txt", "w") as n:
    for k, v in new_jobs_dict.items():
        n.write(f"{k}: {v}\n")
