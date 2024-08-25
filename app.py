from flask import Flask, request, jsonify, send_file, render_template, render_template_string
import os
import sqlite3

app = Flask(__name__)

# Database initialization
def init_db():
    conn = sqlite3.connect('reviews.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS reviews
                 (id INTEGER PRIMARY KEY, first_name TEXT, last_name TEXT, age INTEGER, gender TEXT, comment TEXT)''')
    conn.commit()
    conn.close()

# Serve the main comment.html page
@app.route('/')
def index():
    return send_file('comment.html')

# Route to handle the form submission
@app.route('/submit_review', methods=['POST'])
def submit_review():
    try:
        data = request.get_json()
        print("Received data:", data)

        first_name = data.get('first_name')
        last_name = data.get('last_name')
        age = data.get('age')
        gender = data.get('gender')
        comment = data.get('comment')

        if not first_name or not last_name or not age or not gender or not comment:
            print("Missing data fields")
            return jsonify({'success': False, 'message': 'All fields are required'}), 400

        conn = sqlite3.connect('reviews.db')
        c = conn.cursor()
        c.execute("INSERT INTO reviews (first_name, last_name, age, gender, comment) VALUES (?, ?, ?, ?, ?)",
                  (first_name, last_name, age, gender, comment))
        conn.commit()
        conn.close()

        return jsonify({'success': True})

    except Exception as e:
        print("Error occurred:", e)
        return jsonify({'success': False, 'message': 'Internal Server Error'}), 500

# Route to serve the reviews.html file
@app.route('/reviews')
def reviews_page():
    return send_file('reviews.html')

# API endpoint to get reviews data in JSON format
@app.route('/get_reviews')
def get_reviews():
    conn = sqlite3.connect('reviews.db')
    c = conn.cursor()
    c.execute("SELECT first_name, last_name, age, gender, comment FROM reviews")
    reviews = c.fetchall()
    conn.close()

    reviews_list = [
        {"first_name": review[0], "last_name": review[1], "age": review[2], "gender": review[3], "comment": review[4]}
        for review in reviews
    ]
    return jsonify(reviews_list)

if __name__ == '__main__':
    init_db()
    app.run(debug=True, use_reloader=False)
