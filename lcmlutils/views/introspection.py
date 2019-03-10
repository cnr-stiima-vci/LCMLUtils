import os
import lxml
import pprint
from lxml import etree
from lxml import objectify
import json
from pdb import set_trace as _breakpoint

from django.http import HttpResponse
from django.http import JsonResponse

from lcmlutils.models import XSDValidator


namespaces = {'xs':'http://www.w3.org/2001/XMLSchema',
"re": "http://exslt.org/regular-expressions"}


def list_basic_elements(request):
    xsdv = XSDValidator.objects.filter(active=True).first()
    doc = etree.fromstring(xsdv.xsd_text)
    elements = doc.findall('xs:element', namespaces)
    data = []
    for el in elements:
        ob = {}
        ob['name'] = el.get('name')
        # eligible_as_root hack
        ob['eligible_as_root'] = True if ob['name'] == 'LC_Legend' else False
        data.append(ob)
    
    return JsonResponse({'objects':data})


def derived_classes_list(request, basename):
    xsdv = XSDValidator.objects.filter(active=True).first()
    doc = etree.fromstring(xsdv.xsd_text)
    open_set = set()
    closed_set = set()
    open_set.add(basename)
    while len(open_set)>0:
        baseclass_name = open_set.pop()
        elements = doc.xpath("xs:element[@name='{0}']".format(baseclass_name), namespaces = namespaces)
        if len(elements)>0 and baseclass_name!=basename:
            closed_set.add(baseclass_name)
        xpath = "xs:complexType/xs:complexContent/xs:extension[@base='{0}']/../../@name".format(baseclass_name)
        derived_names = doc.xpath(xpath, namespaces = namespaces)
        for name in derived_names:
            open_set.add(name)

    return JsonResponse({'objects': list(closed_set)})


def handle_simple_type(doc, fd_type, fd):
    stype =  doc.find("xs:simpleType[@name='{0}']".format(fd_type), namespaces)
    choices = []
    if stype is not None:
        stype_type = stype.find('xs:restriction', namespaces)
        enums = stype.findall('.//xs:enumeration', namespaces)
        for en in enums:
            choices.append(en.get('value'))
        fd['type'] = stype_type.get('base')
        if len(choices)>0:
            fd['allowed'] = choices
        else:
            #_breakpoint()
            pattern = stype.find('.//xs:pattern', namespaces)
            if pattern is not None:
                fd['regex'] = pattern.get('value')
            else:
                minInclusive = stype.find('.//xs:minInclusive', namespaces)
                maxInclusive = stype.find('.//xs:maxInclusive', namespaces)
                fd['range'] = {'min':minInclusive.get('value'), 'max':maxInclusive.get('value')}
    else:
        fd['type'] = fd_type


def handle_complex_type(doc, el, fd):
    attributes = el.findall("xs:complexType/xs:attribute", namespaces)
    if len(attributes)==0:
        if fd['type']:
            attributes = doc.findall("xs:complexType[@name='{0}']/xs:attribute".format(fd['type']), namespaces)
    print(fd)
    #_breakpoint()
    if len(attributes)>0:
        #_breakpoint()
        fd['attributes'] = {}
        for attr in attributes:
            print(etree.tostring(attr, pretty_print=True))
            attrs_dd = fd['attributes']
            attr_type = attr.getchildren()[0].getchildren()[0].get('base')
            attr_name = attr.get('name')
            attrs_dd[attr_name] = {'type': attr_type}
            minInclusive = attr.find('.//xs:minInclusive', namespaces)
            maxInclusive = attr.find('.//xs:maxInclusive', namespaces)
            if minInclusive is not None or maxInclusive is not None:
               attrs_dd[attr_name]['range'] = {}
               if minInclusive is not None:
                   attrs_dd[attr_name]['range']['min'] = minInclusive.get('value')
               if maxInclusive is not None:
                   attrs_dd[attr_name]['range']['max'] = maxInclusive.get('value')
        if fd.get('type'):
            del fd['type']

def basic_element_schema(request, basic_element_name):
    extension_stack = []
    et = None
    dd = {}
    dd['fields'] = []
    xsdv = XSDValidator.objects.filter(active=True).first()
    doc = etree.fromstring(xsdv.xsd_text)
    find_key = './/xs:element'+"[@name='" + basic_element_name + "']"
    elem = doc.find(find_key,namespaces)
    if elem:
        et = elem.get('type')
    else:
        ctype = doc.find("xs:complexType[@name='{0}']".format(basic_element_name), namespaces)
        if ctype:
            et = basic_element_name
    if et:
        bContinue = True
        extension_stack.append(et)
    else:
        bContinue = False
    while bContinue:
        et = extension_stack.pop()
        ctype = doc.find("xs:complexType[@name='{0}']".format(et), namespaces)
        ext_el = ctype.find('.//xs:extension', namespaces)
        if ext_el is not None:
            print('inspecting {0}'.format(ext_el.get('base')))
            ext_el_children = ext_el.getchildren()
            for ch in ext_el_children:
                print('child with tag {0}'.format(ch.tag)) 
            extension_stack.append(ext_el.get('base'))
        else:
            bContinue = False
        seq_el = ctype.find('.//xs:sequence', namespaces)
        if seq_el is not None:
            elements = seq_el.findall('xs:element', namespaces)
            for el in elements:
                field_descriptor = {
                    'name': el.get('name'),
                    'type': el.get('type'),
                }
                min_occurs = el.get('minOccurs')
                max_occurs = el.get('maxOccurs')
                if min_occurs == 0:
                    field_descriptor['required'] = (min_occurs=='0')
                handle_complex_type(doc, el, field_descriptor)
                if field_descriptor.get('type'):
                    if 'xs:' not in field_descriptor['type']:
                        handle_simple_type(doc, field_descriptor['type'], field_descriptor)
                else:
                    els = el.findall("xs:complexType/xs:sequence/xs:element", namespaces)
                    if len(els)==1:
                        field_descriptor['type'] = 'list'
                        field_descriptor['items'] = els[0].get('type')
                        if els[0].get('minOccurs'):
                            field_descriptor['min_length'] = int(els[0].get('minOccurs'))
                        if els[0].get('maxOccurs') and els[0].get('maxOccurs')!='unbounded':
                            field_descriptor['max_length'] = int(els[0].get('maxOccurs'))
                    else:
                        field_descriptor['schema'] = []
                        for sel in els:
                            sfd_name = sel.get('name')
                            sd = {'name':sfd_name}
                            if sel.get('type'):
                                sd['type'] = sel.get('type')
                                handle_simple_type(doc, sel.get('type'), sd)
                            else:
                                handle_complex_type(doc, sel, sd)
                            field_descriptor['schema'].append(sd)
                        if len(field_descriptor['schema'])==0:
                            del field_descriptor['schema']
                        else:
                            field_descriptor['type'] = 'dict' #RIVEDERE

                dd['fields'].append(field_descriptor)
    pprint.pprint(dd)
    return JsonResponse({'schema':dd['fields']})
