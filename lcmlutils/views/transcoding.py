import re
import os
import sys
import copy
import lxml
from lxml import etree
from lxml import objectify
import pprint

from pdb import set_trace as _breakpoint

IGNORED_PROPS_LIST = ['name', 'description', 'elements',]

namespaces = {'xs':'http://www.w3.org/2001/XMLSchema',
"re": "http://exslt.org/regular-expressions"}
 

def transcode_lccs3_classes(xml_text):
    doc = etree.fromstring(xml_text)
    lc_classes = doc.findall('elements/LC_LandCoverClass', namespaces)
    classes_list = []
    for lc_class in lc_classes:
        class_dd = {}
        class_dd['name'] = lc_class.find('./name').text
        class_dd['map_code'] = lc_class.find('./map_code').text
        class_dd['elements'] = []
        lc_elements = lc_class.findall('.//LC_LandCoverElement', namespaces = namespaces)
        for el in lc_elements:
            el_dd = {}
            el_dd['element_uuid'] = el.attrib['uuid']
            el_dd['element_type'] = el.attrib['{http://www.w3.org/2001/XMLSchema-instance}type']
            print('handling element {0}...'.format(el_dd['element_type']))
            el_dd['properties'] = {}
            el_stratum = el.getparent().getparent()
            pt_stratum = el_stratum.find('presence_type').text or 'Mandatory'
            pt_stratum_lcs = el_stratum.findall("./elements/LC_LandCoverElement")
            siblings_set = set()
            for lce in pt_stratum_lcs:
                siblings_set.add(lce.get('uuid'))
            siblings_set.remove(el_dd['element_uuid'])
            el_dd['sibling_elements_uuid'] = siblings_set
            el_dd['parent_stratum_presence_type'] = pt_stratum
            for elch in el.getchildren():
                tag = elch.tag
                print('handling property {0}...'.format(tag))
                #if tag=='sequential_temporal_relationship':
                #    _breakpoint() # gestire casi come sequential_temporal_relationship->type
                prop_dd = {}
                if tag not in IGNORED_PROPS_LIST:
                    if elch.text and len(elch.text.strip(' \t\r\n'))>0:
                        #prop_dd['property_name'] = tag
                        elch_val = elch.text
                        if tag=='presence_type':
                            if pt_stratum=='Optional':
                                elch_val = 'Optional'
                        prop_dd['attributes'] = {'value': elch_val}
                        prop_dd['ranged_type'] = False
                        el_dd['properties'][tag] = prop_dd
                    else:
                        prop_name = tag
                        #if tag in props_mapping.keys():
                        #    prop_name = props_mapping[tag].get(el_dd['element_type'])
                        if prop_name:
                            prop_dd = {}
                            #prop_dd['property_name'] = prop_name
                            print(elch.tag)
                            prop_dd['attributes'] = {}
                            for k,v in elch.items():
                                if re.match("^\d+?\.\d+?$", v) is None:
                                    prop_dd['attributes'][k] = v
                                else:
                                    prop_dd['attributes'][k] = float(v)
                            if 'min' in prop_dd['attributes']:
                                prop_dd['ranged_type'] = True
                            for tagc in elch.getchildren():
                                if 'type' not in tagc.keys():
                                    prop_dd['attributes'][tagc.tag] = tagc.text
                            el_dd['properties'][prop_name] = prop_dd                        
            class_dd['elements'].append(el_dd)
        classes_list.append(class_dd)
    pprint.pprint('transcoded class:')
    pprint.pprint(classes_list)
    return classes_list
