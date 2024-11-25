from pdfminer.high_level import extract_text
import pandas as pd

### First extract the data from the pdfs and accompanying csv.


pdf_path = "/Users/stuartbladon/Documents/Duke 2024/AIPI 510/dataset proj/code+data/Intelligence Data/" #You will obviously need to update this, you want this to be the path to the 'intelligence data' folder

data = pd.read_csv("/Users/stuartbladon/Documents/Duke 2024/AIPI 510/dataset proj/code+data/data.csv") # and this, you want this to be the data.csv file

print(data.head())

doc_titles = []
texts = []

# Iterate over the rows of the data DataFrame
for index, row in data.iterrows():
    # Extract text from the PDF
    text = extract_text(pdf_path + row['Doc Title'] + '.pdf')
    
    # Collect data for each row
    doc_titles.append(row['Doc Title'])
    texts.append(text)

# Create the DataFrame from the collected data
df = pd.DataFrame({
    'Doc Title': doc_titles,
    'text': texts
})

data = pd.merge(data, df, on = 'Doc Title', how = 'left')

print(data.head())

### Lets clean up the textual data as best we can

print("This part may take a while")

import nltk
from nltk.corpus import words
from autocorrect import Speller

nltk.download("words")

spell = Speller(lang='en') #initialise spellcheck
valid_words = set(words.words()) 

def clean_text(text):
    """cleans the textual data using spellcheck and valid words"""
    corrected_words = []
    for word in text.split():
        corrected = spell(word)  # Correct the word using autocorrect
        if corrected.lower() in valid_words:  # Check against valid words
            corrected_words.append(corrected)
    return " ".join(corrected_words)


cleaned_texts = []
count = 0
for txt in data['text']:
    cln_txt = clean_text(txt)
    cleaned_texts.append(cln_txt)
    count+=1 #document number (track progress)
    print(count)
data['text'] = cleaned_texts

#save to csv

data = data.loc[:, ~data.columns.str.contains('^Unnamed')]
data.to_csv("intelligence_data.csv", index_label = True)

