import os
import sys

def create_agent(agent_name, agent_goal):
    """
    Cria a estrutura DOE determinística para um novo agente.
    """
    # 1. Definir caminhos
    base_path = f"DEPLOYED_AGENTS/{agent_name}"
    dirs_to_create = [
        f"{base_path}/directives",
        f"{base_path}/execution"
    ]
    print(f"🛠️ Iniciando construção da fábrica para: {agent_name}...")

    # 2. Criar Pastas (Determinístico)
    for directory in dirs_to_create:
        os.makedirs(directory, exist_ok=True)
        print(f" -> Pasta criada: {directory}")

    # 3. Carregar Templates
    # Paths are relative to the project root, where this script is expected to be run from.
    template_base_path = "meta agente/TEMPLATES"
    try:
        with open(f"{template_base_path}/child_directive.md", "r", encoding="utf-8") as f:
            directive_template = f.read()
        with open(f"{template_base_path}/child_script.py", "r", encoding="utf-8") as f:
            script_template = f.read()
    except FileNotFoundError:
        print(f"❌ Erro: Templates não encontrados. Verifique a pasta /{template_base_path}.")
        sys.exit(1)

    # 4. Injetar Variáveis (O "DNA" do Agente)
    directive_content = directive_template.replace("{{AGENT_NAME}}", agent_name)\
        .replace("{{AGENT_GOAL}}", agent_goal)
    script_content = script_template.replace("{{AGENT_GOAL}}", agent_goal)

    # 5. Escrever Arquivos Finais
    with open(f"{base_path}/directives/SOP.md", "w", encoding="utf-8") as f:
        f.write(directive_content)
    with open(f"{base_path}/execution/main.py", "w", encoding="utf-8") as f:
        f.write(script_content)

    print(f"✅ Agente {agent_name} implantado com sucesso!")
    print(f"📍 Local: {base_path}")

if __name__ == "__main__":
    # Exemplo de uso via linha de comando
    # Uso: python "meta agente/EXECUTION/factory.py" "NomeDoAgente" "Objetivo do Agente"
    if len(sys.argv) < 3:
        print("Uso: python factory.py <Nome> <Objetivo>")
    else:
        create_agent(sys.argv[1], sys.argv[2])
