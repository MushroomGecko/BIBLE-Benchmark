import os

import requests
from bs4 import BeautifulSoup
from fpdf import FPDF
from fpdf.enums import XPos, YPos
import sys
curr_thing = 'measurements'

# URL to scrape
link = 'https://www.gotquestions.org/biblical-weights-and-measures.html'

directory = 1
os.makedirs(f'source_data/GotQuestionsScrapes/{curr_thing}/dir{directory}', exist_ok=True)

# Create PDF
pdf = FPDF()
# Register Hack Nerd Font
font_path = "./unifont-16.0.02.ttf"
pdf.add_font("UniFont", "", font_path)
pdf.add_page()
# Send a GET request to the URL
response = requests.get(link)
response.encoding = 'utf-8'

# Parse the HTML content
soup = BeautifulSoup(response.text, 'html.parser')

# Extract the question from the <span> tag
question_tag = soup.find('span', itemprop='name headline', property='og:title')
title = question_tag.get_text(strip=False, separator=' - ') if question_tag else None

# Extract the content from the <div> tag
content_tag = soup.find('div', itemprop='articleBody')

# Remove or process content outside the specified <div>
ignored_div = content_tag.find('div', class_='label gradient-to-tr')
if ignored_div:
    ignored_div.decompose()  # Remove the entire div from content_tag

# Replace every <br> tag with a newline character
if content_tag:
    for br in content_tag.find_all('br'):
        br.replace_with('\n')

# Convert content_tag back to a string after modifications
content = content_tag.get_text(strip=False) if content_tag else None
if '\n\n\n' in content:
    content = content.replace('\n\n', '\n')

while '\n\n\n' in content:
    content = content.replace('\n\n\n', '\n\n')

title = title.strip()
content = content.strip()
print(content)
print(title)

# Set the title font to Hack Nerd (Large size)
pdf.set_font("UniFont", size=20)
pdf.multi_cell(0, 10, title, new_x=XPos.LMARGIN, new_y=YPos.NEXT, align="C")

pdf.set_font("UniFont", size=20)
pdf.multi_cell(0, 10, link, new_x=XPos.LMARGIN, new_y=YPos.NEXT, align="C")

# Set regular text font
pdf.set_font("UniFont", size=12)
pdf.multi_cell(0, 10, content, new_x=XPos.LMARGIN, new_y=YPos.NEXT)
print(title)
print()

os.makedirs(f'source_data/GotQuestionsScrapes/{curr_thing}/dir{directory}', exist_ok=True)

# Save PDF
pdf.output(f"source_data/GotQuestionsScrapes/{curr_thing}/dir{directory}/{link.split('/')[-1]}.pdf")
