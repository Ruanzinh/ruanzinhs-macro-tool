# Ruanzinh's Macro Tool

Esse é meu primeiro projeto, é uma ferramenta de macro para automatizar ações do mouse e teclado, desenvolvida em Python.

## Funcionalidades

 Suporte para Mouse:
  - Auto Click (Botão esquerdo/direito)
  - Auto Hold (Manter pressionado)
  - Delay configurável entre clicks

- Suporte para Teclado:
  - Auto Click (Qualquer tecla)
  - Auto Hold (Manter pressionada)
  - Delay configurável entre pressionamentos

- Recursos:
  - Hotkeys personalizáveis
  - Compatível com Windows/Linux/MacOS
  - Controle preciso de delay

## Como Usar

### Windows
1. Acesse a [página de Releases](https://github.com/Ruanzinh/ruanzinhs-macro-tool/releases)
2. Baixe o arquivo `Ruanzinhs-Macro-Tool.exe`
3. Execute o programa
4. Agora é só usar

### Linux/MacOS
1. Clone o repositório:
```bash
git clone https://github.com/Ruanzinh/ruanzinhs-macro-tool.git
cd ruanzinhs-macro-tool
```

2. Instale o Pynput:
```bash
pip install pynput
```

3. Execute o programa:
```bash
python main.py
```

## Instruções de Uso

### Menu Principal:
- Mouse: Configure macros para mouse
- Teclado: Configure macros para teclado
- Setar Hotkey: Define tecla de ativação
- Iniciar Macro: Inicia a macro configurada
- Finalizar: Encerra o programa

### Controles:
- Use a hotkey definida para ativar/desativar o macro
- CTRL+C para parar a execução atual

## Configuração

### Mouse
1. Escolha o botão (Esquerdo/Direito)
2. Selecione o modo (Auto Hold/Auto Click)
3. Configure o delay (opcional)

### Teclado
1. Pressione a tecla desejada
2. Selecione o modo (Auto Hold/Auto Click)
3. Configure o delay (opcional)

## Notas

- O delay padrão é 0.05 segundos
- Use pontos (não vírgulas) para valores decimais
