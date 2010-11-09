# This is a one off script which of course would love to see implemented
# as a real test.
examples = {
     'presentation_monograph' : 'http://recensio00.fe.rzob.gocept.net/Members/Henrike/auf-dem-weg-nach-europa/'
    ,'presentation_article' : 'http://recensio00.fe.rzob.gocept.net/Members/gerken/dfg/'
    ,'presentation_net' : 'http://recensio00.fe.rzob.gocept.net/Members/Henrike/europaische-friedensvertrage-online/'
    ,'presentation_collection' : 'http://recensio00.fe.rzob.gocept.net/Members/rohschuermann/europa-und-seine-grenzen-im-mittelalter/'
    ,'review_mono' : 'http://recensio00.fe.rzob.gocept.net/rezensionen/zeitschriften/jahrbucher-fur-geschichte-osteuropas/jahrbuecher-fuer-geschichte-osteuropas.-neue-folge-58-2010/heft-1/der-nationalsozialistische-judenmord-und-das-polnische-juedische-verhaeltnis-im-diskurs-der-polnischen-untergrundpresse-194220131944/'
    ,'review_mag' : 'http://recensio00.fe.rzob.gocept.net/rezensionen/zeitschriften/zeitschrift-fur-balkanologie/test-vol/test-issue/ReviewJournal237570024/'
}
sheet_info = {
     'presentation_monograph' : 2
    ,'presentation_article' : 4
    ,'presentation_net' : 5
    ,'presentation_collection' : 3
    ,'review_mono' : 0
    ,'review_mag' : 1
}

startpage = 'http://recensio00.fe.rzob.gocept.net?setLanguage=en&set_language=en'
from zope.testbrowser.browser import Browser
def viewPage(br):
    file('/tmp/bla.html', 'w').write(br.contents)
br = Browser(startpage)
br.getLink('Log in').click()
br.getControl('Login Name').value = 'gerken'
br.getControl('Password').value = 'readme'
br.getControl('Log in').click()
import xlrd
excel = xlrd.open_workbook('fields.xls')

field_data = {}
for key, sheet_index in sheet_info.items():
    new_data = {}
    sheet = excel.sheet_by_index(sheet_index)
    index = 0
    for i in range(1, sheet.nrows):
        if not sheet.cell_value(i, 2):
            continue
        new_data[index] = {'label' : '>' + sheet.cell_value(i, 2).strip() + '<',
                       'description' : '>' + sheet.cell_value(i, 5).strip() + '<'}
        index += 1
    field_data[key] = new_data


for type_name, example_url in examples.items():
    for i in range(3):
        print '-' * 80
    print type_name, example_url
    found_data = {}
    bads = []
    br.open(example_url)
    br.getLink('Edit').click()
#    br.open(br.url + '?setLanguage=en&set_language=en')
    br.open(br.url)
    data = br.contents
    should_be_data = field_data[type_name]
    for should_be_values in should_be_data.values():
        good = True
        index = data.find(should_be_values['label'])
        if index == -1:
            good = False
        if should_be_values['description']:
            if data.find(should_be_values['description']) == -1:
                good = False
        if not good:
            bads.append(should_be_values['label'])
        position = index
        while found_data.has_key(position):
            if position > 0:
                position = data.find(should_be_values['label'], position + 1)
            else:
                position -= 1
        found_data[position] = should_be_values['label']
    positions = found_data.keys()
    positions.sort()
    print '=' * 80
    field_length = 50
    bads = [x[:field_length -1] for x in bads]
    table_string = '%%05s %%0%is %%0%is' % (field_length, field_length)
    print table_string % ("Exists", "Should be", "Is")
    for should_be, is_ in enumerate(positions):
        if is_ > 0:
            is_ = found_data[is_][:field_length - 1]
        else:
            is_ = ''
        should_be = should_be_data[should_be]['label'][:field_length - 1]
        bad = should_be not in bads
        print table_string % (bad, should_be, is_)
