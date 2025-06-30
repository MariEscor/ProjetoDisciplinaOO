# config.py

class Config:
    """
    Classe de configuração para o jogo Profmoon: Crônicas Acadêmicas.

    Esta classe encapsula as principais configurações do jogo como atributos de instância,
    permitindo que esses valores sejam gerenciados de forma orientada a objetos
    e acessados de maneira controlada através de propriedades (getters e setters).

    Atributos:
        __largura_tela (int): Largura da janela do jogo em pixels.
        __altura_tela (int): Altura da janela do jogo em pixels.
        __tam_sprite_padrao (int): Tamanho padrão em pixels para sprites, usado para consistência.
        __vel_animacao (int): Velocidade base da animação para entidades no jogo.
    """
    def __init__(self, largura_tela: int = 1280, altura_tela: int = 720, tam_sprite_padrao: int = 64, vel_animacao: int = 4) -> None:
        self.__largura_tela: int = largura_tela
        self.__altura_tela: int = altura_tela
        self.__tam_sprite_padrao: int = tam_sprite_padrao
        self.__vel_animacao: int = vel_animacao

    @property
    def largura_tela(self) -> int:
        return self.__largura_tela

    @largura_tela.setter
    def largura_tela(self, value: int) -> None:
        if not isinstance(value, int) or value <= 0:
            raise ValueError("Largura da tela tem que ser um int positivo.")
        self.__largura_tela = value

    @property
    def altura_tela(self) -> int:
        return self.__altura_tela

    @altura_tela.setter
    def altura_tela(self, value: int) -> None:
        if not isinstance(value, int) or value <= 0:
            raise ValueError("Altura da tela tem que ser um int positivo.")
        self.__altura_tela = value

    @property
    def tam_sprite_padrao(self) -> int:
        return self.__tam_sprite_padrao

    @tam_sprite_padrao.setter
    def tam_sprite_padrao(self, value: int) -> None:
        if not isinstance(value, int) or value <= 0:
            raise ValueError("Tamanho do sprite padrão deve ser um int positivo.")
        self.__tam_sprite_padrao = value

    @property
    def vel_animacao(self) -> int:
        return self.__vel_animacao
    
    @vel_animacao.setter
    def vel_animacao(self, value: int) -> None:
        if not isinstance(value, int) or value <= 0:
            raise ValueError("Velocidade de animação deve ser um int positivo.")
        self.__vel_animacao = value

    # Define as cores utilizadas no jogo como atributos de classe (constantes)
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

    # Define as camadas do mundo como atributos de classe (constantes)
    CAMADAS_MUNDO = {
        'water': 0.0,
        'bg': 1.0, 
        'shadow': 2.0, 
        'main': 3.0, 
        'top': 4.0 
    }  


    def __del__(self) -> None:
        pass