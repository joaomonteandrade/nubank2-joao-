import threading
import random
import time

# Classe Conta
class Conta:
    def __init__(self, id_conta, saldo_inicial):
        self.id_conta = id_conta
        self.saldo = saldo_inicial
        self.lock = threading.Lock()  # Mutex para garantir que apenas uma thread modifique o saldo de cada vez

    def __repr__(self):
        return f"Conta {self.id_conta} - Saldo: {self.saldo}"

# Classe TransacaoBancaria
class TransacaoBancaria:
    def __init__(self):
        self.log = []

    def registrar_log(self, msg):
        """Registra transações no log"""
        self.log.append(msg)

    def transferir(self, conta_origem, conta_destino, valor):
        """Realiza a transferência de valor entre duas contas com verificação de saldo"""
        # Ordena as contas para evitar deadlock
        primeira_conta, segunda_conta = (conta_origem, conta_destino) if conta_origem.id_conta < conta_destino.id_conta else (conta_destino, conta_origem)

        # Aquisição dos locks na ordem correta para evitar deadlocks
        with primeira_conta.lock:
            with segunda_conta.lock:
                if conta_origem.saldo >= valor:
                    # Transferência realizada
                    conta_origem.saldo -= valor
                    conta_destino.saldo += valor

                    # Log da operação
                    self.registrar_log(f"Transferido {valor} de Conta {conta_origem.id_conta} para Conta {conta_destino.id_conta}. "
                                        f"Saldo final: Conta {conta_origem.id_conta}: {conta_origem.saldo}, "
                                        f"Conta {conta_destino.id_conta}: {conta_destino.saldo}.")
                    return True
                else:
                    # Saldo insuficiente
                    self.registrar_log(f"Falha na transferência de {valor} de Conta {conta_origem.id_conta} para Conta {conta_destino.id_conta}. "
                                        f"Saldo insuficiente. Saldo de Conta {conta_origem.id_conta}: {conta_origem.saldo}.")
                    return False

    def exibir_log(self):
        """Exibe o log de todas as transações realizadas"""
        for linha in self.log:
            print(linha)

# Funções para executar os cenários de teste

def cenário_1_transferencias_simples():
    # Cenário 1: Transferências Simples
    print("\nCenário 1: Transferências Simples")

    contas = [Conta(i, saldo) for i, saldo in enumerate([100, 200, 300], 1)]
    transacao = TransacaoBancaria()

    # Realizar uma transferência simples de Conta 1 para Conta 2
    print(f"Antes da transferência: {contas[0]}, {contas[1]}")
    transacao.transferir(contas[0], contas[1], 50)
    print(f"Após a transferência: {contas[0]}, {contas[1]}")

    # Log das transações
    transacao.exibir_log()

def cenário_2_alta_concorrencia():
    # Cenário 2: Alta Concorrência
    print("\nCenário 2: Alta Concorrência")

    contas = [Conta(i, random.randint(100, 500)) for i in range(1, 101)]
    transacao = TransacaoBancaria()

    # Simulando alta concorrência com várias threads
    num_threads = 50
    num_transferencias = 100

    threads = []
    for _ in range(num_threads):
        t = threading.Thread(target=executar_transferencias, args=(contas, transacao, num_transferencias))
        threads.append(t)
        t.start()

    # Aguardar a finalização de todas as threads
    for t in threads:
        t.join()

    # Exibir log das transações
    transacao.exibir_log()

    # Verificação de consistência do saldo
    saldo_total = sum(conta.saldo for conta in contas)
    print(f"\nSaldo total após todas as transações: {saldo_total}")

def cenário_3_transferencias_saldo_insuficiente():
    # Cenário 3: Transferências com Saldo Insuficiente
    print("\nCenário 3: Transferências com Saldo Insuficiente")

    contas = [Conta(i, saldo) for i, saldo in enumerate([100, 200, 300], 1)]
    transacao = TransacaoBancaria()

    # Tentativa de transferência com saldo insuficiente
    print(f"Antes da tentativa: {contas[0]}, {contas[1]}")
    transacao.transferir(contas[0], contas[1], 150)  # Saldo insuficiente para Conta 1
    print(f"Após a tentativa: {contas[0]}, {contas[1]}")

    # Log das transações
    transacao.exibir_log()

# Função para executar transferências com várias threads (usada nos cenários de alta concorrência)
def executar_transferencias(contas, transacao, num_transferencias):
    for _ in range(num_transferencias):
        conta_origem = random.choice(contas)
        conta_destino = random.choice(contas)
        while conta_origem == conta_destino:
            conta_destino = random.choice(contas)
        valor = random.randint(1, 100)
        transacao.transferir(conta_origem, conta_destino, valor)
        time.sleep(random.uniform(0.1, 0.5))  # Simula uma pequena latência entre as operações

# Função principal para rodar os cenários de teste
def executar_testes():
    cenário_1_transferencias_simples()
    cenário_2_alta_concorrencia()
    cenário_3_transferencias_saldo_insuficiente()

# Execução dos testes
if __name__ == "__main__":
    executar_testes()
