import pandas as pd
from wordcloud import WordCloud
import matplotlib.pyplot as plt
from sklearn.feature_extraction.text import TfidfVectorizer

data = pd.read_csv("/Users/stuartbladon/Documents/Duke 2024/AIPI 510/dataset proj/code+data/intelligence_data.csv") # Again this will need an update

#Very basic analysis

print(data.head())

values = data['Threat level'].value_counts()

plt.figure(figsize=(8, 5))
values.plot(kind='bar', color='skyblue')
plt.title("Threat Level Class Distribution")
plt.ylabel("Count")
plt.show()

#Simple wordclouds

text_total = ''

for txt in data['text']:
    text_total += txt

wordcloud_tot = WordCloud(width=800, height=400, background_color='white').generate(text_total)

text_high = ''
data_filt = data.loc[data['Threat level'] == 'High', 'text']

for txt in data_filt:
    text_high += txt

wordcloud_high = WordCloud(width=800, height=400, background_color='white').generate(text_high)


text_medium = ''
data_filt = data.loc[data['Threat level'] == 'Medium', 'text']

for txt in data_filt:
    text_medium += txt

wordcloud_med = WordCloud(width=800, height=400, background_color='white').generate(text_medium)

fig, axes = plt.subplots(1, 3, figsize=(15, 5))  # Create 1 row and 3 columns of subplots

# Add each word cloud to a subplot
axes[0].imshow(wordcloud_tot, interpolation='bilinear')
axes[0].axis('off')  
axes[0].set_title('Total dataset')

axes[1].imshow(wordcloud_high, interpolation='bilinear')
axes[1].axis('off')
axes[1].set_title('High Threat Level')

axes[2].imshow(wordcloud_med, interpolation='bilinear')
axes[2].axis('off')
axes[2].set_title('Medium Threat Level')

plt.tight_layout()
plt.show()

# Analysis of differences between high and low Threat level

vectorizer = TfidfVectorizer()
tfidf_matrix = vectorizer.fit_transform([text_high, text_medium])
tfidf_scores = tfidf_matrix.toarray()

words = vectorizer.get_feature_names_out()
tfidf_diff = {words[i]: tfidf_scores[0, i] - tfidf_scores[1, i] for i in range(len(words))}

wordcloud = WordCloud(width=800, height=400, background_color='white').generate_from_frequencies(tfidf_diff)

# Display the word cloud
plt.figure(figsize=(10, 5))
plt.imshow(wordcloud, interpolation='bilinear')
plt.axis('off')
plt.title('Word Cloud of TF-IDF Differences')
plt.show()

pd.Series(tfidf_diff).sort_values(ascending=False).head(10).plot(kind='bar', figsize=(10, 5))
plt.title('Top Words: High vs Medium')
plt.show()