import time
import random
import os
import pandas as pd

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


cities = [
    "Austin, TX"
]

doctors = []
seen_profiles = set()


def human_sleep(a=4, b=7):
    time.sleep(random.uniform(a, b))


def start_driver():

    options = Options()
    options.add_argument("--start-maximized")
    options.add_argument("--disable-blink-features=AutomationControlled")

    driver = webdriver.Chrome(options=options)

    return driver


def click_skip(driver):

    try:
        skip = WebDriverWait(driver, 5).until(
            EC.element_to_be_clickable(
                (By.XPATH, "//button[contains(text(),'Skip')]")
            )
        )
        skip.click()
        human_sleep()
    except:
        pass


def scrape_city(driver, city):

    url = f"https://www.zocdoc.com/search?address={city.replace(' ','+')}"
    driver.get(url)

    human_sleep(6,10)

    click_skip(driver)

    while True:

        WebDriverWait(driver,10).until(
            EC.presence_of_element_located((By.TAG_NAME,"article"))
        )

        cards = driver.find_elements(By.TAG_NAME,"article")

        print("Cards found:", len(cards))

        for card in cards:

            try:

                link = card.find_element(
                    By.CSS_SELECTOR,
                    "a[href*='/doctor/']"
                )

                profile = link.get_attribute("href")

                if profile in seen_profiles:
                    continue

                seen_profiles.add(profile)

                name = link.text.strip()

                img = None
                try:
                    img = card.find_element(By.TAG_NAME,"img").get_attribute("src")
                except:
                    pass

                doctors.append({
                    "pic_url": img,
                    "Name": name,
                    "Profile URL": profile,
                    "Specialty": None,
                    "Rating": None,
                    "Review Count": None
                })

                print("Doctor:", name)

            except:
                continue

        human_sleep()

        try:

            next_btn = driver.find_element(
                By.XPATH,"//button[@aria-label='Next']"
            )

            if not next_btn.is_enabled():
                break

            driver.execute_script(
                "arguments[0].click();", next_btn
            )

            human_sleep(6,10)

        except:
            print("No more pages")
            break


def main():

    driver = start_driver()

    for city in cities:
        scrape_city(driver, city)

    driver.quit()

    os.makedirs("output", exist_ok=True)

    df = pd.DataFrame(doctors)

    df.to_csv("output/zocdoc_doctors.csv", index=False)

    print("\nScraping finished")
    print("Total doctors:", len(df))


if __name__ == "__main__":
    main()