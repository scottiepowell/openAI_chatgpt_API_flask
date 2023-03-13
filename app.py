from flask import Flask, request, render_template, url_for

app = Flask(__name__)

# Run the Python code with the provided arguments
import requests
import os

@app.route("/", methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        prompt = request.form['prompt']
        filename = request.form['filename']
        api_endpoint = "https://api.openai.com/v1/completions"
        api_key = os.getenv("OPENAI_API_KEY")

        headers = {
            'Content-Type': 'application/json',
            'Authorization': 'Bearer ' + api_key
        }

        request_data = {
            "model": "text-davinci-003",
            "prompt": f"Write python script to {prompt}. Provide only code, no text",
            "max_tokens": 50,
            "temperature": 0.5
        }

        response = requests.post(api_endpoint, headers=headers, json=request_data)

        if response.status_code == 200:
            response_text = response.json()["choices"][0]["text"]
            with open(filename, "w") as file:
                file.write(response_text)
        else:
            return f"Request failed with status code {str(response.status_code)}"

        # Read the contents of the file and display it
        with open(filename, "r") as file:
            file_contents = file.read()

        # Render the index page with the file contents as context
        return render_template("index.html", file_contents=file_contents)

    else:
        # Render the index page without any context
        return render_template("index.html")

@app.route("/recent_calls")
def recent_calls():
    query_dir = "recent_q"
    filenames = os.listdir(query_dir)

    links = []
    for filename in filenames:
        filepath = os.path.join(query_dir, filename)
        link = {"filename": filename, "url": url_for('query', filename=filename)}
        links.append(link)

    return render_template("recent_calls.html", links=links)

@app.route("/query")
def query():
    filename = request.args.get("filename")
    filepath = os.path.join("recent_q", filename)

    with open(filepath, "r") as file:
        file_contents = file.read()

    return file_contents

@app.route("/result", methods=['POST'])
def result():
    prompt = request.form['prompt']
    filename = request.form['filename']
    api_endpoint = "https://api.openai.com/v1/completions"
    api_key = os.getenv("OPENAI_API_KEY")

    headers = {
        'Content-Type': 'application/json',
        'Authorization': 'Bearer ' + api_key
    }

    request_data = {
        "model": "text-davinci-003",
        "prompt": f"Write python script to {prompt}. Provide only code, no text",
        "max_tokens": 50,
        "temperature": 0.5
    }

    response = requests.post(api_endpoint, headers=headers, json=request_data)

    if response.status_code == 200:
        response_text = response.json()["choices"][0]["text"]
        with open(filename, "w") as file:
            file.write(response_text)
    else:
        return f"Request failed with status code {str(response.status_code)}"

    # Read the contents of the file and display it
    with open(filename, "r") as file:
        file_contents = file.read()

    return file_contents

if __name__ == "__main__":
    app.run(debug=True)