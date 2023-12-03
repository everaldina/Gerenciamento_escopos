import re

def gerenciamento(nome_arq):
    ''' 
        Recebe o nome de um arquivo e executa o gerenciamento de escopo dele.
        Impime os prints e erros da execução.
    '''
    
    # pilha de escopos, cada item da pilha representa um escopo e 
    # composto por uma lista de tabelas de simbolos
    pilha = [[]]
    
    count_linhas = 1
    instrucoes = lista_comandos(nome_arq) # lista com as instruções do arquivo
    
    # percorre as instruções do arquivo
    for linha in instrucoes:
        
        partes = linha.split() # separa a linha em partes separadas por espaços

        # se a linha for vazia, pula para a proxima
        if len(partes) == 0:
            count_linhas += 1
        else:
            # verifica qual regra a linha se encaixa
            match partes[0]:
                case "BLOCO": # cria um novo escopo na pilha
                    bloco = partes[1]
                    pilha.append([])
                    
                case "NUMERO": # cria uma nova variável do tipo NUMERO
                    # junta todo o resto da linha em uma string
                    var = "".join(partes[1:]) 
                    
                    # chama a função de declaração e retorna uma lista de lexemas e uma lista de valores
                    lexemas, valores = declaracao(var)
                    
                    tabela = [] # lista de tabelas de simbols que serao appendados no escopo atual da pilha
                    
                    # percorre os lexemas e valores e cria uma tabela de simbolos para cada
                    for lexema, valor in zip(lexemas, valores):
                        try: # verifica se o valor é um número, se não for lança uma exceção
                            if(tipo(valor) == "NUMERO" or valor == None):
                                tabela.append({"lexema": lexema, "valor": valor, "tipo": "NUMERO", "bloco": bloco})
                        except Exception as ex:
                            print(f"(linha {count_linhas:>2}) Erro: valor não numérico")
                            break
                    
                    # verifica se a variável já foi declarada no mesmo escopo, se não, appenda na pilha do escopo atual
                    if escopo_criacao(tabela, pilha):
                        pilha[len(pilha)-1].extend(tabela)
                    else:
                        print(f"(linha {count_linhas:>2}) Erro: variável já declarada")
                        
                case "CADEIA": # cria uma nova variável do tipo CADEIA
                    # junta todo o resto da linha em uma string
                    var = "".join(partes[1:])
                    
                    # chama a função de declaração e retorna uma lista de lexemas e uma lista de valores
                    lexemas, valores = declaracao(var)
                    
                    tabela = [] # lista de tabelas de simbols que serao appendados no escopo atual da pilha
                    
                    # percorre os lexemas e valores e cria uma tabela de simbolos para cada
                    for lexema, valor in zip(lexemas, valores):
                        
                        # verifica se o valor é uma cadeia, se for adiciona na lista de tabelas
                        if(tipo(valor) == "CADEIA" or valor == None):
                            tabela.append({"lexema": lexema, "valor": valor, "tipo": "CADEIA", "bloco": bloco})
                        else:
                            print(f"(linha {count_linhas}) Erro: valor não é cadeia")
                            break
                        
                    # verifica se a variável já foi declarada no mesmo escopo, se não, appenda na pilha do escopo atual
                    if escopo_criacao(tabela, pilha):
                        pilha[len(pilha)-1].extend(tabela)
                    else:
                        print(f"(linha {count_linhas}) Erro: variável já declarada")
                        
                        
                case "PRINT": # imprime o valor de uma variável
                    
                    var = partes[1] # nome da variável
                    
                    # tenta buscar o valor da variável na pilha, se não encontrar printa o erro
                    try:
                        valor = busca_variavel(var, pilha, count_linhas)
                        print(f"(linha {count_linhas:>2}) PRINT '{var}': {valor}")
                    except Exception as ex:
                        print(str(ex))
                        
                case "FIM": # remove o escopo do topo da pilha
                    pilha.pop()
                    
                case _: # se não for nenhuma das regras acima, é uma atribuição
                    
                    # tenta fazer a atribuição, se não conseguir printa o erro
                    try:
                        var, valor = linha.split("=") # separa a linha em variável e valor
                        atribuicao(var.strip(), valor.strip(), pilha, count_linhas) # atribui o valor a variável
                    except Exception as ex:
                        print(str(ex))
            count_linhas += 1      
    

def lista_comandos(nome_arq):
    '''
        Retorna uma lista com as instruções do arquivo.
        Cada item é uma linha do arquivo com espaços finais e iniciais removidos
    '''
    arquivo = open(nome_arq, 'r') 
    lista = []
    for linha in arquivo:
        lista.append(linha.strip()) # adiciona a linha na lista removendo os espaços finais e iniciais
    arquivo.close()
    return lista


