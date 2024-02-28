from flask import Flask, request, render_template, jsonify, g, redirect, url_for, session, send_from_directory
from flask_session import Session
from werkzeug.utils import secure_filename
import sqlite3
import os
from io import BytesIO
import base64
import numpy as np
import seaborn as sns
import pandas as pd
from itertools import combinations
import re
import matplotlib
matplotlib.use('Agg')  # Configure matplotlib to use the Agg backend for generating plots
import matplotlib.pyplot as plt
import plotly
import plotly.express as px
import json
import tempfile
from flask import send_file
import uuid
import plotly.graph_objects as go
# Configure the Flask app
app = Flask(__name__)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Get the parent directory of this file
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATABASE = os.path.join(BASE_DIR, '..', 'sql', 'PopulationGeneticsDB.sqlite')
#DATABASE2 = os.path.join(BASE_DIR, '..', 'sql', 'fst_matrix.db')



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


# Define route for Admixture form
@app.route('/analysis_tools/admixture')
def admixture_form():
    db = get_db(DATABASE)
    if db is None:
        return "Error: Unable to connect to the database."
    cursor = db.execute('SELECT PopulationID, PopulationName, is_Superpopulation FROM populations')
    all_populations = cursor.fetchall()
    superpopulations = [p for p in all_populations if p['is_Superpopulation'] == 1]
    regular_populations = [p for p in all_populations if p['is_Superpopulation'] == 0]
    return render_template('admixture_form.html', superpopulations=superpopulations, regular_populations=regular_populations)




#PCA ANALYSIS 1
#Define function to fetch Superpopulation data from database.
def fetch_superpopulations(db):
    # Create a cursor object from the database connection.
    # The cursor is used to execute SQL queries
    cursor = db.cursor()
    # Execute SQL query using the cursor. Selects PopulationID 
    # and PopulationName columns from the 'populations' where the 
    #'is_Superpopulation' column is set to 1, indicating true
    cursor.execute('SELECT PopulationID, PopulationName FROM populations WHERE is_Superpopulation = 1')
    # Fetch and return the results of the executed query
    return cursor.fetchall()

# Define function to fetch superpopulation data from the database 
def fetch_regular_populations(db):
    #create cursor object from the databse connection to execute SQL commands 
    cursor = db.cursor()
    # Execute an SQL query to select population IDs and names from the 'populations' table
    cursor.execute('SELECT PopulationID, PopulationName FROM populations WHERE is_Superpopulation = 0')
    # Fetch and return the results of the executed query
    return cursor.fetchall()


   
def fetch_pca_data(selected_ids, per_sample, is_superpopulation=False):
    # Connect to the database using a helper function and get a cursor object.
    db = get_db(DATABASE)
    cursor = db.cursor()
    data = [] # Intialise an empty list to store the results 
    
    # Decide which table and column to use based on whether the data should be per sample.
    if per_sample:
        table = 'individual_pca_coordinates'
        id_column = 'SampleID'
    else:
        table = 'pca_coordinates'
        id_column = 'CoordinateID'

    # Construct a condition for the query based on whether to filter by superpopulation.
    population_condition = "p.is_Superpopulation = 1" if is_superpopulation else "p.is_Superpopulation = 0"
    
    # Create a string of placeholders for the SQL query parameters.
    placeholders = ', '.join(['?'] * len(selected_ids))
    
    # Construct the SQL query string dynamically using table and column names 
    # and filter conditions. This query selects PCA coordinates and population names 
    # for the specified IDs and population type 
    query = f"""
        SELECT i.{id_column} AS id, i.pc1, i.pc2, p.PopulationName
        FROM {table} AS i
        JOIN populations AS p ON i.PopulationID = p.PopulationID
        WHERE {population_condition} AND i.PopulationID IN ({placeholders})
    """

    # Execute the query with the list of selected IDs.
    cursor.execute(query, tuple(selected_ids))
    rows = cursor.fetchall()


    #Loop through the fetched rows to construct a list og dictionaries 
    # each representing a data point.

    for row in rows:
        data_point = {
            'id': row['id'], #ID of the sample or coordinate.
            'pc1': row['pc1'], # The first principal component. 
            'pc2': row['pc2'], # The secound principal component.
            'label': row['PopulationName']
        }
        data.append(data_point)

    # Convert the list of dictionaries into a pandas DataFrame and return it 
    return pd.DataFrame(data)




