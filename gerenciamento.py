import re

def gerenciamento(nome_arq):
    pilha = [[]]
    count_linhas = 1
    instrucoes = lista_comandos(nome_arq)
    for linha in instrucoes:
        partes = linha.split()

        if len(partes) == 0:
            count_linhas += 1
        else:
            match partes[0]:
                case "BLOCO":
                    bloco = partes[1]
                    pilha.append([])
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
                            print(f"(linha {count_linhas:>2}) Erro: valor não numérico")
                            break
                    if escopo_criacao(tabela, pilha):
                        pilha[len(pilha)-1].extend(tabela)
                        #print(f"Apendando no : {bloco}")
                    else:
                        print(f"(linha {count_linhas:>2}) Erro: variável já declarada")
                case "CADEIA":
                    var = "".join(partes[1:])
                    lexemas, valores = declaracao(var)
                    tabela = []
                    for lexema, valor in zip(lexemas, valores):
                        if(tipo(valor) == "CADEIA" or valor == None):
                            tabela.append({"lexema": lexema, "valor": valor, "tipo": "CADEIA", "bloco": bloco})
                            #print(f"Adcionando {lexema} = {valor}")
                        else:
                            print(f"(linha {count_linhas}) Erro: valor não é cadeia")
                        break
                    if escopo_criacao(tabela, pilha):
                        pilha[len(pilha)-1].extend(tabela)
                        #print(f"Apendando no : {bloco}")
                    else:
                        print(f"(linha {count_linhas}) Erro: variável já declarada")
                case "PRINT":
                    var = partes[1]
                    try:
                        valor = busca_variavel(var, pilha, count_linhas)
                        print(f"(linha {count_linhas:>2}) PRINT '{var}': {valor}")
                    except Exception as ex:
                        print(str(ex))
                case "FIM":
                    pilha.pop()
                case _:
                    try:
                        var, valor = linha.split("=")
                        atribuicao(var.strip(), valor.strip(), pilha, count_linhas)
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

# AT ->  ID = CONST | ID
def declaracao(var):
    lexemas = []
    valores = []
    atribuicoes = re.findall("[a-zA-Z][0-9a-zA-Z_]*=[^,]+|[a-zA-Z][0-9a-zA-Z_]*[^,]?", var)
    
    for i in atribuicoes: 
        separado = i.split("=")
        if len(separado) == 2: # AT ->  ID = CONST
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
    raise Exception(f"(linha {linha:>2}) Erro: variável '{variavel}' não declarada")

def atribuicao(variavel, valor, pilha, linha):
    try: # teste de regra atribuicao AT -> ID = CONST | ID
        tipo_var = tipo(valor)
    except Exception as ex:
        raise Exception(f"(linha {linha:>2}) Erro: não existe regra de atribuiçao 'AT -> ID = ID'")
        
    for i in pilha[len(pilha)-1:0:-1]: # percorre a pilha do topo pra baixo
        for tabela in i:
            if tabela["lexema"] == variavel:
                if tabela["tipo"] == tipo_var:
                    tabela["valor"] = valor
                    return
                else:
                    raise Exception(f"(linha {linha:>2}) Erro: valor não é do tipo '{tabela['tipo']}'")
    # se não encontrar a variável na pilha, cria uma nova
    pilha[len(pilha)-1].append({"lexema": variavel, "valor": valor, "tipo": tipo_var, "bloco": "global"})

def tipo(valor):
    if valor is None:
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


def main():
    nome_arq = "exemplo.txt"
    gerenciamento(nome_arq)
    
    
if __name__ == "__main__":
    main()