# AT ->  ID = CONST | ID
def declaracao(var):
    ''' Le uma linha de decalração de variaveis e retorna uma lista de lexemas e uma lista de valores '''
    
    # listas para armazenar os possiveis lexemas e valores da linha de declaração
    lexemas = []
    valores = []
    
    '''
        Regex para separar as atribuições
        [a-zA-Z][0-9a-zA-Z_]*=[^,]+ para atribuições do tipo  AT -> ID = CONST
        [a-zA-Z][0-9a-zA-Z_]*[^,]? para atribuições do tipo  AT -> ID
    '''
    declaracoes = re.findall("[a-zA-Z][0-9a-zA-Z_]*=[^,]+|[a-zA-Z][0-9a-zA-Z_]*[^,]?", var)
    
    '''
        Percorre as declarcao e separa os lexemas e valores.
        Se for uma decalracao do tipo AT -> ID = CONST, o lexema é o primeiro item e o valor é o segundo.
        Se for uma declaracao do tipo AT -> ID, o lexema é o primeiro item e o valor é None.
    '''
    for i in declaracoes: 
        separado = i.split("=")
        if len(separado) == 2: # AT ->  ID = CONST
            lexemas.append(separado[0])
            valores.append(separado[1])
        else: # AT ->  ID
            lexemas.append(separado[0])
            valores.append(None)
    return lexemas, valores


def escopo_criacao(tabela, pilha):
    ''' Verificar se no escopo atual já existe a variável '''
    
    for i in pilha[len(pilha)-1]: # percorre a pilha do escopo atual
        for j in tabela:
            if i["lexema"] == j["lexema"]:
                return False
    return True


def busca_variavel(variavel, pilha, linha):
    ''' Percorre a pilha de tabelas e retorna o valor de uma variável. '''
    
    for i in pilha[len(pilha)-1:0:-1]: # percorre a pilha do topo pra baixo
        for tabela in i:
            if tabela["lexema"] == variavel: # se encontrar a variável na pilha, retorna o valor
                return tabela["valor"]
    # se não encontrar a variável na pilha, lança uma exceção
    raise Exception(f"(linha {linha:>2}) Erro: variável '{variavel}' não declarada")


def atribuicao(variavel, valor, pilha, linha):
    '''
        Atualiza o valor de uma variável na pilha de tabelas.
        Se a variável não existir na pilha, cria uma nova.
        Se o tipo do valor for diferente do tipo da variável, lança uma exceção.
        Se for uma atribuição de uma variavel a outra uma execeção é lançada.
    '''
    
    try: # teste de regra atribuicao AT -> ID = CONST | ID
        tipo_var = tipo(valor)
    except Exception as ex:
        raise Exception(f"(linha {linha:>2}) Erro: não existe regra de atribuiçao 'AT -> ID = ID'")
        
    # percorre a pilha do topo pra baixo
    for i in pilha[len(pilha)-1:0:-1]: 
        for tabela in i:
            # se encontrar a variável na pilha e o tipo for o mesmo, atribui o valor
            if tabela["lexema"] == variavel: 
                if tabela["tipo"] == tipo_var:
                    tabela["valor"] = valor
                    return
                else: # se a atribução for de um tipo diferente do declarado
                    raise Exception(f"(linha {linha:>2}) Erro: valor não é do tipo '{tabela['tipo']}'")
                
    # se não encontrar a variável na pilha, cria uma nova
    pilha[len(pilha)-1].append({"lexema": variavel, "valor": valor, "tipo": tipo_var, "bloco": "global"})


def tipo(valor):
    ''' 
        Verifica o tipo de um valor.
        Retorna "NUMERO" ou "CADEIA" ou None caso seja uma variavel nao inicializada.
        Caso não seja um dos tipos previstos, lança uma exceção.
    '''
    
    if valor is None: # caso seja uma variável não inicializada
        return None
    
    if valor[0] == '"' and valor[len(valor)-1] == '"': # cadeia
        return "CADEIA"
    
    # tenta converter para float, se não conseguir, é uma variável não prevista na gramática
    try:
        float(valor)
        return "NUMERO"
    except ValueError:
        raise Exception()


def print_tabela(tabela):
    ''' Funcao auxiliar para imprimir uma tabela '''
    print(f"{tabela['tipo']} {tabela['lexema']} = {tabela['valor']} | {tabela['bloco']}")


def print_pilha(pilha):
    ''' Imprime a pilha de tabelas '''
    
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