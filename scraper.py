import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin

BASE_URL = "https://shakespeare.mit.edu/"
OUTPUT_FILE = "shakespeare_plays.txt"

def get_soup(url):
    """Fetch a page and return a BeautifulSoup object."""
    response = requests.get(url)
    response.raise_for_status()
    return BeautifulSoup(response.text, "html.parser")

def get_play_links():
    """Get all links from the main table on the homepage."""
    soup = get_soup(BASE_URL)
    tables = soup.find_all("table")
    table = tables[1]
    links = []
    print(table)
    for a in table.find_all("a"):
        href = a.get("href")
        if href:
            full_url = urljoin(BASE_URL, href)
            links.append(full_url)
    return links

def get_entire_play_link(page_url):
    """Return the URL of the 'Entire play' link or None if not found."""
    soup = get_soup(page_url)
    a_tag = soup.find("a", string=lambda text: text and "Entire play" in text)
    if a_tag:
        return urljoin(page_url, a_tag.get("href"))
    return None

def extract_text(url):
    """Extract and return all visible text from a page."""
    soup = get_soup(url)
    for element in soup(["script", "style"]):
        element.decompose()
    text = soup.get_text(separator="\n")
    lines = [line.strip() for line in text.splitlines() if line.strip()]
    return "\n".join(lines)

def main():
    play_links = get_play_links()
    print(play_links)
    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        for link in play_links:
            if "Sonnets" in link:  # special handling for Sonnets
                text = extract_text(link)
                f.write(f"\n{text}\n")
            else:
                entire_play_url = get_entire_play_link(link)
                if entire_play_url:
                    text = extract_text(entire_play_url)
                    f.write(f"\n{text}\n")

    print(f"All plays and sonnets saved in {OUTPUT_FILE}")

if __name__ == "__main__":
    main()
