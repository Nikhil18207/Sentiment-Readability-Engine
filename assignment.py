
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import os
import re
from nltk.tokenize import sent_tokenize, word_tokenize
import string


INPUT_FILE = 'Input.xlsx'
OUTPUT_FILE = 'Output Data Structure.csv'
MASTER_DICT_DIR = 'MasterDictionary'
STOPWORDS_DIR = 'StopWords'
OUTPUT_TEXT_DIR = 'extracted_articles_selenium'

os.makedirs(OUTPUT_TEXT_DIR, exist_ok=True)


def load_stopwords():
    """Loads all stop words from the StopWords directory."""
    all_stopwords = set()
    for filename in os.listdir(STOPWORDS_DIR):
        with open(os.path.join(STOPWORDS_DIR, filename), 'r', encoding='ISO-8859-1') as f:
            words = f.read().splitlines()
            all_stopwords.update(word.lower() for word in words)
    return all_stopwords

def load_master_dictionary():
    """Loads positive and negative words from the MasterDictionary directory."""
    with open(os.path.join(MASTER_DICT_DIR, 'positive-words.txt'), 'r', encoding='ISO-8859-1') as f:
        positive_words = set(word.lower() for word in f.read().splitlines())
    with open(os.path.join(MASTER_DICT_DIR, 'negative-words.txt'), 'r', encoding='ISO-8859-1') as f:
        negative_words = set(word.lower() for word in f.read().splitlines())
    return positive_words, negative_words

ALL_STOP_WORDS = load_stopwords()
POSITIVE_WORDS, NEGATIVE_WORDS = load_master_dictionary()


def extract_article_text_selenium(url, driver):
    """
    Extracts article title and text from a given URL using Selenium.
    Returns a tuple of (title, text) or (None, None) on failure.
    """
    try:
        driver.get(url)
        
       
        soup = BeautifulSoup(driver.page_source, 'html.parser')
        
       
        title = soup.find('h1')
        title_text = title.get_text(strip=True) if title else None

        article_content = soup.find('div', class_='td-post-content') or soup.find('div', class_='entry-content') or soup.find('article')
        
        if not article_content:
            return title_text, "Article text not found."
            
        paragraphs = article_content.find_all('p')
        article_text = '\n'.join([p.get_text(strip=True) for p in paragraphs if p.get_text(strip=True)])
        
      
        footer_tags = article_content.find_all(['footer', 'div'], class_=['td-post-source-tags', 'td-post-share-buttons'])
        for tag in footer_tags:
            tag.decompose()
            
        return title_text, article_text

    except Exception as e:
        print(f"Error extracting {url}: {e}")
        return None, None

def save_article_text(url_id, title, text):
    """Saves the extracted title and text to a file."""
    if title and text:
        with open(os.path.join(OUTPUT_TEXT_DIR, f'{url_id}.txt'), 'w', encoding='utf-8') as f:
            f.write(title + '\n\n' + text)


def get_clean_words(text):
    """Removes punctuation and stop words, then returns a list of clean words."""
    text = text.translate(str.maketrans('', '', string.punctuation))
    words = word_tokenize(text.lower())
    clean_words = [word for word in words if word not in ALL_STOP_WORDS and word.isalpha()]
    return clean_words

def count_syllables(word):
    """Counts syllables in a word based on a simple heuristic."""
    word = word.lower()
    count = 0
    vowels = "aeiouy"
    if word.endswith(('es', 'ed')):
        word = word[:-2]
    if word and word[0] in vowels:
        count += 1
    for index in range(1, len(word)):
        if word[index] in vowels and word[index - 1] not in vowels:
            count += 1
    if word.endswith('e'):
        count -= 1
    if count == 0:
        count = 1
    return count

def is_complex(word):
    """Checks if a word is complex (syllable count > 2)."""
    return count_syllables(word) > 2

