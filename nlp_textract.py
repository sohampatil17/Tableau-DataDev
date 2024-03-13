from openai import OpenAI
import csv

client = OpenAI()

input_text = "The given data details the number of speakers for various languages. There are 1,346,000,000 Chinese speakers. Spanish speakers total 485,063,960, while English has 379,682,200 speakers. Arabic has 373,000,000 speakers. Hindi has 344,650,870 speakers, Portuguese has 236,266,650, Bengali has 233,808,880, and Russian rounds out the list with 146,954,150 speakers."
# input_text = "At Riverside College, the student major distribution showcases a diverse academic preference. Currently, 1,200 students are enrolled in Computer Science, making it the most popular major. Business Administration follows closely with 1,000 students. The Engineering department hosts 850 students. Psychology attracts 750 students, while Biology has 700 enthusiasts. The Literature department, known for its vibrant discussions and critical analyses, has 650 students, and Education rounds out the list with 600 future teachers, reflecting the college's commitment to a well-rounded academic environment."

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

response_content = response.choices[0].message.content

print(response_content)

lines = response_content.strip().split('\n')

with open('data_source.csv', 'w', newline='') as csvfile:
    csvwriter = csv.writer(csvfile)
    for line in lines:
        cleaned_line = line.replace("```","").strip()
        if cleaned_line:
            csvwriter.writerow(cleaned_line.split(','))
