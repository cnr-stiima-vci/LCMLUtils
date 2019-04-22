import itertools
import copy
import pprint
from pdb import set_trace as _breakpoint

r_exclusive_groups = [("Water", "Building"),("UrbanPark","CropYield"),("ForestPlantation",)]
r_mandatory = ["Trees","Herbs"]
r_optional = ["Shrubs",]

q_mandatory = ["Herbs", "Shrubs"]
q_optional = ["Shrubs",]

rmp = list(itertools.permutations(r_mandatory))
qmp = list(itertools.permutations(q_mandatory))

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

rmp = generate_valid_permutations(r_mandatory ,r_optional, r_exclusive_groups, greedy_mode = True)
#qmp = generate_valid_permutations(q_mandatory, q_optional)
pprint.pprint(rmp)
pprint.pprint("number of permutations: {0}".format(len(rmp)))
