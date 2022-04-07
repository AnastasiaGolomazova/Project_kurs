import json
from cpp_struct import cpp_struct

import main_algoritm

with open ("srs\params.json") as f:
    data = json.load(f)

file = open ("srs\main2.cpp")
text = file.read()

readed_structures = [] # список структур для распознования классов и методов
i= 1

# цикл ниже помогает парсить класс, который на данный момент рассматриваем

while text != "":
    end_line_index = text.index('\n')+1 # показывает окончание строки (возращает индекст перехода на сле)
    line = text[:end_line_index] # обрезаем от начала до конца строки и тем самым получаем всю строку
    if "class" in line or  "struct" in line : # если в текущей строке нет ли совпадений с "class" и "struct", то
        end_struct_index = text.index('};')+2 # находим индекс последней строки (захватывая \n);
        line = text[:end_struct_index] # обрезаем текст от начала до конца структуры
        struct = cpp_struct(i, line, "class") # создаем объект класса cpp_struct, 
#передаем номер строки начала пераваемого текста, текст от начала до конца структуры, оназвание структуры соответственно
        readed_structures.append(struct) # добавляем структуру в список
        i += line.count('\n') # увеличваем счетчик
        text = text[end_struct_index:] # обрезаем текст от конца последней строки и до конца всего текста
    else:
        text = text[end_line_index:] # обрезаем текст от конца последней строки и до конца всего текста
        i+=1 # увеличваем счетчик

# вывод класса в консоль и соответствующих строк каждому методу

for i in readed_structures :
    print(i)
    print(i.line_number)
    index = 0
    for j in i.child:
        print(j.line_number,j.text)
        index+=1

# поиск утечек памяти и их вывод в файл "output" (можно открыть файл "output" через exel)

#main_algoritm.master_mind(data["path_ex1"],readed_structures,data)
#main_algoritm.master_mind(data["path_ex2"],readed_structures,data)
#main_algoritm.master_mind(data["path_ex3"],readed_structures,data)
main_algoritm.master_mind(data["path_ex4"],readed_structures,data)
