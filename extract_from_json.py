import json
import re
import os
import sys

# Configurações
json_file = "sessions/core/0ad5b47f4fcc6e5261acf13b240fb80c.json"
base_dir = "restaurante-sistema"

# Verifica se o arquivo existe
if not os.path.exists(json_file):
    print(f"ERRO: Arquivo JSON '{json_file}' não encontrado!")
    # Tenta encontrar o arquivo em outras localizações possíveis
    alt_paths = [
        "0ad5b47f4fcc6e5261acf13b240fb80c.json",
        "sessions/0ad5b47f4fcc6e5261acf13b240fb80c.json",
        "temp_response_core.txt"
    ]
    
    for path in alt_paths:
        if os.path.exists(path):
            print(f"Encontrado em localização alternativa: {path}")
            json_file = path
            break
    
    if json_file == "sessions/core/0ad5b47f4fcc6e5261acf13b240fb80c.json":
        print("Por favor, especifique o caminho correto para o arquivo JSON:")
        json_file = input("> ")
        if not os.path.exists(json_file):
            print(f"Arquivo JSON '{json_file}' não encontrado. Encerrando.")
            sys.exit(1)

print(f"Lendo arquivo JSON: {json_file}")

# Lê o arquivo JSON
try:
    with open(json_file, 'r', encoding='utf-8') as f:
        content = f.read()
        
        # Verifica se é JSON ou texto simples
        if content.strip().startswith('{'):
            session_data = json.loads(content)
            if 'response' in session_data:
                response_text = session_data['response']
            else:
                print("ERRO: O arquivo JSON não contém uma chave 'response'.")
                sys.exit(1)
        else:
            # Assume que é um arquivo de texto direto (como temp_response_core.txt)
            response_text = content
except Exception as e:
    print(f"ERRO ao ler o arquivo: {str(e)}")
    sys.exit(1)

print(f"Arquivo lido com sucesso. Tamanho da resposta: {len(response_text)} caracteres")

# Padrões para encontrar os blocos de código
patterns = [
    # Padrão específico para este formato de resposta - seção numerada com File:
    r'## \d+\. .*?\n\n```php\n// File: ([\w/.-]+)\n(.*?)```',
    
    # Outros padrões de backup
    r'```(?:\w+)?\s*\n(?://|#)\s*File:\s*([\w/.-]+)\s*\n(.*?)```',
    r'### `([\w/.-]+)`\s*\n```(?:\w+)?\s*\n(.*?)```'
]

created_files = []

# Processa cada padrão
for pattern_idx, pattern in enumerate(patterns):
    matches = re.finditer(pattern, response_text, re.DOTALL)
    pattern_matches = 0
    
    for match in matches:
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

# Resumo
print("\n" + "="*50)
print(f"RESUMO DA EXTRAÇÃO:")
print(f"Total de arquivos criados com sucesso: {len(created_files)}")
print("="*50)

if len(created_files) > 0:
    print("\nArquivos criados:")
    for file in created_files:
        print(f" - {file}")
else:
    print("\nNenhum arquivo foi extraído! Possíveis razões:")
    print("1. O formato dos blocos de código na resposta é diferente do esperado")
    print("2. O arquivo JSON não contém os blocos de código esperados")
    print("3. Os arquivos já foram criados anteriormente")
    
    # Tentativa de extrair manualmente um trecho para depuração
    sample = response_text[:500]
    print("\nAmostra do início da resposta para depuração:")
    print("-"*50)
    print(sample)
    print("-"*50)
