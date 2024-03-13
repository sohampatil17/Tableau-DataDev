from flask import Flask, request, render_template
from openai import OpenAI
import os
from tableau_ai import update_tableau_workbook


app = Flask(__name__)

client = OpenAI()

# Function to call OpenAI API and get structured data in CSV format
def extract_data_with_openai(input_text):
    response = client.chat.completions.create(
    model="gpt-4-0125-preview",
    messages=[
            {
                "role": "system", "content": "You are an AI assistant trained to help me convert plain text into well-formated structured data for csv."
            },
            {
                "role": "user", "content": f'Extract structured data in csv format: "{input_text}". Only output the csv format data and nothing else. Ensure the headers are Label, Data'
            }
        ]
    )
    return response.choices[0].message.content.strip().split('\n')


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        input_text = request.form['input_text']
        processing = True
        csv_data = extract_data_with_openai(input_text)
        workb_url = update_tableau_workbook(csv_data)
        processing = False
        updated_url = "https://prod-useast-b.online.tableau.com/t/sohampatilai5401868afb/authoring/soham_workbook/Sheet1#1"  # Replace with your logic to get the updated URL
        return render_template('index.html', workbook_url=updated_url, processing=processing)
    return render_template('index.html', processing=False)

if __name__ == '__main__':
    app.run(debug=True)
