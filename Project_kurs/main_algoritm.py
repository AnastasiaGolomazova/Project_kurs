from asyncio.windows_events import NULL
from msilib.schema import Environment
from black import validate_regex
import pandas

class Analysiator():

    global_data = {}

    # инициализация анализатора
    def __init__(self, json, list_object):
        self.json_file = json
        self.head = json["list_ptr_name"]
        self.get_next = json["get_next"]
        self.set_next = json["set_next"]
        self.list_object = list_object
        

    def set_data(self, name):
        self.name = name
        vector_path = self.json_file[name]
        self.vector_path = vector_path
        self.data = pandas.DataFrame({'Memory':[], 'Environment':[], 'Line':[], 'Current line':[], 'Message': []})
        method = None
        for object in self.list_object:
            try:
                method = self.find_object(object.child,vector_path[0])
            except:
                continue
        if method == None:
            raise Exception("method not found")
        self.lines = self.find_lines(vector_path, method)
        self.number = vector_path[0]
        self.line = self.lines[0]

        if self.checkNULL(self.lines) == False: # специальная проверка для методов, которые создают новый список узлов
        
            self.environment = {self.head:1}
            self.memory = {1:None}
            self.log('<1,None>', f'+<{self.environment[self.head]},{self.head}>')
        else:
            self.environment = {}
            self.memory = {}
        

    # вывод информации о нем
    def log(self, memory = "", environment= "", canDublicate = False):

        message = self.check_self_link()

        numbers = self.data['Line'].to_list()
        if (len(numbers) == 0):
            data = {'Memory':memory, 'Environment':environment, 'Line':self.number,'Current line':self.line, 'Message': message}
            self.data = self.data.append(data, ignore_index=True)
        elif (self.data['Line'].to_list()[-1]!=self.number or canDublicate):
            data = {'Memory':memory, 'Environment':environment, 'Line':self.number,'Current line':self.line, 'Message': message}
            self.data = self.data.append(data, ignore_index=True)

    def check_self_link(self):
        for key, value in self.memory.items():
                if key == value:
                    return "self link"
        return ""

    def contains(self, value = [], reverse = False):
        for element in value:
            if element not in self.line:
                return reverse
        return not reverse

    # vector_path- путь кода
    # list_object - список объектов
    # json_file - json файл
    # master_mind - основной алгоритм поиска утечки
    def analysis (self): 
        memory = self.memory
        environment = self.environment
        head = self.head
        vector_path = self.vector_path

        if memory == {}:
            new_num = 1
        else:
            new_num = 2

        for index in range(len(vector_path)-1):
            self.line = self.lines[index]
            self.number = vector_path[index+1]

            line = self.line

            if self.contains(['*', "="]): # ситуация, если мы объявляем указатель and ситуация, если мы объявляем указатель и присваиваем значение
                ptrs = self.get_ptrs(' ', 1, 3)

                if self.contains(["new"]):
                    environment[ptrs.left] = new_num
                    memory[new_num] = None
                    self.log(f'<{new_num},{memory[new_num]}>', f'+<{environment[ptrs.left]},{ptrs.left}>')
                    new_num+=1
                else:
                    environment[ptrs.left] = environment[ptrs.right[:-1]]
                    self.log(environment = f'+<{environment[ptrs.left]},{ptrs.left}>')

            elif self.contains(['delete']): # ситуация, если мы хотим удалить указатель
                right = self.get_ptrs(' ', None, 1).right[:-1]
                left_number = environment[right]

                self.log(environment = f'-<{environment[right]},{right}>')
                del memory[left_number]

                keys = list(environment.keys())
                for ptr in keys:
                    if environment[ptr] == left_number:
                        environment[ptr] = None
                del environment[right]
                

            elif self.contains(['new', head]): # ситуация, если мы хотим выделить новый узел для головного узла
                #if self.checkNULL(self.lines) == False: # специальная проверка для методов, которые создают новый список узлов
                environment[head] = new_num
                memory[new_num] = None
                self.log(f'<{new_num},{memory[new_num]}>', f'+<{environment[head]},{head}>')
                new_num+=1

            elif self.contains(['new', self.set_next]): # ситуация, если мы хотим выделить новый узел и добавить его в список
                left = self.get_ptrs('->', 0, None).left
                #max_node = max(Memory.values()) ПОДУМАТЬ
                #if Environment[left_ptr] == None:
                old_ptr = environment[left]
                environment[left] = new_num
                memory[old_ptr] = new_num
                memory[new_num] = None

                self.log(memory = f'<{new_num},{memory[new_num]}>')         

                self.log(memory = f'<{old_ptr},{new_num}>', canDublicate= True)    

                new_num +=1
            ######         
            elif self.contains(['new']): # ситуация, если мы хотим выделить новый узел для головного узла
                left = self.get_ptrs(' ', 0, None).left
                environment[left] = new_num
                memory[new_num] = None

                ## откуда old?
                self.log(f'<{new_num},{memory[new_num]}>', f'+<{environment[left]},{left}>')
                new_num += 1
                    
            elif self.contains([self.get_next]) and self.contains([self.set_next], True): # ситуация, если мы приравниваем указатель к getNext другого указателя
                ptrs = self.get_ptrs(' ', 0, None)
                #index = split[2].index('-')           
                #right = split[2][:index]
                left= ptrs.left
                n = environment[left]
                if n is not None:
                    if memory[n] == None:
                        environment[left] = new_num
                        memory[n] = new_num
                        memory[new_num] = None
                        self.log(f'<{n},{memory[n]}>', f'+<{environment[left]},{left}>', canDublicate=True)
                        self.log(f'<{new_num},{memory[new_num]}>', f'+<{environment[left]},{left}>', canDublicate=True)
                        new_num += 1
                    else:
                        environment[left] = memory[n]
                        n = environment[left]
                        self.log(f'<{n},{memory[n]}>', f'+<{environment[left]},{left}>', canDublicate=True)
                else:
                    environment[left] = new_num
                    memory[n] = new_num
                    memory[new_num] = None
                    self.log(f'<{n},{memory[n]}>', f'+<{environment[left]},{left}>', canDublicate=True)
                    self.log(f'<{new_num},{memory[new_num]}>', f'+<{environment[left]},{left}>', canDublicate=True)
                    new_num += 1

            elif self.contains(['=']) and self.contains(["=="], True): # ситуация, если мы хотим присвоить значение указателя к другому
                ptrs = self.get_ptrs(' ', 0, 2)
                environment[ptrs.left] = environment[ptrs.right[:-1]]

                self.log(environment = f'+<{environment[ptrs.left]},{ptrs.left}>')

            elif self.contains([self.get_next, self.set_next]): # ситуация, когда есть get_next и set_next 
                ptrs = self.get_ptrs("->", 0, 1)
                index = ptrs.right.index('(')
                left_number = environment[ptrs.left]
                right_number = environment[ptrs.right[index + 1:]]
                memory[left_number] = memory[right_number]

                self.log(memory = f'<{left_number},{memory[left_number]}>')

            elif self.contains([self.set_next]): # ситуация, если мы хотим выделить новый узел и добавить его в список
                ptrs = self.get_ptrs("->", 0, 1)
                index = ptrs.right.index('(')
                left_number = environment[ptrs.left]
                right_number = environment[ptrs.right[index+1:-2]]
                memory[left_number] = right_number

                self.log(memory = f'<{left_number},{memory[left_number]}>')

            self.log()

        
        results = self.find_leaks(vector_path[0]) # поиск утечки
        self.data = self.data.append({'Memory':''}, ignore_index=True)
        
        for result in results:
            row = {'Memory':result}
            self.data = self.data.append(row, ignore_index=True)

        self.global_data[self.name] = self.data

    # Memory - модель представления связей между узлами
    # data - табличное представление данных, отслеживающее все изменения в Memory и Environment
    # find_leaks - поиск утечки памяти
    def find_leaks (self, vector_start):
        memory = self.memory
        environment = self.environment
        data = self.data
        head = self.head
        
        tree_list = []
        results = []
        
        if head not in environment:
            return ["head don't exist"]
            
        head_num = environment[head]
        current = environment[head]
        step = 0
        while current in memory:
            tree_list.append(current)
            if current not in memory:
                break
            if memory[current] in memory:
                if memory[memory[current]] == current:
                    break
            current = memory[current]
            step += 1
            if step > 1000:
                break

        Environment_leaks = data["Environment"].to_list()
        imposters = []
        for node in memory.keys():
            if node not in tree_list and node != head_num:
                imposters.append(node)
        list_memory = data["Memory"].to_list()
        for imposter in imposters:
            exists = False
            count = 0
            for link in list_memory:
                if link != "":
                    two_elements = link.split(',')
                    #if two_elements[1][:-1] != 'None':
                    left_number = two_elements[0][1:]
                    rigth_number = two_elements[1][:-1]
                    #or left_number == str(imposter)
                    if rigth_number == str(imposter) or (left_number == str(imposter) and rigth_number == "None" and count != 0):
                        #if two_elements[1][:-1] != 'None':
                        #parent_node = two_elements[0][1:]
                        
                        for link in list_memory[count:]: 
                            if link != "":
                                two_elements = link.split(',')
                                #if two_elements[1][:-1] != 'None':
                                rigth = two_elements[1][:-1]
                                left = two_elements[0][1:]
                                if left==left_number and rigth!= str(imposter):
                                    line_number = list(data[data["Memory"] == link]["Line"].to_list())[0]
                                    result = f"leak in string {line_number}"
                                    results.append(result)
                                    exists = True
                                    break
                if exists:
                    break

                count +=1     

        if environment[head] != 1 and 1 in imposters:
            for item in Environment_leaks:
                if head in item:
                    line_number = list(data[data["Environment"] == item]["Line"].to_list())
                    two_elements = item.split(',')
                    left_number = int(two_elements[0][2:])
                    if len(line_number) != 0 and left_number != 1:
                        result = f"leak in string {line_number[0]}"
                        results.append(result)

        if len(results) == 0:
            return ["leaks don't exists"]

        return self.remove_dublicate(results, vector_start)

        

    def checkNULL (self, lines):
        for line in lines:
            if "head == nullptr" in line or "head == NULL" in line:
                return True
       
        return False

    def get_ptrs(self, char, left_index, right_index):
        return pointers(char, self.line, left_index, right_index)

    # list_objects- список объектов среди которых ищем нужный блок кода
    # line_number - номер искомой строки 
    # find_object - нахождение по номеру строки соответствующую строку из кода
    def find_object (self, list_objects, line_number):
        for object in list_objects:
            if line_number >= object.line_number and line_number <= object.line_number+object.length:
                return object
        raise Exception("object not found")

    # vector_path- путь по которому выполняется алгоритм
    # cpp_object - метод, который рассматриваем 
    # find_lines - выборка из метода используемые строки
    def find_lines (self, vector_path, cpp_object):
        lines_list = cpp_object.text.split('\n')
        result  = []
        for number in vector_path[1:]:
            index = number - cpp_object.line_number
            clean_lines = lines_list[index].replace("\t", "")
            result.append(clean_lines)
        return result


    def remove_dublicate(self, input, num):
        result = []
        for item in input:
            if item not in result: #and str(num) not in item:
                result.append(item)
        return result
            
class pointers():
    def __init__(self, char, line, left_index = None, right_index = None):
        split = line.split(char)

        if left_index != None:
            self.left = split[left_index]

        if right_index != None:
            self.right = split[right_index]




    

        






