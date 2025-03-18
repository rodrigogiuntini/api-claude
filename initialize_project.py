from claude_manager import ClaudeProjectManager
import os
import sys

# Inicializa o gerenciador
manager = ClaudeProjectManager()

# Verifica se existe um arquivo project_context.txt, se não, solicita ao usuário
if not os.path.exists("project_context.txt"):
    print("\nNão foi encontrado o arquivo de contexto do projeto (project_context.txt).")
    create_context = input("Deseja criar este arquivo agora? (s/n): ")
    
    if create_context.lower() == 's':
        print("\nVocê pode colar o conteúdo da documentação do projeto.")
        print("Quando terminar, digite 'FIM' em uma linha separada e pressione Enter.\n")
        
        context_lines = []
        while True:
            line = input()
            if line.strip().upper() == "FIM":
                break
            context_lines.append(line)
        
        with open("project_context.txt", "w", encoding="utf-8") as f:
            f.write("\n".join(context_lines))
        
        print("\nArquivo de contexto do projeto criado com sucesso!")
    else:
        print("\nVocê pode criar o arquivo project_context.txt mais tarde se desejar.")

# Verifica se a API key está configurada, se não, tenta carregar do arquivo
if not manager.config["api"]["claude_api_key"]:
    if not manager._load_api_key_from_file():
        api_key = os.environ.get("CLAUDE_API_KEY")
        if not api_key:
            api_key = input("\nDigite sua chave de API do Claude: ")
        
        if api_key:
            manager.set_api_key(api_key)
        else:
            print("\nErro: API key não fornecida. O projeto não funcionará sem uma API key.")
            sys.exit(1)

# Define os módulos do projeto baseados na documentação
modules = [
    {
        "name": "core",
        "description": "Núcleo do sistema, incluindo autenticação e estrutura multi-tenant",
        "priority": 1
    },
    {
        "name": "subscription",
        "description": "Sistema de assinaturas e integração com Stripe",
        "priority": 2
    },
    {
        "name": "restaurant_types",
        "description": "Gestão de diferentes tipos de restaurante e fluxos específicos",
        "priority": 3
    },
    {
        "name": "tables_qrcode",
        "description": "Gerenciamento de mesas e sistema de QR Code",
        "priority": 4
    },
    {
        "name": "menu_orders",
        "description": "Cardápio digital e sistema de pedidos",
        "priority": 5
    },
    {
        "name": "payments",
        "description": "Processamento de pagamentos e divisão de contas",
        "priority": 6
    },
    {
        "name": "integrations",
        "description": "Integrações com serviços externos (iFood, sistemas fiscais)",
        "priority": 7
    }
]

# Cria os módulos se ainda não existirem
existing_module_names = [m["name"] for m in manager.config["project"]["modules"]]

for module in modules:
    if module["name"] not in existing_module_names:
        manager.create_module(
            module["name"],
            module["description"],
            module["priority"]
        )

# Configura o módulo inicial
manager.set_current_module("core")

# Cria a pasta do projeto se não existir
if not os.path.exists("restaurante-sistema"):
    os.makedirs("restaurante-sistema")
    print("\nPasta do projeto 'restaurante-sistema' criada.")

# Imprime relatório inicial do projeto
manager.print_project_report()

print("\nProjeto inicializado com sucesso!")
print("Para iniciar o desenvolvimento do primeiro módulo, execute: python develop_module.py core")