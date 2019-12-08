import pandas as pd
import numpy as np
from biz.getCosine import get_word_vector as gwv, cos_dist as cd

# local test file path
file_path = '../data/test_data_4.csv'
data = pd.read_csv(file_path, header=None)
data.columns = ['No.', 'docu_id', 'mention', 'fb_id', 'fb_score', 'entity']

# get 'mention''s value
data_mention = data["mention"].drop_duplicates()
mentions = data_mention.values

for mention in mentions:

    # get the list of 'entity'
    entity = data[data['mention'] == mention]['entity'].values
    # calculate cosine similarity for the first 'entity'
    similarity_entity = entity[0]
    vec1, vec2 = gwv(mention, entity[0])
    similarity = cd(vec1, vec2)
    # print("start")
    # print(similarity_entity)
    # print(similarity)
    for i in range(1, len(entity)):
        vec1, vec2 = gwv(mention, entity[i])
        # if cosine similarity not equal
        if similarity < cd(vec1, vec2):
            similarity = cd(vec1, vec2)
            similarity_entity = entity[i]
            # if equal, compare 'fb_score'
        elif similarity == cd(vec1, vec2):
            score1 = data['fb_score'][data['mention'] == mention][data['entity'] == similarity_entity].values[0]
            score2 = data['fb_score'][data['mention'] == mention][data['entity'] == entity[i]].values[0]

            if score1 < score2:
                similarity = cd(vec1, vec2)
                similarity_entity = entity[i]
            else:
                pass
        else:
            pass
    data_result = data[data['mention'] == mention][data['entity'] == similarity_entity]
    df_data_result = pd.DataFrame(data_result)
    df_data_result['similarity'] = similarity
    print(df_data_result)

