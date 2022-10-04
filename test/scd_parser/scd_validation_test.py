from logging import root
import unittest, os, sys
import xml.etree.ElementTree as ET
import scd_validation as vali

class SCDTests(unittest.TestCase):
    
    tree = ET.parse('../../config/config.xml')
    global root 
    root = tree.getroot()

    def test_load(self):
        dir = "../../data/scd/"
        file_list = os.listdir(dir)
        for i in file_list:
            file_list[file_list.index(i)] = dir + i
        self.assertListEqual(vali.load(root), file_list)

    def test_scd_name_validation(self):
        self.assertEqual(vali.scd_name_validation(vali.load(root)),0)

    def test_scd_size_validation(self):
        self.assertEqual(vali.scd_size_validation(vali.load(root)),0)

    def test_scd_field_validation(self):
        self.assertEqual(vali.scd_field_validation(vali.load(root)),0)

if __name__=='__main__':
    unittest.main()

    
