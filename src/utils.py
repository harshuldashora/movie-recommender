import ast


def convert(text):
    L = []
    try:
        for i in ast.literal_eval(text):
            L.append(i['name'])
    except:
        return []
    return L

def fetch_director(text):
    L = []
    try:
        for i in ast.literal_eval(text):
            if i['job'] == 'Director':
                L.append(i['name'])
    except:
        return []
    return L
def clean_list(items):
    return [i.replace(" ","").lower() for i in items]