# Assuming these are the variances for the first 10 principal components
pc_variances = [157.311, 49.1541, 11.4908, 8.50634, 7.14746, 5.53621, 5.33917, 5.11019, 4.98798, 4.70189]
total_variance = sum(pc_variances)
pc1_variance_percentage = (pc_variances[0] / total_variance) * 100
pc2_variance_percentage = (pc_variances[1] / total_variance) * 100
overall_variance_percentage = ((pc_variances[0] + pc_variances[1]) / total_variance) * 100


# Define function 'plot_pca' that takes data and a title for the plot plot as arguments.
def plot_pca(pca_data, title):
    
    # Check if the input PCA data is empty. If so, exit the function returning None.
    if pca_data.empty:
        return None

    # Updated the plot title to include the overall variance percentage, formatted to 2 decimal places.
    updated_title = f"{title} (Overall Variance: {overall_variance_percentage:.2f}%)"

    # Create a scatter plot using Plotly Express, plotting pc1 against pc2, coloured by 'label'.
    fig = px.scatter(
        pca_data, x='pc1', y='pc2', color='label',
        title=updated_title,  # Use the updated title here
        labels={
            # Label the axes with their respective name and variance percentages.
            'pc1': f'PC1 ({pc1_variance_percentage:.2f}%)',
            'pc2': f'PC2 ({pc2_variance_percentage:.2f}%)'
        }
    )
    # Update the layout of the plot to have specific margins 
    fig.update_layout(margin=dict(l=40, r=40, t=40, b=30))
    # Return the plot as a JSON string using Plotly's JSON encoder.
    return json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)


# Define a route for the PCA form page with results visualised.
@app.route('/pca_form_with_results')
def pca_form_with_results():
    # Connect to the database.
    db = get_db(DATABASE)

    # Fetch list of superpopulations and regular populations from the database.
    superpopulations = fetch_superpopulations(db)
    regular_populations = fetch_regular_populations(db)
    
    # Retrieve user-selected superpopulations and populations from the session,
    # defaulting to empty lists if not found.
    selected_superpopulations = session.get('selected_superpopulations', [])
    selected_populations = session.get('selected_populations', [])
    
    # Retrieve boolean flags indicating whether to perform per-sample analysis 
    # for super populations and populations, defaulting to False if not found.
    per_sample_super = session.get('per_sample_super', False)
    per_sample_pop = session.get('per_sample_pop', False)
    
    # Retrieve session-stored plots for superpopulations and populations,
    # defaulting to None if not found.
    superpop_plot = session.get('superpop_plot', None)
    pop_plot = session.get('pop_plot', None)

    # Render tand return the PCA form template, passing in all necesary data 
    # for the form fields and visualisations.
    return render_template('pca_form.html', 
                           superpopulations=superpopulations,
                           regular_populations=regular_populations,
                           selected_superpopulations=selected_superpopulations,
                           selected_populations=selected_populations,
                           per_sample_super=per_sample_super,
                           per_sample_pop=per_sample_pop,
                           superpop_plot=superpop_plot,
                           pop_plot=pop_plot)


