from flask import Flask, flash, render_template, redirect, url_for, request, session
from module.database import Database
from controller.IndexController import IndexController

app = Flask(__name__)
app.secret_key = "1b3405de8159fc67675f3bbb"
db = Database()
IndexController = IndexController()


@app.route('/', methods = ['GET'])
def index_contact():
    data = IndexController.index(db)
    return render_template('index.html', data=data)


@app.route('/add/')
def add():
    return render_template('add.html')

@app.route('/add_contact', methods = ['POST', 'GET'])
def add_contact():
    if request.method == 'POST' and request.form['save']:
        if db.insert(request.form):
            flash("A new phone number has been added")
        else:
            flash("A new phone number can not be added")

        return redirect(url_for('index_contact'))
    else:
        return redirect(url_for('index_contact'))

@app.route('/update_contact_get/<int:id>/')
def update_contact_get(id):
    data = db.read(id)

    if len(data) == 0:
        return redirect(url_for('index_contact'))
    else:
        session['update'] = id
        return render_template('update.html', data = data)

@app.route('/update_contact_post', methods = ['POST'])
def update_contact_post():
    if request.method == 'POST' and request.form['update']:

        if db.update(session['update'], request.form):
            flash('A phone number has been updated')

        else:
            flash('A phone number can not be updated')

        session.pop('update', None)

        return redirect(url_for('index_contact'))
    else:
        return redirect(url_for('index_contact'))

@app.route('/delete_contact_get/<int:id>/')
def delete_contact_get(id):
    data = db.read(id)

    if len(data) == 0:
        return redirect(url_for('index_contact'))
    else:
        session['delete'] = id
        return render_template('delete.html', data = data)

@app.route('/delete_contact_post', methods = ['POST'])
def delete_contact_post():
    if request.method == 'POST' and request.form['delete']:

        if db.delete(session['delete']):
            flash('A phone number has been deleted')

        else:
            flash('A phone number can not be deleted')

        session.pop('delete', None)

        return redirect(url_for('index_contact'))
    else:
        return redirect(url_for('index_contact'))

@app.errorhandler(404)
def page_not_found(error):
    return render_template('error.html')

if __name__ == '__main__':
    app.run(port=5061, host="0.0.0.0", debug=True)