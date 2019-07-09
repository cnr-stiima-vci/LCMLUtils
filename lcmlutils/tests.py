import datetime
import os
import pprint

from django.utils import timezone
from django.test import TestCase

from .models import LCCS3Class, LCCS3Legend
from .views.similarity import perform_assessment
from .views.transcoding import transcode_lccs3_classes
from .views.multiverse import generate_valid_permutations
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
	},
"coxfmp_seea7": {
        "class1":"coxs-fmp",
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

def assess_similarity(case_name):
    entry = comparisons_dd.get(case_name)
    if entry:
        c1fn = get_lc_class_fn(entry["class1"])
        c2fn = get_lc_class_fn(entry["class2"])
        c1 = load_lccs_class(c1fn)
        c2 = load_lccs_class(c2fn)
        res = perform_assessment(c1,c2)
        #self.assertEqual(True,True)

def load_and_trancode_class(class_name):
    decoded = None
    if class_name:
        c1fn = get_lc_class_fn(class_name)
        c1 = load_lccs_class(c1fn)
        decoded = transcode_lccs3_classes(c1.xml_text)
        #self.assertEqual(True,True)
    return(decoded)

def get_presence_type_groups(transcoded_class):
    tc = transcoded_class
    groups = {}
    processed_exclusive = set()
    group_types = ['Mandatory','Optional','Exclusive']
    for pt in group_types:
        pprint.pprint(pt)
        els = [el['element_uuid'] for el in tc['elements'] if el['properties']['presence_type']['attributes']['value'] == pt]
        if pt == 'Exclusive':
            groups[pt] = list()
            pprint.pprint(els)
            for uuid in els:
                eg = []
                if uuid not in processed_exclusive:
                    eg = [uuid]
                    processed_exclusive.add(uuid)
                    el = [el for el in tc['elements'] if el['element_uuid'] == uuid][0]
                    eg.extend(list(el['sibling_elements_uuid']))
                    for uuid in list(el['sibling_elements_uuid']):
                        processed_exclusive.add(uuid)
                    groups[pt].append(eg)
        else:
            pprint.pprint(els)
            groups[pt] = list(els)
    return(groups)

def get_flat_list(l):
    flat_list = [item for sublist in l for item in sublist]
    return(flat_list)

class SimilarityTests(TestCase):
    
    def test_similarity_01(self):
       print("testing with utility functions")
       assess_similarity("sylhet21_seea7")
    '''
    def test_pt_01(self):
        print("presence_type typology extraction #1 (sylhet14)")
        transcoded = load_and_trancode_class("sylhet14")
        groups = get_presence_type_groups(transcoded[0])
        self.assertEqual(len(groups['Mandatory']),1)
        pprint.pprint(groups)

    def test_pt_02(self):
        print("presence_type typology extraction #2 (sylhet21)")
        transcoded = load_and_trancode_class("sylhet21")
        groups = get_presence_type_groups(transcoded[0])
        self.assertEqual(len(groups['Mandatory']),2)
        pprint.pprint(groups)
    
    def test_pt_03(self):
        print("presence_type typology extraction #3 (seea4)")
        transcoded = load_and_trancode_class("seea4")
        groups = get_presence_type_groups(transcoded[0])
        pprint.pprint(groups)
        self.assertEqual(len(groups['Mandatory']),1)
        self.assertEqual(len(get_flat_list(groups['Exclusive'])),2)
        pprint.pprint(groups)
    
    def test_pt_04(self):
        print("presence_type typology extraction #4 (seea5)")
        transcoded = load_and_trancode_class("seea5")
        groups = get_presence_type_groups(transcoded[0])
        self.assertEqual(len(groups['Mandatory']),1)
        self.assertEqual(len(groups['Optional']),1)
    '''
    '''
    def test_pt_05(self):
        pprint.pprint("- presence_type typology extraction #3 (seea6)")
        transcoded = load_and_trancode_class("seea6")
        groups = get_presence_type_groups(transcoded[0])
        pprint.pprint(groups)
        self.assertEqual(len(groups['Mandatory']),1)
        self.assertEqual(len(groups['Optional']),3)
    '''
    '''
    def test_permutations_01(self):
        pprint.pprint("permutations on seea4, greedy_mode = False")
        transcoded = load_and_trancode_class("seea4")
        groups = get_presence_type_groups(transcoded[0])
        pprint.pprint(groups)
        mg = groups['Mandatory']
        og = groups['Optional']
        eg = groups['Exclusive']
        permutations = generate_valid_permutations(mg, og, eg, greedy_mode = False)
        pprint.pprint(permutations)
        self.assertEqual(len(permutations),2)
    
    def test_permutations_02(self):
        pprint.pprint("permutations on seea4, greedy_mode = True")
        transcoded = load_and_trancode_class("seea4")
        groups = get_presence_type_groups(transcoded[0])
        pprint.pprint(groups)
        mg = groups['Mandatory']
        og = groups['Optional']
        eg = groups['Exclusive']
        permutations = generate_valid_permutations(mg, og, eg, greedy_mode = True)
        pprint.pprint(permutations)
        self.assertEqual(len(permutations),4)
    
    def test_permutations_03(self):
        pprint.pprint("permutations on seea5, greedy_mode = False")
        transcoded = load_and_trancode_class("seea5")
        groups = get_presence_type_groups(transcoded[0])
        pprint.pprint(groups)
        mg = groups['Mandatory']
        og = groups['Optional']
        eg = groups['Exclusive']
        permutations = generate_valid_permutations(mg, og, eg, greedy_mode = False)
        pprint.pprint(permutations)
        self.assertEqual(len(permutations),2)
    '''
    
    def test_permutations_04(self):
        pprint.pprint("- permutations on seea6, greedy_mode = False")
        transcoded = load_and_trancode_class("seea6")
        groups = get_presence_type_groups(transcoded[0])
        pprint.pprint(groups)
        mg = groups['Mandatory']
        og = groups['Optional']
        eg = groups['Exclusive']
        permutations = generate_valid_permutations(mg, og, eg, greedy_mode = False)
        pprint.pprint("Permuations: ")
        pprint.pprint(permutations)
        self.assertEqual(len(permutations),4)
    
    def test_permutations_05(self):
        pprint.pprint("- permutations on seea6, greedy_mode = True")
        transcoded = load_and_trancode_class("seea6")
        groups = get_presence_type_groups(transcoded[0])
        pprint.pprint(groups)
        mg = groups['Mandatory']
        og = groups['Optional']
        eg = groups['Exclusive']
        permutations = generate_valid_permutations(mg, og, eg, greedy_mode = True)
        pprint.pprint("Permuations: ")
        pprint.pprint(permutations)
        self.assertEqual(len(permutations),8)


    