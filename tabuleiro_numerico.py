import random
import os
import winsound
from datetime import datetime
import pickle
from excessoes_customizadas import NumeroInvalidoException, PosicaoInvalidaException

#Declaração de constantes para cores utilizadas globalmente
CORES = {'vermelho': '\033[31m', 'verde':'\033[32m', 'amarelo': '\033[33m', 'azul': '\033[34m', 'magenta': '\033[35m','ciano': '\033[36m'}
RESET = '\033[0m'

#Criação de um decorador para criar classes únicas
def singleton(cls):
    instances = {}
    def get_instance(*args, **kwargs):
        if cls not in instances:
            instances[cls] = cls(*args, **kwargs)
        return instances[cls]
    return get_instance

#Entidade Jogador, responsável por acoplar todas as informações relevantes sobre os jogadores do jogo.
class Jogador:
    def __init__(self, nome, cor):
        self.nome = nome
        self.cor = cor
        self.pontuacao = 0
        self.objetivo = None
        self.especiais = 0
    
    def sortear_objetivo(self, objetivos):
        self.objetivo = random.choice(objetivos)
        return self.objetivo
    
    def incrementar_pontuacao(self):
        self.pontuacao+=1

    def usar_especial(self):
        self.especiais -= 1

#Entidade Objetivo, responsável por verificar se a condição de vitória de certo jogador foi atendida no tabuleiro.
class Objetivo:
    def verificar_objetivo(self, matriz_tabuleiro, tamanho_tabuleiro):
        return (self.verificar_vertical(matriz_tabuleiro, tamanho_tabuleiro) or 
                self.verificar_horizontal(matriz_tabuleiro, tamanho_tabuleiro) or 
                self.verificar_diagonal(matriz_tabuleiro, tamanho_tabuleiro))

    def verificar_vertical(self, matriz_tabuleiro, tamanho_tabuleiro):
        pass

    def verificar_horizontal(self, matriz_tabuleiro, tamanho_tabuleiro):
        pass

    def verificar_diagonal(self, matriz_tabuleiro, tamanho_tabuleiro):
        pass

#Entidade Objetivo Ascendete, herda a entidade Objetivo e implementa a lógica de verificação para sequências numéricas ascendentes
class ObjetivoAscendente(Objetivo):
    def __str__(self):
        return f"Ascendente"
    
    def __repr__(self) -> str:
        return f'Objetivo Ascendente'

    def verificar_vertical(self, matriz_tabuleiro, tamanho_tabuleiro):
        for coluna in range(tamanho_tabuleiro):
            valor_referencia = matriz_tabuleiro[0][coluna]
            for linha in range(1, tamanho_tabuleiro):
                if matriz_tabuleiro[linha][coluna] != valor_referencia + linha:
                    break
            else:
                return True
        return False

    def verificar_horizontal(self, matriz_tabuleiro, tamanho_tabuleiro):
        for linha in range(tamanho_tabuleiro):
            valor_referencia = matriz_tabuleiro[linha][0]
            for coluna in range(1, tamanho_tabuleiro):
                if matriz_tabuleiro[linha][coluna] != valor_referencia + coluna:
                    break
            else:
                return True
        return False

    def verificar_diagonal(self, matriz_tabuleiro, tamanho_tabuleiro):
        valor_referencia = matriz_tabuleiro[0][0]
        for i in range(1, tamanho_tabuleiro):
            if matriz_tabuleiro[i][i] != valor_referencia + i:
                return False
        return True

#Entidade que herda a entidade Objetivo e implementa a lógica de verificação para sequências numéricas descendentes
class ObjetivoDescendente(Objetivo):
    def __str__(self):
        return f"Descendente"
    
    def __repr__(self) -> str:
        return f'Objetivo Descendente'
        
    def verificar_vertical(self, matriz_tabuleiro, tamanho_tabuleiro):
        for coluna in range(tamanho_tabuleiro):
            valor_referencia = matriz_tabuleiro[0][coluna]
            for linha in range(1, tamanho_tabuleiro):
                if matriz_tabuleiro[linha][coluna] != valor_referencia - linha:
                    break
            else:
                return True
        return False

    def verificar_horizontal(self, matriz_tabuleiro, tamanho_tabuleiro):
        for linha in range(tamanho_tabuleiro):
            valor_referencia = matriz_tabuleiro[linha][0]
            for coluna in range(1, tamanho_tabuleiro):
                if matriz_tabuleiro[linha][coluna] != valor_referencia - coluna:
                    break
            else:
                return True
        return False

    def verificar_diagonal(self, matriz_tabuleiro, tamanho_tabuleiro):
        valor_referencia = matriz_tabuleiro[0][0]
        for i in range(1, tamanho_tabuleiro):
            if matriz_tabuleiro[i][i] != valor_referencia - i:
                return False
        return True

