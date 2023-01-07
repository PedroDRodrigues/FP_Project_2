# Pedro Rodrigues 99300
"""
Esta funcao devolve uma palavra apos as reducoes e correcoes
"""
def corrigir_palavra(str1):
    first_pointer = 0
    second_pointer = 1
    
    while second_pointer != len(str1) and len(str1) > 0:
        if (abs(ord(str1[first_pointer]) - ord(str1[second_pointer])) == 32):
            str1 = str1[:first_pointer] + str1[second_pointer + 1:]
            first_pointer = 0
            second_pointer = 1            
        else:
            first_pointer += 1
            second_pointer += 1
            
    return str1       
"""
Esta funcao verifica se as palavras recebidas sao anagramas
"""
def eh_anagrama(str1, str2):
    if not (isinstance(str1, str) or isinstance(str2, str)):
        return False
    if (len(str1) != len(str2)):
        return False
  
    word1 = str1
    word2 = str2
    word1 = word1.lower()
    word2 = word2.lower()
    word2list = list(word2)
    pos1 = 0
    pos2 = 0
    check = True
    found = False

    if word1 == word2:
        return False
    
    for i in range(len(str1)):
        if ord(str1[i]) < 65 or ord(str1[i]) > 122 or (ord(str1[i]) > 90 and ord(str1[i]) < 97):
            return False
        
    for i in range(len(str2)):
        if ord(str1[i]) < 65 or ord(str1[i]) > 122 or (ord(str1[i]) > 90 and ord(str1[i]) < 97):
            return False    
       
    while pos1 < len(word1) and check == True:
        while pos2 < len(word2list) and not found:
            if word1[pos1] == word2list[pos2]:
                found = True
            else:
                pos2 += 1
        if found == True:
            word2list[pos2] = None
        else:
            check = False
        
        pos1 += 1

    return check
"""
Esta funcao devolve um doc ja com as palavras reduzidas e sem anagramas
"""
def corrigir_doc(doc1):
    fim = len(doc1)
    
    if len(doc1) < 1:
        raise ValueError('corrigir_doc: argumento invalido') 
    if ord(doc1[0]) == 32 or ord(doc1[fim - 1]) == 32:
        raise ValueError('corrigir_doc: argumento invalido') 

    for i in range(len(doc1)):
        if ord(doc1[i]) > 90 and ord(doc1[i]) < 97:
            raise ValueError('corrigir_doc: argumento invalido')   
        if ord(doc1[i]) < 65 or ord(doc1[i]) > 122:        
            if ord(doc1[i]) != 32:
                raise ValueError('corrigir_doc: argumento invalido')  
        if ord(doc1[i]) == 32 and i != fim - 1:
            if ord(doc1[i + 1]) == 32:
                raise ValueError('corrigir_doc: argumento invalido')
    
    doc1 = doc1.split()
    aux = ''
    
    for i in range(len(doc1)):
        palavra = corrigir_palavra(doc1[i])
        if not palavra == '' and i < (len(doc1) - 1):
            aux += palavra + ' '
        if i == (len(doc1) - 1) and palavra != '':
            aux += palavra
    
    aux = aux.split()
    i = 0 
    contador = len(aux)
    
    while i < contador:
        for j in range(len(aux)):
            if eh_anagrama(aux[i], aux[j]) == True:
                del aux[j]
                break
        i += 1
        contador = len(aux)
    
    aux = ' '.join(map(str, aux))
    
    return aux            
"""
Esta funcao recebe um movimento e uma posicao inicial 
e devolve um inteiro que corresponde a nova posicao
'B' - Move para BAIXO
'C' - Move para CIMA
'D' - Move para DIREITA
'E' - Move para ESQUERDA

1 | 2 | 3
-   -   -
4 | 5 | 6
-   -   -
7 | 8 | 9

"""
def obter_posicao(str1, pos1):
    if str1[0] == 'B':
        if pos1 < 7:
            pos1 += 3
    if str1[0] == 'C':
        if pos1 > 3:
            pos1 -=3
    if str1[0] == 'D':
        if pos1 != 3 and pos1 != 6 and pos1 != 9:
            pos1 += 1
    if str1[0] == 'E':
        if pos1 != 1 and pos1 != 4 and pos1 != 7:
            pos1 -= 1            
    return pos1
