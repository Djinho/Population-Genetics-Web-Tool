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
#DATABASE2 = os.path.join(BASE_DIR, '..', 'sql', 'fst_matrix.db')

# Print the database paths to console (for debugging)
print("Database 1 path:", DATABASE)
#print("Database 2 path:", DATABASE2)

def get_db(database):
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(database)
        db.row_factory = sqlite3.Row
        db.execute('PRAGMA foreign_keys = ON')
        db.commit()
    return db
@app.teardown_appcontext
def close_db(error):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()
@app.route('/get_populations')
def get_populations():
    db = get_db(DATABASE)
    cursor = db.execute('SELECT PopulationID, PopulationName FROM populations')
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


# FORM PAGES 
# Define route for analysis tools selection
@app.route('/analysis_tools')
def analysis_tools():
    return render_template('analysis_selection.html')

# Define route for PCA form
@app.route('/analysis_tools/pca')
def pca_form():
    db = get_db(DATABASE)
    if db is None:
        return "Error: Unable to connect to the database."
    cursor = db.execute('SELECT PopulationID, PopulationName FROM populations')
    populations = cursor.fetchall()
    return render_template('pca_form.html', populations=populations)

# Define route for Admixture form
@app.route('/analysis_tools/admixture')
def admixture_form():
    db = get_db(DATABASE)
    if db is None:
        return "Error: Unable to connect to the database."
    cursor = db.execute('SELECT PopulationID, PopulationName FROM populations')
    populations = cursor.fetchall()
    return render_template('admixture_form.html', populations=populations)


@app.route('/analyze', methods=['POST'])
def analyze():
    selected_populations = request.form.getlist('populations[]')
    per_sample = request.form.get('perSample')  # Check if Per Sample is selected
    
    # Decide which analysis to perform based on the Per Sample checkbox
    if per_sample:
        results = perform_pca_individuals(selected_populations)
        session['results'] = results
        return redirect(url_for('display_persample_results'))
    else:
        results = perform_pca(selected_populations)
        session['results'] = results
        return redirect(url_for('display_results'))



