from flask import Flask

app = Flask(__name__)


@app.route('/<category>/<item>', method='GET')
def hello_world(category, item):

    return 'Hello World!'


if __name__ == '__main__':
    app.run()
