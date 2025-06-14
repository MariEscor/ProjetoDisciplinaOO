#2025-06-13 ok

class Config:
    def __init__(self, largura_janela = 1280, altura_janela = 720, tam_sprite_padrao = 64):
        self.__largura_janela = largura_janela
        self.__altura_janela = altura_janela
        self.__tam_sprite_padrao = tam_sprite_padrao

    CORES = {
        'white': '#f4fefa', 
        'pure white': '#ffffff',
        'dark': '#2b292c',
        'light': '#c8c8c8',
        'gray': '#3a373b',
        'gold': '#ffd700',
        'light-gray': '#4b484d',
        'fire':'#f8a060',
        'water':'#50b0d8',
        'plant': '#64a990', 
        'black': '#000000', 
        'red': '#f03131',
        'blue': '#66d7ee',
        'normal': '#ffffff',
        'dark white': '#f0f0f0'
    }  

    @property
    def largura_janela(self) -> int:
        return self.__largura_janela

    @largura_janela.setter
    def largura_janela(self, value: int) -> None:
        if not isinstance(value, int) or value <= 0:
            raise ValueError("Largura da janela deve ser um inteiro positivo.")
        self.__largura_janela = value

    @property
    def altura_janela(self) -> int:
        return self.__altura_janela

    @altura_janela.setter
    def altura_janela(self, value: int) -> None:
        if not isinstance(value, int) or value <= 0:
            raise ValueError("Altura da janela deve ser um inteiro positivo.")
        self.__altura_janela = value

    @property
    def tam_sprite_padrao(self) -> int:
        return self.__tam_sprite_padrao
    
    @tam_sprite_padrao.setter
    def tam_sprite_padrao(self, value: int) -> None:
        if not isinstance(value, int) or value <= 0:
            raise ValueError("Tamanho do sprite padrão deve ser um inteiro positivo.")
        self.__tam_sprite_padrao = value

    def __del__(self):
        print("poh deu moh trabalho fazer essa classe Config e você a matou >:(")