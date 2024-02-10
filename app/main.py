from flask import Flask, request, render_template, g, redirect, url_for, session
from flask_session import Session
import sqlite3
import os
import matplotlib.pyplot as plt
from io import BytesIO
import base64

# Configure the Flask app
app = Flask(__name__)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Get the parent directory of this file
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATABASE = os.path.join(BASE_DIR, '..', 'sql', 'PopulationGeneticsDB.sqlite')

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

@app.route('/analysis_tools/snp')
def snp_analysis_form():
    db = get_db()
    if db is None:
        return "Error: Unable to connect to the database."
    cursor = db.execute('SELECT PopulationID, PopulationName, is_Superpopulation FROM Populations ORDER BY PopulationName')
    populations = cursor.fetchall()
    return render_template('snp_analysis_form.html', populations=populations)

# Define route for SNP analysis results (New Feature)
@app.route('/analyze_snp', methods=['POST'])
def snp_analysis_results():
    snp_id = request.form['snp_id']
    gene_name = request.form['gene_name']
    genomic_coordinates = request.form['genomic_coordinates']
    population = request.form['population']
    results = {
        'snp_id': snp_id,
        'gene_name': gene_name,
        'genomic_coordinates': genomic_coordinates,
        'population': population
    }
    return render_template('snp_results.html', results=results)

# Define route for PCA description page
@app.route('/analysis_tools/pca_description')
def pca_description():
    return render_template('pca_description.html')

# Define route for SNP description page (Added as per your snippet)
@app.route('/analysis_tools/snp_description')
def snp_description():
    # Logic to fetch SNP description data (if necessary)
    # ...
    return render_template('snp_description.html')

# Define route for Admixture description page
@app.route('/analysis_tools/admixture_description')
def admixture_description():
    return render_template('admixture_description.html')

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
    session['results'] = results  # Store the results in the session
    return redirect(url_for('display_results'))

# Define route for displaying PCA results
@app.route('/results')
def display_results():
    results = session.get('results', None)
    if results is None:
        return "Error: No results data provided."
    plot_url = plot_pca(results)
    return render_template('results.html', results=results, plot_url=plot_url)

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

# Function to generate PCA plot
def plot_pca(pca_results):
    x_coords = [result['pc1'] for result in pca_results]
    y_coords = [result['pc2'] for result in pca_results]
    labels = [result['population_name'] for result in pca_results]

    plt.figure(figsize=(10, 8))
    plt.scatter(x_coords, y_coords, alpha=0.5)
    for label, x, y in zip(labels, x_coords, y_coords):
        plt.annotate(label, (x, y), textcoords="offset points", xytext=(0,10), ha='center')
    plt.title('PCA Plot')
    plt.xlabel('PC1')
    plt.ylabel('PC2')
    img = BytesIO()
    plt.savefig(img, format='png', bbox_inches='tight')
    plt.close()
    img.seek(0)
    plot_url = base64.b64encode(img.getvalue()).decode('utf8')
    return plot_url

# Add the new route for analyzing admixture, as requested
@app.route('/analyze_admixture', methods=['POST'])
def analyze_admixture():
    # Implement admixture analysis logic here
    selected_populations = request.form.getlist('populations[]')
    # Placeholder for actual analysis. Replace with your logic.
    results = "Admixture analysis results for: " + ", ".join(selected_populations)
    # Assuming 'admixture_results.html' is your result template
    return render_template('admixture_results.html', results=results)

# Start the Flask application
if __name__ == '__main__':
    app.run(debug=True)
