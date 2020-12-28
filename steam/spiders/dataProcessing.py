# Created by pranaykhattri at 16/11/20
from bs4 import BeautifulSoup
import pandas as pd
import codecs

def cleanData(data):
    statement_list = []
    for count,datum in enumerate(data):
        soup = BeautifulSoup(datum)
        text = (soup.find('div').getText() if (soup.find('div')!=None) else "")
        text = text.replace('\\t','').replace('\\r','')
        # presence of /n means start of next line. So look for that and append statements in a list
        texts = text.split('\\n')
        statements = [t.strip('\\') for t in texts]
        statements = list(filter(None, statements))
        statement_list.extend(list(filter(None, statements)))
    return statement_list

def getDataWithContext(context, statements_list):
    curr_minus_2 = ''
    curr_minus_1 = ''
    curr = ''
    dict = {"by":[], "when":[],"post":[]}
    for index, curr in enumerate(statements_list):
        if context in curr:
            if index>=2:
                curr_minus_1 = statements_list[index-1]
                curr_minus_2 = statements_list[index-2]
            #print (curr_minus_2, "  ", curr_minus_1, "  ", curr)
            dict['by'].append(curr_minus_2)
            dict['when'].append(curr_minus_1)
            dict['post'].append(curr)
    return pd.DataFrame(dict)

if __name__ == '__main__':
    f = open("/Users/pranaykhattri/Downloads/NLP_RA/steam-scraper-master/sc_kenshi.html", "r")
    responses = []
    for response in f:
        response = response.split("****break****")
        responses.extend(response)
    fixed_responses = [r.strip("****break****")[1:-1] for r in responses]

    ## sending list of responses for a game to get a long list of cleaned statements
    statements = cleanData(fixed_responses)

    ## now picking our data from this cleaned list of statements
    context = "crash"
    df = getDataWithContext(context, statements)