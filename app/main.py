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
def fetch_superpopulations(db):
    cursor = db.execute('SELECT PopulationID, PopulationName FROM populations WHERE is_Superpopulation = 1')
    return cursor.fetchall() #ADDITION 

def fetch_regular_populations(db):
    cursor = db.execute('SELECT PopulationID, PopulationName FROM populations WHERE is_Superpopulation = 0')
    return cursor.fetchall()
# Define route for PCA form
#@app.route('/analysis_tools/pca')
#def pca_form():
 #   db = get_db(DATABASE)
  #  if db is None:
   #     return "Error: Unable to connect to the database."
    
    # Fetch superpopulations
    #cursor = db.execute('SELECT PopulationID, PopulationName FROM populations WHERE is_Superpopulation = 1')
    #superpopulations = cursor.fetchall()
    
    # Fetch regular populations
    #cursor = db.execute('SELECT PopulationID, PopulationName FROM populations WHERE is_Superpopulation = 0')
    #regular_populations = cursor.fetchall()

    # Pass both sets to the template
    #return render_template('pca_form.html', superpopulations=superpopulations, regular_populations=regular_populations)
@app.route('/analysis_tools/pca') #ADDITION 2
def pca_form():
    db = get_db(DATABASE)  # Pass DATABASE as an argument to get_db
    if db is None:
        return "Error: Unable to connect to the database."
    
    # Fetch superpopulations
    cursor = db.execute('SELECT PopulationID, PopulationName FROM populations WHERE is_Superpopulation = 1')
    superpopulations = cursor.fetchall()
    
    # Fetch regular populations
    cursor = db.execute('SELECT PopulationID, PopulationName FROM populations WHERE is_Superpopulation = 0')
    regular_populations = cursor.fetchall()

    # Pass both sets to the template
    return render_template('pca_form.html', superpopulations=superpopulations, regular_populations=regular_populations)


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
@app.route('/pca_form_with_results')  #ADDITION 3
def pca_form_with_results():
    db = get_db(DATABASE)
    superpopulations = fetch_superpopulations(db)
    regular_populations = fetch_regular_populations(db)
    selected_populations = session.get('selected_populations', [])
    per_sample = session.get('per_sample', False)
    plot_json = session.get('plot_json', None)
    
    return render_template('pca_form.html', 
                           superpopulations=superpopulations,
                           regular_populations=regular_populations,
                           selected_populations=selected_populations,
                           per_sample=per_sample,
                           plot_json=plot_json)

#@app.route('/analyze', methods=['POST'])
#def analyze():
 #   selected_populations = request.form.getlist('populations[]')
  #  per_sample = request.form.get('perSample')  # Check if Per Sample is selected
    
    # Decide which analysis to perform based on the Per Sample checkbox
   # if per_sample:
    #    results = perform_pca_individuals(selected_populations)
     #   session['results'] = results
      #  return redirect(url_for('display_persample_results'))
    #else:
     #   results = perform_pca(selected_populations)
      #  session['results'] = results
       # return redirect(url_for('display_results'))
@app.route('/analyze', methods=['POST'])
def analyze():
    selected_populations = request.form.getlist('populations[]') #ADDITION/REPACEMENT
    per_sample = 'perSample' in request.form
    session['selected_populations'] = selected_populations
    session['per_sample'] = per_sample

    if per_sample:
        results = perform_pca_individuals(selected_populations)
    else:
        results = perform_pca(selected_populations)
    plot_json = plot_pca(results)

    session['plot_json'] = plot_json
    return redirect(url_for('pca_form_with_results'))


#PCA ANALYSIS 1

# Define route for displaying PCA results
#@app.route('/results')
#def display_results():
 #   results = session.get('results', None)
  #  if results is None:
   #     return "Error: No results data provided."
    #plot_url = plot_pca(results)
    #return render_template('results.html', results=results, plot_url=plot_url)