class ObjetivoPares(Objetivo):
    def __str__(self):
        return f"Pares"
    
    def __repr__(self) -> str:
        return f'Objetivo Pares'

    def verificar_vertical(self, matriz_tabuleiro, tamanho_tabuleiro):
        for coluna in range(tamanho_tabuleiro):
            if matriz_tabuleiro[0][coluna] % 2 == 0:
                valor_referencia = matriz_tabuleiro[0][coluna]
                for linha in range(1, tamanho_tabuleiro):
                    if matriz_tabuleiro[linha][coluna] != valor_referencia + linha + 1:
                        break
                else:
                    return True
        return False

    def verificar_horizontal(self, matriz_tabuleiro, tamanho_tabuleiro):
        for linha in range(tamanho_tabuleiro):
            valor_referencia = matriz_tabuleiro[linha][0]
            for coluna in range(1, tamanho_tabuleiro):
                if matriz_tabuleiro[linha][coluna] != valor_referencia + coluna:
                    break
            else:
                return True
        return False

    def verificar_diagonal(self, matriz_tabuleiro, tamanho_tabuleiro):
        valor_referencia = matriz_tabuleiro[0][0]
        for i in range(1, tamanho_tabuleiro):
            if matriz_tabuleiro[i][i] != valor_referencia + i:
                return False
        return True

class ObjetivoPares(Objetivo):
    def __str__(self):
        return f"Pares"
    
    def __repr__(self) -> str:
        return f'Objetivo Pares'

    def verificar_vertical(self, matriz_tabuleiro, tamanho_tabuleiro):
        for coluna in range(tamanho_tabuleiro):
            if matriz_tabuleiro[0][coluna] % 2 == 0:
                valor_referencia = matriz_tabuleiro[0][coluna]
                for linha in range(1, tamanho_tabuleiro):
                    if matriz_tabuleiro[linha][coluna] != valor_referencia + 2*linha :
                        break
                else:
                    return True
        return False

    def verificar_horizontal(self, matriz_tabuleiro, tamanho_tabuleiro):
        for linha in range(tamanho_tabuleiro):
            if matriz_tabuleiro[linha][0] % 2 == 0:
                valor_referencia = matriz_tabuleiro[linha][0]
                for coluna in range(1, tamanho_tabuleiro):
                    if matriz_tabuleiro[linha][coluna] != valor_referencia + 2*coluna:
                        break
                else:
                    return True
        return False

    def verificar_diagonal(self, matriz_tabuleiro, tamanho_tabuleiro):
        valor_referencia = matriz_tabuleiro[0][0]
        if valor_referencia % 2 != 0:
            return False
        for i in range(1, tamanho_tabuleiro):
            if matriz_tabuleiro[i][i] % 2 != 0 or matriz_tabuleiro[i][i] != valor_referencia + 2*i:
                return False
        return True

class ObjetivoImpar(Objetivo):
    def __str__(self):
        return f"Impar"
    
    def __repr__(self) -> str:
        return f'Objetivo Impar'

    def verificar_vertical(self, matriz_tabuleiro, tamanho_tabuleiro):
        for coluna in range(tamanho_tabuleiro):
            if matriz_tabuleiro[0][coluna] % 2 == 1:
                valor_referencia = matriz_tabuleiro[0][coluna]
                for linha in range(1, tamanho_tabuleiro):
                    if matriz_tabuleiro[linha][coluna] != valor_referencia + 2*linha :
                        break
                else:
                    return True
        return False

    def verificar_horizontal(self, matriz_tabuleiro, tamanho_tabuleiro):
        for linha in range(tamanho_tabuleiro):
            if matriz_tabuleiro[linha][0] % 2 == 1:
                valor_referencia = matriz_tabuleiro[linha][0]
                for coluna in range(1, tamanho_tabuleiro):
                    if matriz_tabuleiro[linha][coluna] != valor_referencia + 2*coluna:
                        break
                else:
                    return True
        return False

    def verificar_diagonal(self, matriz_tabuleiro, tamanho_tabuleiro):
        valor_referencia = matriz_tabuleiro[0][0]
        if valor_referencia % 2 != 1:
            return False
        for i in range(1, tamanho_tabuleiro):
            if matriz_tabuleiro[i][i] % 2 != 1 or matriz_tabuleiro[i][i] != valor_referencia + 2*i:
                return False
        return True

