import time, threading
from os import system
from platform import system as syste
from pynput.mouse import Button, Controller as MouseController
from pynput.keyboard import Controller as KeyboardController
from pynput import keyboard as kb


macro_thread = None
running = True
mouse = MouseController()
keyboard = KeyboardController()
hot_key = None
ativarhotkey = False
mouseoptions = ['Mouse', 'Clique Esquerdo', 'Clique Direito']
macrooptions = ['Macro', 'Auto Hold', 'Auto Click']
escolhamacro = []
temptecla = ''
ms = float(0.05)


def flush_input():
    try:
        from msvcrt import kbhit, getch
        while kbhit():
            getch()

    except ImportError:
        from sys import stdin
        from termios import tcflush, TCIOFLUSH
        tcflush(stdin, TCIOFLUSH)

def clear():
    sistema = syste().lower()
    if sistema == 'windows':
        system('cls')
    else:
        system('clear')



def setHotkey():
    global listener
    def on_press(key):
        global hot_key
        try:
            if hasattr(key, 'char'):
                hot_key = key.char
            else:
                hot_key = key
        except AttributeError:
            hot_key = key
        print(f'hotkey detectada: {hot_key}')
        return False
    
    with kb.Listener(on_press=on_press) as listener:
        listener.join()


def setTecla():
    def on_press(key):
        global temptecla
        try:
            temptecla = key.char
        except AttributeError:
            temptecla = key
        print(f'tecla detectada: {temptecla}')
        return False
    with kb.Listener(on_press=on_press) as listener:
        listener.join()


def hotkeyloop():
    global listener, running

    def on_press(key):
        global hot_key, ativarhotkey
        if not running:
            return False

        if hot_key is None:
            return
        
        # essa porra converte as teclas para string para comparação
        key_str = str(key).replace("'", "")
        hot_key_str = str(hot_key).replace("'", "")

        
        if key_str == hot_key_str:
            ativarhotkey = not ativarhotkey
            clear()
            print(f'Macro {"\033[32mON\033[m" if ativarhotkey else "\033[31mOFF\033[m"}')
            print('(CTRL + C Pra Finalizar)')


    listener = kb.Listener(on_press=on_press)
    listener.start()


def stop_macro():
    global running, listener, ativarhotkey, macro_thread
    running = False
    ativarhotkey = False

    if listener:
        listener.stop()

    if macro_thread and macro_thread.is_alive():
        macro_thread.join(timeout=1)


def opcoes():
    global escolhamacro, hot_key, running
    flush_input()
    while True:
        clear()
        print("-"*50)
        print("Ruanzinh's Macro Tool".center(50))
        print("-"*50)
        time.sleep(2)
        if escolhamacro:
            c = 0
            print('\n', '-'*31, '\n','\033[33m', f'{"SUAS PREFERENCIAS".center(30)}', '\033[m', '\n', '-'*31)
            for i in escolhamacro:
                c += 1
                if c == 1:
                    print(f' \033[32mDispositivo:\033[m {i.capitalize()}')
                    device = i
                else:
                    if device == 'mouse' and c == 2:
                        print(f' \033[32mAlvo:\033[m {mouseoptions[i]}')
                    
                    elif device == 'teclado' and c == 2:
                        print(f' \033[32mAlvo:\033[m {i}')

                    elif c == 3:
                        print(f' \033[32mModo:\033[m {macrooptions[i]}')
            if not hot_key:
                print('-'*50)
        if hot_key:
            print(f' \033[32mHotkey:\033[m {hot_key}')
            print('-'*50)
            
        print("1- Mouse\n2- Teclado\n3- Setar Hotkey\n4- Iniciar Macro\n5- Finalizar Programa")
        while True:
            try:
                flush_input()
                escolha = int((input('\nEscolha: ')))
                if escolha < 1 or escolha > 5:
                    print("\n\033[31mEscolha de 1 a 5.\033[m")
                    time.sleep(1)
                else:
                    break
            except ValueError:
                print("\n\033[31mValor invalido!\033[m\n")
        
        if escolha == 1:
            time.sleep(1)
            clear()
            escolhamacro = mouseaba()

        elif escolha == 2:
            time.sleep(1)
            clear()
            escolhamacro = tecladoaba()

        elif escolha == 3:
            time.sleep(1)
            clear()
            print('Configure sua hotkey: ')
            setHotkey()
            time.sleep(1)

        elif escolha == 4:
            time.sleep(1)
            clear()
            if escolhamacro:
                if hot_key:
                    running = True
                    if not any(t.name == "hotkeyloop" for t in threading.enumerate()):
                        threading.Thread(target=hotkeyloop, daemon=True, name="hotkeyloop").start()

                        if escolhamacro[0] == 'mouse':
                            mousemacro()
                        else:
                            tecladomacro()
                else:
                    print('\033[31mHotkey não definida.\033[m')
                    time.sleep(2)
            else:
                print('Antes, \033[31mConfigure o Macro.\033[m')
                time.sleep(2)

        elif escolha == 5:
            clear()
            print('Finalizando...')
            time.sleep(2)
            quit()

