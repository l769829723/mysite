# -*- coding:utf8 -*-
# all the imports
import json
import os
import time

from flask import Flask, request, g, redirect, session
from flask import url_for, abort, render_template, flash, jsonify

from database.models import Entries
from database.config import db_session

# configurations
BASE_DIR = os.path.split(os.path.abspath(__file__))[0]
DEBUG = True
SECRET_KEY = 'development key'
USERNAME = 'admin'
PASSWORD = 'password'

app = Flask(__name__)
app.config.from_object(__name__)


@app.template_filter('locate_time')
def locate_time(time_stamp):
    local = time.localtime(time_stamp)
    return time.strftime('%Y-%m-%d %H:%M:%S', local)


app.jinja_env.filters['locate_time'] = locate_time


# Close database connection on request later
@app.teardown_appcontext
def shutdown_session(exception=None):
    db_session.remove()

@app.route('/add', methods=['POST'])
def add_entry():
    if not session.get('logged_in'):
        abort(404)
    g.db.execute('insert into entries (title, text) values (?, ?)',
                 [request.form['title'], request.form['text']])
    g.db.commit()
    flash('New entry was successfully posted')
    return redirect(url_for('show_entries'))


@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        if request.form['username'] != app.config['USERNAME']:
            error = 'Invalid username.'
        elif request.form['password'] != app.config['PASSWORD']:
            error = 'Invalid password'
        else:
            session['logged_in'] = True
            flash('You are logged in.')
            return redirect(url_for('home'))
    return render_template('login.html', error=error)


@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    flash('You are logged out.')
    return redirect(url_for('home'))


@app.route('/css_three')
def css_three():
    return render_template('studyhtml/css3.html')


# api
@app.route('/api')
def api():
    abort(404)


@app.route('/api/entries')
def entries():
    page = int(request.args.get('page', 0))
    limit = 20
    limits = limit + page * limit
    last_page = False
    last_num = Entries.query.order_by(Entries.id.desc()).first().id
    if (last_num // page - 20) <= 0:last_page = True
    app.logger.debug("*** The current limits: %d, page: %d . ***" % (limits, page))
    entries = Entries.query.order_by(Entries.stamp.desc()).limit(limits).all()
    entry_list = [{'title': entry.title, 'text': entry.text, 'stamp': entry.stamp} for entry in entries]
    return jsonify({'entries': entry_list, 'last_page': last_page})

@app.route('/api/entries/<title>')
def updated(title):
    error = ''
    entry_list = []
    if title != '':
        last_id = Entries.query.filter(Entries.title == title).order_by(Entries.id.desc()).first().id
        entries = Entries.query.offset(last_id).all()
        entry_list = [{'title': entry.title, 'text': entry.text, 'stamp': entry.stamp} for entry in entries]
    else:
        error = 'No updated record.'
    return jsonify({'entries': entry_list, 'error': error})

@app.route('/home')
def home():
    entries_query = Entries.query.order_by(Entries.id.desc()).limit(20).all()
    entries = [
        {'title': entry.title, 'text': entry.text, 'stamp': entry.stamp.strftime('%Y-%m-%d %H:%M')} for entry in entries_query
    ]
    return render_template('show_entries.html', entries=entries)


if __name__ == '__main__':
    app.run(host='0.0.0.0')
