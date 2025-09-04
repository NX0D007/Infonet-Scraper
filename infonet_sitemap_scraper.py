import requests
from bs4 import BeautifulSoup
import pandas as pd

SITEMAP_INDEX = "https://infonet.fr/sitemap_index.xml"
OUTPUT_FILE = "infonet_sitemap_results.xlsx"

def get_sitemap_urls(sitemap_url):
    """Get all URLs listed in a sitemap XML file."""
    resp = requests.get(sitemap_url)
    soup = BeautifulSoup(resp.text, "xml")
    urls = [loc.get_text() for loc in soup.find_all("loc")]
    return urls

def collect_company_urls():
    """Collect company profile URLs from the main sitemap."""
    sitemaps = get_sitemap_urls(SITEMAP_INDEX)
    company_urls = []
    for sitemap in sitemaps:
        if "companiesByApeCode" in sitemap:
            company_urls += get_sitemap_urls(sitemap)
    return company_urls

def scrape_company_page(url):
    """Extract company info from a company page."""
    resp = requests.get(url)
    soup = BeautifulSoup(resp.text, "html.parser")
    name = soup.find("h1").get_text(strip=True) if soup.find("h1") else ""
    return {
        "name": name,
        "url": url
    }

def main():
    urls = collect_company_urls()[:20]  # limit for demo
    data = [scrape_company_page(u) for u in urls]
    df = pd.DataFrame(data)
    df.to_excel(OUTPUT_FILE, index=False)
    print(f"Saved {len(data)} companies to {OUTPUT_FILE}")

if __name__ == "__main__":
    main()

