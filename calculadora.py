import flet as ft
from flet import colors
from decimal import Decimal

# Lista de configurações para os botões da calculadora
botoes = [
    {'operador': 'AC', 'fonte': colors.BLACK, 'fundo': colors.BLUE_GREY_100}, 
    {'operador': '±', 'fonte': colors.BLACK, 'fundo': colors.BLUE_GREY_100}, 
    {'operador': '%', 'fonte': colors.BLACK, 'fundo': colors.BLUE_GREY_100},
    {'operador': '/', 'fonte': colors.WHITE, 'fundo': colors.ORANGE},
    {'operador': '7', 'fonte': colors.WHITE, 'fundo': colors.WHITE24},
    {'operador': '8', 'fonte': colors.WHITE, 'fundo': colors.WHITE24},
    {'operador': '9', 'fonte': colors.WHITE, 'fundo': colors.WHITE24},
    {'operador': '*', 'fonte': colors.WHITE, 'fundo': colors.ORANGE},
    {'operador': '4', 'fonte': colors.WHITE, 'fundo': colors.WHITE24},
    {'operador': '5', 'fonte': colors.WHITE, 'fundo': colors.WHITE24},
    {'operador': '6', 'fonte': colors.WHITE, 'fundo': colors.WHITE24},
    {'operador': '-', 'fonte': colors.WHITE, 'fundo': colors.ORANGE},
    {'operador': '1', 'fonte': colors.WHITE, 'fundo': colors.WHITE24},
    {'operador': '2', 'fonte': colors.WHITE, 'fundo': colors.WHITE24},
    {'operador': '3', 'fonte': colors.WHITE, 'fundo': colors.WHITE24},
    {'operador': '+', 'fonte': colors.WHITE, 'fundo': colors.ORANGE},
    {'operador': '0', 'fonte': colors.WHITE, 'fundo': colors.WHITE24},
    {'operador': '.', 'fonte': colors.WHITE, 'fundo': colors.WHITE24},
    {'operador': '=', 'fonte': colors.WHITE, 'fundo': colors.ORANGE},
]

# Função principal que configura a página da calculadora
def main(page: ft.Page):
    page.bgcolor = colors.BLACK
    page.window_resizable = False
    page.window_width = 250
    page.window_height = 380
    page.title = 'Calculadora'
    page.window_always_on_top = True

    # Campo de texto para exibir o resultado
    result = ft.Text(value='0', color=colors.WHITE, size=20)

    # Função interna para calcular o resultado das operações
    def calculate(operador, value_at):
        try:    
            value = eval(value_at)

            # Trata os casos de porcentagem e negação
            if operador == '%':
                value /= 100
            elif operador == '±':
                value = -value
        except:
            return 'Error'
        
        # Limita o número de dígitos exibidos
        digits = min(abs(Decimal(value).as_tuple().exponent), 5)
        return format(value, f'.{digits}f')

    # Função para lidar com a seleção de botões
    def select(e):
        value_at = result.value if result.value not in ('0', 'Error') else ''
        value = e.control.content.value

        # Adiciona números ou operadores ao campo de texto
        if value.isdigit():
            value = value_at + value
        elif value == 'AC':
            value = '0'
        else:
            if value_at and value_at[-1] in ('/', '*', '-', '+', '.'):
                value_at = value_at[:-1]

            value = value_at + value
            
            # Calcula o resultado se o último caractere for um operador
            if value[-1] in ('=', '%', '±'):
                value = calculate(operador=value[-1], value_at=value_at)

        result.value = value
        result.update()

    # Configuração da exibição do resultado
    display = ft.Row(
        width=250,
        controls=[result],
        alignment='end',
    )

    # Criação dos botões da calculadora
    btn = [ft.Container(
            content=ft.Text(value=btn['operador'], color=btn['fonte']),
            width=50,
            height=50,
            bgcolor=btn['fundo'],
            border_radius=100,
            alignment=ft.alignment.center,
            on_click=select,
        ) for btn in botoes]
    
    # Configuração do layout do teclado da calculadora
    keyboard = ft.Row(
        width=250,
        wrap=True,
        controls=btn,
        alignment='end'  
    )

    # Adiciona a exibição e o teclado à página
    page.add(display, keyboard)

# Inicia a aplicação
ft.app(target=main)