import xml.etree.ElementTree as ET
import xlrd
import xlwt
from xlwt import Workbook 
from translator import Translator
from bs4 import BeautifulSoup
import nltk
nltk.download('punkt')
from nltk.tokenize import sent_tokenize
import os


path = 'C:/Users/DaireStokes/OneDrive - GOAL/Documents/Learning content/Cybersecurity/CS_fundamentals/I18n/French/verified/'
file = 'Cybersecurity-fundamentals - test.xlf'
xlf_path = os.path.join(path, file)
'''
# file read stream to BS4 object
with open(xlf_path, 'r', encoding='utf8') as file:
    data = file.read()


# create XLIFF representation
soup = BeautifulSoup(data)'''
         

                   
# create workbook
book = xlwt.Workbook(encoding='utf-8')
sheet1 = book.add_sheet('source-language')

def import_file(path=xlf_path):
    #Set the path
    path = 'C:/Users/DaireStokes/OneDrive - GOAL/Documents/Learning content/Cybersecurity/CS_fundamentals/I18n/French/verified/'
    file = 'Cybersecurity-fundamentals.xlf'
    xlf_path = os.path.join(path, file)

    with open (xlf_path, encoding='utf8') as file:
        data = file.read()
    
    # parse and store contents of XLF
    soup = BeautifulSoup(data, 'xml')
    return soup


# get the target and source languages
def set_languages(xliff):
    target_lang =xliff.find('file').get('target-language')
    source_lang = xliff.find('file').get('source-language')
    
    # TODO: write target-language attribute to the XLF file
    
    # create a file name for each XLF file (player or content)
    if xliff.find('file').get('original') != 'English':
        source_fname = f'{path}content_{source_lang}_text.xls'
        target_fname = f'{path}content_{target_lang}_text.xls'
    elif xliff.find('file').get('original') == 'English':
        source_fname = f'{path}player_{source_lang}_text.xls'
        target_fname = f'{path}player_{target_lang}_text.xls'
    else:
        input('Check your file has the attribute original=\"English\" (or other language) or original=\"course\"')

    return source_lang, target_lang, source_fname, target_fname



def copy_source_to_target(xlf):              
    for root in xlf:
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
    



#retrieve each element within a source tag and save it to a source file

# need to pull nested <g> tag contents as individual rows
# print tag_id to troubleshoot

# FIXME: infinite loop
def write_source_text(nodes, sheet='sheet1'):
    i=0
    if list(nodes):
        for tag in nodes:
            if list(tag):
                write_source_text(tag)
            else:
                sheet.write(i, 0, tag.get_text())
                i = i + 1

    # save source text to XLS file
    book.save(source_fname)


def write_translation_xls(source_lang, source_fname, target_lang, target_fname):
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
                if value:
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

    return translatedtext

def write_target_recursive(root, translations): 
    i = 0
    # if the node has child elements, go to next child
    for child in root:
        if child.tag == '{urn:oasis:names:tc:xliff:document:1.2}target' or child.tag == '{urn:oasis:names:tc:xliff:document:1.2}g':
            if not list(child):
                # check the number of sentences
                split_txt_by_tag(child)
                child.text = translations[i]
                i = i + 1
            else:
                write_target_recursive(root)
        else:
            write_target_recursive(child)




#One by one store the translated text within the respective target tag and save it.
# FIXME: not writing the sub elements belonging to the source element - just writing in the text, losing the structure
def write_translation(root=soup):
    i=0            
    for trans in root:
        for header in trans:
            for body in header:
                for target in body:
                    if target.tag == '{urn:oasis:names:tc:xliff:document:1.2}target':
                        for child in target:
                            child.text = translatedtext[i]
                        i=i+1

    return root

def split_txt_by_tag(tag):
    # count sentences
    text = tag.text
    num_sentences = sent_tokenize(text)
    return len(num_sentences)
    
# write XLIFF tree to file
with open(xlf_path, 'wb') as file:
    tree.write(file, encoding='utf-8', xml_declaration=True)

                
'''xliff_file.write(str(root), encoding='utf-8', xml_declaration=True)
xliff_file.close()'''
   
    

# import file
soup = import_file()

# set languages
source_lang, target_lang, source_fname, target_fname = set_languages(soup)

# copy source tags to create target tags
copy_source_to_target(soup)

# write translations to translations file
translations = write_translation_xls(source_lang, source_fname, target_lang, target_fname)

# not validated yet
# replace target tag text with verified translations
write_target_recursive(soup)