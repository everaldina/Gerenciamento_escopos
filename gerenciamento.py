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
                lexemas, valores = atribuicao(var)
                tabela = []
                for lexema, valor in zip(lexemas, valores):
                    tabela.append({"lexema": lexema, "valor": valor, "tipo": "NUMERO", "bloco": bloco})
                if escopo_criacao(tabela, pilha):
                    pilha.append(tabela)
                else:
                    print(f"Erro (linha {count_linhas}): variável já declarada")
            case "CADEIA":
                var = "".join(partes[1:])
                lexemas, valores = atribuicao(var)
                tabela = []
                for lexema, valor in zip(lexemas, valores):
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
                print("atribuicao")
        count_linhas += 1      
    
    
def lista_comandos(nome_arq):
    arquivo = open(nome_arq, 'r') 
    lista = []
    for linha in arquivo:
        lista.append(linha.strip())
    arquivo.close()
    return lista

def atribuicao(var):
    lexemas = []
    valores = []
    posicao_separador = 0
    posicao_igual = 0
    for i in range(len(var)):
        if var[i] == "=":
            posicao_igual = i
            lexemas.append(var[posicao_separador:posicao_igual])
        if var[i] == ",":
            posicao_separador = i
            valores.append(var[posicao_igual+1:posicao_separador-1])
    return lexemas, valores

# verificar se no escopo atual já existe a variável
def escopo_criacao(tabela, pilha):
    for i in pilha[len(pilha)-1]:
        for j in tabela:
            if i["lexema"] == j["lexema"]:
                return False
    return True

def busca_variavel(variavel, pilha, linha):
    for i in pilha[len(pilha)-1:0:-1]: # percorre a pilha de trás pra frente
        for tabela in i:
            if tabela["lexema"] == variavel:
                return tabela["valor"]
    raise Exception(f"Erro (linha {linha}): variável '{variavel}' não declarada")