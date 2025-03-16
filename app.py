from flask import Flask, request, render_template, send_file
import requests
import pandas as pd

app = Flask(__name__)

# Function to fetch backlinks (dummy data for now)
def fetch_backlinks(domain):
    dummy_data = [
        {"url": "https://example1.com", "anchor": "click here", "dr": 50, "spam_score": 3},
        {"url": "https://example2.com", "anchor": "visit us", "dr": 20, "spam_score": 8},
        {"url": "https://example3.com", "anchor": "learn more", "dr": 70, "spam_score": 2},
    ]
    return dummy_data

# Function to identify toxic links
def identify_toxic_links(backlinks):
    toxic_links = []
    for link in backlinks:
        if link.get("dr", 100) < 30 or link.get("spam_score", 0) > 5:
            toxic_links.append(link)
    return toxic_links

# Function to export data to CSV
def export_to_csv(backlinks, filename="backlinks.csv"):
    df = pd.DataFrame(backlinks)
    df.to_csv(filename, index=False)

# Homepage
@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        domain = request.form["domain"]
        backlinks = fetch_backlinks(domain)
        toxic_links = identify_toxic_links(backlinks)
        export_to_csv(backlinks)
        return render_template("results.html", backlinks=backlinks, toxic_links=toxic_links)
    return render_template("index.html")

# Download CSV file
@app.route("/download")
def download():
    return send_file("backlinks.csv", as_attachment=True)

# Run the app
if __name__ == "__main__":
    app.run(debug=True)