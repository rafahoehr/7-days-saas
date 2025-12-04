
import os
import sys
import traceback
import json
from playwright.sync_api import sync_playwright

def get_google_maps_results(service, city):
    """
    Scrapes Google Maps for a specific service in a specific city using Playwright.
    """
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()

        url = f"https://www.google.com/maps/search/{service}+{city}"
        print(f"Searching for URL: {url}")
        page.goto(url, timeout=60000)

        try:
            page.wait_for_selector('button[aria-label="Reject all"]', timeout=5000)
            page.click('button[aria-label="Reject all"]')
        except:
            pass

        page.wait_for_selector('div[role="article"]', timeout=60000)

        results = []

        elements = page.query_selector_all('div[role="article"]')

        for el in elements:
            if len(results) >= 10:
                break

            name = el.query_selector('.qBF1Pd').inner_text() if el.query_selector('.qBF1Pd') else "N/A"

            address_parts = el.query_selector_all('.W4Efsd span')
            address = ""
            if len(address_parts) > 2:
                address = address_parts[2].inner_text()


            phone = "N/A"
            website = "N/A"

            rating_el = el.query_selector('.MW4etd')
            rating = rating_el.inner_text() if rating_el else "N/A"

            results.append({
                "name": name,
                "address": address,
                "phone": phone,
                "website": website,
                "rating": rating
            })

        browser.close()
        return results

def execute_task():
    """
    Main function to execute the scraping task.
    """
    print("--- INICIANDO TAREFA: scrapes Google Maps for a specific service/profession in a specific city ---")

    service = input("Enter the service/profession to search for (e.g., 'Dentist'): ")
    city = input("Enter the city to search in (e.g., 'New York'): ")

    results = get_google_maps_results(service, city)

    with open("results.json", "w", encoding="utf-8") as f:
        json.dump(results, f, indent=4, ensure_ascii=False)

    print(f"Scraping complete. {len(results)} results saved to results.json.")

if __name__ == "__main__":
    try:
        execute_task()
        print("--- SUCESSO ---")
    except Exception as e:
        print("\n!!! FALHA CRÍTICA DETECTADA !!!")
        print(f"Erro: {str(e)}")
        traceback.print_exc()
        sys.exit(1)
