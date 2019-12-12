import nltk
from nltk.stem import WordNetLemmatizer
from nltk.corpus import stopwords
from stop_words import get_stop_words
from nltk.corpus import wordnet


class NLPPreprocessor:
    def __init__(self, text_rdd):
        self.text_rdd = text_rdd

    def tokenization(self):
        def execute(row):
            nltk.data.path.append("venv/nltk_data")

            def stopwords_removal(sentence):
                tokenized_sentence = nltk.tokenize.word_tokenize(sentence)
                return tokenized_sentence

            row["sentences_tokenized"] = [stopwords_removal(s) for s in row["sentences"]]
            return row

        self.text_rdd = self.text_rdd.map(execute)
        return self.text_rdd

# way 1 - pos and then lemma
    # def pos(self):
    #     def get_wordnet_pos(treebank_tag):
    #         if treebank_tag.startswith('J'):
    #             return wordnet.ADJ
    #         elif treebank_tag.startswith('V'):
    #             return wordnet.VERB
    #         elif treebank_tag.startswith('N'):
    #             return wordnet.NOUN
    #         elif treebank_tag.startswith('R'):
    #             return wordnet.ADV
    #         else:
    #             return wordnet.NOUN
    #
    #     def execute_pos(row):
    #         nltk.data.path.append("venv/nltk_data")
    #         row["sentences_pos"] = [[get_wordnet_pos(word) for word in sentence] for sentence in
    #                                 row["sentences_tokenized"]]
    #         return row
    #
    #     self.text_rdd = self.text_rdd.map(execute_pos)
    #     return self.text_rdd
    #
    # def lemmatize(self):
    #
    #     def execute_lemmatize(row):
    #         nltk.data.path.append("venv/nltk_data")
    #         lemmatizer = WordNetLemmatizer()
    #         row["lemmatized_sentences"] = [[lemmatizer.lemmatize(word) for word in sentence] for sentence in
    #                                        row["sentences_pos"]]
    #         return row
    #
    #     self.text_rdd = self.text_rdd.map(execute_lemmatize)
    #     return self.text_rdd


# way 2 - pos & lemma (in one def() )
    def lemmatize(self):

        def get_wordnet_pos(treebank_tag):

            if treebank_tag.startswith('J'):
                return wordnet.ADJ
            elif treebank_tag.startswith('V'):
                return wordnet.VERB
            elif treebank_tag.startswith('N'):
                return wordnet.NOUN
            elif treebank_tag.startswith('R'):
                return wordnet.ADV
            else:
                return None

        def execute_lemmatize(row):
            nltk.data.path.append("venv/nltk_data")
            lemmatizer = WordNetLemmatizer()
            tagged = nltk.pos_tag(row['sentences_tokenized'])
            for word, tag in tagged:
                wntag = get_wordnet_pos(tag)
                if wntag is None:
                    row["lemmatized_sentences"] = lemmatizer.lemmatize(word)
                else:
                    row["lemmatized_sentences"] = lemmatizer.lemmatize(word, pos=wntag)

            return row

        self.text_rdd = self.text_rdd.map(execute_lemmatize)
        return self.text_rdd

#get same errors:
#    "args[0] from __newobj__ args has the wrong class")
# _pickle.PicklingError: args[0] from __newobj__ args has the wrong class


    def stop_words(self):
        nltk.data.path.append("venv/nltk_data");
        stop_words = stopwords.words('english')

        def execute_stop_words(row):
            # NLTK Stopwords
            row["sentences_wo_sw"] = [[word for word in s if word not in stop_words] for s in
                                      row["lemmatized_sentences"]]
            # Other Stopwords
            row["sentences_wo_sw"] = [[word for word in s if word not in get_stop_words('english')] for s in
                                      row["sentences_wo_sw"]]
            return row

        self.text_rdd = self.text_rdd.map(execute_stop_words)
        return self.text_rdd

    def word_fixes(self):
        def apply_word_fixes(row):
            def fix_word(word):
                if word.lower() == "u.s.":
                    return "US"
                return word

            row["npl_text"] = [[fix_word(word) for word in sentence] for sentence in row["sentences_wo_sw"]]
            return row

        self.text_rdd = self.text_rdd.map(apply_word_fixes)
        return self.text_rdd

    def words_to_str(self):
        def convert_words_to_str(row):
            row["npl_text"] = [" ".join(s) for s in row["npl_text"]]
            return row

        self.text_rdd = self.text_rdd.map(convert_words_to_str)
        return self.text_rdd
