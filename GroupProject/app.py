from flask import Flask, render_template, request  # pip install Flask

# Pass in name to determine root path, then Flask can find other files easier
app = Flask(__name__)


# Route - mapping (connecting) a URL to Python function
@app.route('/')
def index():
    return render_template('index.html')

@app.route("/about")
def about():
    return render_template('about.html')

# Runs app only when we run this script directly, not if we import this somewhere else
if __name__ == "__main__":
    app.run(debug=True)

# http://127.0.0.1:5000/