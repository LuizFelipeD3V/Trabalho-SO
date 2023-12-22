import random

def main(): 
    processos = []    #Lista de processos
    num_processos = int(input("Número de processos: "))
    escolha = input("Será aleatório? (1=SIM/2=NAO): ").lower()    # Questiona se será aleatório
    if escolha == "1": # Preenche automaticamente os campos do processo
                processos = criar_processos_aleatorios(num_processos)
                for processo in processos:
                    print(processo)
                    
    elif escolha == "2":    # Solicita detalhes do processo
                processos = criar_processos_manualmente(num_processos) 
                for processo in processos:
                    print(processo)
                     
    else:   # Não reconhece a opção e parte para o menu afim de dar a opção de popular os processos
            print("Opção não reconhecida. Por favor insira uma opção válida")

    while True: # Opções do menu interativo de opções
        print("\nEscolha o algoritmo:")
        print("1=FCFS")
        print("2=SJF Preemptivo")
        print("3=SJF Não Preemptivo ")
        print("4=Prioridade Preemptivo ")
        print("5=Prioridade Não Preemptivo")
        print("6=Mostra lista de processos")
        print("7=Popular processos novamente")
        print("0=Sair")
        escolha = input("Escolha: ")

        if escolha == "1":      # Seleciona o algoritimo FCFS
            if not processos:   # Identifica se há processos na lista
                print("\nNão há processos na lista. Adicione ou gere processos.")
            else:
                historico = fcfs(processos)
                imprimir_historico(historico, processos)

        elif escolha == "2":    # Seleciona o algoritimo SJF Preemptivo
            if not processos:   
                print("\nNão há processos na lista. Adicione ou gere processos.")
            else:
                historico = sjf_preemptivo(processos)
                imprimir_historico(historico, processos)

        elif escolha == "3":    # Seleciona o algoritimo SJF Não Preemptivo
            if not processos:  
                print("\nNão há processos na lista. Adicione ou gere processos.")
            else:
                historico = sjf_nao_preemptivo(processos)
                imprimir_historico(historico, processos)

        elif escolha == "4":    # Seleciona o algoritimo Prioridade Preemptivo
            if not processos:  
                print("\nNão há processos na lista. Adicione ou gere processos.")
            else:
                historico, tempo_medio_espera = prioridade_preemptivo(processos)
                imprimir_historico(historico, processos)
                print(f"Tempo médio de espera: {tempo_medio_espera:.2f}")

        elif escolha == "5":    # Seleciona o algoritimo Prioridade Não Preemptivo
            if not processos:
                print("Não há processos na lista. Adicione ou gere processos primeiro.")
            else:
                historico = prioridade_nao_preemptivo(processos)
                imprimir_historico(historico, processos)

        elif escolha == "6":    # Apresenta a lista de processos
            if not processos: 
                print("\nNão há processos na lista. Adicione ou gere processos.")
            else:
                for processo in processos:
                    print(processo)

        elif escolha == "7":    # Apresenta novamente o formulário de preenchimento de processos
            num_processos = int(input("Número de processos: "))    # Questiona se será aleatório
            escolha = input("Será aleatório? (1=SIM/2=NAO): ").lower()
            if escolha == "1": # Preenche automaticamente os campos do processo
                    processos = criar_processos_aleatorios(num_processos)
                    for processo in processos:
                        print(processo)
            elif escolha == "2":    # Solicita detalhes do processo
                        processos = criar_processos_manualmente(num_processos) 
                        for processo in processos:
                            print(processo)
                            
            else:   # Não reconhece a opção e parte para o menu afim de dar a opção de popular os processos
                    print("\nOpção não reconhecida. Últimos processos populados foram repostos.")

        elif escolha == "0":
            break
        else:
            print("Opção inválida ou não implementada ainda.")

class Processo: # Classe processo que irá administrar cada processo populado
    def __init__(self, id, tempo_execucao, tempo_chegada, prioridade):
        self.id = id
        self.tempo_execucao = tempo_execucao
        self.tempo_restante = tempo_execucao
        self.tempo_chegada = tempo_chegada
        self.prioridade = prioridade
        self.tempo_inicio = None
        self.tempo_espera = 0

    def __str__(self):
        return f"Processo[{self.id}]: tempo_execucao={self.tempo_execucao}, tempo_restante={self.tempo_restante}, tempo_chegada={self.tempo_chegada}, prioridade={self.prioridade}"

