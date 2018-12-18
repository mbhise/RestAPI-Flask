from flask import Flask
from flask import Response

import data

app = Flask(__name__)
data = data.PhoneDataLayer()


def get_results(n=None):
    return u'[' + u', '.join(map(str, data.get_entries(n))) + u']'


def get_results_by_area(area_code, n=None):
    # filter the results by area (and limit if specified)
    if n:
        d = list(filter(lambda entry: entry.area_code == area_code, data.get_all_entries()))
    else:
        d = list(filter(lambda entry: entry.area_code == area_code, data.get_entries(n)))
    return u'[' + u', '.join(map(str, d)) + u']'


@app.route('/results', methods=['GET'])
def results():
    return Response(get_results(), mimetype='application/json')


@app.route('/results/<int:number>', methods=['GET'])
def results_with_limit(number):
    return Response(get_results(number), mimetype='application/json')


@app.route('/resultsForArea/<string:area_code>', methods=['GET'])
def results_by_area(area_code):
    return Response(get_results_by_area(area_code), mimetype='application/json')


@app.route('/resultsForArea/<string:area_code>/<int:number>', methods=['GET'])
def results_by_area_with_limit(area_code, number):
    return Response(get_results_by_area(area_code, number), mimetype='application/json')


if __name__ == '__main__':
    app.run(debug=True)
