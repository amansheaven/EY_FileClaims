from fuzzywuzzy import fuzz,process
def reger(matcher, cor):
    text_lin = cor.split('\n')
    #lin_sel for the fuzzy selected in the line
    lin_sel = process.extractOne(matcher, text_lin)
    print(lin_sel[0])
    lin_tokens = lin_sel[0].split(' ')
    print(lin_tokens)
    print(matcher.split(' '))
    for word in matcher.split(' '):
        token = process.extractOne(word, lin_tokens)
        print(token)
        lin_tokens.remove(token[0])
#     print(lin_tokens)
    out=' '.join(lin_tokens)
#     print('out '+out)
    return out


def reger_find(matcher, cor):
    out = ''
    text_lin = cor.split('\n')
    #lin_sel for the fuzzy selected in the line
    lin_sel = process.extractOne(matcher, text_lin)
    print(lin_sel[0])
    lin_tokens = lin_sel[0].split(' ')
    print(lin_tokens)

    print(matcher.split(' '))
    for word in matcher.split(' '):
        token = process.extractOne(word, lin_tokens)
        print(out)
        out = out +' ' + token[0]
        
#     print('out '+out)
    return out



def initiate(query_string, corpus, mode):
    if mode ==0:
        text = reger(query_string, corpus)
    else :
        query_string.lstrip()
        query_string.rstrip()
        text = reger_find(query_string, corpus)



    print(text)
    text = text.lstrip()
    text  = text.rstrip()
    if ':'in text or '-' in text:
        print('removing')
        text = text.strip(':')
        text = text.strip('-')
        text = text.strip(':')
        
    return text
