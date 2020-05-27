import pymysql.cursors
import pymysql

connection = pymysql.connect(host='bluecello.brief.vet',
                             user='brief',
                             password='a3tBD2GQkyRDESSQ',
                             database='piranha',
                             charset='utf8mb4',
                             cursorclass=pymysql.cursors.DictCursor)

def query(sql, debug=False):
    if debug:
        print(sql)
    if 'SELECT' in sql:
        with connection.cursor() as cursor:
            cursor.execute(sql)
            result = cursor.fetchall()
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
                return True
        except:
            print("FAILED", sql)
            return True
