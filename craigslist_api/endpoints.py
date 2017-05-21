from flask import jsonify, Flask

from craigslist_api.category_mapping import mapping
from craigslist_api.search import get_all_free_items_in_category, get_item_in_category
from craigslist_api.error import InvalidUsage

DEFAULT_CRAIGSLIST_SITE = 'houston'

app = Flask(__name__)


@app.route('/', methods=['GET'])
def index():
    return 'Craigslist API'


@app.route('/items/<string:category>', methods=['GET'])
@app.route('/items/<category>/<item>', methods=['GET'])
def get_craigslist_category_data(category, item=None):
    if category is None and item is None:
        raise InvalidUsage('No category or item specified.', status_code=400)
    elif item is None:
        if category not in mapping:
            raise InvalidUsage(category + ' is not a valid category. These are valid categories: ' +
                                str(mapping.keys()), status_code=400)
        result = get_all_free_items_in_category(DEFAULT_CRAIGSLIST_SITE, category)
        return jsonify(result)
    else:
        result = get_item_in_category(DEFAULT_CRAIGSLIST_SITE, item, category)
        return jsonify(result)


@app.errorhandler(InvalidUsage)
def handle_invalid_usage(error):
    response = jsonify(error.to_dict())
    response.status_code = error.status_code
    return response
