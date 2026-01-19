"""
Last version: Nov 26 2025
Author: Olaf van Waart
"""

import csv
from urllib.parse import urljoin
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import json

BASE = "https://npo.nl"

def get_seasons(series_url):
    """
    Vind alle seizoenen van een NPO Start serie.
    Voorbeeld: https://npo.nl/start/serie/ik-vertrek/afleveringen
    """
    series_base_url = "https://npo.nl/start/serie/" + series_url + "/afleveringen"
    options = webdriver.ChromeOptions()
    # Use headless mode by default; can be overridden by env if needed
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=options)

    driver.get(series_base_url)
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.TAG_NAME, 'body')))

    ## Klik op Seizoen knop om alle seizoenen te laden
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '/html/body/div[2]/main/section/div[2]/div[2]/div/div[1]/div/div/div')))
    knop = driver.find_element(By.XPATH, '/html/body/div[2]/main/section/div[2]/div[2]/div/div[1]/div/div/div')
    knop.click()
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '/html/body/div[2]/dialog/div/section/div/div/ul/li')))

    season_urls = []
    
    for li in driver.find_elements(By.XPATH, '/html/body/div[2]/dialog/div/section/div/div/ul/li'):
        recommender = json.loads(li.get_attribute('data-npo-tag-recommender')).get('recommendation', '').get('recommender', '')
        season_urls.append(recommender)
    
    driver.quit()

    return sorted(set(season_urls))

def get_episode_urls(serie_url, season_url):
    """
    Vind alle aflevering-links binnen één seizoen.
    """
    season_base_url = "https://npo.nl/start/serie/" + serie_url + "/afleveringen/" + season_url
    print("  Seizoen URL:", season_base_url)

    options = webdriver.ChromeOptions()
    #Use headless mode by default; can be overridden by env if needed
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=options)

    driver.get(season_base_url)

    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.TAG_NAME, 'body')))
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '/html/body/div[2]/main/section/div[2]/div[2]/div/div[2]/div/div/ul/li/a')))

    episode_urls = []

    for a in driver.find_elements(By.XPATH, '/html/body/div[2]/main/section/div[2]/div[2]/div/div[2]/div/div/ul/li/a'):
        href = a.get_attribute("href")

        # Alle NPO 'afspelen'-links hebben deze vorm
        if href.endswith("/afspelen"):
            full = urljoin(BASE, href)
            print("  Aflevering gevonden:", full)
            episode_urls.append(full)

    driver.quit()

    return sorted(set(episode_urls))

def scrape_series(series_url):
    seasons = get_seasons(series_url)
    print(f"Gevonden seizoenen: {len(seasons)}")

    all_rows = []

    for s in seasons:
        print("\n--- Seizoen:", s)
        episodes = get_episode_urls(series_url, s)
        print("    Aantal afleveringen:", len(episodes))

        for ep in episodes:
            all_rows.append([series_url, s, ep])

    return all_rows


if __name__ == "__main__":    
    
    with open("series.csv", "r", newline="", encoding="utf-8") as f:
        reader = csv.reader(f)
        next(reader, None) # skip header
        series_urls = [row[0] for row in reader]

    totaal = [["series_url", "season_url", "episode_url"]]

    for url in series_urls:
        totaal.extend(scrape_series(url))
    with open("alle_series_afleveringen.csv", "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerows(totaal)
