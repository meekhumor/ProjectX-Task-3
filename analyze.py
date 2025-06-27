def remove_whitespaces_from_end(clone):
    if clone[len(clone) - 1] == ' ' and len(clone) >= 80:
        return remove_whitespaces_from_end(clone[:len(clone) - 1])
    return clone[:len(clone)]

def line_length_violation(clone):
    if len(clone) < 80:
        return False
    remove_whitespaces_from_end(clone)
    if len(clone) < 80:
        return False
    return True

def remove_comment(clone):
    if clone.find('#') >= 0:
        return clone[:clone.find('#')]
    else:
        return clone

def check_unclosed_string(clone):
    no_of_double = 0
    no_of_single = 0
    for char in clone:
        if char == '\'':
            no_of_single += 1
        elif char == '\"':
            no_of_double += 1
    return no_of_double % 2 != 0 or no_of_single % 2 != 0

def check_print(word):
    if "print" in word:
        return True
    return False

def check_eval(word):
    if "eval" in word:
        return True
    return False

def check_exec(word):
    if "exec" in word:
        return True
    return False

def check_violations(line):
    no_of_violations_for_this_line = 0
    clone = line
    if line_length_violation(clone):
        no_of_violations_for_this_line += 1
    clone = remove_comment(clone)
    if check_unclosed_string(clone):
        no_of_violations_for_this_line += 1
    wordlist = clone.split()
    forbidden_keyword_was_used_in_this_line = False
    for word in wordlist:
        if check_eval(word):
            no_of_violations_for_this_line += 1
            forbidden_keyword_was_used_in_this_line = True
        if check_exec(word):
            no_of_violations_for_this_line += 1
            forbidden_keyword_was_used_in_this_line = True
        if check_print(word):
            no_of_violations_for_this_line += 1
            forbidden_keyword_was_used_in_this_line = True
    return no_of_violations_for_this_line, forbidden_keyword_was_used_in_this_line

no_of_files = int(input("enter the total number of files to be analyzed: "))
file_path_list = []
no_of_violations_list_filewise = []
forbidden_keyword_used_list_filewise = []

for _ in range(no_of_files):
    no_of_violations_in_this_file = 0
    forbidden_keyword_was_used_in_this_file = False
    file_path = input("enter file path: ")
    with open(file_path, 'r') as f:
        for line in f:
            no_of_violations_in_this_line, forbidden_keyword_was_used_in_this_line = check_violations(line)
            no_of_violations_in_this_file += no_of_violations_in_this_line
            forbidden_keyword_was_used_in_this_file = forbidden_keyword_was_used_in_this_file or forbidden_keyword_was_used_in_this_line
    file_path_list.append(file_path)
    no_of_violations_list_filewise.append(no_of_violations_in_this_file)
    forbidden_keyword_used_list_filewise.append(forbidden_keyword_was_used_in_this_file)

max_path_length = 9
for i in range(no_of_files):
    if len(file_path_list[i]) > max_path_length:
        max_path_length = len(file_path_list[i])

s = '| Sr. No. | File Path '
for _ in range(9, max_path_length):
    s += ' '
s += '| Status    | No of violations |'
print(s)

for i in range(no_of_files):
    
    s = '|       ' + str(i + 1) + ' | ' + file_path_list[i]
    
    for i in range(max_path_length - len(file_path_list[i])):
        s += " "
    s += " | "
    
    if no_of_violations_list_filewise[i] == 0:
        s += "CLEAN     | 0                |"
    elif no_of_violations_list_filewise[i] > 5 or forbidden_keyword_used_list_filewise[i]:
        s += "HIGH RISK | "
        s += str(no_of_violations_list_filewise[i])
        if no_of_violations_list_filewise[i] <= 9:
            s += "                |"
        elif no_of_violations_list_filewise[i] <= 99:
            s += "               |"
        else:
            s += "              |"
    else:
        s += "LOW RISK  | "
        s += str(no_of_violations_list_filewise[i])
        s += "                |"
    print(s)