@app.route('/analysis_tools/pca', methods=['GET', 'POST'])
def pca_form():
    db = get_db(DATABASE)
    superpopulations = db.execute('SELECT PopulationID, PopulationName FROM populations WHERE is_Superpopulation = 1').fetchall()
    regular_populations = db.execute('SELECT PopulationID, PopulationName FROM populations WHERE is_Superpopulation = 0').fetchall()

    selected_superpopulations = request.form.getlist('superpopulations[]') if request.method == 'POST' else []
    selected_populations = request.form.getlist('populations[]') if request.method == 'POST' else []
    per_sample_superpop = 'perSampleSuperpop' in request.form if request.method == 'POST' else False
    per_sample_pop = 'perSamplePop' in request.form if request.method == 'POST' else False

    superpop_pca_data = fetch_pca_data(selected_superpopulations, per_sample_superpop, True) if request.method == 'POST' else None
    pop_pca_data = fetch_pca_data(selected_populations, per_sample_pop, False) if request.method == 'POST' else None

    superpop_plot = plot_pca(superpop_pca_data, 'Superpopulations') if superpop_pca_data is not None else None
    pop_plot = plot_pca(pop_pca_data, 'Populations') if pop_pca_data is not None else None


    return render_template('pca_form.html', superpopulations=superpopulations, regular_populations=regular_populations, selected_superpopulations=selected_superpopulations, selected_populations=selected_populations, per_sample_superpop=per_sample_superpop, per_sample_pop=per_sample_pop, superpop_plot=superpop_plot, pop_plot=pop_plot)

@app.route('/analyze', methods=['POST'])
def analyze():
    selected_superpopulations = request.form.getlist('superpopulations[]')
    selected_populations = request.form.getlist('populations[]')
    per_sample_super = 'perSampleSuperpop' in request.form
    per_sample_pop = 'perSamplePop' in request.form

    # Fetch PCA data
    superpop_pca_data = fetch_pca_data(selected_superpopulations, per_sample_super, True) if selected_superpopulations else pd.DataFrame()
    pop_pca_data = fetch_pca_data(selected_populations, per_sample_pop, False) if selected_populations else pd.DataFrame()

    # Generate plots or set to None if no data
    superpop_plot_json = plot_pca(superpop_pca_data, "Superpopulation PCA")
    pop_plot_json = plot_pca(pop_pca_data, "Population PCA")

    # Update session
    session['selected_superpopulations'] = selected_superpopulations
    session['selected_populations'] = selected_populations
    session['per_sample_super'] = per_sample_super
    session['per_sample_pop'] = per_sample_pop
    session['superpop_plot'] = superpop_plot_json if superpop_plot_json else ""
    session['pop_plot'] = pop_plot_json if pop_plot_json else ""

    return redirect(url_for('pca_form_with_results'))




#ADMIXTURE ANALYSIS 2 
@app.route('/analyze_admixture', methods=['POST'])
def analyze_admixture():
    data = request.get_json()
    selected_populations = data.get('populations', [])
    selected_superpopulations = data.get('superpopulations', [])
    all_selected = selected_populations + selected_superpopulations

    db = get_db(DATABASE)
    cursor = db.cursor()

    # SQL query to fetch admixture data for selected populations and superpopulations
    placeholder = ','.join('?' * len(all_selected))
    query = f'''
    SELECT p.PopulationName, a.ancestry_1, a.ancestry_2, a.ancestry_3, a.ancestry_4, a.ancestry_5
    FROM admixture_results AS a
    JOIN populations AS p ON a.PopulationID = p.PopulationID
    WHERE a.PopulationID IN ({placeholder})
    '''

    cursor.execute(query, all_selected)
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




# SNP ANALYSIS 4
# Function to create a Plotly heatmap from the matrix and encode it into JSON
def generate_heatmap(fst_matrix):
    fig = px.imshow(
        fst_matrix,
        text_auto=True,
        labels=dict(x="Population", y="Population", color="FST Value"),
        x=fst_matrix.columns,
        y=fst_matrix.index
    )
    fig.update_xaxes(side="top", tickangle=-45)  # Rotate x-axis labels
    fig.update_yaxes(tickangle=45)  # Rotate y-axis labels
    fig.update_layout(
        font=dict(size=9),  # Adjust font size if necessary
        autosize=False,
        width=1000,  # Increase width to spread out x-axis labels
        height=600,  # Adjust height if necessary
        margin=dict(t=50, l=50, b=100, r=50)  # Increase bottom margin
    )
    fig.update_traces(showscale=True)  # Ensure the color scale is shown
    return json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)

