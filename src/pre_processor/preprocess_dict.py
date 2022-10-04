import os, re, sys
import xml.etree.ElementTree as ET



#return타입은 동의어는 딕셔너리타입 불용어는 리스트타입
def load_dict(root, dict_name):
    for child in root.iter("DictPath"):
        dict_path = child.attrib.get("value")
    dict_path = r"{0}{1}".format(dict_path,"\\")
    with open(dict_path+dict_name+".txt","r",encoding="UTF-8") as d:
        if dict_name == "synonym":
            dict_content={}
            for word in d.readlines():
                temp = word.replace("\n","").split("\t")
                dict_content.setdefault(temp[0],temp[1:])
        elif dict_name == "stopword":
            dict_content={}
            for stopword in d.readlines():
                if stopword[0] != ";":
                    dict_content[stopword.replace("\n","")] = " "
    return dict_content


def process_synonym_morph(dict_content, doc_list):
    for doc in doc_list:
        for key in doc.keys():
            for token in doc[key]:
                synonym = dict_content.get(token["morph"])
                if synonym != None:
                    doc[key][doc[key].index(token)]["synonym"] = synonym
    return doc_list


def process_stopword_morph(dict_content, doc_list):
    for doc in doc_list:
        for key in doc.keys():
            for token in doc[key][::-1]:
                stopword = dict_content.get(token["morph"])
                if stopword != None:
                    del doc[key][doc[key].index(token)]
    return doc_list


def process_synonym_token(dict_content, doc_list):
    for doc in doc_list:
        for key in doc.keys():
            for token in doc[key]:
                synonym = dict_content.get(token)
                if synonym != None:
                    synonym = " ".join(synonym)
                    doc[key][doc[key].index(token)] = doc[key][doc[key].index(token)]+ " " + synonym
    return doc_list


def process_stopword_token(dict_content, doc_list):
    for doc in doc_list:
        for key in doc.keys():
            for token in doc[key][::-1]:
                stopword = dict_content.get(token)
                if stopword != None:
                    del doc[key][doc[key].index(token)]
    return doc_list



def dict_main(root, args, doc_list, dict_name):
    if args.tokenizer=="morph":
        if dict_name == 'synonym':
            dict_content = load_dict(root, dict_name)
            return process_synonym_morph(dict_content, doc_list)
        elif dict_name == 'stopword':
            dict_content = load_dict(root, dict_name)
            return process_stopword_morph(dict_content, doc_list)
    elif args.tokenizer=="tokenizer":
        if dict_name == "synonym":
            dict_content = load_dict(root, dict_name)
            return process_synonym_token(dict_content, doc_list)
        elif dict_name == 'stopword':
            dict_content = load_dict(root, dict_name)
            return process_stopword_token(dict_content, doc_list)
    else:
        raise Exception("if preprocess_dict == True then tokenizer should in [morph,tokenizer]")