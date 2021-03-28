# All props to @salt rock lamp at Data Science Discord community

data['name_tokens']= data['name'].map(lambda y: thread_first(
    y,
    clean_punctuation,
    split_words,
    filter_stopwords,
))


data['name_tokens']= data['name']\
    .map(clean_punctuation)\
    .map(split_words)\
    .map(filter_stopwords)