"""
Esta funcao devolve o inteiro a registar depois de realizar todos os movimentos
"""
def obter_digito(str1, dig1):
    for i in range(len(str1)):
        if str1[i] == 'B':
            if dig1 < 7:
                dig1 += 3
        if str1[i] == 'C':
            if dig1 > 3:
                dig1 -=3
        if str1[i] == 'D':
            if dig1 != 3 and dig1 != 6 and dig1 != 9:
                dig1 += 1
        if str1[i] == 'E':
            if dig1 != 1 and dig1 != 4 and dig1 != 7:
                dig1 -= 1  
    return dig1    
"""
Esta funcao recebe um tuplo com 4 a 10 sequencias de movimentos e devolve um 
tuplo que contem o pin codificado
"""
def obter_pin(tuple1):
    if not (isinstance(tuple1, tuple)): 
        raise ValueError('obter_pin: argumento invalido')
    if len(tuple1) < 4 or len(tuple1) > 10:
        raise ValueError('obter_pin: argumento invalido')
    
    for i in range(len(tuple1)):
        for j in range(len(tuple1[i])):
            if tuple1[i][j] != 'C' and tuple1[i][j] != 'B' and tuple1[i][j] != 'D' and tuple1[i][j] != 'E':
                raise ValueError('obter_pin: argumento invalido')
                
    else: 
        i = 1
        j = 0
        pin = ()
        
        contador = obter_digito(tuple1[j], 5)
        pin = pin + (contador,)

        while i < len(tuple1):
            numero = obter_digito(tuple1[i], pin[j])
            pin = pin + (numero,)
            i += 1
            j += 1
            
        return pin
"""
Esta funcao verifica se a entrada obtida e uma BDB 
Contem entao
-> cadeia de caracteres cifra contendo uma ou mais palavras separadas por 
tracos (todas as letras sao minusculas)
-> cadeia de caracteres checksum contendo uma sequencia de controlo com 5
caracteres mais dois dos []
-> tuplo com dois ou mais numeros inteiros positivos 
"""
def eh_entrada(entry):
    if not isinstance(entry, tuple):
        return False
        
    if not isinstance(entry[0], str):
        return False
    
    else:
        for i in range(len(entry[0])):
            if ord(entry[0][i]) == 45:
                continue 
            if (ord(entry[0][i]) >= 97 and ord(entry[0][i]) <= 122): 
                continue
            else:
                return False
        
    if not isinstance(entry[1], str):
        return False
    
    if len(entry[1]) != 7:
        return False        
    
    if not (ord(entry[1][0]) == 91 or ord(entry[0][6]) == 93):
            return False
        
    if not isinstance(entry[2], tuple):
        return False
    
    if len(entry[2]) < 2:
        return False
    
    return True
"""
Esta funcao verifica se a sequencia de controlo e coerente com a cifra
"""
def validar_cifra(str1, str2):
    count = {}

    for s in str1:
        if s in count and s != '-':
            count[s] += 1
        if not s in count and s != '-':
            count[s] = 1

    count = dict(sorted(count.items(), key=lambda item: item[0]))     
    count = sorted(count, key = count.get, reverse=True)

    for i in range(1,6):
        if count[i-1] != str2[i]:
            return False
    
    return True
"""
Esta funcao recebe varios BDB e devolve todos os que nao estao corretos
(cifra e sequencia de controlo nao coerentes)
"""
def filtrar_bdb(list1):
    aux = list1
    i = 0
    if len(list1) == 0:
        raise ValueError('filtrar_bdb: argumento invalido')
    else:
        while i < len(aux):
            if eh_entrada(aux[i]) == True:
                if validar_cifra(aux[i][0], aux[i][1]) == True: 
                    list1.remove(aux[i])
                    i = 0 
                else: 
                    i += 1
    return list1
"""
Esta funcao recebe um tuplo de inteiros positivos e devolve a menor diferenca 
positiva entre qualquer par
"""
def obter_num_seguranca(tuple1):
    if len(tuple1) == 2:
        result = abs(tuple1[0] - tuple1[1])
    else:
        result = abs(tuple1[0] - tuple1[1])
        for i in range(len(tuple1)):
            for j in range(len(tuple1) - 1):
                if abs(tuple1[i] - tuple1[j]) < result: 
                    if abs(tuple1[i] - tuple1[j]) != 0:
                        result = abs(tuple1[i] - tuple1[j])
    return result
