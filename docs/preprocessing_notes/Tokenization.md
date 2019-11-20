#### 1. Stanford : 

#### `Interface Tokenizer<T>`

```
public interface Tokenizer<T>
extends Iterator<T>
```

* A Tokenizer extends the Iterator interface, but provides a lookahead operation `peek()`



**Method and Description**

`hasNext()`: 

	* boolean
	* Returns `true` if and only if this Tokenizer has more elements.

`next()`:

* `T`

* Returns the next token from this Tokenizer.

`peek()`

* `T`
* Returns the next token, without removing it, from the Tokenizer, so that the same token will be again returned on the next call to next() or peek().

`remove()`

* void
* Removes from the underlying collection the last element returned by the iterator.

`tokenize()`

* `List<T>`
* Returns all tokens of this Tokenizer as a List for convenience.

##### Appendix:

https://nlp.stanford.edu/nlp/javadoc/javanlp-3.5.0/edu/stanford/nlp/process/Tokenizer.html#peek--

#### 2. Apache OpenNLP

###### 1) Tokenization

* Multiple tokenizer implementation:
  * **Whitespace Tokenizer** - A whitespace tokenizer, non whitespace sequences are identified as tokens
  * **Simple Tokenizer** - A character class tokenizer, sequences of the same character class are tokens
  * **Learnable Tokenizer** - A maximum entropy tokenizer, detects token boundaries based on probability model

* API : The Tokenizers can be integrated into an application by the defined API

  * Example: how a model can be loaded.

  ```
  try (InputStream modelIn = new FileInputStream("en-token.bin")) {
    TokenizerModel model = new TokenizerModel(modelIn);
  }
  ```

  After the model is loaded the TokenizerME can be instantiated.

  ```
  Tokenizer tokenizer = new TokenizerME(model);
  ```

  returns an array of Strings, where each String is one token.

  ```
  String tokens[] = tokenizer.tokenize("An input sample sentence.");
  ```

  output:

  ```
  "An", "input", "sample", "sentence", "."
  ```

  * second method: 

    tokenizePos returns an array of Spans, each Span contain the begin and end character offsets of the token in the input String.

  ```
  Span tokenSpans[] = tokenizer.tokenizePos("An input sample sentence.");	
  
  TokenizerME tokenizer = ...
  
  String tokens[] = tokenizer.tokenize(...);
  double tokenProbs[] = tokenizer.getTokenProbabilities();	
  ```

  The tokenProbs array now contains one double value per token, the value is between 0 and 1, where 1 is the highest possible probability and 0 the lowest possible probability.

###### 2) Tokenizer Traning

* Traning tool

OpenNLP has a **command line tool** which is used to train the models available from the model download page on various corpora. 

###### #examples can be seen in Appendix

* Traning API

The Tokenizer offers an API to train a new tokenization model. Basically three steps are necessary to train it:

​		* The application must open a sample data stream

​		* Call the TokenizerME.train method

​		* Save the TokenizerModel to a file or directly use it

###### #examples can be seen in Appendix

###### 3) Detokenizing 



##### Appendix: 

##### https://opennlp.apache.org/docs/1.9.1/manual/opennlp.html#tools.tokenizer

#### 3. NLTK (Natural Language Toolkit)

it is a python library to make programs that work with natural language. 

* provide easy-to-use interfaces : [over 50 corpora and lexical resources](http://www.nltk.org/nltk_data/) , such as WordNet . 
* The library can perform different operations such as tokenizing, stemming, classification, parsing, tagging, and semantic reasoning.

Reference book **[Natural Language Processing with Python](http://nltk.org/book)**

* avaliable at: http://www.nltk.org/book/

* a practical introduction to programming for language processing
* guides the reader through the fundamentals of writing Python programs, working with corpora, categorizing text, analyzing linguistic structure, and more.

Install `nltk`, download datasets:

* see: 

https://www.datacamp.com/community/tutorials/stemming-lemmatization-python

###### Examples can be seen in Appendix

#### Appendix:

http://www.nltk.org