def fcfs(processos):    # Começa o tempo atual e o histórico
    tempo_atual = 0
    historico = []

    for processo in processos:    # Itera entre processos
        if tempo_atual < processo.tempo_chegada:    # Verifica o tempo atual para ver se é menor que o tempo de chegada           
            tempo_atual = processo.tempo_chegada    # Se o tempo atual é menor que o tempo de chegada, avança o tempo atual.
        
        processo.tempo_inicio = tempo_atual # Define o tempo de início e tempo de espera do processo
        processo.tempo_espera = tempo_atual - processo.tempo_chegada
       
        while processo.tempo_restante > 0:  # Executa o processo se houver tempo restante           
            historico.append((tempo_atual, processo.id, processo.tempo_restante))   # Registra o tempo no histórico, decrementa o tempo restante e avança o tempo atual
            processo.tempo_restante -= 1
            tempo_atual += 1

    historico_corrigido = [(t + 1, pid, trest - 1) for t, pid, trest in historico if trest > 0] # Garantia que o tempo comece em 1 na impressão do histórico.
    return historico_corrigido

def sjf_preemptivo(processos):
    tempo_atual = 0    # Começa o tempo atual e as listas de processos prontos e histórico
    processos_prontos = []
    historico = []

    processos_ordenados = sorted(processos, key=lambda x: x.tempo_chegada) # Ordena os processos por tempo de chegada

    for processo in processos:    # Começa os tempos de início e restante para cada processo
        processo.tempo_inicio = None
        processo.tempo_restante = processo.tempo_execucao

    while processos_ordenados or processos_prontos:    # Enquanto houver processos não concluídos ou prontos
        while processos_ordenados and processos_ordenados[0].tempo_chegada <= tempo_atual:  # Move processos que chegaram para a lista de prontos
            processo = processos_ordenados.pop(0)
            processos_prontos.append(processo)
            processos_prontos.sort(key=lambda x: x.tempo_restante)   # Ordena os processos prontos pelo tempo restante

        if processos_prontos:  # Executa o processo pronto com menor tempo restante
            processo_atual = processos_prontos[0]
            if processo_atual.tempo_inicio is None:     # Define o tempo de início se ainda não estiver definido
                processo_atual.tempo_inicio = tempo_atual

            processo_atual.tempo_restante -= 1     # Decrementa o tempo restante e registra no histórico
            historico.append((tempo_atual + 1, processo_atual.id, processo_atual.tempo_restante))

            if processo_atual.tempo_restante == 0:    # Remove o processo da lista de prontos se concluído
                processos_prontos.pop(0)
        else:
            historico.append((tempo_atual + 1, 'nenhum processo', None))     # Se nenhum processo estiver pronto, apenas avança o tempo

        tempo_atual += 1  # Avança o tempo atual

    for processo in processos:    # Calcula o tempo de espera para cada um dos processos
        if processo.tempo_inicio is not None:
            processo.tempo_espera = processo.tempo_inicio - processo.tempo_chegada
        else:
            processo.tempo_espera = 0      # Se o processo não iniciou, o tempo de espera será zero

    return historico


def sjf_nao_preemptivo(processos):
    tempo_atual = 0    # Começa o tempo atual, a lista de processos prontos e o histórico
    processos_prontos = []
    historico = []

    processos_ordenados = sorted(processos, key=lambda x: x.tempo_chegada)    # Ordena os processos por tempo de chegada

    for processo in processos:    # Começa o tempo restante e o tempo de início de cada processo
        processo.tempo_restante = processo.tempo_execucao
        processo.tempo_inicio = None

    while processos_ordenados or processos_prontos:
        while processos_ordenados and processos_ordenados[0].tempo_chegada <= tempo_atual:  # Adiciona processos que chegaram à lista de prontos
            processo = processos_ordenados.pop(0)
            processos_prontos.append(processo)
            processos_prontos.sort(key=lambda x: x.tempo_execucao)     # Ordena a lista de processos prontos pelo tempo de execução (SJF)

        if processos_prontos:
            processo_atual = processos_prontos.pop(0)     # Executa o processo com menor tempo de execução
            if processo_atual.tempo_inicio is None:
                processo_atual.tempo_inicio = tempo_atual

            while processo_atual.tempo_restante > 0:    # Executa o processo até que o tempo restante seja zero
                historico.append((tempo_atual + 1, processo_atual.id, processo_atual.tempo_restante - 1))
                processo_atual.tempo_restante -= 1
                tempo_atual += 1

            processo_atual.tempo_espera = processo_atual.tempo_inicio - processo_atual.tempo_chegada    # Calcula o tempo de espera do processo
        else:
            tempo_atual += 1    # Se não houver processos prontos, avança o tempo

    return historico

