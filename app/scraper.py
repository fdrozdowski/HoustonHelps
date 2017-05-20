from craigslist import CraigslistForSale
import requests
from bs4 import BeautifulSoup

from app.category_mapping import mapping


class CraigslistFreeStuff(CraigslistForSale):
    custom_result_fields = True

    def customize_result(self, result, html_row):
        response = requests.get(result['url'])
        soup = BeautifulSoup(response.text)
        image = soup.find('img')
        result['image'] = image['src'] if image else ''
        return result


def get_free_listings(site, category, number_of_listings):

    results = CraigslistFreeStuff(site=site, category=mapping[category], filters={'query': 'free', 'search_titles': True})
    return list(results.get_results(limit=number_of_listings))
