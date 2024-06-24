import simpy
import random
import matplotlib.pyplot as plt

# Constantes
INTERVALO_LEITURA = 5  # Intervalo de leitura em segundos
NUM_COMPORTAS = 19     # Número de comportas
TAXA_SUCESSO = 0.9     # Taxa de sucesso para funcionamento das comportas
NUM_EXECUCOES = 10     # Número de execuções

# Determina níveis de fechamento para cada comporta e exibe esses
NIVEIS_FECHAMENTO = [2.5 + i * 0.05 for i in range(NUM_COMPORTAS)]  # Exemplo de níveis progressivos
print(NIVEIS_FECHAMENTO)

# Profundidade inicial do rio
PROFUNDIDADE_INICIAL = 2.7

# Para construir visualizacao
tempos = []
profundidades = []
acoes = []
estados_comportas = ["Aberta"] * NUM_COMPORTAS

def leitor_profundidade():
    """Lê a profundidade do rio."""
    return round(random.uniform(2.5, 3.0), 2)

def central(env, profundidade):
    """Central que recebe a profundidade e envia ordem de fechamento/abertura se necessário."""
    print(f'Profundidade {profundidade}.')
    for i in range(NUM_COMPORTAS):
        if profundidade >= NIVEIS_FECHAMENTO[i] and estados_comportas[i] == "Aberta":
            print(f'Enviando ordem de fechamento para a comporta {i + 1}.')
            acoes.append((env.now, profundidade, f'Fechamento Comporta {i + 1}'))
            yield env.process(gerenciar_comporta(env, i + 1, 'fechar'))
        elif profundidade < NIVEIS_FECHAMENTO[i] and estados_comportas[i] == "Fechada":
            print(f'Enviando ordem de abertura para a comporta {i + 1}.')
            acoes.append((env.now, profundidade, f'Abertura Comporta {i + 1}'))
            yield env.process(gerenciar_comporta(env, i + 1, 'abrir'))

def gerenciar_comporta(env, comporta_id, acao):
    """Gerencia uma comporta específica, fechando-a, abrindo-a e verificando falhas."""
    sucesso = random.random() < TAXA_SUCESSO
    if acao == 'fechar' and sucesso:
        print(f'Comporta {comporta_id} fechada com sucesso.')
        estados_comportas[comporta_id - 1] = "Fechada"
    elif acao == 'abrir' and sucesso:
        print(f'Comporta {comporta_id} aberta com sucesso.')
        estados_comportas[comporta_id - 1] = "Aberta"
    else:
        print(f'Comporta {comporta_id} falhou ao {acao}. Notificando manutenção.')
        acoes.append((env.now, PROFUNDIDADE_INICIAL, f'Manutenção Comporta {comporta_id}'))
        yield env.process(manutencao(env, comporta_id))
    yield env.timeout(0)  # Adicionado para garantir que seja um gerador

def manutencao(env, comporta_id):
    """Simula a manutenção e correção de uma comporta."""
    print(f'Iniciando manutenção da comporta {comporta_id}.')
    yield env.timeout(5)  # Simula o tempo de manutenção
    print(f'Manutenção da comporta {comporta_id} concluída. Comporta funcionando corretamente.')
    estados_comportas[comporta_id - 1] = "Aberta"  # Atualiza o estado da comporta após a manutenção

def simular(env):
    """Função principal da simulação."""
    profundidade = PROFUNDIDADE_INICIAL
    for i in range(NUM_EXECUCOES):
        print(f'Execução - #{i + 1}')
        tempos.append(env.now)
        profundidades.append(profundidade)
        yield env.process(central(env, profundidade))
        profundidade = leitor_profundidade()
        yield env.timeout(INTERVALO_LEITURA)

# Criação do ambiente de simulação
env = simpy.Environment()

# Inicialização da simulação
env.process(simular(env))

# Execução da simulação
env.run()

# Visualização da simulação
fig, ax = plt.subplots()
ax.plot(tempos, profundidades, label='Profundidade do Rio')

# Marcadores únicos para a legenda
fechamento_marcado = False
abertura_marcado = False
manutencao_marcado = False

# Marcar as ações tomadas
for tempo, profundidade, acao in acoes:
    if 'Fechamento' in acao and not fechamento_marcado:
        ax.axvline(x=tempo, color='r', linestyle='--', label='Fechamento Comporta')
        fechamento_marcado = True
    elif 'Fechamento' in acao:
        ax.axvline(x=tempo, color='r', linestyle='--')
    elif 'Abertura' in acao and not abertura_marcado:
        ax.axvline(x=tempo, color='b', linestyle='--', label='Abertura Comporta')
        abertura_marcado = True
    elif 'Abertura' in acao:
        ax.axvline(x=tempo, color='b', linestyle='--')
    elif 'Manutenção' in acao and not manutencao_marcado:
        ax.scatter(tempo, NIVEIS_FECHAMENTO[int(acao.split()[-1]) - 1], color='orange', marker='s', label='Manutenção Comporta')
        manutencao_marcado = True
    elif 'Manutenção' in acao:
        ax.scatter(tempo, NIVEIS_FECHAMENTO[int(acao.split()[-1]) - 1], color='orange', marker='s')

# Exibir níveis de fechamento das comportas
for i, nivel in enumerate(NIVEIS_FECHAMENTO):
    ax.axhline(y=nivel, color='gray', linestyle='--', label=f'Comportas ' if i == 0 else "")

ax.set_xlabel('Tempo (s)')
ax.set_ylabel('Profundidade do Rio (m)')
ax.set_title('Simulação de Contingenciamento de Cheias de Rios')
ax.legend()
ax.grid(True)

# Plota o gráfico
plt.show()
