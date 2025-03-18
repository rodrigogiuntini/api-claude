import re
import os
import sys

# Configuração
response_file = "temp_response_core.txt"  # Arquivo de resposta do Claude
base_dir = "restaurante-sistema"          # Diretório base para salvar os arquivos

# Verifica se o arquivo existe
if not os.path.exists(response_file):
    print(f"ERRO: Arquivo '{response_file}' não encontrado!")
    print("Por favor, execute o script no mesmo diretório do arquivo temp_response_core.txt")
    sys.exit(1)

print(f"Lendo o arquivo '{response_file}'...")

# Lê o conteúdo do arquivo
with open(response_file, 'r', encoding='utf-8') as f:
    content = f.read()

# Define padrões para extração de código
patterns = [
    # Padrão para o formato de código usado pelo Claude (### `/caminho/do/arquivo.php`)
    r'###\s*`?/?([\w/.-]+)`?\s*\n```(?:\w+)?\s*\n(.*?)```',
    
    # Padrão alternativo (para nomes de arquivo entre crases)
    r'`([\w/.-]+)`\s*:\s*```(?:\w+)?\s*\n(.*?)```'
]

created_files = []
total_patterns_found = 0

# Processa cada padrão
for pattern_idx, pattern in enumerate(patterns):
    matches = re.finditer(pattern, content, re.DOTALL)
    pattern_matches = 0
    
    for match in matches:
        pattern_matches += 1
        file_path = match.group(1)
        code = match.group(2)
        
        # Remove a barra inicial se existir
        if file_path.startswith('/'):
            file_path = file_path[1:]
            
        # Constrói o caminho completo
        full_path = os.path.join(base_dir, file_path)
        
        # Cria os diretórios necessários
        os.makedirs(os.path.dirname(full_path), exist_ok=True)
        
        # Verifica se o arquivo já existe
        if os.path.exists(full_path):
            print(f"AVISO: Sobrescrevendo arquivo existente: {full_path}")
        
        # Salva o arquivo
        try:
            with open(full_path, 'w', encoding='utf-8') as f:
                f.write(code)
            created_files.append(full_path)
            print(f"SUCESSO: Arquivo criado: {full_path}")
        except Exception as e:
            print(f"ERRO: Falha ao criar arquivo {full_path}: {str(e)}")
    
    print(f"Encontrados {pattern_matches} arquivos usando o padrão {pattern_idx+1}")
    total_patterns_found += pattern_matches

# Resumo
print("\n" + "="*50)
print(f"RESUMO DA EXTRAÇÃO:")
print(f"Total de padrões encontrados: {total_patterns_found}")
print(f"Total de arquivos criados com sucesso: {len(created_files)}")
print("="*50)

if len(created_files) == 0:
    print("\nNenhum arquivo foi extraído! Possíveis razões:")
    print("1. O formato dos blocos de código na resposta é diferente do esperado")
    print("2. O arquivo de resposta não contém blocos de código")
    print("3. Há um problema com as expressões regulares usadas")
    print("\nVerifique o conteúdo do arquivo temp_response_core.txt")
else:
    print("\nPróximos passos:")
    print("1. Verifique os arquivos criados em:", os.path.abspath(base_dir))
    print("2. Configure o ambiente PHP/MySQL conforme necessário")
    print("3. Atualize o claude_manager.py para reconhecer este formato no futuro")
