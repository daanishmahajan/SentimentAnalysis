from textblob import TextBlob
import pandas as pd
import re
import html
import string
import spacy
from spacy.tokens import Doc,Span,Token
from spacymoji import Emoji
# import nltk
# nltk.download("stopwords")
from nltk.corpus import stopwords

stopwords = stopwords.words('english')
path_from="/home/daanish/Desktop/Project/MachineLearning/Twitter/Testfiles/in1.csv"
path_to="/home/daanish/Desktop/Project/MachineLearning/Twitter/Testfiles/out1.csv"
column_names=["SNo","Time","Location","Text"]
dict=("Location","Text")

# path_from="/home/daanish/Desktop/Project/MachineLearning/Twitter/Testfiles/trainin1.csv"
# path_to="/home/daanish/Desktop/Project/MachineLearning/Twitter/Testfiles/trainout1.csv"
# column_names=["Label","Text"]
# dict=["Text"]

class Preprocessing:

    def __init__(self,language="en"):
        # df=pd.read_csv(path_from,usecols=[0,1,2,3],names=column_names,header=None,nrows=5)
        df=pd.read_csv(path_from,usecols=[0,1,2,3],names=column_names,header=None)
        # df=pd.read_csv(path_from,names=column_names,encoding="ISO-8859-1",header=None)
        self.language=language
        # print(df.head())
        # return
        # Doc.set_extension(force=True)
        # Doc.set_extension(self._entities, getter=self.iter_entities, force=True)
        # Span.set_extension(force=True)
        # Span.set_extension(self._entities, getter=self.iter_entities, force=True)
        # Token.set_extension(force=True)
        # Token.set_extension(self._entity_desc, getter=self.get_entity_desc, force=True)

        self.nlp=spacy.load("en_core_web_sm",disable=["parser"])
        self.nlp.add_pipe(Emoji(self.nlp),first=True)

        for key in dict:
            # print(df[key])
            # continue
            # print("Starting Language Conversion to {0} for {1}".format(language,key))
            # self.lang(df[key])
            # print("Done Language Conversion to {0} for {1}".format(language,key))

            print("Starting Noise Removal for {0}".format(key))
            self.remove_noise(df[key])
            print("Done Noise Removal for {0}".format(key))

            if(key=="Text"):
            	# print("Starting Coreference Resolution for {0}".format(key))
            	# self.coref(df[key])
            	# print("Done Coreference Resolution for {0}".format(key))
            
                print("Starting Spellchecking for {0}".format(key))
                self.spellcheck(df[key])
                print("Done Spellchecking for {0}".format(key))

                print("Starting Lemmatisation for {0}".format(key))
                self.lemmatisation(df[key])
                print("Done Lemmatisation for {0}".format(key))			

        df.to_csv(path_to,index=False,encoding="utf-8")
        return

    # language conversion and spellchecking using TextBlob which is built over NLTK and Pattern thus making it suitable for the task
    def lang(self,texts):
        for i in range(len(texts)):
            text=TextBlob(str(texts[i]))
            try:
                text=text.translate(to="en")
                texts.at[i]=str(text)
            except Exception as e:
                print(e)					
        return 

    def spellcheck(self,texts):
        for i in range(len(texts)):
            print("Spellcheck: ",i)
            text=TextBlob(str(texts[i]))
            try:
                text=text.correct()
                texts.at[i]=str(text)
            except Exception as e:
                print(e)					
        return 

    # noise removal using regex
    def remove_noise(self,texts):
        for i in range(len(texts)):
            print("Noise: ",i)
            # print("Before: ",texts[i])
            # Hashtags
            texts.at[i]=re.sub(r"#[\w]*","",str(texts[i]))

            # Handels
            texts.at[i]=re.sub(r"@[\w]*","",str(texts[i]))

            # URLs
            texts.at[i]=re.sub(r"((www\.[^\s]+)|((http|https|ftp)://[^\s]+))","",str(texts[i]))

            # html
            texts.at[i]=html.unescape(str(texts[i]))

            # repeating characters in a word
            rpt_regex = re.compile(r"(.)\1{1,}",re.IGNORECASE)
            texts.at[i]=re.sub(rpt_regex,r"\1",str(texts[i]))

            # RT
            texts.at[i]=re.sub(r"RT","",str(texts[i]))

            # punctuations
            texts.at[i] = re.sub(r"["+string.punctuation+"?"+"]","",str(texts[i]))

            # BackSlashes
            texts.at[i]=re.sub(r"\\[\w]*","",str(texts[i]))            
            # print("After: ",texts[i])
        return

    # lemmatisation using spacy
    def lemmatisation(self,texts):
        for i in range(len(texts)):
            print("Lemma: ",i)
            doc=self.nlp(str(texts[i]))
            tokens=[]
            ents=[]
            for ent in doc.ents:
                ents.append(ent.text)
            for tok in doc:
                # removing emojis
                if(tok._.is_emoji):
                    continue
                if(tok.lemma_!="-PRON-" and tok.text not in ents):
                    tok=tok.lemma_.lower().strip()
                else:
                    tok=tok.lower_
                if(tok not in stopwords):
                    tokens.append(tok)
            texts.at[i]=str(" ".join(tokens))
        return

call=Preprocessing()
