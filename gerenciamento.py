def gerenciamento(nome_arq):
    count_linhas = 0
    reservadas = ["BLOCO", "NUMERO", "CADEIA", "PRINT", "FIM"]
    instrucoes = lista_comandos(nome_arq)
    for linha in instrucoes:
        partes = linha.split()

        match partes[0]:
            case "BLOCO":
                
                blocos = partes[1]
            case "NUMERO":
                var = "".join(partes[1:])
                lexemas, valores = atribuicao(var)
                count_linhas += 1
            case "CADEIA":
                count_linhas += 1
            case "PRINT":
                count_linhas += 1
            case "FIM":
                desempilha(count_blocos)
                count_blocos -= 1
            case "\n":
                count_linhas += 1
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

def desempilha(bloco):
    pass