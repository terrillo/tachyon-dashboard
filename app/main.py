from flask import Flask, Blueprint, request, Response, render_template
import os

import pymysql.cursors
import pymysql

connection = pymysql.connect(host='bluecello.brief.vet',
                             user='brief',
                             password='a3tBD2GQkyRDESSQ',
                             database='piranha',
                             charset='utf8mb4',
                             cursorclass=pymysql.cursors.DictCursor)

def query(sql, debug=False):
    connection.connect()
    if debug:
        print(sql)
    if 'SELECT' in sql:
        with connection.cursor() as cursor:
            cursor.execute(sql)
            result = cursor.fetchall()
            connection.close()
        return result
    else:
        try:
            with connection.cursor() as cursor:
                if isinstance(sql, list):
                    for q in sql:
                        cursor.execute(q)
                else:
                    cursor.execute(sql)
                connection.commit()
                connection.close()
                return True
        except:
            print("FAILED", sql)
            connection.close()
            return True

app = Flask(__name__)

# Index
@app.route('/<month>-<year>', methods=['GET'])
def app_index(month, year):
    this_month = query("SELECT count(*) as 'count' FROM cb_pageviews WHERE MONTH(created) = %s AND YEAR(created) = %s LIMIT 10" % (month, year))[0]['count']
    last_month = query("SELECT count(*) as 'count' FROM cb_pageviews WHERE MONTH(created) = %s AND YEAR(created) = %s LIMIT 10" % ((int(month)-1), year))[0]['count']
    queries = {
        'this_month': this_month,
        'last_month': last_month,
        'users': query("SELECT email FROM user_core LIMIT 10")
    }

    return render_template('index.html', queries=queries)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=80)