def prioridade_preemptivo(processos):
    tempo_atual = 0    # Começa o tempo atual, a fila de processos prontos e o histórico
    fila_prontos = []
    historico = []

    while any(p.tempo_restante > 0 for p in processos):    # Loop principal enquanto houver processos com tempo restante
        for processo in processos:   # Atualizar a fila de prontos com processos que chegaram
            if processo.tempo_chegada <= tempo_atual and processo.tempo_restante > 0 and processo not in fila_prontos:
                fila_prontos.append(processo)

        fila_prontos.sort(key=lambda p: (p.prioridade, p.tempo_chegada))   # Ordenar a fila de prontos pela prioridade e tempo de chegada

        if fila_prontos:
            processo_atual = fila_prontos[0]   # Executar o processo com maior prioridade

            if processo_atual.tempo_inicio is None:
                processo_atual.tempo_inicio = tempo_atual

            historico.append((tempo_atual, processo_atual.id, processo_atual.tempo_restante))
            processo_atual.tempo_restante -= 1

            if processo_atual.tempo_restante == 0:
                fila_prontos.remove(processo_atual)
        else:
            historico.append((tempo_atual, 'nenhum processo', 0))     # Nenhum processo na fila de prontos, registrar 'nenhum processo'

        tempo_atual += 1

    for processo in processos:    # Calcular o tempo de espera para cada processo
        if processo.tempo_inicio is not None:
            processo.tempo_espera = processo.tempo_inicio - processo.tempo_chegada
        else:
            processo.tempo_espera = tempo_atual - processo.tempo_chegada

    tempo_total_espera = sum(p.tempo_espera for p in processos)    # Calcular o tempo médio de espera
    tempo_medio_espera = tempo_total_espera / len(processos) if processos else 0

    historico_corrigido = [(t + 1, pid, r if r is not None else 0) for t, pid, r in historico]    # Correção para garantir que o tempo comece em 1 na impressão do histórico.
    
    return historico_corrigido, tempo_medio_espera


def prioridade_nao_preemptivo(processos):
    tempo_atual = 0 # Inicializa o tempo atual, a lista de processos prontos e o histórico
    processos_prontos = []
    historico = []
    processos_ordenados = sorted(processos, key=lambda x: x.tempo_chegada)

    for processo in processos:  # Inicializa o tempo restante e tempo de início para cada processo
        processo.tempo_restante = processo.tempo_execucao
        processo.tempo_inicio = None

    while processos_ordenados or processos_prontos:
        while processos_ordenados and processos_ordenados[0].tempo_chegada <= tempo_atual: # Adiciona processos que chegaram à lista de prontos
            processo = processos_ordenados.pop(0)
            processos_prontos.append(processo)
            processos_prontos.sort(key=lambda x: (x.prioridade, x.tempo_chegada))   # Ordena por prioridade e, em caso de empate, por tempo de chegada

        if processos_prontos:
            processo_atual = processos_prontos.pop(0)   # Executa o processo com maior prioridade
            if processo_atual.tempo_inicio is None:
                processo_atual.tempo_inicio = tempo_atual

            while processo_atual.tempo_restante > 0:
                historico.append((tempo_atual + 1, processo_atual.id, processo_atual.tempo_restante - 1))
                processo_atual.tempo_restante -= 1
                tempo_atual += 1

            processo_atual.tempo_espera = processo_atual.tempo_inicio - processo_atual.tempo_chegada# Calcula o tempo de espera do processo
        else:
            tempo_atual += 1    # Se não houver processos prontos, avança o tempo

    return historico

def imprimir_historico(historico, processos):    # Itera sobre o histórico de execução
    for tempo, processo_id, tempo_restante in historico:
        if processo_id != 'nenhum processo':
            print(f"tempo[{tempo}]: processo[{processo_id}] restante={tempo_restante}")            # Mostra informações sobre o processo em execução
        else:
            print(f"tempo[{tempo}]: nenhum processo está pronto")            # Mostra quando nenhum processo está pronto

    if processos:
        tempo_total_espera = sum(p.tempo_espera for p in processos)        # Calcula o tempo total de espera
        for p in processos:        # Itera sobre os processos para imprimir os tempos de espera individuais
            print(f"Processo[{p.id}]: tempo_espera={p.tempo_espera}")

        tempo_medio_espera = tempo_total_espera / len(processos)        # Calcula e Mostra o tempo médio de espera
        print(f"\nTempo médio de espera: {tempo_medio_espera:.1f}")
    else:
        print("\nNão há processos para calcular o tempo médio de espera.")

def criar_processos_aleatorios(num_processos):
    return [Processo(i, random.randint(1, 10), random.randint(0, 10), random.randint(1, 10)) for i in range(num_processos)]    # Cria uma lista de processos com informações aleatórias

def criar_processos_manualmente(num_processos):
    processos = []    # Gera novamente a lista de processos
    for i in range(num_processos):    # Solicita informações sobre cada processo
        print(f"Processo {i}:")
        tempo_execucao = int(input("Digite o tempo de execução: "))
        tempo_chegada = int(input("Digite o tempo de chegada: "))
        prioridade = int(input("Digite a prioridade: "))
        processos.append(Processo(i, tempo_execucao, tempo_chegada, prioridade))        # Cria um processo com base nas informações fornecidas
    return processos

if __name__ == "__main__":
    main()