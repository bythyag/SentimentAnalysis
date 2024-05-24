import os
import chardet
import os
import re
import pandas as pd


# Set the folder path
folder_path = "/Users/thyag/Downloads/intershala assignment/StopWords"

# Initialize an empty list to store all words
all_words = []

# Loop through all files in the folder
for filename in os.listdir(folder_path):
    # Check if the file is a text file
    if filename.endswith(".txt"):
        # Open the file in binary mode
        file_path = os.path.join(folder_path, filename)
        with open(file_path, "rb") as file:
            raw_data = file.read()
            # Detect the encoding
            encoding = chardet.detect(raw_data)["encoding"]

        # Open the file in text mode with the detected encoding
        with open(file_path, "r", encoding=encoding) as file:
            # Read the contents of the file
            contents = file.read()
            # Split the contents into words
            words = contents.split()
            # Add the words to the all_words list
            all_words.extend(words)

stopwords= [word.lower() for word in all_words]


# Load the positive and negative word lists
positive_word_list_path = "/Users/thyag/Downloads/intershala assignment/MasterDictionary/positive-words.txt"
negative_word_list_path = "/Users/thyag/Downloads/intershala assignment/MasterDictionary/negative-words.txt"

positive_words = set()
negative_words = set()

# Detect encoding for positive word list
with open(positive_word_list_path, "rb") as file:
    raw_data = file.read()
    encoding = chardet.detect(raw_data)["encoding"]

with open(positive_word_list_path, "r", encoding=encoding) as file:
    for line in file:
        word = line.strip().lower()
        positive_words.add(word)

# Detect encoding for negative word list
with open(negative_word_list_path, "rb") as file:
    raw_data = file.read()
    encoding = chardet.detect(raw_data)["encoding"]

with open(negative_word_list_path, "r", encoding=encoding) as file:
    for line in file:
        word = line.strip().lower()
        negative_words.add(word)

#initilaise dataframe

df = pd.DataFrame()

# Directory containing the files
directory = "/Users/thyag/Downloads/intershala assignment/testFiles"

# Initialize an empty list to store file paths
file_paths = []

# Loop over files in the directory
for filename in os.listdir(directory):
    # Check if the file is a text file
    if filename.endswith(".txt"):
        # Full path to the file
        file_path = os.path.join(directory, filename)
        
        # Append the file path to the list
        file_paths.append(file_path)


