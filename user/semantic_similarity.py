from sentence_transformers import SentenceTransformer,util
import nltk
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
import string 
from upstash_vector import Index
import os
import pickle
import numpy as np
from django.conf import settings


#connection with upstash vector database
index = Index(url="https://evident-marten-67544-us1-vector.upstash.io", token="ABgFMGV2aWRlbnQtbWFydGVuLTY3NTQ0LXVzMWFkbWluTXpoaFl6VTRNemt0WXpZeE9DMDBOMk16TFdJMk1XUXRPR1F4WVdWbE5tTmlaVEJt")

#Reading transformer for embedding of sentence
file_path = settings.MODEL_PATH
model=SentenceTransformer(file_path)


#preprocessing input complaint
def expansion(text):
  text = str(text).lower().strip()

  # Replace certain special characters with their string equivalents
  text = text.replace('%', ' percent')
  text = text.replace('$', ' dollar ')
  text = text.replace('₹', ' rupee ')
  text = text.replace('€', ' euro ')
  text = text.replace('@', ' at ')

  contractions = {
    "ain't": "am not",
    "aren't": "are not",
    "can't": "can not",
    "can't've": "can not have",
    "'cause": "because",
    "could've": "could have",
    "couldn't": "could not",
    "couldn't've": "could not have",
    "didn't": "did not",
    "doesn't": "does not",
    "don't": "do not",
    "hadn't": "had not",
    "hadn't've": "had not have",
    "hasn't": "has not",
    "haven't": "have not",
    "he'd": "he would",
    "he'd've": "he would have",
    "he'll": "he will",
    "he'll've": "he will have",
    "he's": "he is",
    "how'd": "how did",
    "how'd'y": "how do you",
    "how'll": "how will",
    "how's": "how is",
    "i'd": "i would",
    "i'd've": "i would have",
    "i'll": "i will",
    "i'll've": "i will have",
    "i'm": "i am",
    "i've": "i have",
    "isn't": "is not",
    "it'd": "it would",
    "it'd've": "it would have",
    "it'll": "it will",
    "it'll've": "it will have",
    "it's": "it is",
    "let's": "let us",
    "ma'am": "madam",
    "mayn't": "may not",
    "might've": "might have",
    "mightn't": "might not",
    "mightn't've": "might not have",
    "must've": "must have",
    "mustn't": "must not",
    "mustn't've": "must not have",
    "needn't": "need not",
    "needn't've": "need not have",
    "o'clock": "of the clock",
    "oughtn't": "ought not",
    "oughtn't've": "ought not have",
    "shan't": "shall not",
    "sha'n't": "shall not",
    "shan't've": "shall not have",
    "she'd": "she would",
    "she'd've": "she would have",
    "she'll": "she will",
    "she'll've": "she will have",
    "she's": "she is",
    "should've": "should have",
    "shouldn't": "should not",
    "shouldn't've": "should not have",
    "so've": "so have",
    "so's": "so as",
    "that'd": "that would",
    "that'd've": "that would have",
    "that's": "that is",
    "there'd": "there would",
    "there'd've": "there would have",
    "there's": "there is",
    "they'd": "they would",
    "they'd've": "they would have",
    "they'll": "they will",
    "they'll've": "they will have",
    "they're": "they are",
    "they've": "they have",
    "to've": "to have",
    "wasn't": "was not",
    "we'd": "we would",
    "we'd've": "we would have",
    "we'll": "we will",
    "we'll've": "we will have",
    "we're": "we are",
    "we've": "we have",
    "weren't": "were not",
    "what'll": "what will",
    "what'll've": "what will have",
    "what're": "what are",
    "what's": "what is",
    "what've": "what have",
    "when's": "when is",
    "when've": "when have",
    "where'd": "where did",
    "where's": "where is",
    "where've": "where have",
    "who'll": "who will",
    "who'll've": "who will have",
    "who's": "who is",
    "who've": "who have",
    "why's": "why is",
    "why've": "why have",
    "will've": "will have",
    "won't": "will not",
    "won't've": "will not have",
    "would've": "would have",
    "wouldn't": "would not",
    "wouldn't've": "would not have",
    "y'all": "you all",
    "y'all'd": "you all would",
    "y'all'd've": "you all would have",
    "y'all're": "you all are",
    "y'all've": "you all have",
    "you'd": "you would",
    "you'd've": "you would have",
    "you'll": "you will",
    "you'll've": "you will have",
    "you're": "you are",
    "you've": "you have"
    }


  text_decontracted=[]
  for word in text.split():
    if word in contractions:
      word=contractions[word]
    text_decontracted.append(word)
  text=" ".join(text_decontracted)
  text=text.replace("'ve",'have')
  text=text.replace("n't",'not')
  text=text.replace("'re",'are')
  text=text.replace("'ll",'will')
  return text




#removing stopwords
stop_words=set(stopwords.words('english'))
lemmatizer=WordNetLemmatizer()
def remove_stopwords(text):
    text=text.translate(str.maketrans("","",string.punctuation))
    words=text.split()
    words=[lemmatizer.lemmatize(word) for word in words if word not in stop_words]
    text=" ".join(words)
    return text


#getting sentence embedding

def embedding(text):
    emb=model.encode(text,convert_to_tensor=True)
    return emb



#getting cos_sim from vector database
def get_cos_sim_from_upstash(comp_emb):
  result=index.query(
  vector=comp_emb,
  top_k=1,
  include_vectors=False,
  include_metadata=True)
  id=result[0].id
  cos_sim=result[0].score
  return id,cos_sim


def check_semantic_similarity(suggestion):
  suggestion=remove_stopwords(expansion(suggestion.lower()))
  emb=embedding(suggestion)
  id,cos_sim=get_cos_sim_from_upstash(emb)

  # reading  the classifier
  with open("D:/Django-Project/esujhavpetika/esujhavpetika/NLP_files/semantic_classifier.pkl",'rb') as file:
      clf=pickle.load(file)
      cos_sim=np.array([cos_sim])
      cos_sim=cos_sim.reshape(1,-1)
      result=clf.predict(cos_sim)
  if result:
     return id
  else:
     return 

def store_vector_of_suggestion(id,suggestion):
   emb=embedding(suggestion)
   vector=[]
   tup=(id,emb,{id:suggestion})
   vector.append(tup)
   index.upsert(vectors=vector)

   
   
  
   
   




