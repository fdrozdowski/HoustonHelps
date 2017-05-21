import requests
from bs4 import BeautifulSoup
from craigslist import CraigslistForSale
from craigslist_api.category_mapping import mapping

DEFAULT_NUMBER_OF_LISTINGS = 5


class CraigslistFreeStuff(CraigslistForSale):
    custom_result_fields = True

    def customize_result(self, result, html_row):
        response = requests.get(result['url'])
        soup = BeautifulSoup(response.text)
        image = soup.find('img')
        result['image'] = image['src'] if image else ''
        return result


def get_all_free_items_in_category(site, category, number_of_listings=DEFAULT_NUMBER_OF_LISTINGS):
    results = CraigslistFreeStuff(site=site, category=mapping[category],
                                  filters={'query': 'free', 'search_titles': True})
    return list(results.get_results(sort_by='newest', limit=number_of_listings))


def get_item_in_category(site, query, category, number_of_listings=DEFAULT_NUMBER_OF_LISTINGS):
    results = CraigslistFreeStuff(site=site, category=mapping[category],
                                  filters={'query': query, 'search_titles': True})
    return list(results.get_results(sort_by='newest', limit=number_of_listings))