def calculate_fst_improved(frequencies, sample_sizes):
    weights = [sample_sizes[pop] for pop in frequencies.keys()]
    weighted_allele_freq = np.average([freq for freq in frequencies.values()], weights=weights)

    h_within_each_pop = [2 * freq * (1 - freq) for freq in frequencies.values()]
    weighted_h_within = np.average(h_within_each_pop, weights=weights)

    h_total = 2 * weighted_allele_freq * (1 - weighted_allele_freq)

    fst = (h_total - weighted_h_within) / h_total if h_total > 0 else np.nan
    return fst

def extract_frequency(freq_str):
    if not freq_str or freq_str in ['NaN', '', 'None']:
        return np.nan
    try:
        freq_parts = freq_str.split(';')
        freq_str = freq_parts[-1]  # Considering the last part as the relevant frequency
        return float(freq_str)
    except ValueError:
        return np.nan

def calculate_fst_from_averages(data_dicts, selected_populations, population_sample_sizes):
    fst_results = {}
    for pair in combinations(selected_populations, 2):
        freq_data = {pop: [] for pop in pair}
        for snp in data_dicts:
            for pop in pair:
                freq = extract_frequency(snp.get(f'{pop}_Frequency'))
                if not np.isnan(freq):
                    freq_data[pop].append(freq)

        avg_frequencies = {pop: np.nanmean(freq_data[pop]) if len(freq_data[pop]) > 0 else np.nan for pop in pair}

        if np.isnan(avg_frequencies[pair[0]]) or np.isnan(avg_frequencies[pair[1]]):
            fst_results[pair] = np.nan
        else:
            sample_sizes = {pop: population_sample_sizes[pop] for pop in pair}
            fst_results[pair] = calculate_fst_improved(avg_frequencies, sample_sizes)

    fst_matrix = pd.DataFrame(index=selected_populations, columns=selected_populations, dtype=float)
    for (pop1, pop2), avg_fst in fst_results.items():
        fst_matrix.at[pop1, pop2] = avg_fst
        fst_matrix.at[pop2, pop1] = avg_fst
    np.fill_diagonal(fst_matrix.values, 0)
    
    # Prepare data specifically for HTML display
    html_fst_matrix_list = []
    for index, row in fst_matrix.reset_index().iterrows():
        row_dict = {"Population": row["index"]}
        for pop in selected_populations:
            row_dict[pop] = round(row[pop], 7) if pd.notnull(row[pop]) else "N/A"
        html_fst_matrix_list.append(row_dict)

    heatmap_json = generate_heatmap(fst_matrix)
    tmp_directory = os.path.join(os.path.dirname(__file__), 'tmp')
    if not os.path.exists(tmp_directory):
        os.makedirs(tmp_directory)
    import uuid
    fst_matrix_csv_filename = f'fst_matrix_{uuid.uuid4()}.csv'
    fst_matrix_csv_path = os.path.join(tmp_directory, fst_matrix_csv_filename)
    fst_matrix.to_csv(fst_matrix_csv_path)

    return fst_matrix, heatmap_json, fst_matrix_csv_filename, html_fst_matrix_list

population_sample_sizes = {'SIB': 726, 'GBR': 91, 'FIN': 99, 'CHS': 163, 'PUR': 139, 'CDX': 93, 'CLM': 132,
                                       'IBS': 157, 'PEL': 122, 'PJL': 146, 'KHV': 122, 'ACB': 116, 'GWD': 178, 'ESN': 149,
                                       'BEB': 131, 'MSL': 99, 'STU': 114, 'ITU': 107, 'CEU': 179, 'YRI': 178, 'CHB': 103,
                                       'JPT': 104, 'LWK': 99, 'ASW': 74, 'MXL': 97, 'TSI': 107, 'GIH': 103
                                       }

