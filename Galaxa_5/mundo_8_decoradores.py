
'''
Decoradores no Python servem pra modificar funções. É fazer muita coisa por "debaixo dos panos". 
Tratamento de erros, adicionar funcionalidades.. tudo pré pronto.
'''

    
def comprimenta(funcao_que_voce_definir_depois): #O DECORADOR ENTRA ANTES! Embora a sintaxe seja igual de uma função, isso é um decorador.

    def adiciona_texto(numero_escolhido): #aqui vai ter receber o argumento da sua função mesmo.
    
        print(f"Vamos somar o número {numero_escolhido}! Obrigado por utilizar nossa calculadora.")
        valor_final = funcao_que_voce_definir_depois(numero_escolhido)
        return valor_final

    return adiciona_texto


@comprimenta
def soma_cinco(valor):

    valor = valor + 5
    print(valor)


@comprimenta
def soma_dez(valor):

    valor = valor + 10
    print(valor)

numero = int(input("Digite um número inteiro: "))

soma_dez(numero)


