def analyze_text(text):
    """Performs all required text analysis calculations."""
    if not text:
        return {var: 0 for var in [
            'POSITIVE SCORE', 'NEGATIVE SCORE', 'POLARITY SCORE', 'SUBJECTIVITY SCORE',
            'AVG SENTENCE LENGTH', 'PERCENTAGE OF COMPLEX WORDS', 'FOG INDEX',
            'AVG NUMBER OF WORDS PER SENTENCE', 'COMPLEX WORD COUNT',
            'WORD COUNT', 'SYLLABLE PER WORD', 'PERSONAL PRONOUNS', 'AVG WORD LENGTH'
        ]}
    
    sentences = sent_tokenize(text)
    clean_words = get_clean_words(text)
    total_words_count = len(clean_words)
    total_sentences_count = len(sentences)
    
    positive_score = sum(1 for word in clean_words if word in POSITIVE_WORDS)
    negative_score = sum(1 for word in clean_words if word in NEGATIVE_WORDS)
    
    polarity_score = (positive_score - negative_score) / ((positive_score + negative_score) + 0.000001)
    subjectivity_score = (positive_score + negative_score) / (total_words_count + 0.000001)
    
    avg_sentence_length = total_words_count / (total_sentences_count + 0.000001)
    
    complex_word_count = sum(1 for word in clean_words if is_complex(word))
    percentage_complex_words = complex_word_count / (total_words_count + 0.000001)
    
    fog_index = 0.4 * (avg_sentence_length + percentage_complex_words)
    
    syllable_per_word = sum(count_syllables(word) for word in clean_words) / (total_words_count + 0.000001)
    
    pronoun_regex = r'\b(I|we|my|ours|us)\b'
    personal_pronoun_count = len(re.findall(pronoun_regex, text, re.I))
    personal_pronoun_count -= text.count('US') 
    
    avg_word_length = sum(len(word) for word in clean_words) / (total_words_count + 0.000001)

    return {
        'POSITIVE SCORE': positive_score,
        'NEGATIVE SCORE': negative_score,
        'POLARITY SCORE': polarity_score,
        'SUBJECTIVITY SCORE': subjectivity_score,
        'AVG SENTENCE LENGTH': avg_sentence_length,
        'PERCENTAGE OF COMPLEX WORDS': percentage_complex_words,
        'FOG INDEX': fog_index,
        'AVG NUMBER OF WORDS PER SENTENCE': avg_sentence_length,
        'COMPLEX WORD COUNT': complex_word_count,
        'WORD COUNT': total_words_count,
        'SYLLABLE PER WORD': syllable_per_word,
        'PERSONAL PRONOUNS': personal_pronoun_count,
        'AVG WORD LENGTH': avg_word_length
    }


def main():
    """Main function to run the entire process."""
    try:
        df = pd.read_excel(INPUT_FILE)
    except FileNotFoundError:
        print(f"Error: {INPUT_FILE} not found. Please ensure it is in the same directory.")
        return

    chrome_options = Options()
    chrome_options.add_argument('--headless') 
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-dev-shm-usage')
    
    try:
        driver = webdriver.Chrome(options=chrome_options)
    except Exception as e:
        print(f"Error initializing WebDriver: {e}")
        print("Please ensure you have a WebDriver (e.g., chromedriver) installed and its path is correctly configured.")
        return

    output_rows = []

    for index, row in df.iterrows():
        url_id = row['URL_ID']
        url = row['URL']
        
        print(f"Processing URL_ID: {url_id}...")
        
        title, article_text = extract_article_text_selenium(url, driver)
        save_article_text(url_id, title, article_text)
        
        analysis_results = analyze_text(article_text)
        
        output_row = {
            'URL_ID': url_id,
            'URL': url
        }
        output_row.update(analysis_results)
        output_rows.append(output_row)

    driver.quit()

    output_df = pd.DataFrame(output_rows)
    output_df.to_csv(OUTPUT_FILE, index=False)
    print(f"\nProcessing complete. Output saved to {OUTPUT_FILE}")

if __name__ == "__main__":
    main()