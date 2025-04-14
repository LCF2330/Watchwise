from flask import Flask, render_template, request, redirect, url_for, session
from utils.dynamo import get_items, get_item, add_item, update_item, delete_item
from utils.auth import validate_user

app = Flask(__name__)
app.secret_key = 'some-super-secret-key'

@app.route('/')
def watchlist():
    if 'user_id' not in session:
        return redirect(url_for('login'))

    user_id = session['user_id']
    items = get_items(user_id)
    return render_template('watchlist.html', items=items)

@app.route('/add', methods=['GET', 'POST'])
def add():
    if 'user_id' not in session:
        return redirect(url_for('login'))

    user_id = session['user_id']

    if request.method == 'POST':
        title = request.form['title']
        genre = request.form['genre']
        rating = request.form['rating']
        watched = 'watched' in request.form
        add_item(user_id, title, genre, rating, watched)
        return redirect(url_for('watchlist'))

    return render_template('add.html')

@app.route('/update/<title>', methods=['GET', 'POST'])
def update(title):
    if 'user_id' not in session:
        return redirect(url_for('login'))

    user_id = session['user_id']
    item = get_item(user_id, title)

    if item is None:
        return "Item not found", 404

    if request.method == 'POST':
        new_title = request.form['title']
        genre = request.form['genre']
        rating = request.form['rating']
        watched = 'watched' in request.form
        update_item(user_id, title, new_title, genre, rating, watched)
        return redirect(url_for('watchlist'))

    return render_template('update.html', item=item)

@app.route('/delete/<title>', methods=['POST'])
def delete(title):
    if 'user_id' not in session:
        return redirect(url_for('login'))

    user_id = session['user_id']
    item = get_item(user_id, title)

    if item is None:
        return "Item not found", 404

    delete_item(user_id, title)
    return redirect(url_for('watchlist'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        if validate_user(email, password):
            session['user_id'] = email
            return redirect(url_for('watchlist'))
        return render_template('invalid_login.html')
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('user_id', None)
    return redirect(url_for('login'))

if __name__ == "__main__":
    app.run(debug=True)