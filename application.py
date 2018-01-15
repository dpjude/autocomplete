from flask import Flask, Response, render_template, request, jsonify
import json,sys
#from autocomplete import complete
from autocomplete import complete


app = Flask(__name__)

	
@app.route('/autocomplete', methods=['GET', 'POST'])
def autocomplete():
    search = request.args.get('term')
    app.logger.debug(complete(search))
    return Response(json.dumps(complete(search)), mimetype='application/json')

	
@app.route('/')
def index():
    return render_template("search.html")

if __name__ == '__main__':
    app.run(debug=True)