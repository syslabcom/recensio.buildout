import xlrd
import sys

xls_filename = sys.argv[1]
start_row = int(sys.argv[2])
levels = int(sys.argv[3])
xls_file = xlrd.open_workbook(xls_filename)
sheet = xls_file.sheets()[0]

last_level = [{'key' : 'root', 'children': []}, {}, {}, {}]

xml_container = '''<?xml version="1.0" encoding="utf-8"?>
<vdex xmlns="http://www.imsglobal.org/xsd/imsvdex_v1p0"
      xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
      xsi:schemaLocation="http://www.imsglobal.org/xsd/imsvdex_v1p0
                          imsvdex_v1p0.xsd imsvdex_v1p0_thesaurus.xsd
                          http://www.imsglobal.org/xsd/imsmd_rootv1p2p1
                          imsmd_rootv1p2p1.xsd"
      orderSignificant="true"
      profileType="flatTokenTerms"
      language="en">
  <vocabName>
    <langstring language="en">International Standard Classification of Occupations, ISCO-88</langstring>
  </vocabName>
  <vocabIdentifier>ISCO88</vocabIdentifier>
  %s
</vdex>'''

xml_term = '''<term>
<termIdentifier>%(key)s</termIdentifier>
<caption>
<langstring language="de">%(german)s</langstring>
<langstring language="en">%(english)s</langstring>
<langstring language="fr">%(french)s</langstring>
</caption>
%(children)s
</term>'''


for rowid in range(start_row, sheet.nrows):
    row = sheet.row(rowid)
    key = row[levels + 2].value
    if not key:
        continue
    for level in range(levels + 2):
        if row[level].value:
            break
    if level == levels + 1:
        continue
    german = row[level].value
    english = row[levels + 1 + 2 + level].value
    try:
        french = row[2 * (levels + 1) + 2 + level].value
    except:
        import pdb;pdb.set_trace()
        french = row[8 + level].value
    new_data = {'key' : key,
                'german' : german,
                'english' : english,
                'french' : french,
                'children' : []}
    last_level[level + 1] = new_data
    last_level[level]['children'].append(new_data)

def convert(item):
    children = '\n'.join([convert(x) for x in item['children']])
    # XXX Never do this in real code! you are modifying the original input arg
    item['children'] = children
    return xml_term % item

xml_data = xml_container % '\n'.join([convert(x) for x in last_level[0]['children']])

print xml_data.encode('utf8')
