import json
from class1 import cpp_struct

import main_algoritm

with open ("Srs\Params.json") as f:
    data = json.load(f)

file = open ("Srs\main.cpp")
text = file.read()

readed_structures = [] # список структур для распознования классов и методов
i= 1

while text != "":
    end_line_index = text.index('\n')+1 # показывает окончание строки (возращает индекст перехода на сле)
    line = text[:end_line_index] # обрезаем от начала до конца строки и тем самым получаем всю строку
    if "class" in line or  "struct" in line : # если в текущей строке нет ли совпадений с "class" и "struct", то
        end_struct_index = text.index('};')+2 # находим индекс последней строки (захватывая \n);
        line = text[:end_struct_index] # обрезаем текст от начала до конца структуры
        struct = cpp_struct(i, line, "class") 
        readed_structures.append(struct)
        i += line.count('\n')
        text = text[end_struct_index:]
    else:
        text = text[end_line_index:]
        i+=1


for i in readed_structures :
    print(i)
    print(i.line_number)
    index = 0
    for j in i.child:
        print(j.line_number,j.text)
        index+=1


main_algoritm.master_mind(data["path"],readed_structures,data)
