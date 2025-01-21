class transferencia:
    def _init_(self):
        self.log = []

        self.lock = Lock() # os poggers vão resolver dps

        self.transaction_id = 0

        print('Transações inicializando...')

    def transferir(conta_origem, conta_destino, valor):
        menor_id = 0
        if conta_origem.getID() < conta_destino.getID():
            menor_id = conta_origem.getID()
        else:
            menor_id = conta_destino.getID()
    

maria = conta(1, 500)
print(maria.getSaldo())

#teste deposito
maria.depositar(10.5)
print(maria.getSaldo())

#teste retira
maria.sacar(499)
print(maria.getSaldo())

#teste retirar negativo
maria.sacar(499)
print(maria.getSaldo())