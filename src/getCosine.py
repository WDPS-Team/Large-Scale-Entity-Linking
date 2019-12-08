import re
import numpy as np

def get_word_vector(s1, s2):
    """
    :param s1: sentence 1
    :param s2: sentence 2
    :return: return the vector after split
    """

    # split the sentence by the words
    regEx = re.compile('[\\W]*')
    res = re.compile(r"([\u4e00-\u9fa5])")

    p1 = regEx.split(s1.lower())
    str1_list = []
    for str in p1:
        if res.split(str) == None:
            str1_list.append(str)
        else:
            ret = res.split(str)
            for ch in ret:
                str1_list.append(ch)
    # print(str1_list)

    p2 = regEx.split(s2.lower())
    str2_list = []
    for str in p2:
        if res.split(str) == None:
            str2_list.append(str)
        else:
            ret = res.split(str)
            for ch in ret:
                str2_list.append(ch)
    # print(str2_list)

    list_word1 = [w for w in str1_list if len(w.strip()) > 0]  # delete the null character
    list_word2 = [w for w in str2_list if len(w.strip()) > 0]  # delete the null character
   # print(list_word1, list_word2)

    # list all the words and get the union of them
    key_word = list(set(list_word1 + list_word2))
  #  print(key_word)
    # matrix storage vector filled with 0 for given shape and type
    word_vector1 = np.zeros(len(key_word))
    word_vector2 = np.zeros(len(key_word))

    # calculate the frequencies
    # determine the value of each position of the vector in turn
    for i in range(len(key_word)):
        # Traversing the number of times each word in sentence in key_word
        for j in range(len(list_word1)):
            if key_word[i] == list_word1[j]:
                word_vector1[i] += 1
        for k in range(len(list_word2)):
            if key_word[i] == list_word2[k]:
                word_vector2[i] += 1

    # return the vector
   # print(word_vector1)
   # print(word_vector2)
    return word_vector1, word_vector2




def cos_dist(vec1, vec2):
    """
    :param vec1: vector 1
    :param vec2: vector 2
    :return: Return cosine similarity of two vectors
    """
    dist1 = float(np.dot(vec1, vec2) / (np.linalg.norm(vec1) * np.linalg.norm(vec2)))
    return dist1

