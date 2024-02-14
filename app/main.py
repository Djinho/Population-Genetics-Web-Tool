from flask import Flask, request, render_template, jsonify, g, redirect, url_for, session
from flask_session import Session
import sqlite3
import os
from io import BytesIO
import base64
import numpy as np
import seaborn as sns
import pandas as pd
import re
import matplotlib
matplotlib.use('Agg')  # Configure matplotlib to use the Agg backend for generating plots
import matplotlib.pyplot as plt

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

@app.route('/get_populations')
def get_populations():
    db = get_db()
    cursor = db.execute('SELECT PopulationID, PopulationName FROM Populations')
    populations = cursor.fetchall()
    return jsonify([{'PopulationID': population['PopulationID'], 'PopulationName': population['PopulationName']} for population in populations])



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
    FROM pca_coordinates AS c
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


@app.route('/analyze_admixture', methods=['POST'])
def analyze_admixture():
    data = request.get_json()
    selected_populations = data['populations']
    db = get_db()
    cursor = db.cursor()
    
    # SQL query to fetch admixture data for selected populations
    placeholder = ','.join('?' for _ in selected_populations)
    query = f'''
    SELECT p.PopulationName, a.ancestry_1, a.ancestry_2, a.ancestry_3, a.ancestry_4, a.ancestry_5
    FROM admixture_results AS a
    JOIN populations AS p ON a.PopulationID = p.PopulationID
    WHERE a.PopulationID IN ({placeholder})
    '''
    
    cursor.execute(query, selected_populations)
    rows = cursor.fetchall()
    
    # Convert the rows to the correct Plotly structure
    plot_data = []
    ancestries = ['ancestry_1', 'ancestry_2', 'ancestry_3', 'ancestry_4', 'ancestry_5']
    colors = ['rgba(222,45,38,0.8)', 'rgba(204,204,204,1)', 'rgba(62,150,81,0.8)', 'rgba(107,76,154,0.8)', 'rgba(37,37,37,0.8)']
    
    for i, ancestry in enumerate(ancestries):
        trace = {
            'x': [row['PopulationName'] for row in rows],
            'y': [row[ancestry] for row in rows],
            'type': 'bar',
            'name': f'Ancestry {i+1}',
            'marker': {'color': colors[i]}
        }
        plot_data.append(trace)
    
    return jsonify(plot_data)
def analyze_admixture():
    data = request.get_json()
    selected_populations = data['populations']
    db = get_db()
    cursor = db.cursor()
    
    # SQL query to fetch admixture data for selected populations
    query = '''
    SELECT a.PopulationID, p.PopulationName, a.ancestry_1, a.ancestry_2, a.ancestry_3, a.ancestry_4, a.ancestry_5
    FROM admixture_results AS a
    JOIN populations AS p ON a.PopulationID = p.PopulationID
    WHERE a.PopulationID IN ({})
    '''.format(','.join('?' for _ in selected_populations))
    
    cursor.execute(query, selected_populations)
    rows = cursor.fetchall()
    
    # Prepare data for Plotly
    plot_data = [{
        'x': [row['PopulationName'] for row in rows],
        'y': [[row[f'ancestry_{i+1}'] for row in rows] for i in range(5)],
        'type': 'bar',
        'name': 'Ancestry',
        'marker': {
            'color': ['rgba(222,45,38,0.8)', 'rgba(204,204,204,1)', 'rgba(62,150,81,0.8)', 'rgba(107,76,154,0.8)', 'rgba(37,37,37,0.8)']
        }
    }]
    
    return jsonify(plot_data)

    data = request.get_json()
    selected_populations = data['populations']
    db = get_db()
    cursor = db.cursor()
    
    # SQL query to fetch admixture data for selected populations
    query = '''
    SELECT a.PopulationID, p.PopulationName, a.ancestry_1, a.ancestry_2, a.ancestry_3, a.ancestry_4, a.ancestry_5
    FROM admixture_results AS a
    JOIN populations AS p ON a.PopulationID = p.PopulationID
    WHERE a.PopulationID IN ({})
    '''.format(','.join('?' for _ in selected_populations))
    
    cursor.execute(query, selected_populations)
    rows = cursor.fetchall()
    
    # Prepare data for Plotly
    plot_data = {
        'x': [],
        'y': [[] for _ in range(5)],  # Create empty lists for each ancestry
        'type': 'bar',
        'name': 'Ancestry',
        'marker': {'color': ['rgba(20, 20, 20, 0.6)', 'rgba(60, 60, 60, 0.6)', 'rgba(100, 100, 100, 0.6)', 'rgba(140, 140, 140, 0.6)', 'rgba(180, 180, 180, 0.6)']},
    }
    
    for row in rows:
        plot_data['x'].append(row['PopulationName'])
        for i in range(5):
            plot_data['y'][i].append(row[f'ancestry_{i+1}'])
    
    return jsonify([plot_data])

