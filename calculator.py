import math


set_numbers = {'1','2','3','4','5','6','7','8','9','0','.'}
set_sign = {'+': 1, '-': 1, '*': 2, '/': 2}
set_skob = {'(',')'}
set_func = {'exp', 'ln', 'sin', 'cos', 'sqrt'}
set_const = {'pi'}
set_others = {'^'}

def find_error(array):
    check = 0
    vspom = []
    for i in range(len(array)):
        if array[i] not in set_skob:
            if array[0:i].count('(') - array[0:i].count(')') == \
               array[i:].count(')') - array[i:].count('('):
                return(array, check)
            else:
                check = 1
                return('Неправильная скобочная последовательность!', check)

def find(a):
    i = 0
    check = 0
    while i < len(a)-1:
        if type(a[i]) == float:
            if a[i+1] in set_sign or a[i+1] in set_others \
               or a[i+1] == ')':
                i += 1
            else:
                check = i
                break
        elif a[i] in set_sign:
            if type(a[i+1]) == float or a[i+1] in set_skob \
               or a[i+1] in set_func or a[i+1] in set_const:
                i += 1
            else:
                check = i
                break
        elif a[i] in set_skob:
            if type(a[i+1]) == float or a[i+1] in set_skob \
               or a[i+1] in set_func or a[i+1] in set_const \
               or a[i+1] in set_sign:
                i += 1
            else:
                check = i
                break
        elif a[i] in set_func:
            if a[i+1] in set_skob or type(a[i+1]) == float \
               or a[i+1] in set_const or a[i+1] in set_func:
                i += 1
            else:
                check = i
                break
        elif a[i] in set_const:
            if a[i+1] in set_sign or a[i+1] in set_others \
               or a[i+1] in set_skob:
                i += 1
            else:
                check = i
                break
        elif a[i] in set_others:
            if a[i+1] not in set_sign:
                i += 1
            else:
                check = i
                break
    if check == 0:
        if a[len(a)-1] == ')' or type(a[len(a)-1]) == float:
            return (a, check)
        else:
            check = 1
            return ('Некорректный ввод!', check)
    else:
        return ('Некорректный ввод!', check)
    
def parser(a):
    array = []
    check = 0
    memory = ''
    letter_memory = ''
    i = 0
    while i < len(a):
        if a[i] == ' ':
            if memory == '':
                i += 1
            else:
                array.append(float(memory))
                memory = ''
                i += 1
        elif a[i] in set_others:
            if memory == '':
                array.append(a[i])
                i += 1
            else:
                array.append(float(memory))
                memory = ''
                array.append(a[i])
                i += 1
        elif a[i] in set_skob:
            if memory == '':
                array.append(a[i])
                i += 1
            else:
                array.append(float(memory))
                memory = ''
                array.append(a[i])
                i += 1
        elif a[i] in set_numbers:
            memory += a[i]
            i += 1
        elif a[i] in set_sign:
            if a[i+1] == ' ':
                array.append(a[i])
                i += 1
            else:
                if a[i] == '-':
                    memory += a[i]
                    i += 1
                else:
                    check = 1
                    return('Неправильный ввод: ' + a[i], check)
        else:
            letter_memory += a[i]
            if letter_memory in set_func or letter_memory in set_const:
                array.append(letter_memory)
                letter_memory = ''
            i += 1
    if letter_memory != '':
        check = 1
        return('Непонятные символы: ' + letter_memory, check)
    if memory != '':
        array.append(float(memory))
    return(array, check)

def RPN (a):
    out = []
    stack = []
    for elem in a:
        if type(elem) == float or elem in set_const:
            out.append(elem)
        elif elem in set_others or elem in set_func:
            stack.append(elem)
        elif elem == '(':
            stack.append(elem)
        elif elem == ')':
            y = len(stack)
            while y > 0:
                if stack[y-1] != '(':
                    out.append(stack.pop(y-1))
                    y-=1
                else:
                    stack.pop(y-1)
                    break
        elif elem in set_sign:
            if stack == []:
                stack.append(elem)
            else:
                x = len(stack)
                while x > 0:
                    if (stack[x-1] in set_sign and \
                        set_sign[stack[x-1]] >= set_sign[elem]) \
                       or stack[x-1] in set_func or stack[x-1] in set_others:
                        out.append(stack.pop(x-1))
                        x -= 1
                    else:
                        break
                stack.append(elem)
    j = len(stack)
    while j > 0:
        out.append(stack.pop(j-1))
        j -= 1
    return(out)
def calc(a):
    stack = []
    for elem in a:
        if type(elem) == float:
            stack.append(elem)
        elif elem == 'pi':
            stack.append(math.pi)
        elif elem == '+':
            stack.append(stack.pop(len(stack)-2) + stack.pop(len(stack)-1))
        elif elem == '-':
            stack.append(stack.pop(len(stack)-2) - stack.pop(len(stack)-1))
        elif elem == '*':
            stack.append(stack.pop(len(stack)-2) * stack.pop(len(stack)-1))
        elif elem == '^':
            stack.append(stack.pop(len(stack)-2) ** stack.pop(len(stack)-1))
        elif elem == '/':
            if stack[len(stack)-1] != 0:
                stack.append(stack.pop(len(stack)-2) / stack.pop(len(stack)-1))
            else:
                return('Деление на ноль!')
        elif elem == 'exp':
            stack.append(math.exp(stack.pop(len(stack)-1)))
        elif elem == 'ln':
            stack.append(math.log(stack.pop(len(stack)-1)))
        elif elem == 'sin':
            stack.append(math.sin(stack.pop(len(stack)-1)))
        elif elem == 'cos':
            stack.append(math.cos(stack.pop(len(stack)-1)))
        elif elem == 'sqrt':
            stack.append(math.sqrt(stack.pop(len(stack)-1)))
    return(stack)
ed = input()
if parser(ed)[1] == 1:
    print(parser(ed)[0])
else:
    if find_error(parser(ed)[0])[1] == 1:
        print(find_error(parser(ed)[0])[0])
    else:
        if find(find_error(parser(ed)[0])[0])[1] != 0:
            print(find(find_error(parser(ed)[0])[0])[0])
        else:
            print(calc(RPN(find(find_error(parser(ed)[0])[0])[0]))[0])
