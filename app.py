from flask import Flask, render_template, request, redirect, url_for
from src.scraper import scrape  # Adjust import path if necessary

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':

        print(request.form)

        job_name = request.form.get('job_name')
        min_s = int(request.form.get('min_s'))
        max_s = int(request.form.get('max_s'))
        filter_company = request.form.getlist('filter_company')  # Assuming input as a comma-separated list
        filter_employment = request.form.getlist('filter_employment')  # Assuming input as a comma-separated list
        
        # Call the scrape function and pass the input parameters
        scraped_data = scrape(job_name, min_s, max_s, filter_company, filter_employment)
        
        print(scraped_data) 

        # Pass the results to the results template
        return render_template('results.html', scraped_data=scraped_data)

    # Show the form by default
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)