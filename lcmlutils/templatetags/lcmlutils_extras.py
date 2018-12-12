import json
from lxml import etree
import requests
from django import template
from django.http import JsonResponse
#from django.contrib.sites.models import Site
#from geonode.layers.models import Layer
from lcmlutils.models import *

register = template.Library()

@register.inclusion_tag('lcmlutils/show_validators_list.html')
def get_validators():
    dd = {}
    xsd_list = XSDValidator.objects.all()
    validators = [{"name": xsdv.name, "active": xsdv.active} for xsdv in xsd_list]
    dd["validators_list"] = validators
    return dd

def get_legend_info(legend):
    fragment_xml = legend.xml_text
    ll = []
    dd = {}
    if fragment_xml:
        doc = etree.fromstring(fragment_xml)
        els = doc.findall('elements/LC_LandCoverClass')
        dd['classes_count'] = len(els)
    return dd

@register.inclusion_tag('lcmlutils/show_legends_list.html')
def show_legends():
    #get_resp = requests.get(legends_url)
    #data = json.loads(get_resp.content)
    legends = LCCS3Legend.objects.all()
    ll = [{'name':el, 'info':get_legend_info(el)} for el in legends]
    pprint.pprint(ll)
    return {'legends_list': ll}


#server_addr = 'http://149.139.19.8:8080'
'''
server_addr = 'http://{0}:8080'.format(Site.objects.get_current().domain)
legends_url = '{0}/bfis-service/rest/legends'.format(server_addr)

def get_legend_info(legend_name):
    get_resp = requests.get('{0}/{1}'.format(legends_url, legend_name))
    data = json.loads(get_resp.content)
    fragment_xml = data.get('results')
    print(fragment_xml)
    ll = []
    dd = {}
    if fragment_xml:
        doc = etree.fromstring(fragment_xml)
        els = doc.findall('elements/LC_LandCoverClass')
        dd['classes_count'] = len(els)
    return dd

def get_legend_info(legend_name):
    get_resp = requests.get('{0}/{1}'.format(legends_url, legend_name.lower()))
    data = json.loads(get_resp.content)
    fragment_xml = data.get('results')
    ll = []
    if fragment_xml:
        doc = etree.fromstring(fragment_xml)
        els = doc.findall('elements/LC_LandCoverClass')
        for el in els:
            dd = {'name': el.find('name').text, 'map_code':el.find('map_code').text, 'basic_elements':[]}
            bels = el.findall('.//LC_LandCoverElement')
            for be in bels:
                pt = 'Mandatory'
                if be.find('presence_type'):
                    pt = be.find('presence_type').text
                dd['basic_elements'].append({'name': be.find('name').text, 'presence_type': pt})
            ll.append(dd)
    return {'classes_list': ll, 'legend_name': legend_name}


@register.inclusion_tag('lcmlutils/show_classes_list.html')
def show_legend_classes(legend_name, mode = 'long', layer_name = None):
    linfo = get_legend_info(legend_name)
    linfo.update({'mode': mode})
    if layer_name!=None:
        sinfo = sanity_check_for_layer(layer_name)
        linfo.update({'not_in_layer': sinfo['not_in_layer']})
    return linfo


def get_legend_for_layer(layer_name):
    lccs3_legend_name = None
    url = '{0}/bfis-service/rest/layers/{1}/legend'.format(server_addr, layer_name.lower())
    get_resp = requests.get(url)
    data = json.loads(get_resp.content)
    lccs3_legend_name = data.get('results')
    return lccs3_legend_name


@register.assignment_tag
def get_lccs3_legend_for_layer(layer_name):
    return get_legend_for_layer(layer_name)    
    

@register.inclusion_tag('lcmlutils/sanity_check.html')
def sanity_check_for_layer(layer_name):
    messages = []
    layer = Layer.objects.filter(name = layer_name.lower()).first()
    if layer:
        layer_attrs = layer.attributes.values()
        attrnames = [v.get('attribute') for v in layer_attrs]
        if 'LCCS_code' not in attrnames:
            messages.append('<font color="red">LCCS_code field missing</font>: no associations with the legends are possible')
        url = '{0}/bfis-service/rest/layers/{1}/attribute/{2}/values'.format(server_addr, layer_name.lower(), 'LCCS_code')
        get_resp = requests.get(url)
        data = json.loads(get_resp.content)
        layer_values = set(data.get('results',[]))
        lccs3_legend_name = get_legend_for_layer(layer_name.lower())
        linfo = get_legend_info(lccs3_legend_name)
        legend_values = [el.get('map_code') for el in linfo.get('classes_list',[])]
        legend_values = set(legend_values)
        print(layer_values)
        print(legend_values)
        not_in_legend = layer_values.difference(legend_values)
        not_in_layer = legend_values.difference(layer_values)
        if len(not_in_legend)>0:
            messages.append('codes <font color="red">MISSING</font> from the legend: {0}'.format(', '.join(list(not_in_legend))))
        if len(not_in_layer)>0:
            messages.append('<font color="yellow">EXTRA codes</font> in LCCS3 legend: {0}'.format(', '.join(list(not_in_layer))))
    return {'messages':messages, 'not_in_legend':json.dumps(list(not_in_legend)), 'not_in_layer':json.dumps(list(not_in_layer))}



@register.filter
def join_by_attr(the_list, attr_name, separator=', '):
    return separator.join([el.get(attr_name) for el in the_list])


# JSON services

def sanity_check_for_layer_json(request, layername):
    dd = sanity_check_for_layer(layername)
    return JsonResponse({'not_in_layer': list(dd['not_in_layer']), 'not_in_legend': list(dd['not_in_legend'])})

'''