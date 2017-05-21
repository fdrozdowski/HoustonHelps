from flask import jsonify, Flask, escape

from craigslist_api.category_mapping import mapping
from craigslist_api.search import get_all_free_items_in_category, get_item_in_category
from craigslist_api.error import InvalidUsage

DEFAULT_CRAIGSLIST_SITE = 'houston'
API_DESCRIPTION = 'The valid endpoints are GET /items/<category> and GET /items/<category>/<query>'

app = Flask(__name__)


@app.route('/', methods=['GET'])
def index():
    return escape('Craigslist API. ' + API_DESCRIPTION)


@app.route('/items/<string:category>', methods=['GET'])
@app.route('/items/<category>/<query>', methods=['GET'])
def get_craigslist_category_data(category, query=None):
    if category is None and query is None:
        raise InvalidUsage('No category or query specified.', status_code=400)
    elif query is None:
        if category not in mapping:
            raise InvalidUsage(category + ' is not a valid category. These are valid categories: ' +
                               str(mapping.keys()), status_code=400)
        result = get_all_free_items_in_category(DEFAULT_CRAIGSLIST_SITE, category)
        return jsonify(result)
    else:
        result = get_item_in_category(DEFAULT_CRAIGSLIST_SITE, query, category)
        return jsonify(result)


@app.errorhandler(InvalidUsage)
def handle_invalid_usage(error):
    response = jsonify(error.to_dict())
    response.status_code = error.status_code
    return response


@app.errorhandler(404)
def page_not_found(e):
    return escape('The endpoint doesn\'t exist.\n' + API_DESCRIPTION)
