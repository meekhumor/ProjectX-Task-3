import os

cwd=os.getcwd()+'\\src'

def length_violated(file_name): #Checks line lengths by iterating over each line
    len_violated=0
    with open(cwd+"\\"+file_name) as file:
        for line in file:
            if (len(line.strip())>80):
                len_violated+=1
    return len_violated

def forbidden_keywords(file_name): #Counts usage of forbidden keywords. Ignores comments.
    forbidden_count=0
    with open(cwd+"\\"+file_name) as file:
        for line in file:
            line=line.strip()
            if line.count("#"):
                line=line.split("#")[0].strip()
            forbidden_count+=line.count("print") + line.count("eval") +line.count("exec")
    return forbidden_count

def unclosed_quotes(file_name): #Counts unclosed quotes in strings. Also ignores comments.
    quote_violations=0
    with open(cwd+"\\"+file_name) as file:
        for line in file:
            if line.count("#"):
                line=line.split("#")[0].strip()
            if line.count('"')%2==1 or line.count("'")%2==1:
                quote_violations+=line.count('"')%2 + line.count("'")%2
    return quote_violations

def analyze(file):
    violations=length_violated(file)+unclosed_quotes(file)
    forbidden= forbidden_keywords(file)
    if forbidden>0 or violations>5:
        return "HIGH RISK"
    if forbidden==0 and violations==0:
        return "CLEAN"
    if forbidden==0 and violations<=5:
        return "LOW RISK"
    return ""



for file in os.listdir("./src"):
    if file.endswith(".py"):
        print("src/"+file," : ",analyze(file))
