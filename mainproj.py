# mainproj.py

from Projeto.jogo import Jogo  # Importa a classe principal do jogo

def main(start_scene='mundo_aberto') -> None:
    """
    Função principal que inicializa e executa o jogo.
    Permite escolher o mapa inicial via start_scene.
    """
    jogo = Jogo(start_scene=start_scene)
    jogo.executar()
    
def main(start_scene='hospital') -> None:
    """
    Função principal que inicializa e executa o jogo.
    Permite escolher o mapa inicial via start_scene.
    """
    jogo = Jogo(start_scene=start_scene)
    jogo.executar()

if __name__ == "__main__":
    main()
