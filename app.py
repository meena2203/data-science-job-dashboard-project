# Import dependencies
import sqlite3
from flask import Flask, jsonify, render_template 

#################################################

# Flask Setup
app = Flask(__name__)


### SETUP API ROUTES

# Create and define word data route
@app.route("/api/word_data")
def word_data():
    # Connect to the databse and fetch the data from 'job_title' column
    conn = sqlite3.connect('data/jobstats_db.sqlite')
    cur = conn.cursor()
    word_data = cur.execute('select job_title,count(*) from job_stats group by job_title').fetchall()
    conn.close()
       
    # Return a JSON list of word_data
    return jsonify(word_data)

 
# Create and define salary data route
@app.route("/api/salary_data")
def salary_data():
    conn = sqlite3.connect('data/jobstats_db.sqlite')
    cur = conn.cursor()
    average_salary = cur.execute('select job_title as title , count(job_title) as count, ROUND(AVG(salary_in_usd),0) as salary from job_stats GROUP BY job_title order by count(job_title) desc limit 10').fetchall()
    conn.close()
    # print(average_salary)

    # Convert the query results to a dictionary using `job_title` as the key and `average salary_in_usd` as the value
    salary_dict = {}
    for title, count, salary in average_salary:
        salary_dict[title] = salary      

    # Return the JSON representation of your dictionary. 
    return jsonify(salary_dict)


# Create and define employment type data route
@app.route("/api/type_data")
def type_data():
    conn = sqlite3.connect('data/jobstats_db.sqlite')
    cur = conn.cursor()
    employment_types = cur.execute('select remote_ratio, COUNT(job_title) from job_stats GROUP BY remote_ratio').fetchall()
    conn.close()
 
    # Convert the query results to a dictionary using `remote_ratio` as the key and `job_title` as the value
    employment_types_dict = {}
    for type, job_count in employment_types:
        employment_types_dict[type] = job_count    

    # Return the JSON representation of the dictionary
    return jsonify(employment_types_dict)


# Create and define country data route
@app.route("/api/country_data")
def country_data():
    conn = sqlite3.connect('data/jobstats_db.sqlite')
    cur = conn.cursor()
    num_jobs = cur.execute('select company_location, count(*) from job_stats GROUP BY company_location').fetchall()
    #word_data = cur.execute('select job_title,count(*) from job_stats group by job_title').fetchall()
    conn.close()
 
    #Convert the query results to a dictionary using `company_location` as the key and `job_title` as the value
    country_jobs_dict = {}
    for country, count in num_jobs:
        country_jobs_dict[country] =  count 

    # Return the JSON representation of the dictionary
    return jsonify(country_jobs_dict)
  

# Create and define map data route
@app.route("/api/map_data")
def map_data():
    conn = sqlite3.connect('data/updated_jobs_usa_db.sqlite')
    cur = conn.cursor()
    job_postings = cur.execute('select * from updated_jobs_usa').fetchall()
    conn.close()

    # Convert the query results to a dictionary of dictionaries
    job_postings_dict = {}
    i = 0
    for title, company, attribute, location, posted_date, link, latitude, longitude in job_postings:
        job_postings_dict[str(i)] = {
            'latitude': latitude,
            'longitude': longitude,
            'company': company,
            'title': title,
            'attribute': attribute,
            'location': location,
            'posted_date': posted_date,
            'link': link
        }
        i += 1

    # Return the JSON representation of the dictionary of dictionaries
    return jsonify(job_postings_dict)
    

### SETUP WEB ROUTES
# Route to render index.html template
@app.route("/")
def home():

    # Return template and data
    return render_template("index.html")


@app.route("/salary")
def salary():

    # Return template 
    return render_template("salary.html")

@app.route("/type")
def type():

    # Return template and data
    return render_template("type.html")

@app.route("/country")
def country():

    # Return template and data
    return render_template("country.html")

@app.route("/map")
def map():

    # Return template and data
    return render_template("map.html")

@app.route("/word")
def word():

    # Return template and data
    return render_template("word.html")


# Define main behavior
if __name__ == '__main__':
    app.run(debug=True)
