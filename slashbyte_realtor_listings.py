import pandas as pd
from bs4 import BeautifulSoup
import requests



def scraper(base_url, location):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.0.0 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Accept-Language': 'en-US,en;q=0.5',
        'Referer': 'https://www.google.com/',
        'DNT': '1',
        'Upgrade-Insecure-Requests': '1',
        'TE': 'Trailers'
    }

    ad_listings = []
    url = f"{base_url}/realestateandhomes-search/{location}"

    with requests.Session() as session:
        session.headers.update(headers)
        try:
            response = session.get(url)
            response.raise_for_status()
        except requests.exceptions.HTTPError as e:
            print(f"HTTP Error: {e}")
            return
        except requests.exceptions.ConnectionError as e:
            print(f"Connection Error: {e}")
            return

        soup = BeautifulSoup(response.content, 'html.parser')
        for listing in soup.find_all('div', class_='BasePropertyCard_propertyCard__nbKDx'):
            title_tag = listing.find('span', class_='BrokerTitle_titleText__Y8pb0')
            if title_tag and title_tag.get_text(strip=True):
                title = title_tag.get_text(strip=True)
            else:
                title = "No Title"
            price_element = listing.find('div', class_='price-wrapper')
            if price_element:
                price = price_element.get_text(strip=True)
            else:
                price = "N/A"
            url_element = listing.find('a', class_='LinkComponent_anchor__0C2xC')
            if url_element and url_element.has_attr('href'):
                url = base_url + url_element['href']
            else:
                url = "N/A"
            ad_listings.append({"Title": title,"Price": price,"URL": url})
    if ad_listings:
        df = pd.DataFrame(ad_listings)
        df.to_csv('realtor_listings.csv', index=False)
        print("Data saved to realtor_listings.csv")

base_url = 'https://www.realtor.com'
location = 'Chicago_IL'
scraper(base_url, location)