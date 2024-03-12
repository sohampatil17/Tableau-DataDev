import matplotlib.pyplot as plt
import pandas as pd
import io
import base64

# Data
data = {
    'Language': [
        'Chinese (Mandarin)',
        'Spanish',
        'English',
        'Arabic (Egyptian Arabic)',
        'Hindi',
        'Portuguese',
        'Bengali',
        'Russian'
    ],
    'Speakers': [
        1346000000,
        485063960,
        379682200,
        373000000,
        344650870,
        236266650,
        233808880,
        146954150
    ]
}

# Create a DataFrame
df = pd.DataFrame(data)

# Create the pie chart
fig, ax = plt.subplots()
ax.pie(df['Speakers'], labels=df['Language'], autopct='%1.1f%%', startangle=140)
ax.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.

# Save the pie chart to a BytesIO object
buffer = io.BytesIO()
plt.savefig(buffer, format='png')
buffer.seek(0)

# Encode the image to base64 string
pie_chart_base64 = base64.b64encode(buffer.getvalue()).decode('utf-8')

# Close plt object to prevent memory usage
plt.close()

# The pie_chart_base64 variable now holds the base64-encoded image of the pie chart
