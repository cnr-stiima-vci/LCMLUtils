import itertools
import copy
import pprint

def generate_valid_permutations(mandatory_list, optional_list, exclusive_groups, greedy_mode = False):
    # elements in exclusive groups are mandatory in an exclusive way, one for each group and then permutated
    # actually, it's a set product, with one element for group
    exclusive_product_group = list(itertools.product(*exclusive_groups))
    #print(exclusive_product_group)
    # mandatory elements must always be present, creating pseudo-groups
    mandatory_groups = [mandatory_list]
    apl = list(itertools.product(mandatory_groups,exclusive_product_group))
    # these are the lists obtained combining mandatory elements with exclusive elements
    always_present_list = [list(itertools.chain(p1,p2)) for p1, p2 in apl]
    #print(always_present_list)
    # all permutations of these lists should be checked and computed
    ap_perm = []
    if greedy_mode:
        for g in always_present_list:
            ap_perm.extend(list(itertools.permutations(g)))
    else:
        ap_perm = copy.copy(always_present_list)
    # this is the result
    #print(ap_perm)
    # now extending the list with optional elements, creating pseudo-groups
    optional_group = []
    if greedy_mode:
        ol = copy.copy(optional_list)
        nel = len(ol)
        for cnt in range(nel):
            n = cnt+1
            o_combs = itertools.combinations(ol,n)
            optional_group.extend(o_combs)
    else:
        optional_group = [(el,) for el in optional_list]
    # since these elements are optional, they can be matched as last resort only
    pc =  list(itertools.product(ap_perm, optional_group))
    #print(pc)
    #_breakpoint()
    permutations = copy.copy(ap_perm)
    additional_elements = [list(itertools.chain(p1,p2)) for p1, p2 in pc]
    permutations.extend(additional_elements)
    # now all permutations have been computed
    return permutations
    #return pc


def get_presence_type_groups(transcoded_class):
    tc = transcoded_class
    groups = {}
    processed_exclusive = set()
    group_types = ['Mandatory','Optional','Exclusive']
    for pt in group_types:
        pprint.pprint(pt)
        els = [el['element_uuid'] for el in tc if el['properties']['presence_type']['attributes']['value'] == pt]
        if pt == 'Exclusive':
            groups[pt] = list()
            pprint.pprint(els)
            for uuid in els:
                eg = []
                if uuid not in processed_exclusive:
                    eg = [uuid]
                    processed_exclusive.add(uuid)
                    el = [el for el in tc if el['element_uuid'] == uuid][0]
                    eg.extend(list(el['sibling_elements_uuid']))
                    for uuid in list(el['sibling_elements_uuid']):
                        processed_exclusive.add(uuid)
                    groups[pt].append(eg)
        else:
            pprint.pprint(els)
            groups[pt] = list(els)
    return(groups)
