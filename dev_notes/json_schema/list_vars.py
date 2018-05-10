import json
from collections import OrderedDict

fname = 'input/test_data.json'


def get_file_dict():
    info = None
    with open(fname, 'r') as f:
        content = f.read()
        info = json.loads(content, object_pairs_hook=OrderedDict)
    return info['data']


def get_keys(dict_info):
    """return key info"""
    key_list = []
    for k in dict_info.keys():
        print(k)
        key_list.append(k)
    return key_list

def run_it():

    info = get_file_dict()
    print(info.keys())
    sections = OrderedDict()

    info_pieces = (('self', info['self']),
                   ('dataset', info['dataset']),
                   ('dataset.dataSource', info['dataset']['dataSource']),
                   ('variable', info['variables']['year']),
                   ('variableDisplay.editable', info['variableDisplay']['editable']),
                   ('variableDisplay', info['variableDisplay']['ccode']),
                  )

    for name, section_info in info_pieces:
        if isinstance(section_info, list):
            sections[name] = section_info
        else:
            sections[name] = list(section_info.keys())

    print(json.dumps(sections, indent=4))
    output_lines = []
    for section_name, section_attrs in sections.items():
        output_lines.append(section_name)
        for name in section_attrs:
            output_lines.append('\t%s' % name)
    print('\n'.join(output_lines))
    open('output/list.txt', 'w').write('\n'.join(output_lines))



if __name__ == '__main__':
    run_it()
