import os
from flask import Flask, render_template, request, redirect, url_for, session
from log_parser import analyze_log_file # Import our backend logic

app = Flask(__name__)
app.secret_key = 'your_secret_key_here' # Change this to a random, secret key

# Create an 'uploads' directory if it doesn't exist
UPLOAD_FOLDER = 'uploads'
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/')
def index():
    """Renders the main index page with the file upload form."""
    return render_template('index.html')

@app.route('/analyze', methods=['POST'])
def analyze():
    """Handles the file upload and performs log analysis."""
    if 'log_file' not in request.files:
        return redirect(request.url) # Redirect back if no file part

    file = request.files['log_file']

    # If the user does not select a file, the browser submits an empty file without a filename.
    if file.filename == '':
        return redirect(url_for('index')) # Redirect back if no selected file

    if file:
        # Securely save the uploaded file
        filename = file.filename
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)

        # Analyze the uploaded file
        analysis_results = analyze_log_file(filepath)

        # Store results in session to pass to the results page (simple way)
        session['analysis_results'] = analysis_results
        session['analyzed_filename'] = filename

        # Clean up the uploaded file after analysis
        os.remove(filepath)

        return redirect(url_for('results'))

@app.route('/results')
def results():
    """Displays the log analysis results."""
    analysis_results = session.pop('analysis_results', None)
    analyzed_filename = session.pop('analyzed_filename', 'No file analyzed')

    if not analysis_results:
        # If no results in session, redirect back to index
        return redirect(url_for('index'))

    return render_template('results.html', results=analysis_results, filename=analyzed_filename)

if __name__ == '__main__':
    # Run the Flask development server
    app.run(debug=False)