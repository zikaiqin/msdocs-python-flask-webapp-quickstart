import os
from flask import (
    Flask, redirect, render_template, request,
    send_from_directory, url_for
)

from database import DataBase

database = DataBase()
app = Flask(__name__)

@app.route('/')
def index():
    print('Request for index page received')
    return render_template('index.html')

@app.route('/favicon.ico')
def favicon():
    return send_from_directory(
        os.path.join(app.root_path, 'static'),
        'favicon.ico',
        mimetype='image/vnd.microsoft.icon'
    )

@app.route('/hello', methods=['POST'])
def hello():
    name = request.form.get('name')

    if name:
        print('Request for hello page received with name=%s' % name)

        sql_count = "SELECT COUNT(*) AS count FROM Visit WHERE visitor_name=?; "
        sql_insert = "INSERT INTO Visit(visitor_name) VALUES (?); "

        with database.connect() as connection:
            cur = connection.cursor()
            cur.execute(sql_insert + sql_count, (name,) * 2)

            cur.nextset()
            count = cur.fetchall()[0][0]

            greeting = 'Welcome back' if count > 1 else 'Hello'
            message = (
                f"You've visited us {count} times!" if count > 1 else
                'It is nice to meet you!'
            )
            return render_template('hello.html', name = name, greeting = greeting, message = message)

    else:
        print('Request for hello page received with no name or blank name -- redirecting')
        return redirect(url_for('index'))


if __name__ == '__main__':
    app.run()
