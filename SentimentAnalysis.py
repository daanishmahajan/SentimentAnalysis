from sklearn.pipeline import Pipeline
from sklearn.naive_bayes import MultinomialNB
from sklearn.feature_extraction.text import CountVectorizer,TfidfTransformer
from sklearn.model_selection import train_test_split,GridSearchCV
from sklearn.metrics import classification_report
import pandas as pd
import numpy as np
import pickle as pk
import os

datafile="/home/daanish/Desktop/Project/MachineLearning/Twitter/Testfiles/trainout0.csv"
testfile="/home/daanish/Desktop/Project/MachineLearning/Twitter/Testfiles/out01.csv"
resfile="/home/daanish/Desktop/Project/MachineLearning/Twitter/Testfiles/outf01.csv"
modelfile="/home/daanish/Desktop/Project/MachineLearning/Twitter/model/model0.sav"
column_names_train=["Label","Text"]
column_names_test=["SNo","Time","Location","Text"]

class Model:
    def __init__(self):
        self.load_params()
        return

    def load_params(self):
        df=pd.read_csv(datafile,names=column_names_train,header=None)
        df["Text"].replace("",np.nan,inplace=True)
        df.dropna(subset=["Text"],inplace=True)
        for i in range(0,10):
            df=df.sample(frac=1).reset_index(drop=True)
        self.labels=df["Label"]
        self.data=df["Text"]

        self.text_clf=Pipeline([("vect",CountVectorizer()),
                                ("tfidf",TfidfTransformer()),
                                ("clf",MultinomialNB())])
        self.tuned_parameters={
            "vect__ngram_range":[(1,1),(1,2),(2,2)],
            "vect__max_df":[0.5,0.75,1.0],
            "tfidf__use_idf":[True,False],
            "tfidf__norm":["l1","l2"],
            "clf__alpha":[1,1e-1,1e-2,1e-4,1e-8]
        }
        return

    def train_model(self,test_size=0.33,random_state=42,cv=10,score="f1_macro"):
        try:
            if(os.path.getsize(modelfile)>0):
                return
        except OSError as e:
            print(e)
        x_train,x_test,y_train,y_test=train_test_split(self.data,self.labels,test_size=test_size,random_state=random_state)
        clf=GridSearchCV(self.text_clf,self.tuned_parameters,cv=cv,scoring=score)
        clf.fit(x_train,y_train)
        self.save_model(clf)
        print("Best_Score: ",clf.best_score_)
        print("Best_Params: ",clf.best_params_)
        print("Classification_Report_SplittedData: ",classification_report(y_test,clf.predict(x_test),digits=4))
        print("Classification_Report_CompleteData: ",classification_report(self.labels,clf.predict(self.data),digits=4))
        return

    def test_model(self,testfile=testfile):
        df=pd.read_csv(testfile,names=column_names_test,header=None)
        df["Text"].replace("",np.nan,inplace=True)
        df.dropna(subset=["Text"],inplace=True)
        model=self.load_model()
        polarity=model.predict(df["Text"])
        print(polarity)
        self.write_to_csv(df,polarity)
        return

    def save_model(self,model):
        pk.dump(model,open(modelfile,"wb"))
        return

    def load_model(self):
        model=pk.load(open(modelfile,"rb"))
        return model

    def write_to_csv(self,df,polarity):
        polarity=pd.Series(polarity)
        df.insert(loc=4,column="Label",value=polarity)
        df.to_csv(resfile,index=False,encoding="utf-8")
        return

print("Loading Model")
sentiment=Model()
print("Starting Training")
sentiment.train_model()
print("Finished Training")
print("Starting Testing")
sentiment.test_model()
print("Finished Testing")

