from flask import Flask, render_template, request, redirect, url_for
from utils import dynamo

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/watchlist')
def watchlist():
    user_id = 'some_user_id' 
    items = dynamo.get_items(user_id) 
    return render_template('watchlist.html', items=items)


@app.route('/add_to_watchlist', methods=['POST'])
def add_to_watchlist():
    if request.method == 'POST':
        user_id = request.form['user_id']
        item_id = request.form['item_id']
        title = request.form['title']
        genre = request.form['genre']
        rating = request.form['rating']

        # Add item to DynamoDB
        dynamo.add_item(user_id, item_id, title, genre, rating)
        return redirect(url_for('watchlist'))  # Redirect to watchlist after adding

if __name__ == '__main__':
    app.run(debug=True)
