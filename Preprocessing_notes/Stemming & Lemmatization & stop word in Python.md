#### In this tutorial, we use the Python `nltk` package which is `Natural Language Tool Kit`



#### 1. Stemming with Python `nltk` package

* Porter Stemmer

  * uses **Suffix Stripping** to produce stems
  * its algorithm uses to generate stems, not often generate stems that are actual English words. 

  * Advantages: 

    1) simplicity

    2) speed

  It is commonly useful in **Information Retrieval** (IR) Environments  for **fast recall** and **fetching of search queries**. 

* Lancaster Stemmer

  * Interative algorithm, one table containing about 120 rules indexed by the last letter of a suffix.

  * Disad:

  **heavy stemming** due to iterations and **over-stemming** may occur. Over-stemming causes the stems to be not linguistic, or they may have no meaning.

##### running example

![running example](/Users/yiizHeeen/Documents/GitHub/WDPS-2019/Preprocessing_notes/pics/pycharm.png)

* Conlusion : porter is more precise than lancaster



* SnowballStemmers

  * It supports different languages. 
  * For example, in English:

  ```
  from nltk.stem.snowball import SnowballStemmer
  
  englishStemmer=SnowballStemmer("english")
  englishStemmer.stem("having")
  ```

  output:

  ```
  have
  ```



#### 2. Stop words

* need to download the `stopwords corpus` from using `nltk.download()`

* Example:

```
englishStemmer2=SnowballStemmer("english", ignore_stopwords=True)
englishStemmer2.stem("having")
```

output:

```
having
```

before using `ignore_stopwords=True`, *having* was stemmed to *have* but after using it, it is ignored by the stemmer. 



#### 3. Lemmatization

* Python NLTK provides **WordNet Lemmatizer** that uses the WordNet Database to lookup lemmas of words.
* Download the WordNet corpora before using 
  * Example:

```
import nltk
from nltk.stem import WordNetLemmatizer
wordnet_lemmatizer = WordNetLemmatizer()

sentence = "He was running and eating at same time. He has bad habit of swimming after playing long hours in the Sun."
punctuations="?:!.,;"
sentence_words = nltk.word_tokenize(sentence)
for word in sentence_words:
    if word in punctuations:
        sentence_words.remove(word)

sentence_words
print("{0:20}{1:20}".format("Word","Lemma"))
for word in sentence_words:
    print ("{0:20}{1:20}".format(word,wordnet_lemmatizer.lemmatize(word)))
```

output:

![image-20191110155033895](/Users/yiizHeeen/Documents/GitHub/WDPS-2019/Preprocessing_notes/pics/before.png)

* need to provide the context : parts-of-speech (POS)

```
for word in sentence_words:
    print ("{0:20}{1:20}".format(word,wordnet_lemmatizer.lemmatize(word, pos="v")))
```

output:

![image-20191110155147751](/Users/yiizHeeen/Documents/GitHub/WDPS-2019/Preprocessing_notes/pics/after_le.png)



#### 4. Applications 

1. Text mining 
2. Information Retrieval (IR) Environments : use stemming and lemmatization 
3. Document Clustering

##### #Details can be seen in appendix



#### 5. Stemming or Lemmatization ?

- Stemming and Lemmatization both generate the root form of the inflected words. The difference is that **stem** might not be an actual word whereas, **lemma** is an actual language word.
- **Stemming** follows an algorithm with steps to perform on the words which makes it faster. Whereas, in **lemmatization**, you used WordNet corpus and a corpus for stop words as well to produce lemma which makes it slower than stemming. You also had to define a parts-of-speech to obtain the correct lemma.
- Conclusion:
  * Focus on speed : use stemming.
  * Need accuracy : use lemmatization as it uses a corpus to match root forms.





##### Appendix: 

https://www.datacamp.com/community/tutorials/stemming-lemmatization-python

