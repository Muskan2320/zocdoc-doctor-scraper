from playwright.sync_api import sync_playwright
import pandas as pd
import os
import time

cities = [
    "New York, NY",
    "Philadelphia, PA",
    "Austin, TX"
]

doctors = []
seen_profiles = set()


def clean_text(val):
    if val:
        return val.strip()
    return None


def scrape_city(page, city):

    offset = 0

    while True:

        url = f"https://www.zocdoc.com/search?address={city.replace(' ', '+')}&offset={offset}"

        print(f"\nScraping {city} | offset={offset}")

        page.goto(url)
        page.wait_for_load_state("networkidle")

        cards = page.query_selector_all("article")

        print("Doctor cards found:", len(cards))

        if len(cards) == 0:
            break

        for card in cards:

            try:

                name_el = card.query_selector("h2")
                name = clean_text(name_el.inner_text()) if name_el else None

                profile_el = card.query_selector("a")
                profile_url = profile_el.get_attribute("href") if profile_el else None

                if profile_url and profile_url.startswith("/"):
                    profile_url = "https://www.zocdoc.com" + profile_url

                if not profile_url or profile_url in seen_profiles:
                    continue

                seen_profiles.add(profile_url)

                img_el = card.query_selector("img")
                img_url = img_el.get_attribute("src") if img_el else None

                specialty = None
                specialty_el = card.query_selector("div:has-text('Doctor')")
                if specialty_el:
                    specialty = clean_text(specialty_el.inner_text())

                rating = None
                rating_el = card.query_selector("span[aria-label*='stars']")
                if rating_el:
                    rating = clean_text(rating_el.inner_text())

                review_count = None
                review_el = card.query_selector("span:has-text('reviews')")
                if review_el:
                    review_count = clean_text(review_el.inner_text())

                doctors.append({
                    "pic_url": img_url,
                    "Name": name,
                    "Profile URL": profile_url,
                    "Specialty": specialty,
                    "Rating": rating,
                    "Review Count": review_count
                })

            except Exception as e:
                continue

        offset += 10

        time.sleep(2)


def main():

    with sync_playwright() as p:

        browser = p.chromium.launch(headless=False)

        page = browser.new_page()

        for city in cities:
            scrape_city(page, city)

        browser.close()

    df = pd.DataFrame(doctors)

    os.makedirs("output", exist_ok=True)

    df.to_csv("output/zocdoc_doctors.csv", index=False)

    print("\nScraping finished!")
    print("Total doctors collected:", len(df))
    print("CSV saved to: output/zocdoc_doctors.csv")


if __name__ == "__main__":
    main()