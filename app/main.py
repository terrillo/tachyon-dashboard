from flask import Flask, Blueprint, request, Response, render_template
import os

from data import *

app = Flask(__name__)
app.config['TEMPLATES_AUTO_RELOAD'] = True

# Before * request
@app.before_request
def before_request():
    connection.connect()
    app.jinja_env.cache = {}

# After * reqeust
@app.after_request
def after_request(response):
    try:
        connection.close()
    except:
        pass
    return response

# Index
@app.route('/<month>-<year>', methods=['GET'])
def app_index(month, year):
    this_month = query("SELECT count(*) as 'count' FROM cb_search_data WHERE MONTH(timestamp) = %s AND YEAR(timestamp) = %s LIMIT 10" % (month, year))[0]['count']
    last_month = query("SELECT count(*) as 'count' FROM cb_search_data WHERE MONTH(timestamp) = %s AND YEAR(timestamp) = %s LIMIT 10" % ((int(month)-1), year))[0]['count']
    queries = {
        'this_month': this_month,
        'last_month': last_month,
        'users': query("SELECT email FROM user_core LIMIT 10")
    }

    return render_template('index.html', queries=queries)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=80)
