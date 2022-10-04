# -*- coding: utf-8 -*-

import re, os
import xml.etree.ElementTree as ET


def make_struct(root):
    field_name_list = only_field_name(root)
    Document = {i:"None" for i in field_name_list}
    return Document

def load(root):
    for child in root.iter("BasePath"):
        scd_path = child.attrib.get('value')
    scd_path = r"{0}{1}".format(scd_path,"\\")
    text = []
    for root,subdirs,files in os.walk(scd_path):
        for file in files:
            with open(scd_path+file,'r', encoding='UTF-8') as f :
                text.append(f.read())
    text_output = '\n\n'.join(text)
    return text_output


def field_name(root): 
    list = []
    for child in root.iter("ScdField"):
        for z in child:
            list.append('<')
            list.append(z.attrib.get('name'))
            list.append('>')
    f = [f'{list[i*3]}{list[i*3+1]}{list[i*3+2]}' for i in range(0, len(list)//3)]
    return f

def only_field_name(root):
    field_name_list = []
    for child in root.iter("ScdField"):
        for i in child:
            field_name = i.attrib.get("name")
            field_name_list.append(field_name)
    return field_name_list


def clean_text(text,name):
    for i in name:
        text = text.replace(i,"")
    return text


def cleaning(text):
    text = re.sub("[-=+,#/\?:^$@*\"※“”~&%ㆍ!』\\‘|\(\)\[\]\<\>`\'…》【】·⍺βγⅳⅲⅴ□▲’㈜◆ㅇ]", ' ', text).lower()
    return text


def struct(root,args):
    name = field_name(root)
    result = re.split(r"[\n]", load(root)) 
    only_name = only_field_name(root)
    Document = make_struct(root)

    index_list = []
    doc_list = []

    for idx in range(0, len(result)):
        for n in range(0,len(name)):
            if name[n] in result[idx]:
                index_list.append(idx)
                if(len(index_list)==len(name)):
                    for i in range(0,len(only_name)):
                        if(i==len(only_name)-1):
                            if args.cleaning:
                                Document[only_name[i]] = cleaning(clean_text(''.join(result[index_list[i]]),name))
                            else:
                                Document[only_name[i]] = clean_text(''.join(result[index_list[i]]),name)
                        else:
                            if args.cleaning:
                                Document[only_name[i]] = cleaning(clean_text(''.join(result[index_list[i]:index_list[i+1]]),name))
                            else:
                                Document[only_name[i]] = clean_text(''.join(result[index_list[i]:index_list[i+1]]),name)
                    index_list=[]                   
                    doc_list.append(Document)
                    Document = make_struct(root)
    return doc_list

 

def parser_main(root, args):
    return struct(root,args)
