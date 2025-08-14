# Sentiment-Readability-Engine

A Python script for extracting, preprocessing, and analyzing text from articles to calculate sentiment and readability metrics. The script processes URLs from an input Excel file, extracts article content, cleans the text, performs sentiment and readability analysis, and saves the results in a CSV file.

## Table of Contents
- [Overview](#overview)
- [Core Logic](#core-logic)
  - [Data Extraction](#data-extraction)
  - [Text Preprocessing](#text-preprocessing)
  - [Text Analysis](#text-analysis)
- [How to Run the Script](#how-to-run-the-script)
  - [Dependencies](#dependencies)
  - [NLTK Data](#nltk-data)
  - [WebDriver](#webdriver)
  - [Directory Structure](#directory-structure)
  - [Execution](#execution)
- [Output](#output)

## Overview
The **Sentimental Scraper** is designed to scrape article content from URLs listed in an Excel file, preprocess the extracted text, and compute various sentiment and readability metrics. The script uses Selenium for web scraping, BeautifulSoup for parsing HTML, and NLTK for text processing. The results are saved in a structured CSV file for further analysis.

## Core Logic
The script's workflow is divided into three main stages:

### Data Extraction
- Reads the `Input.xlsx` file to retrieve `URL_ID` and `URL` for each article.
- Uses **Selenium** to open each URL and fetch the complete web page content.
- Employs **BeautifulSoup** to parse the HTML and extract the article's title and main body text.
- Removes unnecessary elements like footers, share buttons, or advertisements to ensure clean text.
- Saves the extracted title and article text for each `URL_ID` into separate `.txt` files in a folder named `extracted_articles_selenium` for further processing.

### Text Preprocessing
- Cleans the extracted text to prepare it for analysis.
- Loads **StopWords** from the provided `StopWords` directory to create a list of words to ignore during analysis.
- Loads the **MasterDictionary** to obtain lists of positive and negative words for sentiment analysis.
- Removes punctuation from the text.
- Tokenizes the text into individual words using NLTK.
- Converts all words to lowercase for consistency.
- Filters out any words that appear in the stopword list.

### Text Analysis
- Performs sentiment and readability analysis on the preprocessed text.
- Calculates **sentiment scores**:
  - Positive Score
  - Negative Score
  - Polarity Score
  - Subjectivity Score
- Computes **readability metrics**:
  - Average Sentence Length
  - Percentage of Complex Words
  - Fog Index
- Determines additional metrics:
  - Word Count
  - Syllable per Word
  - Personal Pronouns
  - Average Word Length
- Saves all calculated metrics into a single CSV file named `Output Data Structure.csv`.

## How to Run the Script

### Dependencies
Install the required Python libraries using the following command:
```bash
pip install pandas selenium beautifulsoup4 nltk
