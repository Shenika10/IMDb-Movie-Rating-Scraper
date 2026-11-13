from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd
import time

# -----------------------------
# Setup Chrome
# -----------------------------
service = Service(ChromeDriverManager().install())

options = webdriver.ChromeOptions()

# Uncomment the next line if you want Headless Mode
# options.add_argument("--headless=new")

driver = webdriver.Chrome(service=service, options=options)

driver.maximize_window()

# -----------------------------
# Open IMDb Top 250
# -----------------------------
url = "https://www.imdb.com/chart/top/"
driver.get(url)

# Wait for page to load
time.sleep(5)

# -----------------------------
# Locate all movie rows
# -----------------------------
movies = driver.find_elements(By.CSS_SELECTOR, "li.ipc-metadata-list-summary-item")

rank_list = []
title_list = []
year_list = []
rating_list = []

for index, movie in enumerate(movies, start=1):

    try:
        title = movie.find_element(
            By.CSS_SELECTOR,
            "h4.ipc-title__text"
        ).text
    except:
        title = "N/A"

    try:
        metadata = movie.find_elements(
            By.CSS_SELECTOR,
            "div.cli-title-metadata li"
        )

        year = metadata[0].text

    except:
        year = "N/A"

    try:
        rating = movie.find_element(
            By.CSS_SELECTOR,
            "span.ipc-rating-star--rating"
        ).text

    except:
        rating = "N/A"

    rank_list.append(index)
    title_list.append(title)
    year_list.append(year)
    rating_list.append(rating)

# -----------------------------
# Create DataFrame
# -----------------------------
df = pd.DataFrame({
    "Rank": rank_list,
    "Movie": title_list,
    "Release Year": year_list,
    "IMDb Rating": rating_list
})

# -----------------------------
# Print Output
# -----------------------------
print(df)

# -----------------------------
# Save to CSV
# -----------------------------
df.to_csv("imdb_top_250_movies.csv", index=False)

print("\nData saved successfully as imdb_top_250_movies.csv")

driver.quit()