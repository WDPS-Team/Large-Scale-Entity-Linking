#### 1. Constituency parsing 

breaks a text into sub-phrases. Non-terminals in the tree are types of phrases, the terminals are the words in the sentence, and the edges are unlabeled.

###### Example: "John sees Bill"

![image-20191110202218463](/Users/yiizHeeen/Desktop/image-20191110202218463.png)

#### 2. Dependency parsing

connects words according to their relationships. Each vertex in the tree represents a word, child nodes are words that are dependent on the parent, and edges are labeled by the relationship.

![image-20191110202250239](/Users/yiizHeeen/Desktop/image-20191110202250239.png)

#### 3. How to choose? 

* If you are interested in sub-phrases within the sentence, you probably want the constituency parse. 
* If you are interested in the dependency relationships between words, then you probably want the dependency parse.

###### In fact, the way it really works is to always parse the sentence with the constituency parser, and if needed, it performs a deterministic (rule-based) transformation on the constituency parse tree to convert it into a dependency tree.

