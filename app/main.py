from flask import Flask, request, render_template, g, redirect, url_for, session
from flask_session import Session  # Make sure to install Flask-Session
import sqlite3
import os

app = Flask(__name__)
# Configure the Flask app to use filesystem-based sessions
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Get the parent directory of this file
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
# The database file should be in the 'sql' folder, one level up from the base directory
DATABASE = os.path.join(BASE_DIR, '..', 'sql', 'PopulationGeneticsDB.sqlite')

print("DATABASE path:", DATABASE)

# Function to get a database connection
def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
        db.row_factory = sqlite3.Row
        db.execute('PRAGMA foreign_keys = ON')
        db.commit()
    return db

# Function to close the database connection
@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()

# Define route for the main page
@app.route('/')
def index():
    return render_template('index.html')

# Define route for analysis tools selection
@app.route('/analysis_tools')
def analysis_tools():
    return render_template('analysis_selection.html')

# Define route for PCA form
@app.route('/analysis_tools/pca')
def pca_form():
    db = get_db()
    if db is None:
        return "Error: Unable to connect to the database."
    cursor = db.execute('SELECT PopulationID, PopulationName FROM Populations')
    populations = cursor.fetchall()
    return render_template('pca_form.html', populations=populations)

# Define route for Admixture form
@app.route('/analysis_tools/admixture')
def admixture_form():
    db = get_db()
    if db is None:
        return "Error: Unable to connect to the database."
    cursor = db.execute('SELECT PopulationID, PopulationName FROM Populations')
    populations = cursor.fetchall()
    return render_template('admixture_form.html', populations=populations)

# Define route for tutorials
@app.route('/tutorials')
def tutorials():
    return render_template('tutorials.html')

# Define route for about page
@app.route('/about')
def about():
    return render_template('about.html')

# Define route for contact page
@app.route('/contact')
def contact():
    return render_template('contact.html')

# Define route for analysis request
@app.route('/analyze', methods=['POST'])
def analyze():
    selected_populations = request.form.getlist('populations[]')
    results = perform_pca(selected_populations)
    # Store the results in the session
    session['results'] = results
    return redirect(url_for('display_results'))

# Define route for displaying results
@app.route('/results')
def display_results():
    # Retrieve the results from the session
    results = session.get('results', None)
    if results is None:
        return "Error: No results data provided."
    return render_template('results.html', results=results)

# Function to perform PCA analysis
def perform_pca(selected_populations):
    db = get_db()
    if db is None:
        return []
    placeholders = ','.join('?' for _ in selected_populations)
    query = f'''
    SELECT p.PopulationName, c.CoordinateID, c.PC1, c.PC2
    FROM PCACoordinates AS c
    JOIN Populations AS p ON c.PopulationID = p.PopulationID
    WHERE c.PopulationID IN ({placeholders})
    '''
    cursor = db.execute(query, selected_populations)
    pca_data = cursor.fetchall()
    return [{'population_name': row['PopulationName'], 'coordinate_id': row['CoordinateID'], 'pc1': row['PC1'], 'pc2': row['PC2']} for row in pca_data]

# Start the Flask application
if __name__ == '__main__':
    app.run(debug=True)
