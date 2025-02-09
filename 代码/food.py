import extract_feature
import pymysql
# import SimpleSentence
import re
import nltk.data
import html_filter
# import SimpleFeatureExtraction
from collections import Counter
import csv


def connect_sql():
    db = pymysql.connect(
        host='localhost',
        port=3306,
        user='root',
        passwd='',
        db='googleplaydate',
        charset='utf8'
    )
    return db


# 输出：一个列表，列表中每一项是一个字典dic
# 从information表中读出的
def read_sql(app):
    # print version info
    database = connect_sql()
    cursor = database.cursor()
    sql = "SELECT * from "+app
    # sql = "SELECT * from type1 where id = 'a50indianrecipesinhindi.goyo.com.a50indianrecipesinhindi'"
    cursor.execute(sql)
    result = cursor.fetchall()
    data = []
    for row in result:
        # line = unicodedata.normalize('NFKD', row[4]).encode('ascii', 'ignore')
        #description = Filter.filters(row[4])
        dic = {'id': row[0], 'name': row[1], 'download_num': row[2],
               'score': row[3], 'description': row[4], 'price': row[5],
               'category': row[6], 'score_num': row[7]}
        data.append(dic)
    database.close()
    return data

'''def word_count():
    f = open("features.txt", 'r')
    lines = f.readlines()
    for f in lines:
        f.strip('\n')
    List_set = set(lines)
    dic_list = list()
    for item in List_set:
        # print("%s: %d" % (item, lines.count(item)))
        dic_list.append((lines.count(item), item))
    result = sorted(dic_list)
    for d in result:
        print("%s: %d" % (d[1], d[0]))


def feature_extraction(description, is_print = False):
    description_features = list()
    sentence_list = SimpleSentence.split_sent(description)  # 将描述文本拆分为句子列表(粗粒度)(变小写)
    for sentence in sentence_list:
        if is_print:
            print sentence
        # f.write("%s\n" % sentence)
        fine_sentence_list = SimpleSentence.remove_bracket(sentence)  # 去除了一些特殊字符
        for fine_sentence in fine_sentence_list:
            features = SimpleFeatureExtraction.get_sentence_feature(fine_sentence)
            for feature in features:
                if is_print:
                    print feature
                for word in feature:
                    description_features.append(word)
    return description_features'''

def temp_filters(d):
    oldS = d
    newS = ''
    character_set = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's',
                     't', 'u', 'v', 'w', 'x', 'y', 'z', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L',
                     'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z', '`', '!', '@', '#', '$',
                     '%', '^', '&', '*', '(', ')', '_', '+', '=', '-', '~', ',', '.', '/', '?', '>', '<', ';', ':',
                     '1', '2', '3', '4', '5', '6', '7', '8', '9', '0', '\'', '|', '\\', '"', '\'', ' ']

    # 删除连续的非英文字符
    for s in oldS:
        if s not in character_set:
            print('有违规字符')
            return []
        else:
            newS += s

    # print oldS
    # newS = newS.encode('utf-8')
    newS = newS.lstrip('.')
    newS = newS.strip(' ')
    newS = newS.replace(". .", ".")
    newS = newS.replace(" . ", ".")
    newS = newS.replace(". ", ".")
    newS = newS.replace(" .", ".")
    newS = newS.replace("..", ".")
    newS = newS.replace("..", ".")

    sentence = []
    temp = ''
    for j in newS:
        temp += j
        if j == '.':
            temp = temp.strip('(')
            temp = temp.strip(')')
            temp = temp.strip('%')
            temp = temp.strip(' ')
            temp = temp.strip(',')

            if temp != '.':
                sentence.append(temp)
            temp = ''
    real_sentence = []
    for i in sentence:
        i = i.strip('-')
        if len(i) > 20:
            real_sentence.append(i)
    return real_sentence


def feature_to_str(a, features):
    features_str = [a]
    feature = ""
    for i in features:
        for j in i:
            feature = feature+j+" "
        feature = feature.strip()
        feature = feature + ";"
    features_str.append(feature)
    return features_str


def isEng(n):
    character_set = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's',
                     't', 'u', 'v', 'w', 'x', 'y', 'z', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L',
                     'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z', '`', '!', '@', '#', '$',
                     '%', '^', '&', '*', '(', ')', '_', '+', '=', '-', '~', ',', '.', '/', '?', '>', '<', ';', ':',
                     '1', '2', '3', '4', '5', '6', '7', '8', '9', '0', '\'', '|', '\\', '"', '\'', ' ']
    for i in n:
        if i not in character_set:
            return 1
    return 0


# 此程序输出的是真集对照表
if __name__ == "__main__":
    namelist = ["food"]
    for i in namelist:
        counter = 0
        file = i + "_1000.csv"
        informations = read_sql(i)
        descriptions = []
        num = 1
        for i in informations:
            # print(i)
            print(counter)
            counter += 1
            if counter < 1000:
                d = i['description']
                name = i['name']
                d_num = str(i['download_num'])
                score = str(i['score'])
                re_num = str(i['score_num'])
                # print d
                d = html_filter.filters(d)  # 去除文本中的某些unicode字符
                sentence = temp_filters(d)
                # csv_file = open(file, 'ab+')  # 打开方式还可以使用file对象
                # writer = csv.writer(csv_file)
                if sentence != []:
                    # print(sentence)
                    for j in sentence:
                        features = []
                        features.append([j])
                        features.append([name])
                        features.append([d_num])
                        features.append([score])
                        features.append([re_num])
                        temp = extract_feature.extract(j)
                        features.extend(temp)
                        if temp == []:
                            features = []
                        if isEng(name) > 0:
                            features = []
                        if features != [] and j != []:
                            # print(features)
                            with open(file, 'a', newline='') as csvFile:
                                writer = csv.writer(csvFile)
                                print(features)
                                try:
                                    writer.writerow(features)
                                    writer.writerow([" "])
                                except():
                                    print('名字中有非英语字母，但描述中没有')
                            csvFile.close()



