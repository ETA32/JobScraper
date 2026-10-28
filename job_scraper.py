import asyncio
from playwright.async_api import async_playwright
from playwright_stealth import Stealth  # Or use async-equivalent variations
from bs4 import BeautifulSoup
import os
from dotenv import load_dotenv

load_dotenv()

JOB_FOLDER = os.getenv("JOB_FOLDER")

"""Links"""
test = "https://www.scrapethissite.com/pages/forms/"
ziprecruiterjobs = "https://www.ziprecruiter.com/browse/titles/"
ziprecruitersalaries = "https://www.ziprecruiter.com/browse/salaries"
indeedjobs = "https://www.indeed.com/browsejobs"
salaryexpert = "https://www.salaryexpert.com/salary/browse/jobs"
career_com = "https://www.career.com/jobs/-by-title"
# salary_com = #"https://www.salary.com/research/salary"

"""Scraping Jobs"""
# response = requests.get(ziprecruiterjobs)
# print(response.status_code)
## print(response.text)
# beautiful_soup = BeautifulSoup(response.content, "html.parser")
# print(beautiful_soup.prettify())

# async def scrape_cloudflare():
#     async with async_playwright() as p:
#         """ Launching (custom arguments to bypass basic sandbox detection)"""
#         browser = await p.chromium.launch(
#             headless=False,  # Headful mode is safer for high-security targets
#             args=[
#                 "--disable-blink-features=AutomationControlled",
#                 "--start-maximized"
#             ] )
#         """Creating realistic context w/ matched viewports and User-Agents"""
#         context = await browser.new_context(
#             user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
#             viewport={"width": 1920, "height": 1080}
#         )
#         page = await context.new_page()
#         # await page.add_init_script(self.script_payload)
#         # stealth = Stealth()
#         # stealth.apply_stealth_sync(page)
#         await Stealth()
#         await page.goto("https://www.scrapethissite.com/pages/forms/", wait_until="domcontentloaded")
#         """Inserting realistic delay to let Turnstile challenges resolve"""
#         await asyncio.sleep(5)
#         print(await page.title())
#         await browser.close()
# asyncio.run(scrape_cloudflare())

from seleniumbase import sb_cdp
from playwright.sync_api import sync_playwright

testnumber = 2
sb = sb_cdp.Chrome()
endpoint_url = sb.get_endpoint_url()
# Attaching Playwright to the active stealth browser
with sync_playwright() as p:
    browser = p.chromium.connect_over_cdp(endpoint_url)
    default_context = browser.contexts[0]
    page = default_context.pages[0] if default_context.pages else default_context.new_page()
    page.goto(f"{ziprecruiterjobs}A?page={testnumber}")
    # page.screenshot(path="stealth_test.png", fullPage=True)
    page.wait_for_timeout(3000)
    # print(f"Successfully bypassed! Page title: {page.title()}")
    html_content = page.content()
    browser.close()

soup = BeautifulSoup(html_content, "html.parser")
# print (soup)
# items = soup.find_all("div", class_="site_content")
# print(items)
# for item in items:
#     print (item.text)

# jobs = soup.find_all("td")
# for job in jobs:
    # print (job.text)

pagelist = []
pages = soup.find_all("a", class_="pagination_item")
for page in pages:
    # print(page.get_text())
    # print(type(page.get_text()))
    pagelist.append(page.get_text())
print(type(int(pagelist[-2])))


"""Adding Scraped jobs (Dict) matching Good jobs (List) to new dict"""
good_jobs_dict = {}
with open (f"{JOB_FOLDER}goodjobs_final.txt", "r") as f:
    good_checked_jobs = f.readlines()
# print(len(good_checked_jobs))
for job in good_checked_jobs:
    good_jobs_dict = {k: v for k, v in job_dict.items() if k == job}
print(len(good_jobs_dict))
with open (f"{JOB_FOLDER}new_good_jobs.txt", "w") as n:
    for k, v in good_jobs_dict.items():
        n.write(f"{k}: {v}\n")


"""Filtering Scraped jobs using Bad & Good jobs"""
new_jobs_dict = {}
# all_jobs_final = []
with open (f"{JOB_FOLDER}goodjobs_final.txt", "r") as good, open (f"{JOB_FOLDER}bad_checked_jobs_clean.txt", "r") as bad:
    good_jobs = good.readlines()
    bad_jobs = bad.readlines()
    all_jobs = good_jobs + bad_jobs
    all_jobs_clean = [item.replace("\n", "") for item in all_jobs]
    # print(all_jobs_clean)
    # all_jobs_final += all_jobs_clean

    # for job in all_jobs_clean:
    #     print(job)
    #     new_jobs_dict = {k: v for k, v in job_dict.items() if k == job}
    # print(len(new_jobs_dict))
    new_jobs_dict = {k: v for k, v in job_dict.items() if k not in all_jobs_clean}
    print(len(new_jobs_dict))

with open (f"{JOB_FOLDER}new_new_jobs.txt", "w") as w:
    for k, v in new_jobs_dict.items():
        w.write(f"{k}: {v}\n")

# print(all_jobs_clean[0])
# print(bad_jobs[0])
# print(type(bad_jobs[0]))