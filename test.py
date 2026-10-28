from seleniumbase import sb_cdp
from playwright.sync_api import sync_playwright
from bs4 import BeautifulSoup
from bs4 import BeautifulSoup
import requests
import os
from dotenv import load_dotenv

load_dotenv()

JOB_FOLDER = os.getenv("JOB_FOLDER")

test = "https://www.scrapethissite.com/pages/forms/"
testdict = {"site": "https://www.scrapethissite.com/pages/forms/"}
ziprecruiterjobs = "https://www.ziprecruiter.com/browse/titles/"
salary_expert_test = {"salary_expert_t": "https://www.salaryexpert.com/salary/job/activities-counselor/united-states"}

for item in range(1, 168):
    print(f"bing bong {item}")
    print(type(item))

# max_tries = 10
# for item in range(1, max_tries):
#     try:
#         print(f"bing bong {item}")
#     # except item > 7:
#     #     break
#     # break
#
# numdict = {2: 2, 5:5, 6:6}
# for item in range(1,11):
#     if item in numdict and 1 < numdict[item] < 11:
#         numdict[item] += 1
#     elif item not in numdict:
#         numdict[item] = 1
#
# print(numdict)

# with open (f"{JOB_FOLDER}checked_jobs_careerplanner.rtf", "r") as f:
#     all_jobs_checked = f.readlines()
# print(len(all_jobs_checked))
# # print(type(all_jobs_checked))
# bad_checked_jobs = [item for item in all_jobs_checked if item not in good_checked_jobs]
# print(len(bad_checked_jobs))

# with open (f"{JOB_FOLDER}goodjobs_final.txt", "r") as good, open (f"{JOB_FOLDER}bad_checked_jobs_clean.txt", "r") as bad, open (f"{JOB_FOLDER}new_new_jobs.txt", "r") as new:
#     good_jobs = good.readlines()
#     bad_jobs = bad.readlines()
#     # print(len(good_jobs))
#     # print(len(bad_jobs))
#     all_jobs = good_jobs + bad_jobs
#     # print(len(all_jobs))
#     new_jobs = new.readlines()
#     for job in new_jobs:
#         print(job.lower())
#         if  job.lower() in all_jobs:
#             # new_jobs.remove(job)
#             print(job)

# response = requests.get(test)
# print(response.status_code)
# # print(response.text)
# beautiful_soup = BeautifulSoup(response.content, "html.parser")
# print(beautiful_soup.prettify())
#
# list = []
# pages = beautiful_soup.find_all("a", class_="data-attribution")
# for page in pages:
#     list.append(page.get_text())
# print(list)

sb = sb_cdp.Chrome()
endpoint_url = sb.get_endpoint_url()
# letters = ("X", "Y", "Z")
# for letter in letters:
#     with sync_playwright() as p:
#         browser = p.chromium.connect_over_cdp(endpoint_url)
#         default_context = browser.contexts[0]
#         page = default_context.pages[0] if default_context.pages else default_context.new_page()
#         page.goto(f"{ziprecruiterjobs}{letter}")
#         page.wait_for_timeout(3000)
#         html_content = page.content()
#         browser.close()
#     soup = BeautifulSoup(html_content, "html.parser")
#     """Pagination prep"""
#     pagelist = []
#     pages = soup.find_all("a", class_="pagination_item")
#     for page in pages:
#         pagelist.append(page.get_text())
#     print(pagelist)
#     if pagelist:
#         finalpage = int(pagelist[-2]) + 1
#         """Pages 2-X"""
#         for number in range(2, finalpage):  # scrape last pagenumber from ^
#             with sync_playwright() as p:
#                 browser = p.chromium.connect_over_cdp(endpoint_url)
#                 default_context = browser.contexts[0]
#                 page = default_context.pages[0] if default_context.pages else default_context.new_page()
#                 page.goto(f"{ziprecruiterjobs}{letter}?page={number}")
#                 page.wait_for_timeout(3000)
#                 html_content = page.content()
#                 browser.close()
#             soup = BeautifulSoup(html_content, "html.parser")
#     else:
#         print(f"{letter}: No pages found")
#         continue

# ----------------------------------------------------------------------

def block_ads(route):
    # Match Google ads or leads domain/path
    if 'googleads' in route.request.url or 'g.doubleclick.net' in route.request.url:
        route.abort()
    else:
        route.continue_()
#
def stealth_scrape(key, value):
    with sync_playwright() as p:
        browser = p.chromium.connect_over_cdp(endpoint_url)
        default_context = browser.contexts[0]
        page = default_context.pages[0] if default_context.pages else default_context.new_page()
w        page.route("**/cookie_push_onload*", lambda route: route.abort())
        page.route("**/pagead2.googlesyndication.com/**", lambda route: route.abort())
        page.route("**googleads**", lambda route: route.abort())
        page.route("**adtrafficquality**", lambda route: route.abort())
        page.route('**/*', block_ads)
        """website link here"""
        page.goto(f"{value}", wait_until="domcontentloaded")
        page.wait_for_timeout(30000)
        # page.locator("id=main-content").wait_for()
        # print(f"Successfully bypassed! Page title: {page.title()}")
        html_content = page.content()
        browser.close()
    soup = BeautifulSoup(html_content, "html.parser")
    return soup

# for key, value in salary_expert_test.items():
#     soup = stealth_scrape(key, value)
#     print(soup)



# def retry_scraping(retry_dict, scrape_dict):
#     # print(retry_dict)
#     retry_count = len(retry_dict)
#     # print(retry_count)
#     attempts_counter = {}
#     while retry_count > 0:
#         finished_keys = []
#         for key, value in retry_dict.items():
#             if type(scrape_dict[key]) == list:
#                 retry_count -= 1
#                 finished_keys += [key]
#                 pass
#             else:
#                 if key not in attempts_counter:
#                     soup = stealth_scrape(key, value)
#                     zip_refining(soup, scrape_dict)
#                     attempts_counter[key] = 1
#                 elif key in attempts_counter and 0 < attempts_counter[key] < 5:
#                     soup = stealth_scrape(key, value)
#                     zip_refining(soup, scrape_dict)
#                     attempts_counter[key] += 1
#                 else:
#                     finished_keys += [key]
#                     retry_count -= 1
#                     pass
#         print("attempts counter:", attempts_counter)
#         for item in finished_keys:
#             # print(item)
#             if item in retry_dict:
#                 del retry_dict[item]
#             if item in attempts_counter:
#                 del attempts_counter[item]
#         print(retry_dict)
#         print(retry_count)
# retrytestdict = {"site": "https://www.scrapethissite.com/pages/forms/",
#                  "site2": "https://www.scrapethissite.com/pages/forms/",
#                  "site3": ["https://www.scrapethissite.com/pages/forms/", 3, 4], }
# scrapetestdict = {"site": "https://www.scrapethissite.com/pages/forms/",
#                  "site2": ["https://www.scrapethissite.com/pages/forms/", 2, 3],
#                  "site3": ["https://www.scrapethissite.com/pages/forms/", 3, 4], }
# retry_scraping(retrytestdict, scrapetestdict)