#loop for making a dataframe containing all the values
for i in range(100):
    text_file_path = file_paths[i]
    with open(text_file_path, "r", encoding="utf-8") as file:
        # Skip the first line
        next(file)
        text = file.read()

    # Convert the text to lowercase
    text = text.lower()

    # Split the text into words
    text_words = text.split()
    # Remove the stop words from the text words
    filtered_words = [word for word in text_words if word not in stopwords]

    new_filtered_words = ' '.join(filtered_words)

    # Calculate positive and negative word scores
    positive_score = 0
    negative_score = 0

    for word in filtered_words:
        if word in positive_words:
            positive_score += 1
        elif word in negative_words:
            negative_score -= 1

    polarity_score = (positive_score - abs(negative_score)) / (positive_score + abs(negative_score) + 0.000001)
    Subjectivity_Score = (positive_score + abs(negative_score))/ ((len(filtered_words)) + 0.000001)


    def average_sentence_length(text):
        # Count the number of sentences
        sentences = text.split('.')
        num_sentences = len(sentences)

        # Remove empty strings
        sentences = [sentence.strip() for sentence in sentences if sentence.strip()]

        # Count the number of words
        num_words = sum(len(sentence.split()) for sentence in sentences)

        # Calculate the average sentence length
        if num_sentences > 0:
            average_length = num_words / num_sentences
        else:
            average_length = 0

        return average_length


    def count_syllables(word):
        """Count the number of syllables in a word."""
        vowels = "aeiouy"
        num_syllables = 0
        prev_char_was_vowel = False
        word = word.lower()
        
        # Handle special cases
        if word.endswith("es") or word.endswith("ed"):
            word = word[:-2]

        for char in word:
            if char in vowels:
                if not prev_char_was_vowel:
                    num_syllables += 1
                prev_char_was_vowel = True
            else:
                prev_char_was_vowel = False

        # Adjust for words ending with "le"
        if word.endswith("le") and len(word) > 2:
            num_syllables += 1

        # Ensure at least one syllable counted for non-empty words
        if len(word) > 0 and num_syllables == 0:
            num_syllables = 1

        return num_syllables

    def percentage_complex_words(text):
        # Tokenize the text into words
        words = text.split()

        # Count the number of complex words
        num_complex_words = sum(1 for word in words if count_syllables(word) > 2)

        # Calculate the total number of words
        num_words = len(words)

        # Calculate the percentage of complex words
        if num_words > 0:
            percentage = (num_complex_words / num_words) * 100
        else:
            percentage = 0

        return percentage

    # Example usage:
    #text = "This is a sample sentence with some complex words like 'complicated' and 'entanglement'."

    def count_syllables(word):
        word = word.lower()
        vowels = "aeiouy"
        count = 0
        if word[0] in vowels:
            count += 1
        for index in range(1, len(word)):
            if word[index] in vowels and word[index - 1] not in vowels:
                count += 1
        if word.endswith("e"):
            count -= 1
        if count == 0:
            count += 1
        return count

    def is_complex_word(word):
        return count_syllables(word) >= 3

    def gunning_fog_index(text):
        # Split text into sentences
        sentences = re.split(r'[.!?]', text)
        sentences = [sentence.strip() for sentence in sentences if sentence.strip()]
        
        # Split text into words
        words = re.findall(r'\w+', text)
        
        # Count complex words
        complex_words = [word for word in words if is_complex_word(word)]
        
        total_words = len(words)
        total_sentences = len(sentences)
        total_complex_words = len(complex_words)
        
        if total_sentences == 0:  # Avoid division by zero
            return 0
        
        gfi = 0.4 * ((total_words / total_sentences) + 100 * (total_complex_words / total_words))
        
        return gfi

    gfi_score = gunning_fog_index(new_filtered_words)



    def average_words_per_sentence(text):
        # Define a simple sentence tokenizer based on punctuation
        sentences = re.split(r'[.!?]+', text)
        
        # Remove any empty sentences that may result from the split
        sentences = [sentence.strip() for sentence in sentences if sentence.strip()]
        
        total_sentences = len(sentences)
        total_words = sum(len(sentence.split()) for sentence in sentences)
        
        # Calculate the average number of words per sentence
        if total_sentences == 0:
            return 0
        
        average = total_words / total_sentences
        return average

    average = average_words_per_sentence(text)


    def count_syllables(word):
        """Count the number of syllables in a word."""
        vowels = "aeiouy"
        num_syllables = 0
        prev_char_was_vowel = False
        word = word.lower()
        
        # Handle special cases
        if word.endswith("es") or word.endswith("ed"):
            word = word[:-2]

        for char in word:
            if char in vowels:
                if not prev_char_was_vowel:
                    num_syllables += 1
                prev_char_was_vowel = True
            else:
                prev_char_was_vowel = False

        # Adjust for words ending with "le"
        if word.endswith("le") and len(word) > 2:
            num_syllables += 1

        # Ensure at least one syllable counted for non-empty words
        if len(word) > 0 and num_syllables == 0:
            num_syllables = 1

        return num_syllables

    def complex_word_count(text):
        # Tokenize the text into words
        words = text.split()

        # Count the number of complex words
        num_complex_words = sum(1 for word in words if count_syllables(word) > 2)

        return num_complex_words

    # Example usage:
    #text = "This is a sample sentence with some complex words like 'complicated' and 'entanglement'."

    def count_syllables(word):
        """Count the number of syllables in a word."""
        vowels = "aeiouy"
        num_syllables = 0
        prev_char_was_vowel = False
        word = word.lower()
        
        # Handle special cases
        if word.endswith("es") or word.endswith("ed"):
            word = word[:-2]

        for char in word:
            if char in vowels:
                if not prev_char_was_vowel:
                    num_syllables += 1
                prev_char_was_vowel = True
            else:
                prev_char_was_vowel = False

        # Adjust for words ending with "le"
        if word.endswith("le") and len(word) > 2:
            num_syllables += 1

        # Ensure at least one syllable counted for non-empty words
        if len(word) > 0 and num_syllables == 0:
            num_syllables = 1

        return num_syllables

    def syllable_count_per_word(text):
        # Tokenize the text into words
        words = text.split()

        # Count the number of syllables in each word
        syllable_counts = [count_syllables(word) for word in words]

        return syllable_counts

    def average_syllables_per_word(text):
        # Get the counts of syllables per word
        syllable_counts = syllable_count_per_word(text)
        
        # Calculate the average syllable per word
        total_syllables = sum(syllable_counts)
        total_words = len(syllable_counts)
        
        if total_words > 0:
            average_syllables = total_syllables / total_words
        else:
            average_syllables = 0
        
        return average_syllables

    # Example usage:
    #text = "This is a sample sentence with some complex words like 'complicated' and 'entanglement'."

    def count_personal_pronouns(text):
        # Define the list of personal pronouns
        personal_pronouns = ["I", "we", "my", "ours", "us"]
        
        # Compile regex pattern to match personal pronouns
        pattern = r"\b(?:{})\b".format("|".join(personal_pronouns))

        # Find all matches of personal pronouns in the text
        matches = re.findall(pattern, text, flags=re.IGNORECASE)

        # Exclude matches that are part of other words (e.g., "US" as a country)
        matches = [match for match in matches if match.lower() != "us"]

        # Count the occurrences of personal pronouns
        count = len(matches)

        return count

    def average_word_length(text):
        # Tokenize the text into words
        words = text.split()

        # Calculate the total number of characters in all words
        total_characters = sum(len(word) for word in words)

        # Calculate the total number of words
        total_words = len(words)

        # Calculate the average word length
        if total_words > 0:
            average_length = total_characters / total_words
        else:
            average_length = 0

        return average_length

    new_data = {
        "POSITIVE SCORE": [positive_score],
        "NEGATIVE SCORE": [negative_score],
        "POLARITY SCORE": [polarity_score],
        "SUBJECTIVITY SCORE": [Subjectivity_Score],
        "AVG SENTENCE LENGTH": [average_sentence_length(new_filtered_words)],
        "PERCENTAGE OF COMPLEX WORDS": [percentage_complex_words(new_filtered_words)],
        "FOG INDEX": [gfi_score],
        "AVG NUMBER OF WORDS PER SENTENCE": [average],
        "COMPLEX WORD COUNT": [complex_word_count(text)],
        "WORD COUNT": [len(filtered_words)],
        "SYLLABLE PER WORD": [average_syllables_per_word(text)],
        "PERSONAL PRONOUNS": [count_personal_pronouns(text)],
        "AVG WORD LENGTH": [average_word_length(text)]
    }

    new_df = pd.DataFrame(new_data)
    # Append the new DataFrame to the existing one
    df = pd.concat([df, new_df], ignore_index=True)
    


# Load an Excel file into a DataFrame
df_index = pd.read_excel('/Users/thyag/Downloads/intershala assignment/Output Data Structure.xlsx')
#drop rest of the columns and merge with the produced dataframe and then make a csv file
df_index = df_index[['URL_ID', 'URL']]
df_merged = df_index.join(df)
df.to_excel("data.xlsx", index=False)