#Function to perform PCA analysis
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
#def plot_pca(pca_results):
 #   x_coords = [result['pc1'] for result in pca_results]
  #  y_coords = [result['pc2'] for result in pca_results]
   # labels = [result['population_name'] for result in pca_results]

    #plt.figure(figsize=(10, 8))
    #plt.scatter(x_coords, y_coords, alpha=0.5)
    #for label, x, y in zip(labels, x_coords, y_coords):
     #   plt.annotate(label, (x, y), textcoords="offset points", xytext=(0,10), ha='center')
    #plt.title('PCA Plot')
    #plt.xlabel('PC1')
    #plt.ylabel('PC2')
    #img = BytesIO()
    #plt.savefig(img, format='png', bbox_inches='tight')
    #plt.close()
    #img.seek(0)
    #plot_url = base64.b64encode(img.getvalue()).decode('utf8')
    #return plot_url
def plot_pca(pca_data):
    # Assuming pca_data is already in the correct format
    df = pd.DataFrame(pca_data)
    fig = px.scatter(df, x='pc1', y='pc2', color='population_name',
                     labels={"pc1": "PC1", "pc2": "PC2"}, #ADDITION
                     title="PCA Plot")
    fig.update_layout(width=700)  # Adjust width here
    plot_json = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
    return plot_json
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
#@app.route('/results_persample')
#def display_persample_results():
 #   results = session.get('results', None)
  #  if results is None:
   #     return "Error: No results data provided."
    #plot_url = plot_pca_individuals(results)  # Ensure you modify the plotting function to handle individual results
    #return render_template('Per_sample_pca.html', results=results, plot_url=plot_url)



#PLOT PCA FOR SAMPLES 
#def plot_pca_individuals(pca_results):
    # Assuming pca_results includes a 'population_name' for each sample
 #   populations = list(set([result['population_name'] for result in pca_results]))
    # Assign a unique color to each population
  #  colors = plt.cm.rainbow(np.linspace(0, 1, len(populations)))
   # population_color_map = dict(zip(populations, colors))
    
    #plt.figure(figsize=(10, 8))
    #for result in pca_results:
     #   x = result['pc1']
      #  y = result['pc2']
       # population = result['population_name']
        #plt.scatter(x, y, alpha=0.5, label=population, color=population_color_map[population])
    
    # Create a legend with population labels
    #handles, labels = plt.gca().get_legend_handles_labels()
    #by_label = dict(zip(labels, handles))  # Eliminate duplicate labels
    #plt.legend(by_label.values(), by_label.keys(), title="Populations")
    
    #plt.title('PCA Plot for Individual Samples')
    #plt.xlabel('PC1')
    #plt.ylabel('PC2')
    
    #img = BytesIO()
    #plt.savefig(img, format='png', bbox_inches='tight')
    #plt.close()
    #img.seek(0)
    #plot_url = base64.b64encode(img.getvalue()).decode('utf8')
    #return plot_url
def plot_pca_individuals(pca_results):
    fig = go.Figure()
    for result in pca_results:
        fig.add_trace(go.Scatter(x=[result['pc1']], y=[result['pc2']],
                                 mode='markers', name=result['population_name']))
    
    fig.update_layout(
        title='PCA Plot for Individual Samples',
        xaxis_title='PC1',                              #ADDITION/REPLACEMENT
        yaxis_title='PC2',
        width=700  # Adjust width here
    )
    return json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)



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




# FST ANALYSIS 3 
#@app.route('/fst_calculator', methods=['GET', 'POST'])
#def calculate_fst():
 #   if request.method == 'POST':
  #      population1 = request.form.get('population1')
   #     population2 = request.form.get('population2')
        
    #    db = get_db(DATABASE2)
     #   cur = db.cursor()
      #  cur.execute('SELECT fst_value FROM fst_data WHERE population1 = ? AND population2 = ? UNION ALL SELECT fst_value FROM fst_data WHERE population1 = ? AND population2 = ?', (population1, population2, population2, population1))
       # fst_value = cur.fetchone()
        
        #if fst_value:
         #   fst_value = fst_value['fst_value']
        #else:
         #   fst_value = 'Not Found'
        
        #cur.execute('SELECT DISTINCT population1 FROM fst_data')
        #populations = [row['population1'] for row in cur.fetchall()]
        
        #return render_template('fst_calculator.html', populations=populations, fst_value=fst_value, population1=population1, population2=population2)
    #else:
     #   db = get_db(DATABASE2)
      #  cur = db.cursor()
       # cur.execute('SELECT DISTINCT population1 FROM fst_data')
        #populations = [row['population1'] for row in cur.fetchall()]
        
        #return render_template('fst_calculator.html', populations=populations, fst_value=None)
    

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

