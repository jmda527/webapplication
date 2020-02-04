import numpy as np
import pandas as pd
import glob
import jieba as jb
import pickle
import sqlite3
import os
from sklearn.naive_bayes import MultinomialNB
from sklearn.model_selection import GridSearchCV
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer


class Trash_sep(object):
    trash=['、','。','(',')','「','」','《','》','：','-','─','，','（','）','『 ','』',' : ','_']
    names = []
    maxtran = []
    model_jmda = []

    def __init__(self,place='危險物品管理組'):
        self.place = place

    def cutword(self,string):
        cutstr = ' '.join(jb.cut(string))
        for i in self.trash:
            while i in cutstr:
                cutstr=cutstr.replace(i,'')
        return cutstr

    def preproccessing_direct(self,xlsx):
        data = pd.read_excel(xlsx)
        data['主旨'] = data['主旨'].astype('str')
        data.dropna(inplace=True)
        data_cut = data.iloc[:]
        data_cut['主旨'] = data['主旨'].apply(self.cutword)

        # transfer names to numbers
        trans = LabelEncoder().fit(data_cut['承辦人'])
        self.names = trans.classes_
        data_cut['承辦人'] = trans.transform(data_cut['承辦人'])
        x_train, x_test, y_train, y_test = train_test_split(data_cut['主旨'], data_cut['承辦人'], test_size=0.2,
                                                            random_state=0)

        # transfer words into vectors
        self.maxtran = TfidfVectorizer()
        self.maxtran.fit(data_cut['主旨'])
        matric = self.maxtran.transform(x_train)

        # create model
        self.model_jmda = MultinomialNB()
        param = {'alpha': np.linspace(0.01, 0.1, 50)}
        grid = GridSearchCV(self.model_jmda, param, cv=10, scoring='accuracy')
        grid.fit(matric, y_train)
        alpha_best = grid.best_params_['alpha']
        self.model_jmda = MultinomialNB(alpha=alpha_best)
        self.model_jmda.fit(matric, y_train)

    def predicting(self,words):
        word_cut=self.cutword(words)
        word_vector=self.maxtran.transform([word_cut])
        prob = np.round(self.model_jmda.predict_proba(word_vector)*100,2)[0]
        score_dict = pd.Series({i:j for i,j in zip(self.names,prob)}).sort_values(ascending=False)[0:3]
        first_score = float(score_dict[0])
        name_list = score_dict.index
        score_list = score_dict.values
        return name_list,score_list,first_score
