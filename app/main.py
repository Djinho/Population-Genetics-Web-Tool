from flask import Flask, request, render_template, g
import sqlite3

app = Flask(__name__)
DATABASE = 'C:/Users/Djinh/Documents/Population-Genetics-Web-Tool/PopulationGeneticsDB.sqlite'

def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
        db.row_factory = sqlite3.Row
        db.execute('PRAGMA foreign_keys = ON')
        db.commit()
    return db

@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()

@app.route('/')
def index():
    db = get_db()
    cursor = db.execute('SELECT PopulationID, PopulationName FROM Populations')
    populations = cursor.fetchall()
    return render_template('index.html', populations=populations)

@app.route('/analyze', methods=['POST'])
def analyze():
    analysis_type = request.form.get('analysis_type')
    population1_id = request.form.get('population1')
    population2_id = request.form.get('population2')

    if analysis_type == 'PCA':
        results = perform_pca(population1_id, population2_id)
        results['population1_name'] = population_name_from_id(population1_id)
        results['population2_name'] = population_name_from_id(population2_id)
    else:
        results = {'message': 'Analysis type not supported.'}

    return render_template('analyze.html', results=results)

def perform_pca(population1_id, population2_id):
    db = get_db()
    cursor = db.execute('SELECT * FROM PCACoordinates WHERE PopulationID IN (?, ?)', (population1_id, population2_id))
    pca_data = cursor.fetchall()
    # Process your pca_data as needed to perform PCA analysis here
    pca_results = {'PCA_Result': pca_data}  # Assuming pca_data has the right structure
    return pca_results

def population_name_from_id(population_id):
    db = get_db()
    cursor = db.execute('SELECT PopulationName FROM Populations WHERE PopulationID = ?', (population_id,))
    result = cursor.fetchone()
    return result['PopulationName'] if result else None

if __name__ == '__main__':
    app.run(debug=True)
