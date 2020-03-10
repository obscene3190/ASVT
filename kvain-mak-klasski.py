from prettytable import PrettyTable
from sympy.logic import simplify_logic

# Структура для элемента уровня. Содержит строку-значение и атрибут "было ли сравнение"
class LvlSet:
    def __init__(self, line):
        self.line = line
        self.was_comp = 0
        
# сравнение строк и получение новой строки с ~
def Compare(line1, line2):
    line = str()
    dismatches = 0
    for letter1, letter2 in zip(str(line1), str(line2)):
        if (letter1 == letter2):
            line += letter1
        else:
            line += '~'
            dismatches+=1
    if (dismatches == 1):
        # для наглядности выводим, какие элементы были использованы и во что они превратились
        print(line1, line2, '->', line)
        return line
    return None

#сравнение на этапе формирования таблицы
def Compare2(line1, line2):
    for letter1, letter2 in zip(str(line1), str(line2)):
        if (not((letter1 == letter2) or (letter1 == '~'))):
            return None
    return 1
        
# функция обработки ввода и распределения слов по группам        
def Input():
    sets_list = [] # лист изначальных наборов для формирования таблицы
    sets = [] # лист объектов уровней
    file = open('ASVT1.txt', 'r')
    for line in file:
        line = line.replace('\n', '')
        sets_list.append(line)
        
        sets.append(LvlSet(line))
    return sets, sets_list

# функция выделения финальных импликант
def Prime_implicants(sets):
    # imps, изначально n значений
    was_compare = 1 # флаг, показывающий, было ли произведено хоть одно сравнение(и сформирван след. уровень)
    imps = sets
    fin_list = [] # лист финальных состояний
    while(was_compare == 1):
        # 1 этап: производим все возможные сравнения и формируем новый уровень
        was_compare = 0 # сбрасываем флаг 
        next_lvl = []
        for i in range(0, len(imps)-1):
            for j in range(i+1, len(imps)):
                line = Compare(imps[i].line, imps[j].line)
                if (line != None):
                    was_compare = 1
                    next_lvl.append(LvlSet(line))
                    imps[i].was_comp = 1
                    imps[j].was_comp = 1
        #final stations check
        # 2 этап: из особенности структуры выделяем финальные импликанты на уровне
        for i in imps:
            if(i.was_comp == 0): fin_list.append(i.line)
        #changing lists
        # на всякий удаляем одинаковые элементы
        imps = list(set(next_lvl))
        #print(fin_list)                   
    return fin_list

# делаем красивую таблицу с помощью PrettyTable.
def Create_table(sets, imps):
    sets = list(sets)
    sets.insert(0, 'imps')
    print('\n\n\n')
    print(sets, imps)
    th = sets
    td = dict()
    # формируем строки
    for imp in imps:
        td[imp] = [0]*(len(sets)-1)
        td[imp].insert(0, imp)
        for key, i in zip(sets, range(0, len(sets))):
            if (Compare2(imp, key) != None): td[imp][i] = 'V'
            else:
                if (i != 0): td[imp][i] = '_'
    table = PrettyTable(th)
    for key in td.keys():
        table.add_row(td[key])
    print(table)
    ff = open('text.txt', 'w')
    ff.write(str(table))# Печатаем таблицу
    return table

# функция для упрощения полученного списка первичных испликант
def Simplify(imps):
    p = ['a', 'b', 'c', 'd', 'e', 'f']
    dnf = ''
    for imp in imps:
        imp_s = ''
        for i in range(0, 6):
            if (imp[i] == '0'): imp_s +=' & ' + '~' + p[i]
            if (imp[i] == '1'): imp_s +=' & ' + p[i]
            if (imp[i] == '~'): imp_s += ''
        dnf +='(' + imp_s[3:] + ') | '
    dnf = dnf[0:-3]
    dnf = str(simplify_logic(dnf, 'dnf'))
    print(dnf)   

if __name__ == "__main__":
    group_lvl, sets = Input()
    imps = Prime_implicants(group_lvl)
    Create_table(sets,imps)
    Simplify(imps)
