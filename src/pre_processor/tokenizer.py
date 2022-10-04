import re, os
import xml.etree.ElementTree as ET
import pandas as pd

from PyKomoran import *
komoran = Komoran("EXP")

from kobert_transformers import get_tokenizer
tokenizer_sp = get_tokenizer()

#config에서 get_processfield
def get_process_field(root):
    process_field = []
    for child in root.iter("ProcessField"):
        for i in child:
            process_field.append(i.attrib.get("name"))
    return process_field


def get_process_morph_tag(root):
    for child in root.iter("MorphtagPath"):
        morphtag_path = child.attrib.get("value")
    morphtag_path = r"{0}{1}".format(morphtag_path,"\\")
    files = os.listdir(morphtag_path)      
    data = pd.read_excel(morphtag_path+files[0])
    df = pd.DataFrame(data).iloc[:,[1,3]]
    df = df.loc[df["포함여부"]=="O"]
    return df.iloc[:,0].tolist()


#tokenized fields value return
#공백 단위로 토큰화
def tokenizer(field_list, document_list):
    tokenized_doc_list = []
    for document in document_list:
        tokenized_text_doc = {i:" " for i in field_list}
        for i in field_list:
            tokenized_text_doc[i] = document[i].split(" ")
            tokenized_text_doc[i] = list(filter(None, tokenized_text_doc[i]))
        tokenized_doc_list.append(tokenized_text_doc)
    return tokenized_doc_list


#형태소분석기사용한 토큰화
def morpheme(field_list, morph_tag_list, document_list):
    morpheme_doc_list = []
    for document in document_list:
        morpheme_doc = {i:" " for i in field_list}
        for i in field_list:
            morph_list = []
            temp = komoran.get_plain_text(document[i]).split(" ")
            for word in temp:
                temp_dict = {"morph":word[:word.find("/")], "tag":word[word.find("/")+1:]}
                if temp_dict["tag"] in morph_tag_list:
                    morph_list.append(temp_dict)
            morpheme_doc[i] = morph_list
        morpheme_doc_list.append(morpheme_doc)
    return morpheme_doc_list


#Sentencepiece를 사용한 토큰화
def sentencep(field_list, document_list):
    sp_doc_list = []
    orignal = []
    for document in document_list:
        sp_doc = {i:[] for i in field_list}
        for i in field_list:
            lines = list(filter(None,document[i].split(".")))
            lines = [line+' .' for line in lines]
            for words in lines:
                line_temp = {}
                tokens = []
                slot_label_mask = []
                for word in words.split():
                    word_tokens = tokenizer_sp.tokenize(word)
                    if not word_tokens:
                        word_tokens = [tokenizer_sp.unk_token]
                    tokens.extend(word_tokens)
                    slot_label_mask.extend([0] + [-100] * (len(word_tokens) - 1))
                line_temp["tokens"] = tokens
                line_temp["slot_label_mask"] = slot_label_mask
                sp_doc[i].append(line_temp)
                orignal.append(words.split())
        sp_doc_list.append(sp_doc)
    return sp_doc_list, orignal


#처리해야하는 field만 return
def process_field_doc(field_list, document_list):
    tokenized_doc_list = []
    for document in document_list:
        tokenized_text_doc = {i:" " for i in field_list}
        for i in field_list:
            tokenized_text_doc[i] = document[i]
        tokenized_doc_list.append(tokenized_text_doc)
    return tokenized_doc_list



def token_main(root, args, doc_list):
    process_field = get_process_field(root)
    
    if args.tokenizer=="sp":
        return sentencep(process_field, doc_list)
    elif args.tokenizer=="morph":
        morph_tag_list = get_process_morph_tag(root)
        return morpheme(process_field, morph_tag_list, doc_list)
    elif args.tokenizer=="tokenizer":
        return tokenizer(process_field, doc_list)
    else:
        raise Exception("--tokenizer can be [sp, morph, tokenizer]")