class Tabuleiro:
    def __init__(self, tamanho:int):
        self.tamanho = tamanho
        self.numeros_disponiveis = list(range(1,tamanho**2 + 1))
        self.matriz_visual = [[" " for _ in range(tamanho)] for _ in range(tamanho)] # Criação de uma matriz NxN preenchida por strings vazias
        self.matriz_numerica = [[-1 for _ in range(tamanho)] for _ in range(tamanho)] # Criação de uma matriz NxN preenchida por -1
    
    def mostrar_tabuleiro(self):
        numeros_horizontais = " ".join([f"{i + 1:^7}" for i in range(self.tamanho)])
        print(f'\t     {numeros_horizontais}')
        linha_horizontal = "+" + '-'*(8 * self.tamanho -1) + "+"
        
        print(f"\t    {linha_horizontal}")
        for i in range(self.tamanho):
            linha = f" {i + 1}  |"
            for j in range(self.tamanho):
                linha += f"{'':>2}{self.matriz_visual[i][j]:^3}{'':>2}" + "|"
            print(f'\t{linha}')
            print(f"\t    {linha_horizontal}")
    
    def atualizar_tabuleiro(self, posicao, numero, cor):
        linha, coluna = posicao[0] - 1, posicao[1] - 1
        # Adiciona o numero passado na matriz numérica
        self.matriz_numerica[linha][coluna] = numero
        # Adiciona o numero passado em forma de string colorida para a matriz visual de acordo com a quantidade de dígitos
        self.matriz_visual[linha][coluna] = f'{"" if numero > 9 else " "}{CORES[cor]}{numero}{RESET} '
        # Remove numero passado dos numeros disponíveis no tabuleiro
        self.numeros_disponiveis.remove(numero)
    
    def limpar_linha(self, indice):
        for coluna in range(self.tamanho):
            numero_removida = self.matriz_numerica[indice][coluna]
            self.matriz_numerica[indice][coluna] = -1
            self.matriz_visual[indice][coluna] = ' '   
            if numero_removida != -1:
                self.numeros_disponiveis.append(numero_removida)

    def limpar_coluna(self, indice):
        for linha in range(self.tamanho):
            numero_removida = self.matriz_numerica[linha][indice]
            self.matriz_numerica[linha][indice] = -1
            self.matriz_visual[linha][indice] = ' '   
            if numero_removida != -1:
                self.numeros_disponiveis.append(numero_removida)

        