#PCA ANALYSIS 1

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
    db = get_db(DATABASE)
    if db is None:
        return []
    placeholders = ','.join('?' for _ in selected_populations)
    query = f'''
    SELECT p.PopulationName, c.CoordinateID, c.PC1, c.PC2
    FROM pca_coordinates AS c
    JOIN populations AS p ON c.PopulationID = p.PopulationID
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

#PER SAMPLE PCA
def perform_pca_individuals(selected_populations):
    db = get_db(DATABASE)
    if db is None:
        return []
    placeholders = ','.join('?' for _ in selected_populations)
    query = f'''
    SELECT p.PopulationName, i.SampleID, i.PC1, i.PC2
    FROM individual_pca_coordinates AS i
    JOIN populations AS p ON i.PopulationID = p.PopulationID
    WHERE i.PopulationID IN ({placeholders})
    '''
    cursor = db.execute(query, selected_populations)
    pca_data = cursor.fetchall()
    return [{'population_name': row['PopulationName'], 'sample_id': row['SampleID'], 'pc1': row['PC1'], 'pc2': row['PC2']} for row in pca_data]


#DISPLAY PER SAMPLE RESULTS 
@app.route('/results_persample')
def display_persample_results():
    results = session.get('results', None)
    if results is None:
        return "Error: No results data provided."
    plot_url = plot_pca_individuals(results)  # Ensure you modify the plotting function to handle individual results
    return render_template('Per_sample_pca.html', results=results, plot_url=plot_url)



#PLOT PCA FOR SAMPLES 
def plot_pca_individuals(pca_results):
    # Assuming pca_results includes a 'population_name' for each sample
    populations = list(set([result['population_name'] for result in pca_results]))
    # Assign a unique color to each population
    colors = plt.cm.rainbow(np.linspace(0, 1, len(populations)))
    population_color_map = dict(zip(populations, colors))
    
    plt.figure(figsize=(10, 8))
    for result in pca_results:
        x = result['pc1']
        y = result['pc2']
        population = result['population_name']
        plt.scatter(x, y, alpha=0.5, label=population, color=population_color_map[population])
    
    # Create a legend with population labels
    handles, labels = plt.gca().get_legend_handles_labels()
    by_label = dict(zip(labels, handles))  # Eliminate duplicate labels
    plt.legend(by_label.values(), by_label.keys(), title="Populations")
    
    plt.title('PCA Plot for Individual Samples')
    plt.xlabel('PC1')
    plt.ylabel('PC2')
    
    img = BytesIO()
    plt.savefig(img, format='png', bbox_inches='tight')
    plt.close()
    img.seek(0)
    plot_url = base64.b64encode(img.getvalue()).decode('utf8')
    return plot_url



#ADMIXTURE ANALYSIS 2 
@app.route('/analyze_admixture', methods=['POST'])
def analyze_admixture():
    data = request.get_json()
    selected_populations = data['populations']
    db = get_db(DATABASE)
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



# FST ANALYSIS 3 
@app.route('/fst_calculator', methods=['GET', 'POST'])
def calculate_fst():
    if request.method == 'POST':
        population1 = request.form.get('population1')
        population2 = request.form.get('population2')
        
        db = get_db(DATABASE2)
        cur = db.cursor()
        cur.execute('SELECT fst_value FROM fst_data WHERE population1 = ? AND population2 = ? UNION ALL SELECT fst_value FROM fst_data WHERE population1 = ? AND population2 = ?', (population1, population2, population2, population1))
        fst_value = cur.fetchone()
        
        if fst_value:
            fst_value = fst_value['fst_value']
        else:
            fst_value = 'Not Found'
        
        cur.execute('SELECT DISTINCT population1 FROM fst_data')
        populations = [row['population1'] for row in cur.fetchall()]
        
        return render_template('fst_calculator.html', populations=populations, fst_value=fst_value, population1=population1, population2=population2)
    else:
        db = get_db(DATABASE2)
        cur = db.cursor()
        cur.execute('SELECT DISTINCT population1 FROM fst_data')
        populations = [row['population1'] for row in cur.fetchall()]
        
        return render_template('fst_calculator.html', populations=populations, fst_value=None)
    

# SNP ANALAYSIS 4
@app.route('/autocomplete/gene_names')
def autocomplete_gene_names():
    query = request.args.get('term', '')  # 'term' is a common query parameter used by jQuery UI Autocomplete
    db = get_db(DATABASE)
    cursor = db.cursor()
    cursor.execute("SELECT DISTINCT GeneName FROM SNP_Data WHERE GeneName LIKE ?", (f'%{query}%',))
    results = cursor.fetchall()
    gene_names = [result['GeneName'] for result in results]
    return jsonify(gene_names)
@app.route('/analysis_tools/snp', methods=['GET', 'POST'])
@app.route('/snp-analysis', methods=['GET', 'POST'])
def snp_analysis():
    db = get_db(DATABASE)
    cursor = db.cursor()

    populations = ['AFR', 'AMR', 'EAS', 'EUR', 'SAS', 'ACB', 'ASW', 'BEB', 'CDX', 'CEU', 'CHB', 'CHS', 'CLM', 'ESN', 'FIN', 'GBR', 'GIH', 'GWD', 'IBS', 'ITU', 'JPT', 'KHV', 'LWK', 'MSL', 'MXL', 'PEL', 'PJL', 'PUR', 'SIB', 'STU', 'TSI', 'YRI']
    if request.method == 'POST':
        selected_snps = request.form.getlist('selected_snps[]')
        selected_populations = request.form.getlist('selected_populations[]')

        if not selected_populations:
            return "No population selected", 400

        # Base query with all the static columns

        base_query = """
            SELECT SNPID, GeneName, Chromosome, Position, ID, REF, ALT, GeneType,
                   ClinicalSignificance, ExonicFunction, DistanceToAdjacentGenes
        """
       
        # Add dynamic selection for frequency columns
        frequency_columns = ', '.join(f"{pop}_Frequency" for pop in selected_populations)
        query = f"{base_query}, {frequency_columns} FROM SNP_Data WHERE ID IN ({','.join(['?'] * len(selected_snps))})"
        cursor.execute(query, selected_snps)
        results = cursor.fetchall()

        # Convert the results into a list of dictionaries
        columns = [desc[0] for desc in cursor.description]
        snp_data_dicts = [dict(zip(columns, row)) for row in results]

        return render_template('snp_results.html', snp_data=snp_data_dicts, selected_populations=selected_populations)
    else:
        # Fetching initial SNP data for display
        cursor.execute('SELECT Position, ID, GeneName FROM SNP_Data')
        snp_data = cursor.fetchall()
        snp_data_dicts = [{col[0]: value for col, value in zip(cursor.description, row)} for row in snp_data]

        return render_template('snp_analysis.html', snp_data=snp_data_dicts, populations=populations)


 #ABOUT PAGES

 # Define route for PCA description page
@app.route('/analysis_tools/pca_description')



# DESCRIPTION PAGES AND EXTRAS 
# Define route for PCA description page
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





# Start the Flask application
if __name__ == '__main__':
    app.run(debug=True)

