from flask import Flask, jsonify, request
from craigslist_api.search import get_all_free_items_in_category, get_item_in_category
from craigslist_api.error import InvalidUsage

app = Flask(__name__)
DEFAULT_CRAIGSLIST_SITE = 'houston'


@app.route('/items/<string:category>', methods=['GET'])
def get_craigslist_category_data(category):
    if category is None:
        return InvalidUsage('No category specified.', status_code=400)
    else:
        result = get_all_free_items_in_category(DEFAULT_CRAIGSLIST_SITE, category)
        return jsonify(result)


@app.route('/items/<string:category>/<string:item>', methods=['GET'])
def get_craigslist_item_data(category, item):
    if category is None and item is None:
        return InvalidUsage('No category or item specified.', status_code=400)
    elif item is None:
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

if __name__ == '__main__':
    app.run()
