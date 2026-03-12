from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import pandas as pd
import time
import os

cities = [
    "New York, NY",
    "Philadelphia, PA",
    "Austin, TX"
]

doctors = []
seen = set()

options = Options()
options.add_argument("--start-maximized")
options.add_argument("--disable-blink-features=AutomationControlled")

driver = webdriver.Chrome(options=options)

for city in cities:

    offset = 0

    while True:

        url = f"https://www.zocdoc.com/search?address={city.replace(' ','+')}&offset={offset}"

        print("Opening:", url)

        driver.get(url)

        time.sleep(8)

        cards = driver.find_elements(By.TAG_NAME, "article")

        print("Cards:", len(cards))

        if len(cards) == 0:
            break

        for c in cards:

            try:

                name = c.find_element(By.TAG_NAME,"h2").text
                profile = c.find_element(By.CSS_SELECTOR,"a[href*='/doctor/']").get_attribute("href")

                if profile in seen:
                    continue

                seen.add(profile)

                img = c.find_element(By.TAG_NAME,"img").get_attribute("src")

                doctors.append({
                    "pic_url": img,
                    "Name": name,
                    "Profile URL": profile,
                    "Specialty": None,
                    "Rating": None,
                    "Review Count": None
                })

            except:
                pass

        offset += 10

        time.sleep(3)

driver.quit()

os.makedirs("output", exist_ok=True)

df = pd.DataFrame(doctors)
df.to_csv("output/zocdoc_doctors.csv", index=False)

print("Total doctors:", len(df))