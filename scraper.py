from craigslist import CraigslistForSale
CraigslistForSale.show_filters()
free_filter = CraigslistForSale(filters={'query':'free', 'search_titles': True}, )
for result in free_filter.get_results(sort_by='newest'):
    print(result)