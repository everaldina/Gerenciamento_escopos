class Tabela:
    def __init__(self, lexema, valor, tipo, escopo):
        self.__lexema = lexema
        self.__valor = valor
        self.__tipo = tipo
        self.__escopo = escopo
    
    def get_lexema(self):
        return self.__lexema
    def set_lexema(self, lexema):
        self.__lexema = lexema
        
    def get_valor(self):
        return self.__valor
    def set_valor(self, valor):
        self.__valor = valor
    
    def get_tipo(self):
        return self.__tipo
    def set_tipo(self, tipo):
        self.__tipo = tipo
    
    def get_escopo(self):
        return self.__escopo
    def set_escopo(self, escopo):
        self.__escopo = escopo
    
    
    

