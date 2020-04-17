from flask import Flask, render_template
app = Flask(__name__)

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

@app.route("/search")
def search():
    return render_template("search.html")

if __name__ == "__main__":
    app.run()
