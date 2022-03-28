
class cpp_struct(object):
    child = []
    def __init__(self, line_number, text, _type):
       self.line_number = line_number
       self.text = text
       self.type = _type
       self.length = 0
       self.parse()

    def parse (self): 
        class_line_index = self.text.index('\n') # Возвращаем интекс конца первой строки
        first_line = self.text[:class_line_index] # Присваиваем первую строку (вырезаем до конца индекса первой строки)
        
        if "(" in first_line:
            index = self.text.index('(') # возращаем индекс '('
            first_line = first_line[:index] # берём строку до открывающей скобки
        elif " (" in first_line:
            index = self.text.index(' (') # возращаем индекс '('
            first_line = first_line[:index]

        if " " in first_line: 
            if " (" in first_line:
                self.name = first_line
            else:
                self.name = first_line.split(" ")[1] # если пробел существует, то берём второй слово и сохраняем как имя
        else:
            self.name = first_line # иначе присваиваем все одно слово целиком 
        

        if self.type == 'class':
            public_index = self.text.index('public') # возращаем индекс 'p'
            i = self.line_number + self.text[:public_index].count('\n')+1 # Присваиваем текущий индекс
           # + индекс следующей строки после 'public' вырезанного текст
            self.text = self.text[public_index+7:] # присваиваем текст от 'public' и до конца
            
            while '\t' in self.text: # пока есть табуляция в тексте
                index = self.text.index('\t') # присваиваем индекс конца текущей строки
                next = self.text[index+1] # присваиваем переменной следующую строку без табуляции (перенос на следующую строку)
                if next !=' ' and next !='\n': # если в строка не пустая и нет переноса на следующую строку
                    end_index = self.text.index('\n\t}') # последний получаем индекс конца текста до закрывающей '}'
                    line = self.text[index+1:end_index+3] #
                    struct = cpp_struct(i, line, "method")
                    self.child.append(struct)
                    i += line.count('\n')+1
                    self.text = self.text[end_index+3:]
                else:
                    i +=1
                    self.text = self.text[index+2:]
                
        self.length = self.text.count('\n')
        print(self.line_number, self.length)
        
    def __str__(self):
        return self.name