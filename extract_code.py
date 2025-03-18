import re
import os
import sys
import json

# Configuração
response_file = "temp_response_core.txt"  # Arquivo de resposta do Claude
base_dir = "restaurante-sistema"          # Diretório base para salvar os arquivos

# Verifica se o arquivo existe
if not os.path.exists(response_file):
    print(f"ERRO: Arquivo '{response_file}' não encontrado!")
    sys.exit(1)

# Lê o conteúdo do arquivo
with open(response_file, 'r', encoding='utf-8') as f:
    content = f.read()

# Também podemos tentar ler de arquivos JSON de sessão se necessário
if len(content.strip()) == 0 or content.startswith('{'):
    try:
        # Tenta ler como um arquivo JSON de sessão
        data = json.loads(content)
        if 'response' in data:
            content = data['response']
        print("Lendo conteúdo do arquivo JSON de sessão")
    except:
        pass

# Padrões para extração de código
patterns = [
    # Formato padrão: ```language\ncode```
    r'```(?:\w+)?\s*\n(.*?)```',
    
    # Formato específico: // File: caminho/do/arquivo.php
    r'// File: ([\w/.-]+)\s*\n(.*?)(?=```|// File:|$)',
    
    # Formato usado pelo Claude neste caso: core/Router.php
    r'(?:// |#) File: ([\w/.-]+)\s*\n(.*?)(?=```|(?:// |#) File:|$)'
]

created_files = []
total_patterns_found = 0

# Procura padrões específicos de cabeçalho de arquivo
file_header_matches = re.finditer(r'## \d+\. (.*?)\n\n```php\n// File: ([\w/.-]+)', content, re.DOTALL)
for match in file_header_matches:
    file_title = match.group(1).strip()
    file_path = match.group(2).strip()
    print(f"Encontrado arquivo com título: {file_title}, caminho: {file_path}")

# Processa cada padrão
for pattern_idx, pattern in enumerate(patterns):
    matches = re.finditer(pattern, content, re.DOTALL)
    pattern_matches = 0
    
    for match in matches:
        if pattern_idx == 0:  # Formato padrão de código
            # Verifica se é apenas um bloco de código sem caminho de arquivo
            continue
            
        elif pattern_idx in [1, 2]:  # Formatos específicos com caminho de arquivo
            file_path = match.group(1).strip()
            code = match.group(2).strip()
            
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
                pattern_matches += 1
            except Exception as e:
                print(f"ERRO: Falha ao criar arquivo {full_path}: {str(e)}")
    
    print(f"Encontrados {pattern_matches} arquivos usando o padrão {pattern_idx+1}")
    total_patterns_found += pattern_matches

# Tenta extrair arquivos do formato específico usado pelo Claude nesta resposta
specific_pattern = r'## \d+\. (.*?)\n\n```php\n// File: ([\w/.-]+)\n(.*?)```'
specific_matches = re.finditer(specific_pattern, content, re.DOTALL)
specific_count = 0

for match in specific_matches:
    file_title = match.group(1).strip()
    file_path = match.group(2).strip()
    code = match.group(3).strip()
    
    # Remove a barra inicial se existir
    if file_path.startswith('/'):
        file_path = file_path[1:]
        
    # Constrói o caminho completo
    full_path = os.path.join(base_dir, file_path)
    
    # Cria os diretórios necessários
    os.makedirs(os.path.dirname(full_path), exist_ok=True)
    
    # Salva o arquivo
    try:
        with open(full_path, 'w', encoding='utf-8') as f:
            f.write(code)
        created_files.append(full_path)
        print(f"SUCESSO: Arquivo criado pelo formato específico: {full_path}")
        specific_count += 1
    except Exception as e:
        print(f"ERRO: Falha ao criar arquivo {full_path}: {str(e)}")

print(f"Encontrados {specific_count} arquivos usando o padrão específico")

# Resumo
print("\n" + "="*50)
print(f"RESUMO DA EXTRAÇÃO:")
print(f"Total de padrões encontrados: {total_patterns_found + specific_count}")
print(f"Total de arquivos criados com sucesso: {len(created_files)}")
print("="*50)

if len(created_files) > 0:
    print("\nArquivos criados:")
    for file in created_files:
        print(f" - {file}")