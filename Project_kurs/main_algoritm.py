from asyncio.windows_events import NULL
import pandas

# list_objects- список объектов среди которых ищем нужный блок кода
# line_number - номер искомой строки 
# find_object - нахождение по номеру строки соответствующую строку из кода
def find_object (list_objects, line_number):
    for object in list_objects:
        if line_number >= object.line_number and line_number <= object.line_number+object.length:
            return object
    raise Exception("object not found")

# vector_path- путь по которому выполняется алгоритм
# cpp_object - метод, который рассматриваем 
# find_lines - выборка из метода используемые строки
def find_lines (vector_path, cpp_object):
    lines_list = cpp_object.text.split('\n')
    result  = []
    for number in vector_path[1:]:
        index = number - cpp_object.line_number
        clean_lines = lines_list[index].replace("\t", "")
        result.append(clean_lines)
    return result

# Memory - модель представления связей между узлами
# data - табличное представление данных, отслеживающее все изменения в Memory и Environment
# find_leaks - поиск утечки памяти
def find_leaks (Memory, data, Environment, head):
    tree_list = []
    results = []
    current = Environment[head]
    while current in Memory:
        tree_list.append(current)
        if current not in Memory:
            break
        current = Memory[current]
    Environment_leaks = data["Environment"].to_list()
    if len(tree_list) == len(Memory) and len(results) ==0:
        return ["leaks don't exists"]
    else:
        imposters = []
        for node in Memory.keys():
            if node not in tree_list:
                imposters.append(node)
        list_memory = data["Memory"].to_list()
        for imposter in imposters:
            for link in list_memory:
                if link != "":
                    two_elements = link.split(',')
                    rigth_number = int(two_elements[1][:-1])
                    if rigth_number == imposter:
                        parent_node = int(two_elements[0][1:])
                        for link in list_memory: 
                           if link != "":
                              two_elements = link.split(',')
                              rigth = int(two_elements[1][:-1])
                              left = int(two_elements[0][1:])
                              if left==parent_node and rigth!= imposter:
                                 line_number = list(data[data["Memory"] == link]["Line"].to_list())[0]
                                 result = f"leak in string {line_number}"
                                 results.append(result)
                                 break
    if Environment[head] != 1 :
        for item in Environment_leaks:
            if head in item:
                line_number = list(data[data["Environment"] == item]["Line"].to_list())
                two_elements = item.split(',')
                left_number = int(two_elements[0][2:])
                if len(line_number) != 0 and left_number != 1:
                    result = f"leak in string {line_number}"
                    results.append(result)
    return results


# vector_path- путь кода
# list_object - список объектов
# json_file - json файл
# master_mind - основной алгоритм поиска утечки
def master_mind (vector_path, list_object, json_file): 
    method = None
    for object in list_object:
        try:
            method = find_object(object.child,vector_path[0])
        except:
            continue
    if method == None:
        raise Exception("method not found")

    lines = find_lines(vector_path, method)
    Memory = {1:2}

    head = json_file["list_ptr_name"]

    Environment = {head:1}

    get_next = json_file["get_next"]
    set_next = json_file["set_next"]

    data = pandas.DataFrame({'Memory':{}, 'Environment':{}, 'Line':{}})
    data = data.append({'Memory':'<1,2>', 'Environment':f'+<{Environment[head]},{head}>', 'Line':vector_path[0]}, ignore_index=True)
     
    for index in range(len(vector_path)-1):
        line = lines[index]
        number_line = vector_path[index+1]
        split = line.split(' ')
        row = {}
        if '*' in line: # ситуация, если мы объявляем указатель
            if "=" in line: # ситуация, если мы объявляем указатель и присваиваем значение
                left_ptr = split[1] 
                if "new" in line:
                    max_node = max(Memory.values())
                    Environment[left_ptr] = max_node
                    Memory[max_node] = max_node+1
                    row = {'Memory':f'<{max_node},{Memory[max_node]}>', 'Environment':'', 'Line':number_line}
                else:
                    rigth_ptr = split[3][:-1]
                    Environment[left_ptr]=Environment[rigth_ptr]
                    row = {'Memory':'', 'Environment':f'+<{Environment[left_ptr]},{left_ptr}>', 'Line':number_line}
        elif 'delete' in line: # ситуация, если мы хотим удалить указатель
            delete_node = split[1] 
            rigth_ptr = delete_node[:-1]
            number_node = Environment[rigth_ptr]
            row = {'Memory':'', 'Environment':f'-<{Environment[rigth_ptr]},{rigth_ptr}>', 'Line':number_line}
            del Memory[number_node]
            del Environment[rigth_ptr]

        elif "new" in line and head in line: # ситуация, если мы хотим выделить новый узел для головного узла
            Environment[head] = -1
            Memory[-1] = -2
            row = {'Memory':'<-1,-2>', 'Environment':f'+<{Environment[head]},{head}>', 'Line':number_line}

        elif get_next in line and set_next not in line: # ситуация, если мы приравниваем указатель к getNext другого указателя
            index = split[2].index('-')           
            rigth_ptr = split[2][:index]
            left_ptr= split[0]
            Environment[left_ptr] = Environment[rigth_ptr]+1
            left_node = Environment[left_ptr]
            Memory[left_node] = left_node + 1

            row = {'Memory':f'<{left_node},{Memory[left_node]}>', 'Environment':f'+<{Environment[left_ptr]},{left_ptr}>', 'Line':number_line}

        elif '=' in line: # ситуация, если мы хотим присвоить значение указателя к другому
            left_ptr= split[0]
            rigth_ptr = split[2][:-1]
            Environment[left_ptr] = Environment[rigth_ptr]
            row = {'Memory':'', 'Environment':f'+<{Environment[left_ptr]},{left_ptr}>', 'Line':number_line}

        elif get_next in line and set_next in line: # ситуация, когда есть get_next и set_next 
            split = line.split("->")
            left_ptr = split[0]
            index = split[1].index('(')
            rigth_ptr = split[1][index+1:]
            number_node = Environment[left_ptr]
            right_number = Environment[rigth_ptr]
            Memory[number_node] = Memory[right_number]

            row = {'Memory':f'<{number_node},{Memory[number_node]}>', 'Environment':'', 'Line':number_line}

        elif "new" in line and set_next in line: # ситуация, если мы хотим выделить новый узел и добавить его в список
            split = line.split("->")
            left_ptr= split[0]
            max_node = max(Memory.values())
            Environment[left_ptr] = max_node
            Memory[max_node] = max_node+1

            row = {'Memory':f'<{max_node},{Memory[max_node]}>', 'Environment':'', 'Line':number_line}
        
        if row!={}:
            data = data.append(row, ignore_index=True)
    
    results = find_leaks(Memory, data, Environment, head) # поиск утечки
    data = data.append({'Memory':''}, ignore_index=True)
    
    for result in results:
        row = {'Memory':result}
        data = data.append(row, ignore_index=True)

    data.to_csv('output.csv', sep=';')





            
            



    

        






