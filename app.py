from flask import Flask, request, render_template, send_file
import requests
import csv

app = Flask(__name__)

# Fetch backlinks from the Postman Mock API
def fetch_backlinks(domain):
    mock_api_url = "https://8708051d-256c-45b7-9bc7-6d5b783e9cd0.mock.pstmn.io/"  # Your mock server URL
    try:
        print(f"Fetching backlinks for domain: {domain}")  # Debugging statement
        response = requests.get(mock_api_url)
        print(f"API Response Status Code: {response.status_code}")  # Debugging statement
        if response.status_code == 200:
            data = response.json()
            print(f"API Response Data: {data}")  # Debugging statement
            # Simulate dynamic behavior by including the domain in the response
            for i, link in enumerate(data.get("backlinks", [])):
                link["url"] = f"https://{domain}/backlink{i+1}"  # Fix URL formatting
            return data.get("backlinks", [])
        else:
            print(f"Error fetching data: {response.status_code}")
            return []
    except Exception as e:
        print(f"An error occurred: {e}")
        return []

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
        print(f"Form submitted with domain: {domain}")  # Debugging statement
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