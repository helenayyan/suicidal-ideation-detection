"""
Expands contractions, removes stopwords, etc and writes the posts in a json files with key as user id and value as list of posts (=5)
Input Files:
word_contractions_expansion.json, combined_data_Task_A.csv, trainUserIds_TaskA_Final.csv OR testUserIds_TaskA_Final.csv, task_A_train.posts.csv
Output Files:
User_To_Posts.json
"""

import csv
from datetime import datetime
from nltk.corpus import stopwords
import nltk
import re
import unidecode
import json
#import random
from collections import defaultdict


with open('C:\\CLPsych Challenge\\Dataset\\PreProcessing\\word_contractions_expansion.json') as f:
    cList = json.load(f)

c_re = re.compile('(%s)' % '|'.join(cList.keys()))

sw = stopwords.words("english")
extra_stop_words = ["cannot", "could", "would", "us", "may", "might", "need", "ought", "shall", "alls", "n't", "'s", "'ve", "'t", "'m", "'d", "'ll", "t"]
sw.extend(extra_stop_words)


def expandContractions(text, c_re=c_re):
    def replace(match):
        return cList[match.group(0)]
    return c_re.sub(replace, text)


def humanize_unixtime(unix_time):
    time = datetime.fromtimestamp(int(unix_time)).strftime('%d-%m-%Y %H.%M')
    return time


def word_cleaner(word):
    word = unidecode.unidecode(word)
    if(word.lower() in sw):
        word = " "
        
    word = word.replace("_PERSON_", " ")
    word = word.replace("_IP_", " ")
    word = word.replace("_EMAIL_", " ")
    word = word.replace("_URL_", " ")
    word = word.replace("tldr", " ")
    word = word.replace("&lt", " ")
    # word = word.replace(".", " ")
    p = re.compile('([A-Za-z]+)[.]')
    word = p.sub(r'\1 ', word)
    p = re.compile('[.]([A-Za-z]+)')
    word = p.sub(r' \1', word)
    word = word.replace("!", " ")
    word = word.replace(",", " ")
    word = word.replace("/", " ")
    word = word.replace("~", " ")
    # word = word.replace("-", " ")
    word = word.replace("--", " ")
    word = word.replace("-", " ")
    word = word.replace("(", " ")
    word = word.replace(")", " ")
    word = word.replace("#", " ")
    word = word.replace("?", " ")
    word = word.replace("..", " ")
    word = word.replace("...", " ")
    word = word.replace("???", " ")
    word = word.replace(":", " ")
    word = word.replace("[", " ")
    word = word.replace("]", " ")
    word = word.replace("*", " ")
    word = word.replace("\"", " ")
    word = word.replace("&", " ")
    word = word.replace("{", " ")
    word = word.replace("}", " ")
    word = word.replace("@", " ")
    word = word.replace("???", " ")
    word = word.replace("$", " ")
    word = word.replace("^", " ")
    word = word.replace("\n", " ")
    word = word.replace("\t", " ")
    word = word.replace("\r", " ")
    word = word.replace("`", " ")
    word = word.replace("'", " ")
    word = word.replace(";", " ")
    #if(word == "." or word == " ." or word == " . " or word == ". "):
    if(len(word) == 1 or word == "." or word == " ." or word == " . " or word == ". "):
        word = " "
    return word

path ="C:\\CLPsych Challenge\\Dataset\\clpsych19_training_data\\combined_data_Task_A.csv"
all_data = dict()
file = open(path, 'r', encoding = 'utf8')
reader_data = csv.reader(file)
for i, row in enumerate(reader_data):
    if(i == 0):
        continue
    all_data[(row[0], row[1])] = row


train_user_label_path ="C:\\CLPsych Challenge\\Dataset\\clpsych19_training_data\\trainUserIds_TaskA_Final.csv"
file =open(train_user_label_path, 'r', encoding = 'utf8')
reader_train = csv.reader(file, delimiter=',')
train_user_id_label = dict()
for row in reader_train:
    train_user_id_label[row[0]] = row[1]


