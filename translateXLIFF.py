import xml.etree.cElementTree as ET
import xlrd
import xlwt
from xlwt import Workbook 
from translator import Translator
from bs4 import BeautifulSoup


#Set the path
path = 'C:/e-learning/Cybersecurity/CS_Fund/french/translationtxt/Cybersecurity-fundamentals-spanish.xlf'
course_player = int(input("Are you translating course content or course player labels? 1 = content  2 = player labels...     "))
player_source_lang = "English"

tree = ET.parse(path) # TODO: remove this

with open (path, encoding='utf8') as file:
    data = file.read()

# parse and store contents of XLF
trans_xlf = BeautifulSoup(data, 'xml')


# get the target and source languages
if course_player == 1:
    target_lang = trans_xlf.find('file', {'original': {'course'}}).get('target-language')
    source_lang = trans_xlf.find('file', {'original': {'course'}}).get('source-language')
    source_fname = f'content_{source_lang}_text.xls'
    target_fname = f'content_{target_lang}_text.xls'
elif course_player == 2:
    target_lang = trans_xlf.find('file', {'original': {player_source_lang}}).get('target-language')
    source_lang = trans_xlf.find('file', {'original': {player_source_lang}}).get('source-language')
    source_fname = f'player_{source_lang}_text.xls'
    target_fname = f'player_{target_lang}_text.xls'
else:
    input('Enter \'1\' or \'2\'.....   ')

root = trans_xlf


# open the translation file
xliff_file = open(path, 'w', encoding='utf-8')


for root in root:
    for file in root.findAll('file'):
        for body in file:
            for trans in body:
                if not trans == '\n': # only write the tag when <trans-unit><target> does not exist
                    if not trans.target:
                        # get the entire source tag first
                        target = str(trans.source).replace('<source>', '<target>')
                        target = target.replace('</source>', '</target>')
                        target_tag = BeautifulSoup(target, 'xml')
                        trans.append(target_tag)
    
xliff_file.write(str(root))                    
                   
# create workbook
book = xlwt.Workbook(encoding='utf-8')
sheet1 = book.add_sheet('source-language')


#retrieve each element within a source tag and save it to a source file
i=0

# need to pull nested <g> tag contents as individual rows
# print tag_id to troubleshoot
for tag in trans_xlf.findAll('source'):
    tag_txt = tag.get_text()
    sheet1.write(i, 0, tag.get_text())
    i = i + 1

# save source text to XLS file
book.save(source_fname)

# create instance of the text translator
translator = Translator()
#Writing to file
wb = Workbook()
sheet1 = wb.add_sheet('target-language')


#Reading file
wb_r = xlrd.open_workbook(source_fname)
sheet = wb_r.sheet_by_index(0)
sheet.cell_value(0,0)
print('********************')

#for each row and column, fetch the text, translate, and save in translate file
for column in range(sheet.nrows):
    for row in range(sheet.ncols):
        value = str(sheet.cell_value(column, row))
	  #To detect any other xml tags within the source tag
        htmltag=bool(BeautifulSoup(value, "html.parser").find())
        if (htmltag):
            sheet1.write(column, row, value)
        else:
            value = translator.translate_text(value, source_lang, target_lang)
            value=str(value).strip()
            sheet1.write(column, row, value)

# save target text to XLS 
wb.save(target_fname)


#create a list and store all the translated text
translatedtext=[]


# open the source XLS 
twb_r = xlrd.open_workbook(target_fname)
tsheet = twb_r.sheet_by_index(0)
tsheet.cell_value(0,0)
# opening the destination excel file 
for column in range(tsheet.nrows):
    for row in range(tsheet.ncols):
        value = str(tsheet.cell_value(column, row))
        translatedtext.append(value)


#get the root element 
tree=ET.ElementTree(file=path)
root=tree.getroot()

#One by one store the translated text within the respective target tag and save it.
'''
for file in root.findAll('file'):
    for body in file:
        for target in body:
            target=str(translatedtext[i])
            i=i+1
'''  

i=0            
for trans in root:
    for header in trans:
        for body in header:
            for target in body:
                if(target.tag=='{urn:oasis:names:tc:xliff:document:1.2}target'):
                    target.text=(translatedtext[i])
                    #print(target.text)
                    i=i+1

xliff_file.write(ET.tostring(tree), encoding='utf-8')

                
'''xliff_file.write(str(root), encoding='utf-8', xml_declaration=True)
xliff_file.close()'''


