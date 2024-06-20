class NumeroInvalidoException(Exception):
    def __str__(self):
        return f'[ERRO] Número Indisponível. Digite um número no intervalo 1xN^2'

class PosicaoInvalidaException(Exception):
    def __str__(self):
        return f'[ERRO] Posição Inválida. Digite uma posição dentro do limite NxN' 
