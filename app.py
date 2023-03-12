from flask import Flask, request

app = Flask(__name__)

@app.route("/")
def index():
    return """
    <form method='POST' action='/result'>
        <label for='prompt'>Prompt:</label>
        <input type='text' name='prompt' id='prompt'>
        <br><br>
        <label for='filename'>Filename:</label>
        <input type='text' name='filename' id='filename'>
        <br><br>
        <input type='submit' value='Submit'>
    </form>
    """

@app.route("/result", methods=['POST'])
def result():
    prompt = request.form['prompt']
    filename = request.form['filename']
    
    # Run the Python code with the provided arguments
    import requests
    import os

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