def round_and_preserve_format(value):
    # Return a default value if input is None
    if value is None:
        return 'N/A'  
    def process_element(element):
        try:
            return str(round(float(element), 3))
        except ValueError:  # In case the element can't be converted to float
            return element
    try:
        genotype_part, allele_freq_part = value.split(';')
        genotypes = genotype_part.split(':')
        rounded_genotypes = [process_element(g) for g in genotypes]
        rounded_genotype_part = ":".join(rounded_genotypes)
        rounded_allele_freq_part = process_element(allele_freq_part)
        return f"{rounded_genotype_part};{rounded_allele_freq_part}"
    except ValueError:  # In case the value doesn't follow the expected format
        return value  # Return the original value or a placeholder if preferred

app.jinja_env.filters['round_preserve'] = round_and_preserve_format


@app.route('/autocomplete/gene_names')
def autocomplete_gene_names():
    query = request.args.get('term', '')
    # Placeholder for DB connection and query execution
    # Assuming `get_db` and `DATABASE` are defined elsewhere in your code
    db = get_db(DATABASE)
    cursor = db.cursor()
    cursor.execute("SELECT DISTINCT GeneName FROM SNP_Data WHERE GeneName LIKE ?", (f'%{query}%,',))
    results = cursor.fetchall()
    gene_names = [result['GeneName'] for result in results]
    return jsonify(gene_names)

@app.route('/analysis_tools/snp', methods=['GET', 'POST'])
@app.route('/snp-analysis', methods=['GET', 'POST'])
def snp_analysis():
    # Placeholder for DB connection
    # Assuming `get_db` and `DATABASE` are defined elsewhere in your code
    db = get_db(DATABASE)
    cursor = db.cursor()

    populations = ['ACB', 'ASW', 'BEB', 'CDX', 'CEU', 'CHB', 'CHS', 'CLM', 'ESN', 'FIN', 'GBR', 'GIH', 'GWD', 'IBS', 'ITU', 'JPT', 'KHV', 'LWK', 'MSL', 'MXL', 'PEL', 'PJL', 'PUR', 'SIB', 'STU', 'TSI', 'YRI']
    if request.method == 'POST':
        action = request.form.get('action')
        selected_snps = request.form.getlist('selected_snps[]')
        selected_populations = request.form.getlist('selected_populations[]')

        if not selected_populations:
            return "No population selected", 400

        base_query = '''
            SELECT SNPID, GeneName, Chromosome, Position, ID, REF, ALT, GeneType, 
                   ClinicalSignificance, ExonicFunction, DistanceToAdjacentGenes
                   '''
        if not selected_snps:
            return "No SNP selected", 400
        frequency_columns = ", ".join(f"{pop}_Frequency" for pop in selected_populations)
        query = f"{base_query}, {frequency_columns} FROM SNP_Data WHERE ID IN ({','.join(['?'] * len(selected_snps))})"
        cursor.execute(query, selected_snps)
        results = cursor.fetchall()

        columns = [desc[0] for desc in cursor.description]
        snp_data_dicts = [dict(zip(columns, row)) for row in results]

        if action == 'Analyze':
            return render_template('snp_results.html', snp_data=snp_data_dicts, selected_populations=selected_populations)
        elif action == 'Calculate FST':
            fst_matrix, heatmap_json, fst_matrix_csv_filename, html_fst_matrix_list = calculate_fst_from_averages(snp_data_dicts, selected_populations, population_sample_sizes)
            return render_template('snp_fst.html', fst_heatmap_json=heatmap_json, selected_populations=selected_populations, fst_matrix_list=html_fst_matrix_list, fst_matrix_csv_filename=fst_matrix_csv_filename)
        # Handle other actions or missing actions
        return "Unrecognized action", 400
    else:
        cursor.execute('SELECT Position, ID, GeneName FROM SNP_Data')
        snp_data = cursor.fetchall()
        snp_data_dicts = [{col[0]: value for col, value in zip(cursor.description, row)} for row in snp_data]
        return render_template('snp_analysis.html', snp_data=snp_data_dicts, populations=populations)

@app.route('/download/<filename>')
def download_route(filename):
    tmp_directory = os.path.join(os.path.dirname(__file__), 'tmp')
    return send_from_directory(tmp_directory, filename, as_attachment=True)
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

