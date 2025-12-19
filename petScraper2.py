from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import time
import re
import csv

BASE_LIST_URL = "https://24petconnect.com/PP1296?at=CAT"
PROFILE_BASE = "https://24petconnect.com/PP1296/Details/PP1296/"

def create_driver():
    opts = Options()
    opts.add_argument("--headless")       # comment out to see the browser
    opts.add_argument("--window-size=1920,1080")
    opts.add_argument("--no-sandbox")
    opts.add_argument("--disable-gpu")

    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=opts)
    return driver


def fetch_listing(driver):
    print("Loading listing page…")
    driver.get(BASE_LIST_URL)
    time.sleep(5)  # wait for JS

    soup = BeautifulSoup(driver.page_source, "html.parser")

    pets = []

    # Exact selector for names with IDs
    name_spans = soup.select("span.text_Name.results")
    for span in name_spans:
        text = span.get_text(strip=True)
        match = re.match(r"(.+?)\s*\((\d+)\)", text)
        if not match:
            continue
        name = match.group(1).strip()
        pet_id = match.group(2).strip()
        pet_url = PROFILE_BASE + pet_id

        pets.append({
            "name": name,
            "pet_id": pet_id,
            "profile_url": pet_url
        })

    print(f"Found {len(pets)} pets")
    return pets

def fetch_profile(driver, cat):
    print("Opening profile:", cat["profile_url"])
    driver.get(cat["profile_url"])
    time.sleep(7)

    soup = BeautifulSoup(driver.page_source, "html.parser")
    detail_container = soup.find("div", class_="animalDetailsBox")

    if not detail_container:
        return {
            "name": cat["name"],
            "pet_id": cat["pet_id"],
            "age": None,
            "gender": None,
            "breed": None,
            "color": None,
            "location": None,
            "profile_url": cat["profile_url"],
        }

    # ---------------- HELPER FUNCTIONS ---------------- #

    def find_value(label_regex):
        label = detail_container.find(text=re.compile(label_regex, re.IGNORECASE))
        if label and label.parent:
            val = label.parent.find_next_sibling()
            if val:
                return val.get_text(strip=True)
        return None

    def extract_gender_color(text):
        match = re.search(
            r"I\s+am\s+a\s+(\w+),\s*([a-z\s]+?)\s+[A-Z]",
            text,
            re.IGNORECASE,
        )
        if match:
            return match.group(1).strip(), match.group(2).strip()
        return None, None

    def extract_breed(text):
        match = re.search(
            r"I\s+am\s+a\s+\w+,\s*.*?\s+(.*?)(?:\.)?$",
            text,
            re.IGNORECASE,
        )
        return match.group(1).strip() if match else None
    def clean_breed_prefix(breed):
        if not breed:
            return None

        # Remove leading "and <color(s)>" phrases
        breed = re.sub(
            r"^(and\s+)?(white|black|brown|gray|grey|orange|tan|cream|buff)(\s+and\s+(white|black|brown|gray|grey|orange|tan|cream|buff))*\s+",
            "",
            breed,
            flags=re.IGNORECASE
    )

        return breed.strip()

    def find_age():
        age_el = detail_container.find(
            lambda tag: tag.has_attr("class")
            and "age" in " ".join(tag["class"]).lower()
        )
        return age_el.get_text(strip=True) if age_el else None

    # ---------------- EXTRACTION ---------------- #

    gender_value = find_value(r"Sex|Gender")
    color_value = find_value(r"\bColor\b")
    breed_value = None

    descriptive_line = detail_container.find(
        text=re.compile(r"I\s+am\s+a", re.IGNORECASE)
    )

    descriptive_text = None
    if descriptive_line:
        descriptive_text = (
            descriptive_line.parent.get_text(strip=True)
            if descriptive_line.parent
            else descriptive_line.strip()
        )

        g, c = extract_gender_color(descriptive_text)
        if g:
            gender_value = g
        if c:
            color_value = c

        breed_value = extract_breed(descriptive_text)

    if not breed_value:
        breed_value = find_value(r"\bBreed\b")

    if breed_value:
        breed_value = breed_value.rstrip(".").strip()
        breed_value = clean_breed_prefix(breed_value)

    age_raw = find_age()
    age_cleaned = None
    if age_raw:
        age_cleaned = re.sub(
            r"(?:The\s+shelter\s+staff\s+think\s+I\s+am\s+about\s+|\bAge\b:?\s*)",
            "",
            age_raw,
            flags=re.IGNORECASE,
        )
        age_cleaned = re.sub(
            r"\s*(months?|years?)\s*old$|\s*(month|year)\s*$",
            "",
            age_cleaned,
            flags=re.IGNORECASE,
        ).strip()

    return {
        "name": cat["name"],
        "pet_id": cat["pet_id"],
        "age": age_cleaned,
        "gender": gender_value,
        "breed": breed_value,
        "color": color_value,
        "location": find_value(r"\bLocation\b"),
        "profile_url": cat["profile_url"],
    }
def save_csv(data, filename="pets2.csv"):
    if not data:
        print("No data to save.")
        return

    keys = data[0].keys()
    with open(filename, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=keys)
        writer.writeheader()
        writer.writerows(data)
    print("Saved to", filename)


if __name__ == "__main__":
    driver = create_driver()

    pets = fetch_listing(driver)

    if not pets:
        print("No pets were found — check selector or JS loading")
        driver.quit()
        exit()

    results = []
    for pet in pets:
        details = fetch_profile(driver, pet)
        results.append(details)

    save_csv(results)

    driver.quit()


