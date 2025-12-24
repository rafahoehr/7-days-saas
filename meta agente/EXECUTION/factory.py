import os
import sys

def create_agent(agent_name, agent_goal):
    """
    Cria a estrutura DOE determinística para um novo agente.
    """
    # 1. Definir caminhos de forma robusta
    # Caminho base para DEPLOYED_AGENTS, relativo à raiz do projeto (um nível acima de 'meta agente/EXECUTION')
    project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
    base_path = os.path.join(project_root, 'DEPLOYED_AGENTS', agent_name)

    dirs_to_create = [
        os.path.join(base_path, 'directives'),
        os.path.join(base_path, 'execution')
    ]
    print(f"🛠️ Iniciando construção da fábrica para: {agent_name}...")

    # 2. Criar Pastas (Determinístico)
    for directory in dirs_to_create:
        os.makedirs(directory, exist_ok=True)
        print(f" -> Pasta criada: {directory}")

    # 3. Carregar Templates de forma robusta
    # O caminho para a pasta TEMPLATES é relativo à localização deste script
    script_dir = os.path.dirname(os.path.abspath(__file__))
    templates_path = os.path.abspath(os.path.join(script_dir, '..', 'TEMPLATES'))

    try:
        directive_template_path = os.path.join(templates_path, 'child_directive.md')
        script_template_path = os.path.join(templates_path, 'child_script.py')

        with open(directive_template_path, "r", encoding="utf-8") as f:
            directive_template = f.read()
        with open(script_template_path, "r", encoding="utf-8") as f:
            script_template = f.read()
    except FileNotFoundError:
        print(f"❌ Erro: Templates não encontrados no caminho esperado: {templates_path}")
        sys.exit(1)

    # 4. Injetar Variáveis (O "DNA" do Agente)
    directive_content = directive_template.replace("{{AGENT_NAME}}", agent_name)\
        .replace("{{AGENT_GOAL}}", agent_goal)
    script_content = script_template.replace("{{AGENT_GOAL}}", agent_goal)

    # 5. Escrever Arquivos Finais
    sop_path = os.path.join(base_path, 'directives', 'SOP.md')
    main_py_path = os.path.join(base_path, 'execution', 'main.py')

    with open(sop_path, "w", encoding="utf-8") as f:
        f.write(directive_content)
    with open(main_py_path, "w", encoding="utf-8") as f:
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
