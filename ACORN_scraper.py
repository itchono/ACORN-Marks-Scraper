'''
pip install python-dotenv
pip install selenium

download chrome driver, https://chromedriver.chromium.org/
and add it to system PATH

provide credentials in file called .env
form should be of

UTORID = utorid
UTORPW = password
'''
import os
import dotenv
from selenium import webdriver
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
import re

driver = webdriver.Chrome()

dotenv.load_dotenv()


driver.get("https://acorn.utoronto.ca/sws")

WebDriverWait(driver, 10).until(EC.title_contains("weblogin"))

driver.find_element_by_id("username").send_keys(os.environ.get("UTORID"))
driver.find_element_by_id ("password").send_keys(os.environ.get("UTORPW"))
driver.find_element_by_name("_eventId_proceed").click()


WebDriverWait(driver, 10).until(EC.title_contains("ACORN"))


driver.get("https://acorn.utoronto.ca/sws/#/history/academic")

WebDriverWait(driver, 2)

container = driver.find_element_by_class_name("academic-history-recent")

content = container.get_attribute("innerHTML")

with open("dump.html", "w") as f:
    f.write(content)

pattern = re.compile(
    r"<td>(.*?)</td>\n\t*<td>(.*?)</td>\n\t*<td class=\"course-weight\">.*?</td>\n\t*<td class=\"course-mark\">\n\t*(.*?)\n\t*<!---->\n\t*<\/td>")

grades = re.findall(pattern, content)

with open("marks.txt", "w") as f:
    for gradeset in grades:
        course, name, grade = gradeset

        if not grade:
            grade = "Not released yet"

        f.write(f"{course}: {grade}\n")

print("Dumped raw HTML to dump.html and marks to marks.txt.")
