import simpy
import random
import matplotlib.pyplot as plt

# Constantes
INTERVALO_LEITURA = 5  # Intervalo de leitura em segundos
NUM_COMPORTAS = 19     # Número de comportas
TAXA_SUCESSO = 0.9     # Taxa de sucesso para funcionamento das comportas
NUM_EXECUCOES = 10     # Número de execuções

TEMPOS_PLOT = []
PROFUNDIDADES_PLOT = []
ACOES = []

def leitor_profundidade():
    """Lê a profundidade do rio."""
    return round(random.uniform(2.5, 3.0), 2)

def central(env, profundidade):
    """Central que recebe a profundidade e envia ordem de fechamento se necessário."""
    if profundidade >= 2.7:
        print(f'Profundidade do rio: {profundidade}m. Enviando ordem de fechamento para as comportas.')
        ACOES.append((env.now, profundidade, "enchente"))
        yield env.process(gerenciar_comportas(env, profundidade))
    else:
        print(f'Profundidade do rio: {profundidade}m. Nível seguro, sem ação necessária.')
        ACOES.append((env.now, profundidade, "nivel-seguro"))
        yield env.timeout(0)

def gerenciar_comportas(env, profundidade):
    """Gerencia as comportas, fechando-as e verificando falhas."""
    for i in range(NUM_COMPORTAS):
        sucesso = random.random() < TAXA_SUCESSO
        if not sucesso:
            print(f'Comporta {i + 1} falhou ao fechar. Notificando manutenção.')
            ACOES.append((env.now, profundidade, f"falha-comporta-{i + 1}"))
            yield env.process(manutencao(env, i + 1, profundidade))
        else:
            ACOES.append((env.now, profundidade, f"comporta-{i + 1}-fechada"))
            print(f'Comporta {i + 1} fechada com sucesso.')
        yield env.timeout(0)

def manutencao(env, comporta_id, profundidade):
    """Simula a manutenção e correção de uma comporta."""
    print(f'Iniciando manutenção da comporta {comporta_id}.')
    ACOES.append((env.now, profundidade, f"manutencao-comporta-{comporta_id}"))
    yield env.timeout(1)
    print(f'Manutenção da comporta {comporta_id} concluída. Comporta funcionando corretamente.')

def simular(env):
    """Função principal da simulação."""
    for _ in range(NUM_EXECUCOES):
        print(f'Execução - #{int(_)+1}')
        profundidade = leitor_profundidade()
        TEMPOS_PLOT.append(env.now)
        PROFUNDIDADES_PLOT.append(profundidade)
        yield env.process(central(env, profundidade))
        yield env.timeout(INTERVALO_LEITURA)

# Criação do ambiente de simulação
env = simpy.Environment()

# Inicialização da simulação
env.process(simular(env))

# Execução da simulação
env.run()

# Plotagem do gráfico de nível do rio
plt.figure(figsize=(10, 5))
plt.plot(TEMPOS_PLOT, PROFUNDIDADES_PLOT, marker='o', linestyle='-')
plt.axhline(y=2.7, color='r', linestyle='--', label='Nível de Ação (2.7m)')
plt.xlabel('Tempo (s)')
plt.ylabel('Profundidade do Rio (m)')
plt.title('Nível do Rio ao Longo do Tempo')
plt.ylim(2.5, 4.0)
plt.legend()
plt.grid(True)
plt.show()

# Plotagem do gráfico de comportamento das comportas
fig, ax = plt.subplots(figsize=(10, 5))

# Lista para rastrear ações já adicionadas à legenda
acoes_adicionadas = set()

for tempo, profundidade, acao in ACOES:
    if "comporta-" in acao and "fechada" in acao:
        if 'Comporta Fechada' not in acoes_adicionadas:
            ax.scatter(tempo, profundidade, color='green', label='Comporta Fechada', marker='o')
            acoes_adicionadas.add('Comporta Fechada')
        else:
            ax.scatter(tempo, profundidade, color='green', marker='o')
    elif "falha-comporta-" in acao:
        if 'Falha da Comporta' not in acoes_adicionadas:
            ax.scatter(tempo, profundidade, color='red', label='Falha da Comporta', marker='x')
            acoes_adicionadas.add('Falha da Comporta')
        else:
            ax.scatter(tempo, profundidade, color='red', marker='x')
    elif "manutencao-comporta-" in acao:
        if 'Manutenção da Comporta' not in acoes_adicionadas:
            ax.scatter(tempo, profundidade, color='blue', label='Manutenção da Comporta', marker='s')
            acoes_adicionadas.add('Manutenção da Comporta')
        else:
            ax.scatter(tempo, profundidade, color='blue', marker='s')

# Adiciona as legendas para os eventos
handles, labels = ax.get_legend_handles_labels()
by_label = dict(zip(labels, handles))
ax.legend(by_label.values(), by_label.keys())

ax.set_xlabel('Tempo (s)')
ax.set_ylabel('Profundidade do Rio (m)')
ax.set_title('Comportamento das Comportas ao Longo do Tempo')
ax.set_ylim(2.5, 4.0)
ax.grid(True)

plt.show()
