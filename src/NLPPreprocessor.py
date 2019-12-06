import nltk
from nltk.stem import WordNetLemmatizer
from nltk.corpus import stopwords
from stop_words import get_stop_words

class NLPPreprocessor:
    def __init__(self, text_rdd):
        self.text_rdd = text_rdd

    def tokenization(self):
        def execute(row):
            stop_words = stopwords.words('english')

            def stopwords_removal(sentence):
                tokenized_sentence = nltk.tokenize.word_tokenize(sentence)
                return tokenized_sentence
            row["sentences_tokenized"] = [stopwords_removal(s) for s in row["sentences"]]
            return row
        
        self.text_rdd = self.text_rdd.map(execute)
        return self.text_rdd

    def lemmatize(self):

        def execute_lemmatize(row):
            lemmatizer = WordNetLemmatizer()
            row["lemmatized_sentences"] = [ [lemmatizer.lemmatize(word) for word in sentence] for sentence in row["sentences_tokenized"]] 
            return row
        self.text_rdd = self.text_rdd.map(execute_lemmatize)
        return self.text_rdd

    
    def stop_words(self):

        stop_words = stopwords.words('english')
        def execute_stop_words(row):
            # NLTK Stopwords
            row["sentences_wo_sw"] = [ [word for word in s if word not in stop_words] for s in row["lemmatized_sentences"] ]
            # Other Stopwords
            row["sentences_wo_sw"] = [ [word for word in s if word not in get_stop_words('english')] for s in row["sentences_wo_sw"] ]
            return row
        self.text_rdd = self.text_rdd.map(execute_stop_words)
        return self.text_rdd

    def word_fixes(self):
        def apply_word_fixes(row):

            def fix_word(word):
                if word.lower() == "U.S.":
                    return "US"
                return word
            row["npl_text"] = [ [fix_word(word) for word in sentence] for sentence in row["sentences_wo_sw"]] 
            return row
        self.text_rdd = self.text_rdd.map(apply_word_fixes)
        return self.text_rdd


    def words_to_str(self):
        def convert_words_to_str(row):
            row["npl_text"] = [ " ".join(s) for s in row["npl_text"] ]
            return row
        self.text_rdd = self.text_rdd.map(convert_words_to_str)
        return self.text_rdd

        

