from flask import Flask, request, render_template, send_file
import csv

app = Flask(__name__)

# Dummy backlink data for testing
def fetch_backlinks(domain):
    return [
        {"url": f"https://{domain}/backlink1", "anchor": "click here", "dr": 50, "spam_score": 3},
        {"url": f"https://{domain}/backlink2", "anchor": "visit us", "dr": 20, "spam_score": 8},
        {"url": f"https://{domain}/backlink3", "anchor": "learn more", "dr": 70, "spam_score": 2},
    ]

# Identify toxic links
def identify_toxic_links(backlinks):
    toxic_links = []
    for link in backlinks:
        if link.get("dr", 100) < 30 or link.get("spam_score", 0) > 5:
            toxic_links.append(link)
    return toxic_links

# Export backlinks to CSV
def export_to_csv(backlinks, filename="backlinks.csv"):
    keys = backlinks[0].keys()  # Get the keys (column names) from the first row
    with open(filename, mode="w", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=keys)
        writer.writeheader()
        writer.writerows(backlinks)

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