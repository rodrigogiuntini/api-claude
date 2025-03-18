from claude_manager import ClaudeProjectManager
import argparse
import json
from datetime import datetime

def main():
    parser = argparse.ArgumentParser(description='Gerar relatórios do projeto SaaS Restaurante')
    parser.add_argument('--backup', action='store_true', help='Criar backup do projeto')
    parser.add_argument('--detailed', action='store_true', help='Gerar relatório detalhado')
    parser.add_argument('--json', action='store_true', help='Salvar relatório em formato JSON')
    args = parser.parse_args()

    # Inicializa o gerenciador
    manager = ClaudeProjectManager()
    
    # Backup
    if args.backup:
        backup_dir = manager.backup_project()
        print(f"Backup criado em: {backup_dir}")
    
    # Relatório básico sempre é impresso
    manager.print_project_report()
    
    # Relatório detalhado
    if args.detailed:
        print("\n" + "="*50)
        print("RELATÓRIO DETALHADO")
        print("="*50)
        
        # Detalhes de cada módulo
        print("\nDETALHES DOS MÓDULOS:")
        for module in manager.config["project"]["modules"]:
            print(f"\n{module['name'].upper()}")
            print(f"  Descrição: {module['description']}")
            print(f"  Status: {module['status']}")
            print(f"  Progresso: {module['progress']}%")
            print(f"  Criado em: {datetime.fromisoformat(module['created_at']).strftime('%d/%m/%Y')}")
            
            if module['completed_at']:
                completed_date = datetime.fromisoformat(module['completed_at']).strftime('%d/%m/%Y')
                print(f"  Concluído em: {completed_date}")
            
            # Arquivos do módulo
            if module['files']:
                print(f"  Arquivos ({len(module['files'])}):")
                for file in module['files']:
                    print(f"    - {file}")
        
        # Estatísticas de uso da API
        print("\nESTATÍSTICAS DE USO DA API:")
        print(f"  Total de tokens utilizados: {manager.config['history']['total_tokens_used']}")
        print(f"  Total de sessões: {len(manager.config['history']['sessions'])}")
        
        # Últimas sessões
        print("\nÚLTIMAS SESSÕES:")
        sessions = manager.config['history']['sessions']
        for i, session in enumerate(sessions[-5:], 1):
            timestamp = datetime.fromisoformat(session['timestamp']).strftime('%d/%m/%Y %H:%M')
            print(f"  {i}. {timestamp} - Módulo: {session['module']} - Tokens: {session['tokens_used']}")
    
    # Salvar em JSON
    if args.json:
        report_filename = f"project_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        with open(report_filename, 'w', encoding='utf-8') as f:
            json.dump(manager.get_project_report(), f, indent=4)
        print(f"\nRelatório salvo em JSON: {report_filename}")

if __name__ == "__main__":
    main()
