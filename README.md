# 🌡️ CPU Thermal Dashboard

Um monitor de hardware moderno e minimalista desenvolvido em **Python** e **C++**, utilizando a biblioteca do **Open Hardware Monitor** para obter leituras precisas de sensores de baixo nível.

## 🚀 Características

- **Interface LCD Dinâmica**: Visual inspirado em telas de cristal líquido com tema Dark.
- **Feedback Visual por Cores**: 
  - 🟢 **Verde**: Temperatura estável (< 60°C).
  - 🟡 **Amarelo**: Carga moderada (60°C - 80°C).
  - 🔴 **Vermelho**: Alerta crítico (> 80°C).
- **Persistência de Dados**: Exibe as temperaturas **Mínima** e **Máxima** alcançadas durante a sessão.
- **Alta Precisão**: Diferente da API WMI padrão, utiliza drivers de baixo nível para leitura real do die da CPU.

## 🛠️ Tecnologias Utilizadas

* **Python 3.12**: Lógica principal e interface.
* **PyQt5**: Framework para a interface gráfica (GUI).
* **C++ / .NET**: Ponte de comunicação com sensores de hardware.
* **Pythonnet**: Integração entre o ambiente Python e a DLL do Open Hardware Monitor.

## 📋 Pré-requisitos

Antes de rodar o projeto, você precisará:

1.  **Python 3.12.x** instalado.
2.  Executar o terminal/editor como **Administrador** (necessário para ler sensores de hardware).
3.  As seguintes bibliotecas Python:
    ```bash
    pip install PyQt5 pythonnet
    ```

## 🔧 Instalação e Execução

1.  Clone o repositório:
    ```bash
    git clone [https://github.com/seu-usuario/nome-do-repositorio.git](https://github.com/seu-usuario/nome-do-repositorio.git)
    ```
2.  Certifique-se de que o arquivo `OpenHardwareMonitorLib.dll` está na mesma pasta que o script.
3.  **Importante**: Clique com o botão direito na DLL -> Propriedades -> Marque **Desbloquear**.
4.  Execute a aplicação:
    ```bash
    python main_gui.py
    ```

## 📸 Preview
*(Adicione aqui um screenshot da sua janela rodando)*

---
Desenvolvido por [Seu Nome]