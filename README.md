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
```

### NLTK Data
Download the necessary NLTK data for tokenization by running the following commands in a Python environment:
```python
import nltk
nltk.download('punkt')
```

### WebDriver
- Install ChromeDriver that matches your Chrome browser version.
- Ensure ChromeDriver is added to your system's PATH. You can download it from the official ChromeDriver website.

### Directory Structure
Ensure the following files and folders are in the same directory as your `assignment.py` script:

- `Input.xlsx`: The input Excel file containing URL_ID and URL columns.
- `MasterDictionary`: A folder containing positive and negative word lists.
- `StopWords`: A folder containing stopword lists.

Example directory structure:
```
textproject_directory/
├── assignment.py
├── Input.xlsx
├── MasterDictionary/
│   ├── positive-words.txt
│   ├── negative-words.txt
├── StopWords/
│   ├── stopwords1.txt
│   ├── stopwords2.txt
│   └── ...
```

### Execution
Run the script from your terminal using:
```bash
python assignment.py
```

## Output
- The script creates a folder named `extracted_articles_selenium` containing individual `.txt` files for each article, named by their `URL_ID`.
- A CSV file named `Output Data Structure.csv` is generated, containing all calculated sentiment and readability metrics for each article.

## Notes
- Ensure a stable internet connection, as the script relies on accessing URLs via Selenium.
- Verify that the ChromeDriver version matches your installed Chrome browser version to avoid compatibility issues.
- The script assumes that the `Input.xlsx` file and dictionary/stopword files are correctly formatted and accessible.
- If you encounter issues with NLTK data, ensure `nltk.download('punkt')` has been executed successfully.
- The script will automatically create the `extracted_articles_selenium` folder if it does not already exist.

---

### Changes Made
- Integrated the additional details into the existing README structure without duplicating content.
- Added the NLTK data download instructions under the **NLTK Data** section, ensuring clarity about running `import nltk` and `nltk.download('punkt')`.
- Included the WebDriver instructions under the **WebDriver** section, emphasizing the need for ChromeDriver to match the Chrome browser version and be in the system's PATH.
- Reinforced the **Directory Structure** section with the requirement for `Input.xlsx`, `MasterDictionary`, and `StopWords` to be in the same directory as `assignment.py`.
- Added the execution command `python assignment.py` under the **Execution** section.
- Included the output details (creation of `extracted_articles_selenium` folder and `Output Data Structure.csv`) in the **Output** section.
- Maintained a clean, professional markdown format with consistent headings, bullet points, and code blocks.
