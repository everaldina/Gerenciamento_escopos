
# Gerenciamento de Escopos

Repositório para criação de um gerenciador de escopo para a disciplina de Compiladores.

O projeto utiliza uma pilha para armazenar os escopos, onde cada escopo é representado por uma lista de dicionários. Cada dicionário armazena o lexema, valor, tipo e bloco de uma variável.

Desenvolvido por: [Everaldina Barbosa](https://github.com/everaldina).

## Como Executar o Projeto
Para executar o projeto, basta rodar o arquivo `gerenciamento.py`.

Na função `main`, é possível alterar o nome do arquivo de entrada. Este arquivo deve estar na mesma pasta do arquivo `gerenciamento.py` e conter o código a ser analisado.

A saída do programa será mostrada no terminal.

## Características do Projeto
 - Existem dois tipos de dados: 'NUMERO' e 'CADEIA'.
 - Além disso, existem apenas as palavras reservadas 'BLOCO', 'PRINT' e 'FIM'.
 - É possível fazer atribuições, declarações e prints de variáveis.

### Escopos
Cada vez que é encontrado um bloco, é criado um novo escopo e adicionado à pilha. Quando é encontrado um fim de bloco, o escopo é removido da pilha.

### Declarações
Declarações de variáveis são adicionadas ao escopo atual. Caso a variável já tenha sido declarada no escopo atual, é mostrado um erro. Variáveis declaradas em outro escopo com o mesmo nome são permitidas, e a variável do escopo mais interno passa a valer para aquele bloco.

Também é permitido declarar variáveis implicitamente em uma expressão. Por exemplo: `a = 1`. Nesse caso, é adicionada ao escopo atual a variável 'a' com o valor 1 e tipo 'NUMERO'.

### Atribuições
Atribuições são permitidas para variáveis já declaradas ou implicitamente declaradas. Caso a variável não tenha sido declarada, o tipo da variável é deduzido.

Atribuições de variáveis já declaradas devem ser feitas com constantes do mesmo tipo.
 - Exemplo: `NUMERO a`
 - Nesse caso, só será possível atribuir números à variável 'a'.

Em atribuições de variáveis implicitemente declaradas, o conteúdo da variável também tem que continuar sendo do mesmo tipo.
-  Exemplo:  `a = 1`
-  Nesse caso, só será possível atribuir posteriormente números à variável 'a'.

Não é possível atribuir uma variável a outra. Por exemplo: `a = b`. Nesse caso, é mostrado um erro.

### Prints
Prints são feitas para variáveis já declaradas, se não do escopo atual em algum dos anteriores. Caso a variável não tenha sido declarada, é exibido um erro.


## Exemplo
No repositorio existe um arquivo de exemplo chamado `exemplo.txt`, como um arquivo contendo o código a ser analisado, a saida esperada do programa esta no arquivo `saida_esperada.txt`. 

Executando o arquivo `gerenciamento.py` com o arquivo `exemplo.txt` como entrada, a saida esperada é mostrada no terminal.
