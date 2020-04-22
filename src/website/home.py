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

def results_adder(query, filename):
    files = file_name_gen(filename)
    files.remove
    results = []
    for index in range(0, len(files)):
        df = pd.read_csv(files[index], encoding="latin1")
        for i in range(0, len(df)):
            # MODIFY/REMOVE
            if len(results) == 30:
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
        data1 = results_adder(item_name, '../scraper/ralphs_data/13321 Jamboree Rd, Tustin, CA/')
        data2 = results_adder(item_name, '../scraper/ralphs_data/14400 Culver Dr, Irvine, CA/')
        data3 = results_adder(item_name, '../scraper/ralphs_data/6300 Irvine Blvd, Irvine, CA/')
        return render_template("search.html", data1=data1, data2=data2, data3=data3)

    return render_template("search.html")

@app.route("/map")
def map():
   return render_template("map.html")


if __name__ == "__main__":
    app.run()