#def plot_admixture(ancestry_data):
    fig, ax = plt.subplots(figsize=(10, 5))  # Adjust the size as needed

    # Width of the bars: can also be len(x) sequence
    bar_width = 0.4

    indices = np.arange(len(ancestry_data))

    bottom = np.zeros(len(ancestry_data))

    colors = ['red', 'green', 'blue', 'yellow', 'purple']  # Adjust the number of colors as needed

    for i, row in enumerate(ancestry_data):
        for j, ancestry in enumerate(row[1:]):  # Skip the PopulationID
            ax.bar(indices[i], ancestry, bar_width, bottom=bottom[i], color=colors[j])
            bottom[i] += ancestry

    ax.set_xlabel('Samples')
    ax.set_ylabel('Ancestry Proportion')
    ax.set_title('Admixture Plot')
    ax.set_xticks(indices)
    ax.set_xticklabels([row['PopulationID'] for row in ancestry_data], rotation=90)

    ax.legend(['Ancestry 1', 'Ancestry 2', 'Ancestry 3', 'Ancestry 4', 'Ancestry 5'])

    buf = BytesIO()
    plt.savefig(buf, format='png', bbox_inches='tight')
    plt.close()
    buf.seek(0)

    plot_url = base64.b64encode(buf.getvalue()).decode('utf-8')
    
    return 'data:image/png;base64,' + plot_url


@app.route('/download_heatmap', methods=['POST'])
def download_heatmap():
    data = request.get_json()
    selected_populations = data['populations']
    # Your logic to fetch the heatmap data and generate the plot...
    # After generating the plot:
    buf = BytesIO()
    plt.savefig(buf, format='png')
    plt.close()
    buf.seek(0)
    return send_file(
        buf,
        as_attachment=True,
        attachment_filename='heatmap.png',
        mimetype='image/png'
    )





@app.route('/generate_heatmap_data', methods=['POST'])
def generate_heatmap_data():
    data = request.get_json()
    selected_populations = data['populations']
    db = get_db()
    cursor = db.cursor()

    # SQL query to fetch admixture data for selected populations
    placeholders = ','.join(['?'] * len(selected_populations))
    query = f'''
    SELECT p.PopulationName, a.ancestry_1, a.ancestry_2, a.ancestry_3, a.ancestry_4, a.ancestry_5
    FROM admixture_results AS a
    JOIN populations AS p ON a.PopulationID = p.PopulationID
    WHERE a.PopulationID IN ({placeholders})
    '''
    cursor.execute(query, selected_populations)
    rows = cursor.fetchall()

    # Transpose the rows to a format suitable for a heatmap (2D list)
    heatmap_data = [[row[ancestry] for row in rows] for ancestry in ['ancestry_1', 'ancestry_2', 'ancestry_3', 'ancestry_4', 'ancestry_5']]

    # Convert the data to a DataFrame for Seaborn
    df = pd.DataFrame(heatmap_data, columns=[row['PopulationName'] for row in rows], index=['Ancestry 1', 'Ancestry 2', 'Ancestry 3', 'Ancestry 4', 'Ancestry 5'])

    # Generate the heatmap
    plt.figure(figsize=(10, 8))
    sns.heatmap(df, annot=True, fmt=".2f", linewidths=.5, cmap='viridis')
    plt.title('Admixture Heatmap')

    # Save the plot to a BytesIO buffer
    buf = BytesIO()
    plt.savefig(buf, format='png', bbox_inches='tight')
    plt.close()
    buf.seek(0)

    # Encode the image to base64 string
    heatmap_image = base64.b64encode(buf.getvalue()).decode('utf8')

    # Return the base64-encoded image
    return jsonify({'heatmap_image': 'data:image/png;base64,' + heatmap_image})



def generate_base64_image():
    buf = BytesIO()
    plt.figure()
    plt.plot([1, 2, 3], [4, 5, 6])  # Example plot
    plt.title("Example Plot")
    plt.savefig(buf, format='png')
    plt.close()
    image_base64 = base64.b64encode(buf.getvalue()).decode('utf-8')
    return image_base64
# Example route to display the plot
@app.route('/plot')
def plot():
    image_base64 = generate_base64_image()
    return render_template('plot.html', image_base64=image_base64)

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




def plot_admixture_heatmap(ancestry_data):
    # Convert data to a DataFrame for easier manipulation
    df = pd.DataFrame(ancestry_data).set_index('population_name')

    # Set up the heatmap figure
    plt.figure(figsize=(10, 6))

    # Plot the heatmap using Seaborn
    sns.heatmap(df.transpose(), cmap='viridis', annot=True, fmt=".3f", cbar_kws={'label': 'Ancestry Proportion'})

    # Customize labels and title
    plt.xlabel('Population')
    plt.ylabel('Ancestry Components')
    plt.title('Admixture Heatmap')

    # Save the plot to a BytesIO buffer
    buf = BytesIO()
    plt.savefig(buf, format='png', bbox_inches='tight')
    plt.close()
    buf.seek(0)

    # Convert the plot to a base64-encoded string
    plot_url = base64.b64encode(buf.getvalue()).decode('utf-8')

    return 'data:image/png;base64,' + plot_url


# Start the Flask application
if __name__ == '__main__':
    app.run(debug=True)
