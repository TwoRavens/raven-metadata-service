import json
from collections import OrderedDict

fname = 'input/a_var_specs_01.txt'
NA_CONSTANT = 'NA'

def get_file_info():
    return [x.strip().split('\t')
            for x in open(fname, 'r').readlines()
            if len(x.strip()) > 0]

def format_line(line):
    """get the defn"""
    attr, desc, jtype, format, enum, required = line

    od = OrderedDict()

    if enum == 'number, NA' and type != 'string':
        inner_od = OrderedDict()

        inner_od['type'] = jtype.split()[0]
        if format:
            inner_od['format'] = format
        if jtype.find('of numbers') > -1:
            inner_od["items"] = dict(type="number")

        #if enum:
        #    inner_od['enum'] = [x.strip()
        #                        for x in enum.split(',')
        #                        if len(x.strip()) > 0]

        od['type'] = [jtype.split()[0], 'string']
        od['description'] = desc
        od['oneOf'] = [inner_od,
                       dict(type='string',
                            enum=[NA_CONSTANT])]
        return attr, od
    else:
        od['type'] = jtype
        od['description'] = desc
        if format:
            od['format'] = format
        if enum:
            od['enum'] = [x.strip()
                          for x in enum.split(',')
                          if len(x.strip()) > 0]

        return attr, od

def run_it():

    od = OrderedDict()
    for line in get_file_info():
        print(line)
        attr, specs = format_line(line)
        od[attr] = specs

    output = json.dumps(od, indent=4)
    print(output)
    open('output/schema_out.json', 'w').write(output)

if __name__ == '__main__':
    run_it()
