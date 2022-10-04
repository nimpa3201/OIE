from logging import root
import unittest, os, sys, re
import parser_main as parser
import xml.etree.ElementTree as ET

class SCDTests(unittest.TestCase):
    tree = ET.parse('../../config/config.xml')
    global root 
    root = tree.getroot()

    def test_make_struct(self):
        self.assertIsNotNone(parser.make_struct(root))

    def test_load(self):
        self.assertIsNotNone(parser.load(root))

    def test_field_name(self):
        list = ['<DOCID>', '<Date>', '<TITLE>', '<WRITER>', '<CONTENT>', '<ATTACHNAME>', '<ATTACHEXT>', '<ATTACHCON>', '<LINK>', '<FILELINK>', '<ALIAS>']
        self.assertListEqual(list, parser.field_name(root))

    def test_only_field_name(self):
        list = ['DOCID','Date','TITLE', 'WRITER', 'CONTENT', 'ATTACHNAME', 'ATTACHEXT', 'ATTACHCON', 'LINK', 'FILELINK', 'ALIAS']
        self.assertListEqual(list, parser.only_field_name(root))

    def test_clean_text(self):
        list = parser.struct(root)
        for i in list:
            self.assertNotIn("<DOCID>",i.DOCID)
    
    def test_cleaning(self):
        list = parser.struct(root)
        special_string = "[ - = + , # / \ ? : ^ $ . @ * \ \" ※ ~ & % ㆍ ! 』 \ \ ‘ | \ ( \ ) \ [ \ ] \ < \ > ` \ ' … 》 【 】 · ]"
        special_list = special_string.split()
        for i in list:
            for s in special_list:
                self.assertNotIn(s,i.CONTENT)

    def test_struct(self):
        self.assertIsNotNone(parser.struct(root))
    


if __name__=='__main__':
    unittest.main() 
