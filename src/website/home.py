from flask import Flask, render_template, request
import sys
import pandas as pd
import os
import glob
import string

app = Flask(__name__)

def file_name_gen(directoryPath):
    result = []
    for files in glob.glob(directoryPath + '*.csv'):
        result.append(files)
    return result

def results_adder(query):
    files = file_name_gen('../scraper/ralphs_data/13321 Jamboree Rd, Tustin, CA/')
    files.remove
    results = []
    for index in range(0, len(files)):
        df = pd.read_csv(files[index], encoding="latin1")
        for i in range(0, len(df)):
            # MODIFY/REMOVE
            if len(results) == 10:
                return results
            print(files[index])
            if(query.lower() in (df["Category"][0]).lower()):
                results.append([df["Product"][i], df["Price"][i], df["Url"][i]])
                continue
            elif (query.lower() in (df["Product"][i]).lower()):
                results.append([df["Product"][i], df["Price"][i], df["Url"][i]])
            else:
                continue
    return results

@app.route("/")
def home():
    return render_template("home.html")

@app.route("/about")
def about():
    return render_template("about.html")

@app.route("/stats")
def stats():
    return render_template("stats.html")

@app.route("/donate")
def donate():
    return render_template("donate.html")

@app.route("/search", methods=['GET', 'POST'])
def search():
    if request.method == 'POST':
        item_name = request.form['search']
        print(item_name)
        data=results_adder(item_name)
        print(data)
        return render_template("search.html", data=data)

    return render_template("search.html")

if __name__ == "__main__":
    app.run()
