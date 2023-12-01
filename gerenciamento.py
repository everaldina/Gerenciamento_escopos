import re

def gerenciamento(nome_arq):
    pilha = []
    count_linhas = 0
    reservadas = ["BLOCO", "NUMERO", "CADEIA", "PRINT", "FIM"]
    instrucoes = lista_comandos(nome_arq)
    for linha in instrucoes:
        partes = linha.split()

        match partes[0]:
            case "BLOCO":
                bloco = partes[1]
            case "NUMERO":
                var = "".join(partes[1:])
                lexemas, valores = declaracao(var)
                tabela = []
                for lexema, valor in zip(lexemas, valores):
                    if(tipo(valor) != "NUMERO"):
                        print(f"Erro (linha {count_linhas}): valor não numérico")
                        break
                    else:
                        tabela.append({"lexema": lexema, "valor": valor, "tipo": "NUMERO", "bloco": bloco})
                if escopo_criacao(tabela, pilha):
                    pilha.append(tabela)
                else:
                    print(f"Erro (linha {count_linhas}): variável já declarada")
            case "CADEIA":
                var = "".join(partes[1:])
                lexemas, valores = declaracao(var)
                tabela = []
                for lexema, valor in zip(lexemas, valores):
                    if(tipo(valor) != "CADEIA"):
                        print(f"Erro (linha {count_linhas}): valor não é uma cadeia")
                        break
                    else:
                        tabela.append({"lexema": lexema, "valor": valor, "tipo": "CADEIA", "bloco": bloco})
                if escopo_criacao(tabela, pilha):
                    pilha.append(tabela)
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
                pilha.pop()
            case "\n":
                pass
            case _:
                try:
                    var, valor = linha.split("=")
                    atribuicao(var, valor, pilha, count_linhas)
                except ValueError:
                    print(f"Erro (linha {count_linhas}): comando inválido")
        count_linhas += 1      
    
    
def lista_comandos(nome_arq):
    arquivo = open(nome_arq, 'r') 
    lista = []
    for linha in arquivo:
        lista.append(linha.strip())
    arquivo.close()
    return lista

def declaracao(var):
    lexemas = []
    valores = []
    atribuicoes = re.findall("[a-zA-Z][0-9a-zA-Z_]*=.+", var)
    for i in atribuicoes:
        lex, val = i.split("=")
        lexemas.append(lex)
        valores.append(val)
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
    if valor[0] == '"' and valor[len(valor)-1] == '"':
        return "CADEIA"
    try:
        float(valor)
        return "NUMERO"
    except ValueError:
        return None