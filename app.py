from flask import Flask, request, render_template
from openai import OpenAI
import os
from tableau_ai import update_tableau_workbook

app = Flask(__name__)

client = OpenAI()


workbook_ids = {
    "piechart": "e15641ce-06bf-478f-a977-c9fb01a48fb5",
    "bargraph": "cb8da8ce-7989-4566-a2fa-9e9c3176f000",
    "bubbles": "d5dbeb02-177b-4eaf-967a-1c92dc94fe17",
    "linegraph": "90f0c0b5-3163-4e08-80e0-826d90f3cc81",
    "map": "82cd3511-32c8-4b33-8ddf-e996c706e88f"
}


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

def get_chart_type(input_text):
    response = client.chat.completions.create(
        model="gpt-4-0125-preview",
        messages=[
            {
                "role": "system",
                "content": "You are an AI trained to classify text descriptions into chart types such as piechart, or bargraph, or linegraph, or map, or bubbles."
            },
            {
                "role": "user",
                "content": f"Identify the chart type: {input_text}. Return only the word as the output and your options are piechart, or bargraph, or linegraph, or map, or bubbles."
            }
        ]
    )
    # Assume the response is a single word that is the chart type
    chart_type = response.choices[0].message.content.strip().lower()
    return chart_type

@app.route('/', methods=['GET', 'POST'])
def index():
    input_text = ''
    workb_url = None
    if request.method == 'POST':
        input_text = request.form['input_text']
        chart_type = get_chart_type(input_text)
        workbook_id = workbook_ids.get(chart_type, None)
        csv_data = extract_data_with_openai(input_text)
        workb_url = update_tableau_workbook(csv_data, workbook_id, chart_type)
    return render_template('index.html', workbook_url=workb_url, input_text=input_text)

if __name__ == '__main__':
    app.run(debug=True)
