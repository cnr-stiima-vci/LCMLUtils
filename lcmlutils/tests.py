import datetime
import os

from django.utils import timezone
from django.test import TestCase

from .models import LCCS3Class, LCCS3Legend
from .views.similarity import perform_assessment
from lcmlutils.settings import DATA_PATH
from pdb import set_trace as _breakpoint
from lxml import etree

comparisons_dd = {
"sylhet22_seea4": {
   		"class1":"sylhet22",
   		"class2":"seea4",
   		"notes":"",
		"expected_value":None,
		"error_threshold":None
	},
"sylhet4_seea6": {
		"class1":"sylhet4",
		"class2":"seea6",
		"notes":""
	},
"sylhet21_seea7": {
		"class1":"sylhet21",
		"class2":"seea7",
		"notes":"sal vs mangroves"
	}
}

namespaces = {'xs':'http://www.w3.org/2001/XMLSchema',
"re": "http://exslt.org/regular-expressions"}

def get_lc_class_fn(lcc_name):
    fn = os.path.join(DATA_PATH,"tests",lcc_name+".lccs")
    return fn

def load_lccs_class(lcc_fn):
    lccs_class = None
    if os.path.exists(lcc_fn):
        lccs_class = LCCS3Class()
        with open(lcc_fn,'rt') as f1:
            lccs_class.xml_text = f1.read()
        doc = etree.fromstring(lccs_class.xml_text)
    return lccs_class

def test_case(case_name):
    entry = comparisons_dd.get(case_name)
    if entry:
        c1fn = get_lc_class_fn(entry["class1"])
        c2fn = get_lc_class_fn(entry["class2"])
        c1 = load_lccs_class(c1fn)
        c2 = load_lccs_class(c2fn)
        res = perform_assessment(c1,c2)
        #self.assertEqual(True,True)

class SimilarityTests(TestCase):
   def test00(self):
       print("testing with utility functions")
       _breakpoint()
       test_case("sylhet21_seea7")