"""
Esta funcao recebe uma cifra e um num de seguranca e devolve o texto decifrado
"""
def decifrar_texto(str1, int1):
    i = 0
    aux = list(str1)
    
    while int1 - 26 > 0:
        int1 -= 26
    int_par = int1 + 1
    int_impar = int1 - 1
    
    while i < len(str1):
        if aux[i] == '-':
            aux[i] = " "
        if aux[i] and i % 2 == 0 and aux[i] != " ":
            if (ord(aux[i]) + int_par) > 122:
                aux[i] = chr(ord(aux[i]) + int_par - 26)
            else:
                aux[i] = chr(ord(aux[i]) + int_par)
        if aux[i] and i % 2 != 0 and aux[i] != " ":
            if (ord(aux[i]) + int_par) > 122:
                aux[i] = chr(ord(aux[i]) + int_impar - 26)
            else:
                aux[i] = chr(ord(aux[i]) + int_impar)            
        i += 1 
    
    str1 = "".join(aux)
    
    return str1
"""
Esta funcao recebe uma lista contendo uma ou mais BDB e devolve a lista de mesmo
tamanho descodificada ou entao devolve um erro
"""
def decifrar_bdb(list1):
    for i in range(len(list1)):
        if eh_entrada(list1[i]) == False:
            raise ValueError('decifrar_bdb: argumento invalido')
    
    for i in range(len(list1)):
        list1[i] = decifrar_texto(list1[i][0], obter_num_seguranca(list1[i][2]))
    
    return list1
"""
Esta funcao recebe um argumento de qualquer tipo e devolve True se corresponder
a um dicionario com a informacao de utilizador (nome, senha e regra individual)
"""
def eh_utilizador(entry):
    if not isinstance(entry, dict):
        return False
    else:
        if len(entry['name']) < 1:
            return False
        if len(entry['pass']) < 1:
            return False
        if not isinstance(entry['rule'], dict):
            return False        
        if len(entry['rule']['char']) != 1:
            return False
        if ord(entry['rule']['char']) < 97 or ord(entry['rule']['char']) > 122:
            return False
        if not isinstance(entry['rule']['vals'], tuple):
            return False
        if entry['rule']['vals'][0] <= 0:
            return False
        if entry['rule']['vals'][1] <= 0:
            return False        
        if entry['rule']['vals'][0] >= entry['rule']['vals'][1]:
            return False
    
    return True
"""
Esta funcao recebe uma senha e um dicionario contendo a regra individual e 
devolve True se a senha cumpre todas as regras
As senhas tambem tem pelo menos tres vogais minusculas e tem pelo menos um dos
caracteres que aparece duas vezes consecutivas
"""
def eh_senha_valida(str1, dict1):
    check = 0
    contador = 0
    minusculas = 0
    
    if len(str1) < 3:
        return False
    
    for i in range(len(str1) - 1):
        if str1[i] == str1[i+1]:
            check = 1
    
    if check == 0:
        return False
    
    for i in range(len(str1)):
        if str1[i] == dict1['char']:
            contador += 1
            if contador < dict1['vals'][0] or contador > dict1['vals'][1]:
                return False
            
    for i in range(len(str1)):
        if str1[i] == 'a' or str1[i] == 'b' or str1[i] == 'c' or str1[i] == 'd' or str1[i] == 'e':
            minusculas += 1
    
    if minusculas < 3:
        return False
    
    return True
"""
Esta funcao recebe uma lista com um ou mais dicionarios correspondente a entrada 
BDB e devolve a lista ordenada alfabeticamente com os nomes de utilizadores com
senhas erradas
"""
def filtrar_senhas(list1):
    aux = []
    if len(list1) == 0:
        raise ValueError('filtrar_senhas: argumento invalido')    
    else:
        for i in range(len(list1)):
            if not eh_utilizador(list1[i]):
                raise ValueError('filtrar_senhas: argumento invalido')
            else:
                if not eh_senha_valida(list1[i]['pass'], list1[i]['rule']):
                    aux.append(list1[i]['name'])
                    
        aux.sort() 
    
    return aux    