from flask import Flask, Response, render_template, request, jsonify
import json,sys
from autocomplete import ac_tri_angle
from autocomplete import ac_inverted_index


app = Flask(__name__)

	
@app.route('/tri-angle', methods=['GET', 'POST'])
def tri_angle():
    search = request.args.get('term')
    app.logger.debug("In main.py tri_angle(), the search term is :" + search)
    return Response(json.dumps(ac_tri_angle(search)), mimetype='application/json')

@app.route('/inverted-index', methods=['GET', 'POST'])
def inverted_index():
    search = request.args.get('term')
    app.logger.debug("In main.py inverted_index(), the search term is :" + search)
    return Response(json.dumps(ac_inverted_index(search)), mimetype='application/json')

	
@app.route('/')
def index():
    return render_template("search.html")

if __name__ == '__main__':
    app.run(debug=True)