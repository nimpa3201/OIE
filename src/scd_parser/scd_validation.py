import os, sys
import xml.etree.ElementTree as ET

def load(root):
    path_list = []
    for child in root.iter("BasePath"):
        path = child.attrib.get('value')
        path = r"{0}{1}".format(path,"\\")
    for root,subdirs,files in os.walk(path):
        for file in files:
            path_list.append(path+file)
    return path_list

def scd_size_validation(path_list):
    for list in path_list:
        if os.path.getsize(list) > 2147483648:
            sys.exit("SCD file size error")
    return 0

def scd_name_validation(path_list):
    #SCD 이름 validation
    for list in path_list:
        scd_name = os.path.basename(list)
        if len(scd_name) > 31:
            sys.exit("SCD file name error")
    return 0
'''''''''
def scd_field_validation(path_list):
    #문서의 필드 개수 validation
    for list in path_list:
        with open(list,'r', encoding='UTF-8') as g:
            data = g.read()
            if len(data.split("<DOCID>"))-1 > 256:
                sys.exit("SCD field error")
    return 0
'''''''''
def validation_main(root):
    path_list = load(root)
    scd_size_validation(path_list)
    scd_name_validation(path_list)
    #scd_field_validation(path_list)
