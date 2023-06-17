import gdb
import re

class StdStringPrinter:
    def __init__(self, val):
        self.val = val

    def to_string(self):
        import pdb
        last : int = int(self.val['last'])
        #print ('last : ' , int(last))
        #print ( 'elements' , self.val['elements'].type)
        # Cast pointer to specific type
        #pdb.set_trace()
        elements_type = self.val['elements'].dereference()
        try:#detect null ptr by dereferencing its value
            dummy = str(elements_type)
        except gdb.MemoryError:
            return "Non initialize variable"
        
        arr='{'
        for index in range(0,last+1):
            arr+= str(index) + '=> ' + str(elements_type['ea'][index]) + (", " if index != last else "}")

        return arr


def str_lookup_function(val):
    lookup_tag = val.type.tag
    #print ('TAG => ', lookup_tag)
    if lookup_tag is None:
        return None
    #regex = re.compile("^show_vector_append__integer_vectors__vector$")
    regex = re.compile("^.*integer_vectors__vector$")
    if regex.match(lookup_tag):
        return StdStringPrinter(val)
    return None

def register_printers():
    gdb.pretty_printers.append (str_lookup_function)
    return gdb.pretty_printers

gdb.pretty_printers.append(str_lookup_function)
