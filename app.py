from flask import Flask, render_template, request, redirect, url_for
from utils.dynamo import get_items, get_item, add_item, update_item, delete_item

app = Flask(__name__)

USER_ID = "some_user_id"  # Use a dynamic user ID in production

@app.route('/')
def watchlist():
    items = get_items(USER_ID)
    return render_template('watchlist.html', items=items)

@app.route('/add', methods=['GET', 'POST'])
def add():
    if request.method == 'POST':
        title = request.form['title']
        genre = request.form['genre']
        rating = request.form['rating']
        watched = 'watched' in request.form  # Checkbox for 'watched'
        add_item(USER_ID, title, genre, rating, watched)
        return redirect(url_for('watchlist'))
    return render_template('add.html')

@app.route('/update/<title>', methods=['GET', 'POST'])
def update(title):
    item = get_item(USER_ID, title)
    
    if item is None:
        return "Item not found", 404  # Item not found
    
    if request.method == 'POST':
        new_title = request.form['title']
        genre = request.form['genre']
        rating = request.form['rating']
        watched = 'watched' in request.form  # Checkbox for 'watched'

        # Update the item in the database
        update_item(USER_ID, title, new_title, genre, rating, watched)

        return redirect(url_for('watchlist'))

    return render_template('update.html', item=item)

@app.route('/delete/<title>', methods=['POST'])
def delete(title):
    item = get_item(USER_ID, title)
    
    if item is None:
        return "Item not found", 404  # Item not found
    
    # Proceed with deleting the item from the DynamoDB table
    delete_item(USER_ID, title)
    
    return redirect(url_for('watchlist'))

if __name__ == "__main__":
    app.run(debug=True)