def mouseaba():
    # Lista para armazenar as escolhas, primeiro pra reconhecer o dispositivo, segundo pra escolha do botao (1 / 2), e terceiro pro auto 
    escolhadomouse = ['mouse']
    
    # Atraso do click
    global ms

    # Escolha do botão
    print("Selecione um botão:\n\n1- Clique Esquerdo\n2- Clique Direito\n")
    while True:
        try:
            flush_input()
            escolha = int(input("Sua escolha: "))
            if escolha < 1 or escolha > 2:
                print("\n\033[31mValor Incorreto,\033[m Novamente faça a ", end='')
            else:
                escolhadomouse.append(escolha)
                time.sleep(1)
                clear()
                break

        except ValueError:
            print("\n\033[31mDigite um valor válido,\033[m e novamente faça a ", end='')

    # Escolha do Auto
    print("1- Auto Hold\n2- Auto Click\n")
    while True:
        try:
            flush_input()
            escolha = int(input('Sua escolha: '))
            if escolha < 1 or escolha > 2:
                print("\n\033[31mValor Incorreto,\033[m Novamente faça a ", end='')
            else:
                escolhadomouse.append(escolha)

                if escolha == 2:
                    while True:
                        flush_input()
                        escolhams = input(f'\nQual o tempo de atraso? (Atual: {ms})\nPressione ENTER caso queira continuar com o valor atual, ou digite um valor: ').strip()
                        if escolhams == '':
                            break
                        try:
                            ms = float(escolhams)
                            break
                        except ValueError:
                            print('\n\033[31mValor inválido! Digite um valor flutuante. (USE PONTOS AO INVÉS DE VÍRGULAS)\033[m')
                            time.sleep(2)
                        
                time.sleep(1)
                clear()
                return escolhadomouse

        except ValueError:
            print("\n\033[31mDigite um número válido,\033[m e novamente faça a ", end='')


def tecladoaba():
    global temptecla, ms
    # Lista para armazenar as escolhas, primeiro pra reconhecer o dispositivo, segundo pra escolha do botao (1 / 2), e terceiro pro auto 
    escolhadoteclado = ['teclado']

    # Escolha do botão
    print('Digite uma tecla para ser repetida: ')
    setTecla()
    time.sleep(1)
    clear()
    escolhadoteclado.append(temptecla)
    # Escolha do Auto
    print("1- Auto Hold\n2- Auto Click\n")
    while True:
        try:
            flush_input()
            escolha = int(input('Sua escolha: '))
            if escolha < 1 or escolha > 2:
                print("\n\033[31mValor Incorreto,\033[m Novamente faça a ", end='')
            else:
                escolhadoteclado.append(escolha)
                
                if escolha == 2:
                    while True:
                        flush_input()
                        escolhams = input(f'\nQual o tempo de atraso? (Atual: {ms})\nPressione ENTER caso queira continuar com o valor atual, ou digite um valor: ').strip()
                        if escolhams == '':
                            break
                        try:
                            ms = float(escolhams)
                            break
                        except ValueError:
                            print('\n\033[31mValor inválido! Digite um valor flutuante. (USE PONTOS AO INVÉS DE VÍRGULAS)\033[m')
                            time.sleep(2)
                time.sleep(1)
                clear()
                return escolhadoteclado

        except ValueError:
            print("\033[31mDigite um número válido,\033[m e novamente faça a ", end='')


def mousemacro():
    global ativarhotkey, escolhamacro
    botao = Button.left if escolhamacro[1] == 1 else Button.right
    modo = escolhamacro[2]
    is_pressed = False
    
    print('Iniciando Macro do Mouse (CTRL + C Pra Finalizar)')

    while True:
        try:
            if ativarhotkey:
                if modo == 1: # Auto Hold
                    if not is_pressed:
                        mouse.press(botao)
                        is_pressed = True
            else:
                if modo == 1 and is_pressed: # Liberar o auto hold
                    mouse.release(botao)
                    is_pressed = False

            if modo == 2: # Auto click
                if ativarhotkey:
                    mouse.click(botao)
                    time.sleep(ms)
            
            time.sleep(0.01)
        except KeyboardInterrupt:
            if is_pressed: # solta pra garantir q vai dar de boa
                mouse.release(botao)
            stop_macro()
            print('\nVoltando para a pagina inicial...')
            time.sleep(2)
            opcoes()

def tecladomacro():
    global ativarhotkey, escolhamacro
    tecla = escolhamacro[1]
    modo = escolhamacro[2]
    is_pressed = False

    print('Iniciando Macro do Teclado (CTRL + C Pra Finalizar)')

    while True:
        try:
            if ativarhotkey:
                if modo == 1: # Auto hold
                    if not is_pressed:
                        keyboard.press(tecla)
                        is_pressed = True
                    
            else:
                if is_pressed: # Libera tambem o auto hold
                    keyboard.release(tecla)
                    is_pressed = False

            if modo == 2 and ativarhotkey: # Auto Click
                keyboard.tap(tecla)
                time.sleep(ms)
            
            time.sleep(0.01)

        except KeyboardInterrupt:
            if is_pressed: # TU JA SABE PRA Q SERVE
                keyboard.release(tecla)
            stop_macro()
            print('\nVoltando para a pagina inicial...')
            time.sleep(2)
            opcoes()
