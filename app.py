from flask import Flask, render_template, request, jsonify
import sqlite3
from flask_cors import CORS


def dict_fact(cursor, row):
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
        return d


def init_db():
    connection = sqlite3.connect('database.db')
    print("sucessfuly opened database")
    connection.execute('CREATE TABLE IF NOT EXISTS accounts (id INTEGER PRIMARY KEY AUTOINCREMENT, fname TEXT, '
                       'uname TEXT, passw TEXT, email TEXT )')
    print('succesfully open table')


init_db()
app = Flask(__name__)
CORS(app)


@app.route('/add-now/', methods=['POST'])
def add_now():
    if request.method == "POST":
        post_data = request.get_json()
        fname = post_data['fname']
        uname = post_data['uname']
        passw = post_data['passw']
        email = post_data['email']
        print(fname, uname, passw, email)
        try:
            with sqlite3.connect('database.db') as con:
                cur = con.cursor()
                cur.execute("INSERT INTO accounts (fname, uname , passw, email) VALUES (?, ?, ?, ?)",
                            (fname, uname, passw, email))
                cur.execute("INSERT INTO admin (uname, passw) VALUES ('admin','admin')",
                            (uname, passw))
                con.commit()
                message = fname + "successfully created account"
        except Exception as e:
            con.rollback()
            message = "Error occured in insert operation:" + str(e)
        finally:
            return jsonify(msg=message)


@app.route('/show-record/', methods=['GET'])
def list_users():
    rows = []
    #if request.method == GET:
    try:
        with sqlite3.connect('database.db') as con:
            con.row_factory = dict_fact
            cur = con.cursor()
            cur.execute("SELECT * FROM accounts")
            con.commit()
            rows = cur.fetchall()

    except Exception as e:
        print("Something happened when getting data from db:" + str(e))

    finally:
        con.close()
        return jsonify(rows)


if __name__ == '__main__':
    app.run(debug=True)
