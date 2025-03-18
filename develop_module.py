from claude_manager import ClaudeProjectManager
import argparse
import os
import sys

def get_user_prompt_input():
    """Permite que o usuário adicione requisitos específicos ao prompt."""
    print("\nAdicione requisitos específicos para este prompt (termine com uma linha vazia):")
    lines = []
    while True:
        line = input()
        if not line:
            break
        lines.append(line)
    return "\n".join(lines)

def main():
    # Parse argumentos da linha de comando
    parser = argparse.ArgumentParser(description='Desenvolver um módulo do projeto SaaS Restaurante')
    parser.add_argument('module', help='Nome do módulo a ser desenvolvido')
    parser.add_argument('--progress', type=int, help='Atualizar o progresso do módulo (0-100)')
    parser.add_argument('--complete', action='store_true', help='Marcar módulo como concluído')
    parser.add_argument('--prompt', help='Prompt direto para o módulo (evita entrada interativa)')
    parser.add_argument('--prompt-file', help='Arquivo contendo o prompt para o módulo')
    parser.add_argument('--api-key', help='Chave API do Claude (tem precedência sobre api.txt)')
    args = parser.parse_args()

    # Inicializa o gerenciador
    manager = ClaudeProjectManager()
    
    # Define a API key (prioridade para o argumento de linha de comando)
    if args.api_key:
        print(f"Usando API key fornecida via argumento --api-key")
        manager.set_api_key(args.api_key)
    # Se não fornecida via argumento, tenta carregar do arquivo
    elif not manager.config["api"]["claude_api_key"]:
        if not manager._load_api_key_from_file():
            key = os.environ.get("CLAUDE_API_KEY")
            if not key:
                key = input("Digite sua chave de API do Claude: ")
            if key:
                manager.set_api_key(key)
            else:
                print("Erro: API key não fornecida. O desenvolvimento não pode continuar.")
                sys.exit(1)

    # Define o módulo atual
    try:
        module_exists = False
        for module in manager.config["project"]["modules"]:
            if module["name"] == args.module:
                module_exists = True
                break
        
        if not module_exists:
            print(f"Erro: Módulo '{args.module}' não encontrado.")
            print("Módulos disponíveis:")
            for module in manager.config["project"]["modules"]:
                print(f" - {module['name']}: {module['description']} (status: {module['status']})")
            return
        
        manager.set_current_module(args.module)
    except Exception as e:
        print(f"Erro ao definir módulo atual: {str(e)}")
        return

    # Atualiza o progresso se especificado
    if args.progress is not None:
        manager.update_module_progress(args.module, args.progress)
    
    # Marca como concluído se especificado
    if args.complete:
        manager.complete_module(args.module)
        print(f"Módulo '{args.module}' marcado como concluído!")
        return

    # Gera um prompt base para o módulo
    base_prompt = manager.generate_module_prompt()
    
    # Obtém os requisitos específicos do usuário (de diferentes fontes conforme a prioridade)
    user_requirements = None
    
    # 1. Da linha de comando (--prompt)
    if args.prompt:
        user_requirements = args.prompt
        print(f"\nUsando prompt fornecido via argumento --prompt:\n{user_requirements[:100]}...\n")
    
    # 2. De um arquivo (--prompt-file)
    elif args.prompt_file:
        try:
            with open(args.prompt_file, 'r', encoding='utf-8') as f:
                user_requirements = f.read()
            print(f"\nUsando prompt do arquivo '{args.prompt_file}'")
        except Exception as e:
            print(f"Erro ao ler arquivo de prompt: {str(e)}")
            user_requirements = None
    
    # 3. De entrada interativa (padrão)
    if user_requirements is None:
        user_requirements = get_user_prompt_input()
    
    # Substitui a seção de requisitos no prompt base
    if user_requirements:
        prompt = base_prompt.replace(
            "[Descreva aqui os requisitos específicos para esta etapa do desenvolvimento]",
            user_requirements
        )
    else:
        prompt = base_prompt
    
    # Confirma envio (automático para --prompt ou --prompt-file)
    if args.prompt or args.prompt_file:
        print("\nConfirmação automática com --prompt ou --prompt-file")
        confirm = 's'
    else:
        # Mostra o prompt final
        print("\n" + "="*50)
        print("PROMPT A SER ENVIADO:")
        print("="*50)
        print(prompt)
        print("="*50)
        confirm = input("\nEnviar este prompt para o Claude? (s/n): ")
    
    if confirm.lower() != 's':
        print("Operação cancelada.")
        return
    
    # Envia para o Claude
    print("\nEnviando prompt para o Claude...")
    response_json, response_text = manager.send_prompt_to_claude(prompt)
    
    if response_json:
        print("\nResposta recebida com sucesso!")
        
        # Salva a resposta em um arquivo temporário para referência
        with open(f"temp_response_{args.module}.txt", "w", encoding="utf-8") as f:
            f.write(response_text)
        
        # Extrai e salva código
        print("\nExtraindo e salvando código...")
        created_files = manager.extract_and_save_all_code(response_text)
        
        if created_files:
            print(f"\nArquivos criados ({len(created_files)}):")
            for file in created_files:
                print(f" - {file}")
        else:
            print("\nNenhum arquivo foi criado a partir da resposta.")
        
        # Pergunta sobre o progresso (exceto se foi usado --prompt ou --prompt-file)
        if not args.prompt and not args.prompt_file:
            progress = input("\nAtualizar progresso do módulo? (0-100, Enter para pular): ")
            if progress and progress.isdigit():
                manager.update_module_progress(args.module, int(progress))
        
        print("\nDesenvolvimento do módulo concluído com sucesso!")
    else:
        print(f"\nErro ao obter resposta: {response_text}")

if __name__ == "__main__":
    main()