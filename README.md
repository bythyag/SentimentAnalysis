# Blackcoffer Data Extraction and NLP Assignment

This project is a solution to the Blackcoffer Data Extraction and NLP Assignment. The objective is to extract textual data articles from provided URLs, perform text analysis, and compute various variables.

## Project Structure

The project consists of the following files:

- `dataExtraction.ipynb`: Python script to extract article text from the given URLs
- `finalCode.py`: Python script to perform textual analysis and compute variables
- `input.xlsx`: Input file containing the list of article URLs
- `output.csv`: Output file with the computed variables for each article
- `README.md`: This file, providing an overview of the project

## Dependencies

The project requires the following Python libraries:

- BeautifulSoup
- Requests
- NLTK
- Pandas

You can install the dependencies using pip:

```
pip install beautifulsoup4 requests nltk pandas
```

## Running the Project

1. Ensure that you have Python installed on your system.
2. Install the required dependencies as mentioned above.
3. Place the `input.xlsx` file in the project directory.
4. Run the `data_extraction.py` script to extract article text from the URLs:
   ```
   python data_extraction.py
   ```
   This will generate text files for each article in the project directory.

5. Run the `data_analysis.py` script to perform textual analysis and compute variables:
   ```
   python data_analysis.py
   ```
   This will generate the `output.csv` file with the computed variables for each article.

## Approach

### Data Extraction
- Used the `requests` library to fetch the HTML content of each URL.
- Utilized `BeautifulSoup` to parse the HTML and extract the article title and text.
- Saved the extracted text in separate files named with the URL_ID.

### Data Analysis
- Loaded the extracted text files and performed textual analysis using NLTK.
- Computed variables such as positive score, negative score, polarity score, subjectivity score, etc.
- Utilized NLTK's sentiment analysis and text processing functionalities.
- Calculated additional variables like average sentence length, percentage of complex words, FOG index, etc.
- Stored the computed variables in a pandas DataFrame and exported it to `output.csv`.

## Output Structure

The output file (`output.csv`) contains the following columns:

- All input variables from `input.xlsx`
- POSITIVE SCORE
- NEGATIVE SCORE
- POLARITY SCORE
- SUBJECTIVITY SCORE
- AVG SENTENCE LENGTH
- PERCENTAGE OF COMPLEX WORDS
- FOG INDEX
- AVG NUMBER OF WORDS PER SENTENCE
- COMPLEX WORD COUNT
- WORD COUNT
- SYLLABLE PER WORD
- PERSONAL PRONOUNS
- AVG WORD LENGTH

The output follows the structure specified in the "Output Data Structure.xlsx" file.
