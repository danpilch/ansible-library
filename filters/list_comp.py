# addressing the lack of a compact list comprehension in ansible

def list_comp(lst, elem_key):
    """return the elem_keys of items in lst, as a list"""
    return [unicode(i[elem_key]) for i in lst]

def list_comp_joined(lst, elem_key):
    """return the elem_keys of items in lst, as a unicode sequence"""
    return u' '.join(list_comp(lst, elem_key))

def to_list(lst):
    """return a list that was originally comma-separated - we may also pass in a list because of orders in ansible logic to return if it type=list"""
    if type(lst) == list:
        return lst
    else:
        return lst.split(',')

class FilterModule(object):

    def filters(self):
        return {
            'list_comp' : list_comp,
            'list_comp_joined' : list_comp_joined,
            'to_list': to_list
        }
