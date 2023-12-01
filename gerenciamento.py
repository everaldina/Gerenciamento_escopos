import re

def gerenciamento(nome_arq):
    pilha = [[]]
    count_linhas = 1
    instrucoes = lista_comandos(nome_arq)
    for linha in instrucoes:
        #print(f"linha {count_linhas}: {linha}")
        partes = linha.split()

        if len(partes) == 0:
            count_linhas += 1
        else:
            match partes[0]:
                case "BLOCO":
                    bloco = partes[1]
                    pilha.append([])
                    #print(f"(linha {count_linhas}) entrando no bloco: {bloco}")
                case "NUMERO":
                    var = "".join(partes[1:])
                    lexemas, valores = declaracao(var)
                    tabela = []
                    for lexema, valor in zip(lexemas, valores):
                        try:
                            if(tipo(valor) == "NUMERO" or valor == None):
                                tabela.append({"lexema": lexema, "valor": valor, "tipo": "NUMERO", "bloco": bloco})
                                #print(f"Adcionando {lexema} = {valor}")
                        except Exception as ex:
                            print(f"Erro (linha {count_linhas}): valor não numérico")
                            break
                    if escopo_criacao(tabela, pilha):
                        pilha[len(pilha)-1].extend(tabela)
                        #print(f"Apendando no : {bloco}")
                    else:
                        print(f"Erro (linha {count_linhas}): variável já declarada")
                case "CADEIA":
                    var = "".join(partes[1:])
                    lexemas, valores = declaracao(var)
                    tabela = []
                    for lexema, valor in zip(lexemas, valores):
                        if(tipo(valor) == "CADEIA" or valor == None):
                            tabela.append({"lexema": lexema, "valor": valor, "tipo": "CADEIA", "bloco": bloco})
                            #print(f"Adcionando {lexema} = {valor}")
                        else:
                            print(f"Erro (linha {count_linhas}): valor não é cadeia")
                        break
                    if escopo_criacao(tabela, pilha):
                        pilha[len(pilha)-1].extend(tabela)
                        #print(f"Apendando no : {bloco}")
                    else:
                        print(f"Erro (linha {count_linhas}): variável já declarada")
                case "PRINT":
                    var = partes[1]
                    try:
                        valor = busca_variavel(var, pilha, count_linhas)
                        print(f"PRINT (linha {count_linhas}): {valor}")
                    except Exception as ex:
                        print(str(ex))
                case "FIM":
                    #print(f"(linha {count_linhas}) saindo do bloco: {bloco}")
                    pilha.pop()
                case _:
                    try:
                        var, valor = linha.split("=")
                        atribuicao(var, valor, pilha, count_linhas)
                    except Exception as ex:
                        print(str(ex))
            count_linhas += 1      
    
    
def lista_comandos(nome_arq):
    arquivo = open(nome_arq, 'r') 
    lista = []
    for linha in arquivo:
        lista.append(linha.strip())
    arquivo.close()
    return lista

# AT ->  ID = VALOR | ID
def declaracao(var):
    lexemas = []
    valores = []
    atribuicoes = re.findall("[a-zA-Z][0-9a-zA-Z_]*=[^,]+|[a-zA-Z][0-9a-zA-Z_]*[^,]?", var)
    
    for i in atribuicoes: 
        separado = i.split("=")
        if len(separado) == 2: # AT ->  ID = VALOR
            lexemas.append(separado[0])
            valores.append(separado[1])
        else: # AT ->  ID
            lexemas.append(separado[0])
            valores.append(None)
    return lexemas, valores

# verificar se no escopo atual já existe a variável
def escopo_criacao(tabela, pilha):
    for i in pilha[len(pilha)-1]:
        for j in tabela:
            if i["lexema"] == j["lexema"]:
                return False
    return True

def busca_variavel(variavel, pilha, linha):
    for i in pilha[len(pilha)-1:0:-1]: # percorre a pilha do topo pra baixo
        for tabela in i:
            if tabela["lexema"] == variavel:
                return tabela["valor"]
    raise Exception(f"Erro (linha {linha}): variável '{variavel}' não declarada")

def atribuicao(variavel, valor, pilha, linha):
    for i in pilha[len(pilha)-1:0:-1]: # percorre a pilha do topo pra baixo
        for tabela in i:
            if tabela["lexema"] == variavel:
                if tabela["tipo"] == tipo(valor):
                    tabela["valor"] = valor
                else:
                    raise Exception(f"Erro (linha {linha}): valor não é do tipo '{tabela['tipo']}'")
                return
    raise Exception(f"Erro (linha {linha}): variável '{variavel}' não declarada")

def tipo(valor):
    if valor == None:
        return None
    if valor[0] == '"' and valor[len(valor)-1] == '"':
        return "CADEIA"
    try:
        float(valor)
        return "NUMERO"
    except ValueError:
        raise Exception()

def print_tabela(tabela):
    print(f"{tabela['tipo']} {tabela['lexema']} = {tabela['valor']} | {tabela['bloco']}")

def print_pilha(pilha):
    print("PILHA:---------------")
    for i in pilha:
        for j in i:
            print_tabela(j)
    print("FIM PILHA-----------")
gerenciamento("teste.txt")