# Entidade que manipula informações sobre uma única partida
class Partida:

    # Exibe informações úteis sobre a partida ao imprimir o respectivo objeto
    def __str__(self):
        return f"{self.jogadores[0].nome} vs {self.jogadores[1].nome}"
     
    # Contrói o objeto partida com informações passadas posteriormente
    def __init__(self, tabuleiro:Tabuleiro):
            self.tabuleiro = tabuleiro
            self.jogadores = (None, None)
            self.terminou = False
            self.jogador_atual = 0 

    # Inicializa o looping de jogo até que as condições de vitória ou empate sejam concluídas.
    def iniciar_partida(self):
        while not self.terminou:
            # Começa o turno do jogador
            jogador = self.jogadores[self.jogador_atual]
            jogada_valida = False

            while not jogada_valida:
                try:
                    self.tabuleiro.mostrar_tabuleiro()
                    print(f'Turno de {CORES[jogador.cor]}{jogador.nome}{RESET}')
                    if jogador.especiais:
                        resposta = input("Utilizar Especial? [s/n] | > ").strip()
                        if resposta == 's':
                            area_de_acao = self.pegar_area_especial()
                            jogador.usar_especial()
                            limpar_terminal()
                            print(f"{CORES[jogador.cor]}{jogador.nome}{RESET} USOU SEU ESPECIAL EM {area_de_acao}")
                            self.tabuleiro.mostrar_tabuleiro()

                    posicao = self.pegar_posicao_jogador(jogador)
                    numero = self.pegar_numero_jogador(jogador, posicao)
                    self.tabuleiro.atualizar_tabuleiro(posicao,numero,jogador.cor)
                    GerenciadorDePartidas().salvar_partidas()

                    resultado = self.verificar_fim_de_partida()
                    # Verifica se houve retorno na verificação de fim de partida
                    if resultado:
                        self.terminou = True
                        limpar_terminal()
                        self.tabuleiro.mostrar_tabuleiro()
                        return resultado
                    
                    # Passa o turno para o próximo jogador
                    self.jogador_atual = abs(self.jogador_atual - 1)
                    jogada_valida = True
                    limpar_terminal()

                except PosicaoInvalidaException as e:
                    limpar_terminal()
                    print(e)

                except NumeroInvalidoException as e:
                    limpar_terminal()
                    print(e)

                except ValueError:
                    limpar_terminal()
                    print("[ERRO] Entrada inválida. Digite um número.")

                # Captura excessão relacionada à saída de uma partida em andamento
                except KeyboardInterrupt:
                    GerenciadorDePartidas().salvar_partidas()
                    print("FINALIZANDO PARTIDA...")
                    return

    # Verifica se houve empate ou vencedores no turno
    def verificar_fim_de_partida(self):
        jogadores_vencedores = self.verificar_vitorias()
        if jogadores_vencedores:
            # Verifica se há mais de um vencedor
            if len(jogadores_vencedores) == 2:
                vencedores = " e ".join(jogador.nome for jogador in jogadores_vencedores)
                return f"{vencedores} venceram a partida!!"    
            else:
                return f'{jogadores_vencedores[0].nome} venceu a partida!!'
        elif self.verificar_empate():
            return 'A partida empatou!!'

    # Verifica se houve vencedores
    def verificar_vitorias(self):
        jogadores_vencedores = []
        for jogador in self.jogadores:
            if jogador.objetivo.verificar_objetivo(self.tabuleiro.matriz_numerica, self.tabuleiro.tamanho):
                jogador.incrementar_pontuacao()
                jogadores_vencedores.append(jogador)
        return jogadores_vencedores

    # Verifica se todas os espaços do tabuleiro já forma ocupados 
    def verificar_empate(self):
        return all(all(celula != -1 for celula in linha) for linha in self.tabuleiro.matriz_numerica)

    def pegar_area_especial(self):
        while True:
            area = input("  Área [LN ou CN] |> ").strip()
            if len(area) != 2 or not area[1].isdigit():
                print("[ERRO] Entrada Inválida. Use 'L' seguido de um número para linha ou 'C' seguido de um número para coluna.")
            else:
                tipo_area = area[0].upper()
                indice = int(area[1]) - 1
                
                if indice in range(self.tabuleiro.tamanho): 
                    if tipo_area == 'L':
                        self.tabuleiro.limpar_linha(indice)
                        return f'LINHA {indice+1}'
                    elif tipo_area == 'C':
                        self.tabuleiro.limpar_coluna(indice)
                        return f'COLUNA {indice+1}'
                    else:
                        print("[ERRO] Entrada Inválida. Use 'L' para linha e 'C' para coluna")
                else:
                    print(f"[ERRO] Entrada Inválida. Digite um índice entre 1 e {self.tabuleiro.tamanho + 1}")

    # Recebe a posição passada pelo jogador
    def pegar_posicao_jogador(self, jogador):
        while True:
            posicao = tuple(map(int, input(f"Posição [NxN] |> ").split("x")))
            if self.eh_posicao_valida(posicao):
                return posicao
            else:
                raise PosicaoInvalidaException
    
    # Valida posição passada pelo jogador
    def eh_posicao_valida(self,posicao):
        linha, coluna = posicao
        # Verifica se posicao está no intervalo 1xN
        if 1 <= linha <= self.tabuleiro.tamanho and 1 <= coluna <= self.tabuleiro.tamanho:
            # Verifica se posicao é um espaço vazio
            if self.tabuleiro.matriz_numerica[linha-1][coluna-1] == -1:
                return True
        return False

    # Recebe o número passado pelo jogador
    def pegar_numero_jogador(self, jogador, posicao):
        while True:
            numero = int(input(f"Número em {'x'.join(map(str, posicao))} |> "))
            # Verifica se o número está entre os disponíveis no tabuleiro
            if numero in self.tabuleiro.numeros_disponiveis:
                return numero
            else:
                raise NumeroInvalidoException   

# Entidade singular responsável por gerenciar informações relacionadas aos múltiplos jogadores registrados. 
@singleton
class GerenciadorDeJogador:
    def __init__(self):
        self.jogadores = {}

    def criar_jogador(self, nome, cor):
        if nome not in self.jogadores:
            jogador = Jogador(nome, cor)
            self.jogadores[nome] = jogador
            return jogador
        else:
            print(f"Jogador com o nome '{nome}' já existe.")
            self.jogadores[nome].cor = cor
            return self.jogadores[nome]

    def carregar_jogadores(self, partidas):
        for partida in partidas:
            for jogador in partida.jogadores:
                if jogador.nome not in self.jogadores:
                    self.jogadores[jogador.nome] = jogador
                else:
                    self.atualizar_pontuacao(jogador.nome, jogador.pontuacao)

    def obter_jogadores(self):
        return list(self.jogadores.values())

    def atualizar_pontuacao(self, nome, pontuacao):
        if nome in self.jogadores:
            self.jogadores[nome].pontuacao = pontuacao

    def mostrar_ranking(self):
        jogadores_ordenados = sorted(self.jogadores.values(), key=lambda jogador: jogador.pontuacao, reverse=True)
        # Mostrar o ranking no terminal
        if jogadores_ordenados:
            print("\n=== RANKING DE JOGADORES ===")
            print("{:<10} {:<10} {:<10}".format("POSIÇÃO", "NOME", "PLACAR"))
            print("=" * 28)

            for i, jogador in enumerate(jogadores_ordenados, start=1):
                print("{:<10} {:<10} {:<10}".format(i, jogador.nome, jogador.pontuacao))

            print("=" * 28)
        else:
            print("Nenhum jogador registrado.")

