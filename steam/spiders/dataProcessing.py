# Created by pranaykhattri at 16/11/20
from bs4 import BeautifulSoup
import pandas as pd
import os, fnmatch
import codecs

def cleanData(data):
    statement_list = []
    for count,datum in enumerate(data):
        soup = BeautifulSoup(datum)
        #text = (soup.find('div').getText() if (soup.find('div')!=None) else "")
        text = [t.getText() if t!=None else "" for t in soup.find_all('div')]
        text = list(dict.fromkeys(text))
        text_list = [t.replace('\\t','').replace('\\r','') for t in text]
        # presence of /n means start of next line. So look for that and append statements in a list
        texts = [t for text in text_list for t in text.split('\\n') ]
        texts = list(dict.fromkeys(texts))
        statements = [t.strip('\\') for t in texts]
        statements = list(filter(None, statements))
        statement_list.extend(list(filter(None, statements)))
    return statement_list

def getDataWithContext(context, statements_list):
    curr_minus_2 = ''
    curr_minus_1 = ''
    curr = ''
    dict = {"context":[], "by":[], "when":[],"post":[]}
    for index, curr in enumerate(statements_list):
        if context in curr:
            if index>=2:
                curr_minus_1 = statements_list[index-1]
                curr_minus_2 = statements_list[index-2]
            #print (curr_minus_2, "  ", curr_minus_1, "  ", curr)
            if curr_minus_2 not in dict['by'] and curr_minus_1 not in dict['context'] and curr not in dict['post']:
                dict['context'].append(context)
                dict['by'].append(curr_minus_2)
                dict['when'].append(curr_minus_1)
                dict['post'].append(curr)
    return pd.DataFrame(dict)

if __name__ == '__main__':
    path = os.path.abspath(os.getcwd())
    html_files = []
    listOfFiles = os.listdir(('/'.join((path.split('/')[:-2]))).__str__())
    pattern = "*.html"
    for entry in listOfFiles:
        if fnmatch.fnmatch(entry, pattern):
            html_files.append(entry)
    for file in html_files:
        f = open(('/'.join((path.split('/')[:-2]))).__str__()+"/"+ file, "r")
        responses = []
        for response in f:
            response = response.split("****break****")
            responses.extend(response)
        fixed_responses = [r.strip("****break****")[1:-1] for r in responses]

        ## sending list of responses for a game to get a long list of cleaned statements
        statements = cleanData(fixed_responses)

        ## now picking our data from this cleaned list of statements
        dict = {"context": [], "by": [], "when": [], "post": []}
        df = pd.DataFrame(dict)
        context_list = ['crash', 'bug', 'feature']
        for context in context_list:
            #context = "crash"
            df1 = getDataWithContext(context, statements)
            df = df.append(df1, ignore_index=True)
        pd.DataFrame.to_csv(df, ('/'.join((path.split('/')[:-2]))).__str__()+"/"+ file.split('.')[0]+".csv")