taskA_path ="C:\\CLPsych Challenge\\Dataset\\clpsych19_training_data\\task_A_train.posts.csv"


file =open(taskA_path, 'r', encoding = 'utf8')
reader_user = csv.reader(file, delimiter=',')
taskA_user_posts = defaultdict(list)
for i, row in enumerate(reader_user):
    if(i == 0):
        continue
    taskA_user_posts[row[1]].append(row[0])

just_user_posts_train = list()

posts_users_individual = defaultdict(list)

for user in taskA_user_posts:
    user_posts = list()
    for row in taskA_user_posts[user]:
        user_posts.append(all_data[(row, user)])
    posts_sorted_by_date = sorted(user_posts, key=lambda x : x[3], reverse=True)
    for i, post in enumerate(posts_sorted_by_date):
        user_post_combined = ""
        user_id = post[1]
        post[4] = expandContractions(post[4])
        post[4] =' '.join(post[4].split('\t'))
        post[4] ='.'.join(post[4].split('\n'))
        post[4] =' '.join(post[4].split('|'))
        post[4] =' '.join(post[4].split('\r'))
        
        post[5] = expandContractions(post[5])
        post[5] =' '.join(post[5].split('\t'))
        post[5] ='.'.join(post[5].split('\n'))
        post[5] =' '.join(post[5].split('|'))
        post[5] =' '.join(post[5].split('\r'))
        
        word_tokenized_title = nltk.word_tokenize(post[4])
        word_tokenized_post = nltk.word_tokenize(post[5])

        for word in word_tokenized_title:
            user_post_combined += word_cleaner(word) + " "
        
        for word in word_tokenized_post:
            user_post_combined += word_cleaner(word) + " "
        user_post_combined = re.sub(' +', ' ',user_post_combined)
        #user_post_combined = ' '.join(user_post_combined.split(' '))
        user_post_combined = user_post_combined.strip()
        user_post_combined = user_post_combined.lower()
        posts_users_individual[user_id].append(user_post_combined)
        just_user_posts_train.append(user_post_combined)

"""
with open("C:\\CLPsych Challenge\\Dataset\\PreProcessing\\Non-PreProcessed-Data\\User_Posts_Processed_Train_Full_Final.tsv",'w', encoding = 'utf8', newline='') as outcsv:
        writer = csv.writer(outcsv, delimiter='\t',quotechar = '"')
        for row in all_train_posts_of_users_combined:
            writer.writerow(row)

with open("C:\\CLPsych Challenge\\Dataset\\PreProcessing\\Non-PreProcessed-Data\\User_Posts_Processed_Test_Final.tsv",'w', encoding = 'utf8', newline='') as outcsv:              
        writer = csv.writer(outcsv, delimiter='\t', quotechar = '"')
        for row in all_test_posts_of_users_combined:
            writer.writerow(row)
"""
#with open("C:\\CLPsych Challenge\\Dataset\\PreProcessing\\Full_Train_Data.tsv",'w', encoding = 'utf8', newline='') as outcsv:   
#        writer = csv.writer(outcsv, delimiter='\t', quotechar = '"')
#        for row in all_test_posts_of_users_combined:
#            writer.writerow(row)
#        for i, row in enumerate(all_train_posts_of_users_combined):
#            if(i == 0):
#                continue
#            writer.writerow(row)
       
with open("C:\\CLPsych Challenge\\Dataset\\PreProcessing\\Only_User_Posts_Train.txt",'w', encoding = 'utf8', newline='') as outcsv:   
        writer = csv.writer(outcsv,quotechar='"')
        for row in just_user_posts_train:
            writer.writerow([row])

with open('C:\\CLPsych Challenge\\Dataset\\PreProcessing\\User_To_Posts.json', 'w') as fp:
    json.dump(posts_users_individual, fp)