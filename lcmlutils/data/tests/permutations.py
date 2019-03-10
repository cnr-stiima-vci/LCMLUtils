import itertools
from pdb import set_trace as _breakpoint

r_mandatory = ["Trees","Herbs"]
r_optional = ["Shrubs",]

q_mandatory = ["Herbs", "Shrubs"]
q_optional = ["Shrubs",]

rmp = list(itertools.permutations(r_mandatory))
qmp = list(itertools.permutations(q_mandatory))

def generate_valid_permutations(mandatory_list, optional_list):
    optional_group = [(el,) for el in optional_list]
    rmp = list(itertools.permutations(mandatory_list))
    #print(optional_group)
    #print(rmp)
    pc =  list(itertools.product(rmp, optional_group))
    #print(pc)
    #_breakpoint()
    permutations = [list(itertools.chain(p1,p2)) for p1, p2 in pc]
    permutations.insert(0,(mandatory_list))
    return permutations
    #return pc

rmp = generate_valid_permutations(r_mandatory ,r_optional)
qmp = generate_valid_permutations(q_mandatory, q_optional)

print(rmp)
print(qmp)
possible_combinations = list(itertools.product(rmp,qmp))
print(possible_combinations)

def count_basic_elements_with_name_and_value_including_additional_propname_in_transcoded_class(transcoded_class, prop_name, value, prop2_name):
    return sum(
        elem['properties'][propname].get('attributes').get('value')==value \
            for elem in transcoded_class \
                for propname in elem.get('properties').keys() \
                    if propname==prop_name and prop2_name in elem.get('properties').keys())    


def compute_property_extensiveness(transcoded_class, prop_name):
    extensiveness_length = len(transcoded_class)
    excl_elems_found = count_basic_elements_with_name_and_value_including_additional_propname_in_transcoded_class(transcoded_class, 'presence_type', 'Exclusive', prop_name)    
    tempseq_elems_found = count_basic_elements_with_name_and_value_including_additional_propname_in_transcoded_class(transcoded_class, 'presence_type', 'Temporal Sequence Depending', prop_name)
    mandatory_elems_found = count_basic_elements_with_name_and_value_including_additional_propname_in_transcoded_class(transcoded_class, 'presence_type', 'Mandatory', prop_name)
    opt_elems_found = count_basic_elements_with_name_and_value_including_additional_propname_in_transcoded_class(transcoded_class, 'presence_type', 'Optional', prop_name)
    print("exclusive: {0}; mandatory: {1}; temporal: {2}; optional {3}".format(excl_elems_found, mandatory_elems_found, tempseq_elems_found, opt_elems_found))
    if excl_elems_found>0:
        extensiveness_length = 1
    else:
        extensiveness_length = mandatory_elems_found
        if tempseq_elems_found:
            tempseq_types = collect_values_for_props_with_name_having_additional_propname_in_transcoded_class(transcoded_class, 'sequential_temporal_relationship', 'type',)
            tempseq_sy_found = sum([v == 'Sequential Same Year' for v in tempseq_types])
            print("tempseq sy: {0}".format(tempseq_sy_found))
            extensiveness_length += tempseq_sy_found if tempseq_sy_found>0 else 1
    print("extensiveness_length: {0}".format(extensiveness_length))
    return extensiveness_length


def compute_property_extensiveness_score(qe_tc, ref_tc, prop_name):
    """
    Computes property extensiveness on transcoded classes (see: transcode_lccs3_classes in similarity module)

    Parameters
    ----------
    qe_tc : dict
        Transcoded query class
    ref_tc : dict
        Transcoded reference class
    prop_name : string
        Property name to use
    """
    count_props_with_name_and_value_in_transcoded_class
    return 0
