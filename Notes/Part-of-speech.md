#### 1. Rule-based POS Tagging — set of rules constructed manually

* use dictionary or lexicon for getting possible tags for tagging each word
* if a word has more than one possible tag, then use hand-written rules to identify the correct tag.
* disambiguation can also be performed in rule-based tagging by analyzing the linguistic features of a word along with its preceding as well as following words.

#### 2. Stochastic POS Tagging (HMM) — high accuracy

* finding the sequence of tags which is most likely to have generated a given word sequence. 
* model this process by using HMM, where **tags** are the **hidden states** that produced the **observable output,** i.e., the **words**.

* components:
  * A : tag transition probabilities P(ti |ti−1) which represent the probability of a tag occurring given the previous tag. 
  * B: emission probabilities, P(wi |ti), represent the probability, given a tag (say MD), that it will be associated with a given word (say will).

##### Appendix:

https://www.tutorialspoint.com/natural_language_processing/natural_language_processing_part_of_speech_tagging.htm

http://web.stanford.edu/~jurafsky/slp3/8.pdf





#### 3. one example: rule-based POS — use patches

* Ads:

1) robust,  the rules are automatically acquired.

2) a vast reduction in stored information required

3)  the perspicuity of a small set of meaningful rules as opposed to the large tables of statistics needed for stochastic taggers

4) ease of finding and implementing improvements to the tagger

5) better portability from one tag set or corpus genre to another. 

* Steps:

1) the test corpus was tagged by the simple lexical tagger. 

2) each of the **patches** was in turn applied to the corpus

![image-20191110200353517](/Users/yiizHeeen/Desktop/image-20191110200353517.png)

###### Example of patches see:

https://www.aclweb.org/anthology/H92-1022.pdf

