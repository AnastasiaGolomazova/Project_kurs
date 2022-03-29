
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
        index = number - cpp_object.line_number -2
        clean_lines = lines_list[index].replace("\t", "")
        result.append(clean_lines)


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

    head = json_file["list_ptr_name"]

    Environment = {head:1}

    get_next = json_file["get_next"]
    set_next = json_file["set_next"]

    data = pandas.DataFrame({'Mamory':{}, 'Environment':{}, 'Line':{}, 'Data_loss':{}})
    data = data.append({'Mamory':'<1,2>', 'Environment':f'+<{Environment[head]},{head}>', 'Line':vector_path[0], 'Data_loss':''}, ignore_index=True)
   
    
    for index in range(len(vector_path)-1):
        line = lines[index]
        number_line = vector_path[index+1]
        split = line.split(' ')
        row = {}
        if '*' in line: # ситуация, если мы объявляем указатель
            left_ptr = split[1]
            if "=" in line:  # ситуация, если мы объявляем указатель и присваиваем значение
                rigth_ptr = split[3][:-1]
                Environment[left_ptr]=Environment[rigth_ptr]
                row = {'Mamory':'', 'Environment':f'+<{Environment[left_ptr]},{left_ptr}>', 'Line':number_line, 'Data_loss':''}
        elif 'delete' in line:
            delete_node = split[1] # TODO доделать 

        elif "new" in line and head in line:
            Environment[head] = -1
            Mamory[-1] = -2
            row = {'Mamory':'<-1,-2>', 'Environment':f'+<{Environment[left_ptr]},{left_ptr}>', 'Line':number_line, 'Data_loss':''}

        elif get_next in line and set_next not in line: # ситуация, если мы приравниваем указатель к getNext другого указателя
            index = split[2].index('-')           
            rigth_ptr = split[2][:index]
            left_ptr= split[0]
            Environment[left_ptr] = Environment[rigth_ptr]+1
            left_node = Environment[left_ptr]
            Mamory[left_node] = left_node + 1

            row = {'Mamory':f'<{left_node},{Mamory[left_node]}>', 'Environment':f'+<{Environment[left_ptr]},{left_ptr}>', 'Line':number_line, 'Data_loss':''}

        elif '=' in line:
            left_ptr= split[0]
            rigth_ptr = split[2][:-1]
            Environment[left_ptr] = Environment[rigth_ptr]
            row = {'Mamory':'', 'Environment':f'+<{Environment[left_ptr]},{left_ptr}>', 'Line':number_line, 'Data_loss':''}

        elif get_next in line and set_next in line: # ситуация, когда есть get_next и set_next 
            split = line.split("->")
            left_ptr = split[0]
            index = split[1].index('(')
            rigth_ptr = split[1][index+1:]
            number_node = Environment[left_ptr]
            right_number = Environment[rigth_ptr]
            Mamory[number_node] = Mamory[right_number]

            row = {'Mamory':f'<{number_node},{Mamory[number_node]}>', 'Environment':'', 'Line':number_line, 'Data_loss':''}

        elif "new" in line and set_next in line:
            split = line.split("->")
            left_ptr= split[0]
            max_node = max(Mamory.values())
            Environment[left_ptr] = max_node
            Mamory[max_node] = max_node+1

            row = {'Mamory':f'<{max_node},{Mamory[max_node]}>', 'Environment':'', 'Line':number_line, 'Data_loss':''}
        
        if row!={}:
            data = data.append (row, ignore_index=True)


    data.to_csv('output.csv', sep=';')





            
            



    

        






