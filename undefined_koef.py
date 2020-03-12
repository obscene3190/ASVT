import itertools

null_koef = []
one_sets = {'001001', '111001', '011001', '110001', '011101', '110101', '000101', '001111', '101111', '110111', '000111', '001011', '101011', '110011', '100011', '000011', '101010', '111010', '011010', '110010', '100010', '000010', '101110', '011110', '110110', '010100', '000100', '001000', '101000', '011000', '100000', '000000'}; n = '1234566'

def Bin(n, m):
    n = str(bin(n))[2:]
    return '0'*(m-len(n))+n
  
# Функция формирования строки коэффициентов вида ('n1n2', 'line[n1]line[n2]')
def line_forming(line_):
    line = list(line_)
    combs = []
    for i in range(1, 7):
        for j in list(itertools.combinations(n, i)):
            j = ''.join(j)
            combs.append([j])
    for i in combs:
        set_ = '' # сочетание переменных, соотвествующее номерам из набора
        for j in i[0]:
            set_+=str(line[int(j)-1])
        i.append(set_)
    return combs

# Формирование списка нулевых коэффициентов
def null_koef_processing():
    for i in range(0, 64):
        i = Bin(i, 6)
        if (i not in one_sets):
            set_ = line_forming(i)
            for j in set_:
                null_koef.append(j)
                
# Функция для подсчета числа вхождений элемента в систему
def count_in(el, sys):
    count = 0
    for line in sys:
        if (el in line): count+=1
    return count

# Функция формирования системы, учитывающая нулевые коэффициенты
def system_forming():
    system = []
    for i in one_sets:
        line = line_forming(i)
        con = True
        while(con):
            con = False
            for j in line:
                if (j in null_koef):
                    con = True
                    line.remove(j)
        system.append(line)
    return system

# Работа с системой по алгоритму минимизации с помощью 
def processing_sys(system):
    final_koef = []
    while(len(system) > 0):
        # сортировка
        system = sorted(system, key = lambda x: len(x))
        # находим длину минимального набора и ищем все мономы минимальной длины
        line = system[0]
        min_len = 6
        min_monoms = []
        for line in system:
            for element in line:
                if (len(element[0]) < min_len): min_len = len(element[0])
        for line in system:
            for element in line:
                if (len(element[0]) == min_len): min_monoms.append(element)
        # Находим моном, который встречается больше всех
        monom = max(min_monoms, key = lambda x: count_in(x, system))
        final_koef.append(monom)
        # Записав его в наше покрытие, удаляем все строки, в которых он есть
        con = True
        while(con):
            con = False
            for line in system:
                if (monom in line): 
                    con = True
                    system.remove(line) 
    return final_koef

if __name__ == "__main__":
    null_koef_processing()
    system = system_forming()
    #print(system)
    answer = processing_sys(system)
    answer = {tuple(x) for x in answer}
    print(answer)
    print(len(answer))