# Entidade singular responsável por gerenciar informações relacionadas às múltiplas partidas registradas. 
@singleton
class GerenciadorDePartidas:
    def __init__(self):
        # Armazena objetos partida
        self.partidas = []

    # Cria e configura uma partida de acordo com os parâmetros passados
    def criar_partida(self,tamanho, jogadores, modo_super = None):
        # Instancia o tabuleiro e passando-o para o objeto partida
        tabuleiro = Tabuleiro(tamanho)
        partida = Partida(tabuleiro)
        partida.jogadores = jogadores

        # Sorteia os objetivos dos jogadores de forma que cada jogador possua um objetivo diferente
        objetivos = [ObjetivoAscendente(), ObjetivoDescendente(), ObjetivoImpar(), ObjetivoPares()]
        objetivo_jogador1 = jogadores[0].sortear_objetivo(objetivos)
        objetivos.remove(objetivo_jogador1)
        jogadores[1].sortear_objetivo(objetivos)

        # Configura modo super adicionando um quantidade de especiais aos jogadores
        if modo_super:
            for jogador in jogadores:
                jogador.especiais += modo_super
        
        # Armazena, salva e retorna o objeto partida criado
        self.partidas.append(partida)
        self.salvar_partidas()
        return partida
    
    # Salva todas as partidas simultaneamente em forma de objetos
    def salvar_partidas(self):
        with open('partidas.bin', 'wb') as arquivo:
            pickle.dump(GerenciadorDePartidas().partidas, arquivo)

    # Seleciona uma partida dentre aquelas em andamento
    def selecionar_partida(self):
        while True:
            partidas_em_andamento = [partida for partida in self.partidas if not partida.terminou]
            if partidas_em_andamento:
                for i, partida in enumerate(partidas_em_andamento):
                    print(f'{i+1} {partida.jogadores[0].nome} vs {partida.jogadores[1].nome}')
                try:
                    index_partida = int(input('Partida [N] |> '))
                    # Validação de índice: 1 a len(self.partidas)
                    if 1 <= index_partida <= len(self.partidas) and not partidas_em_andamento[index_partida - 1].terminou:
                        return partidas_em_andamento[index_partida - 1]
                    else:
                        limpar_terminal()
                        print("[ERRO] Partida inválida. Digite um número dentre os listados.")
                except ValueError:
                    limpar_terminal()
                    print("[ERRO] Entrada inválida. Digite um número.")
            else:
                print("Nenhum partida foi encontrada. Comece um NOVO JOGO.")
                return None

    # Carrega partidas salvas e jogadores registrados.
    def carregar_partidas(self):
        try:
            with open('partidas.bin', 'rb') as arquivo:
                partidas_carregadas = pickle.load(arquivo)
                if partidas_carregadas:
                    GerenciadorDeJogador().carregar_jogadores(partidas_carregadas)
                self.partidas = partidas_carregadas
        except FileNotFoundError:
            print("Nenhum partida foi encontrada. Comece um NOVO JOGO.")

    # Inicializa uma partida passada
    def comecar_partida(self, partida:Partida):
        print(partida.iniciar_partida())
        self.salvar_partidas()

    def remover_partida(self, indice):
        partida_removida = self.partidas.pop(indice)
        self.salvar_partidas()
        return partida_removida.jogadores


# Limpa o terminal em tempo de execução
def limpar_terminal():
    # Verifica se o sistema operacional é Windows
    if os.name == 'nt':
        os.system('cls')
    # Se for outro sistema operacional, usa o comando 'clear'
    else:
        os.system('clear')

jogador1= GerenciadorDeJogador().criar_jogador('Pedro','azul')
jogador2= GerenciadorDeJogador().criar_jogador('João','verde')

partida1 = GerenciadorDePartidas().criar_partida(3,(jogador1,jogador2),1)
partida1.iniciar_partida()