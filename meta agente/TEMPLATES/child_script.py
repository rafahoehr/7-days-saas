import os
import sys
import traceback

# Este é o script semente (Seed Script).
# O Agente (Orquestrador) deve evoluir este código conforme necessário.

def execute_task():
    print("--- INICIANDO TAREFA: {{AGENT_GOAL}} ---")

    # [A IA PREENCHERÁ A LÓgica ESPECÍFICA AQUI]
    # Exemplo: requests.get('...')

    # Simulação de lógica placeholder
    # Remova ou substitua isso na primeira execução real
    pass

if __name__ == "__main__":
    try:
        execute_task()
        print("--- SUCESSO ---")
    except Exception as e:
        # O BLOCO DE AUTO-TÊMPERA
        # Isso garante que o erro seja visível para o Agente corrigir
        print("\n!!! FALHA CRÍTICA DETECTADA !!!")
        print(f"Erro: {str(e)}")
        print("Traceback completo para análise:")
        traceback.print_exc()
        # Código de saída 1 avisa o orquestrador que algo quebrou
        sys.exit(1)
