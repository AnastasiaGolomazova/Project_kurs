
from asyncio.windows_events import NULL
import pandas

def find_object (list_objects, line_number): # список объектов среди которых ищем нужный блок кода и номер искомой строки
    for object in list_objects:
        if line_number >= object.line_number and line_number <= object.line_number+object.length:
            return object
    raise Exception("object not found")

def find_lines (vector_path, cpp_object): # путь программы, объект в котором проводиться анализ (из find_object)
    lines_list = cpp_object.text.split('\n')
    result  = []
    for number in vector_path[1:]:
        index = number - cpp_object.line_number
        result.append(lines_list[index])

    return result

# путь и список объектов
def master_mind (vector_path, list_object, json_file): # основной метод
    method = None
    for object in list_object:
        try:
            method = find_object(object.child,vector_path[0])
        except:
            continue
    if method == None:
        raise Exception("method not found")

    lines = find_lines(vector_path, method)
    Mamory = {1:2}
    Environment = {json_file["list_ptr_name"]:1}

    get_next = json_file["get_next"]
    set_next = json_file["set_next"]

    last_number = 1
    
    for index in range(len(vector_path)):
        line = lines[index]
        number_line = vector_path[index]
        split = line.split(' ')
        if '*' in line: # ситуация, если мы объявляем указатель
            left_ptr = split[1]
            if "=" in line:  # ситуация, если мы объявляем указатель и присваиваем значение
                rigth_ptr = split[3][:-1]
                Environment[left_ptr]=Environment[rigth_ptr]
        elif get_next in line and set_next not in line: # ситуация, если мы приравниваем указатель к getNext другого указателя
            index = split[2].index('-')           
            rigth_ptr = split[2][:index]
            left_ptr= split[0]
            Environment[left_ptr] = Environment[rigth_ptr]+1
        elif get_next in line and set_next in line:
            split = line.split("->")
            left_ptr = split[0]
            index = split[1].index('(')
            rigth_ptr = split[1][index:]
            number_node = Environment[left_ptr]
            



    

        






