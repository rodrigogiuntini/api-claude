import os
import json
import requests
import time
import re
from datetime import datetime
import hashlib
import logging
from pathlib import Path
import shutil

class ClaudeProjectManager:
    """
    Gerenciador de desenvolvimento para o projeto SaaS de Restaurantes usando API do Claude.
    Gerencia tokens, contexto, histórico e arquivos gerados durante o desenvolvimento.
    """
    
    def __init__(self, config_file="claude_project_config.json"):
        """Inicializa o gerenciador de projeto com a configuração básica."""
        self.config_file = config_file
        self.config = self._load_or_create_config()
        self.setup_logging()
        self.logger.info("Gerenciador de projeto inicializado")
        
        # Caminho base para o projeto
        self.base_path = "/Applications/XAMPP/xamppfiles/htdocs/restaurante_sistema"
        
    def setup_logging(self):
        """Configura o sistema de logs."""
        log_dir = "logs"
        os.makedirs(log_dir, exist_ok=True)
        
        self.logger = logging.getLogger("claude_project")
        self.logger.setLevel(logging.INFO)
        
        # Handler para arquivo
        file_handler = logging.FileHandler(
            f"{log_dir}/project_{datetime.now().strftime('%Y%m%d')}.log"
        )
        file_handler.setLevel(logging.INFO)
        
        # Handler para console
        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.INFO)
        
        # Formato dos logs
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        file_handler.setFormatter(formatter)
        console_handler.setFormatter(formatter)
        
        # Limpa handlers existentes
        self.logger.handlers = []
        
        # Adiciona handlers ao logger
        self.logger.addHandler(file_handler)
        self.logger.addHandler(console_handler)
    
    def _load_or_create_config(self):
        """Carrega a configuração ou cria um arquivo de configuração novo."""
        if os.path.exists(self.config_file):
            with open(self.config_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        else:
            # Configuração inicial
            default_config = {
                "api": {
                    "claude_api_key": "",
                    "api_endpoint": "https://api.anthropic.com/v1/messages",
                    "model": "claude-3-sonnet-20240229"
                },
                "project": {
                    "name": "restaurante-sistema",
                    "version": "0.0.1",
                    "progress": 0,
                    "modules": []
                },
                "context": {
                    "current_module": "",
                    "completed_modules": [],
                    "in_progress_modules": []
                },
                "history": {
                    "sessions": [],
                    "total_tokens_used": 0
                }
            }
            with open(self.config_file, 'w', encoding='utf-8') as f:
                json.dump(default_config, f, indent=4)
            return default_config
    
    def save_config(self):
        """Salva a configuração atual no arquivo."""
        with open(self.config_file, 'w', encoding='utf-8') as f:
            json.dump(self.config, f, indent=4)
        self.logger.info("Configuração salva")
    
    def set_api_key(self, api_key):
        """Define a chave da API do Claude."""
        self.config["api"]["claude_api_key"] = api_key
        self.save_config()
        # Mostra parte da chave para debug
        if api_key:
            masked_key = f"{api_key[:10]}...{api_key[-5:]}" if len(api_key) > 15 else "muito curta"
            print(f"API key configurada: {masked_key}")
        self.logger.info("API key configurada")
    
    def _load_api_key_from_file(self, file_path="api.txt"):
        """Carrega a chave da API a partir de um arquivo de texto."""
        try:
            if os.path.exists(file_path):
                with open(file_path, 'r', encoding='utf-8') as f:
                    api_key = f.read().strip()
                    # DEBUG: exibe parte da chave
                    if api_key:
                        masked_key = f"{api_key[:10]}...{api_key[-5:]}" if len(api_key) > 15 else "muito curta"
                        print(f"API key carregada do arquivo {file_path}: {masked_key}")
                        self.set_api_key(api_key)
                        self.logger.info(f"API key carregada do arquivo {file_path}")
                        return True
                    else:
                        print(f"Arquivo {file_path} existe mas está vazio")
            else:
                print(f"Arquivo {file_path} não encontrado")
        except Exception as e:
            self.logger.error(f"Erro ao carregar API key do arquivo: {str(e)}")
            print(f"Erro ao carregar API key: {str(e)}")
        return False
    
    def _load_project_context(self, context_file="project_context.txt"):
        """Carrega o contexto do projeto a partir de um arquivo."""
        try:
            if os.path.exists(context_file):
                with open(context_file, 'r', encoding='utf-8') as f:
                    context = f.read()
                self.logger.info(f"Contexto do projeto carregado de {context_file}")
                return context
            else:
                self.logger.warning(f"Arquivo de contexto '{context_file}' não encontrado")
                return "Descrição detalhada do projeto não disponível."
        except Exception as e:
            self.logger.error(f"Erro ao carregar contexto do projeto: {str(e)}")
            return "Erro ao carregar contexto do projeto."
    
    def create_module(self, module_name, description, priority=1):
        """Cria um novo módulo para desenvolvimento."""
        module = {
            "name": module_name,
            "description": description,
            "status": "pending",
            "priority": priority,
            "created_at": datetime.now().isoformat(),
            "completed_at": None,
            "files": [],
            "dependencies": [],
            "progress": 0
        }
        
        self.config["project"]["modules"].append(module)
        self.save_config()
        self.logger.info(f"Módulo '{module_name}' criado")
        return module
    
    def set_current_module(self, module_name):
        """Define o módulo atual de trabalho."""
        found = False
        for module in self.config["project"]["modules"]:
            if module["name"] == module_name:
                found = True
                self.config["context"]["current_module"] = module_name
                if module_name not in self.config["context"]["in_progress_modules"]:
                    self.config["context"]["in_progress_modules"].append(module_name)
                module["status"] = "in_progress"
                self.save_config()
                self.logger.info(f"Módulo atual definido como '{module_name}'")
                break
        
        if not found:
            self.logger.error(f"Módulo '{module_name}' não encontrado")
    
    def complete_module(self, module_name):
        """Marca um módulo como concluído."""
        for i, module in enumerate(self.config["project"]["modules"]):
            if module["name"] == module_name:
                module["status"] = "completed"
                module["completed_at"] = datetime.now().isoformat()
                module["progress"] = 100
                
                # Remove from in_progress and add to completed
                if module_name in self.config["context"]["in_progress_modules"]:
                    self.config["context"]["in_progress_modules"].remove(module_name)
                if module_name not in self.config["context"]["completed_modules"]:
                    self.config["context"]["completed_modules"].append(module_name)
                
                self.save_config()
                self._recalculate_project_progress()
                self.logger.info(f"Módulo '{module_name}' marcado como concluído")
                return True
        
        self.logger.error(f"Módulo '{module_name}' não encontrado")
        return False
    
    def _recalculate_project_progress(self):
        """Recalcula o progresso do projeto baseado nos módulos."""
        modules = self.config["project"]["modules"]
        if not modules:
            self.config["project"]["progress"] = 0
            return
        
        completed = [m for m in modules if m["status"] == "completed"]
        in_progress = [m for m in modules if m["status"] == "in_progress"]
        
        # Calcula progresso como: (completed + in_progress * seu_progresso) / total
        total_progress = len(completed) * 100
        for module in in_progress:
            total_progress += module["progress"]
        
        project_progress = total_progress / len(modules)
        self.config["project"]["progress"] = round(project_progress, 2)
        self.save_config()
        self.logger.info(f"Progresso do projeto atualizado: {self.config['project']['progress']}%")
    
    def update_module_progress(self, module_name, progress):
        """Atualiza o progresso de um módulo específico."""
        if not 0 <= progress <= 100:
            self.logger.error(f"Progresso deve estar entre 0 e 100. Recebido: {progress}")
            return False
        
        for module in self.config["project"]["modules"]:
            if module["name"] == module_name:
                module["progress"] = progress
                if progress == 100:
                    self.complete_module(module_name)
                else:
                    self.save_config()
                    self._recalculate_project_progress()
                self.logger.info(f"Progresso do módulo '{module_name}' atualizado para {progress}%")
                return True
        
        self.logger.error(f"Módulo '{module_name}' não encontrado")
        return False

    def send_prompt_to_claude(self, prompt_text, save_history=True):
        """
        Envia um prompt para a API do Claude e retorna a resposta.
        
        Args:
            prompt_text: O texto do prompt para enviar
            save_history: Se deve salvar o histórico da conversa
            
        Returns:
            A resposta completa da API e o texto da resposta extraído
        """
        # Verifica se há uma API key configurada
        api_key = self.config["api"]["claude_api_key"]
        if not api_key:
            # Tenta carregar do arquivo api.txt
            if not self._load_api_key_from_file():
                self.logger.error("API key não configurada")
                return None, "API key não configurada. Por favor, configure a API key."
            api_key = self.config["api"]["claude_api_key"]
            
        # DEBUG: exibe parte da chave para confirmação
        masked_key = f"{api_key[:10]}...{api_key[-5:]}" if len(api_key) > 15 else "muito curta"
        print(f"Usando API key: {masked_key}")
        
        headers = {
            "x-api-key": api_key,
            "anthropic-version": "2023-06-01",
            "content-type": "application/json"
        }
        
        data = {
            "model": self.config["api"]["model"],
            "max_tokens": 10000,
            "messages": [{"role": "user", "content": prompt_text}]
        }
        
        try:
            start_time = time.time()
            response = requests.post(
                self.config["api"]["api_endpoint"],
                headers=headers,
                json=data
            )
            end_time = time.time()
            
            if response.status_code == 200:
                response_json = response.json()
                content = response_json.get("content", [])
                text = "".join([block.get("text", "") for block in content if block.get("type") == "text"])
                
                # Registra estatísticas
                tokens_used = response_json.get("usage", {}).get("input_tokens", 0) + \
                              response_json.get("usage", {}).get("output_tokens", 0)
                
                self.config["history"]["total_tokens_used"] += tokens_used
                
                if save_history:
                    # Cria um ID para essa sessão
                    session_id = hashlib.md5(f"{prompt_text}_{datetime.now().isoformat()}".encode()).hexdigest()
                    
                    # Salva a sessão no histórico
                    session = {
                        "id": session_id,
                        "timestamp": datetime.now().isoformat(),
                        "module": self.config["context"]["current_module"],
                        "prompt": prompt_text,
                        "response": text,
                        "tokens_used": tokens_used,
                        "response_time": round(end_time - start_time, 2)
                    }
                    
                    # Salva a sessão no histórico e no arquivo
                    self.config["history"]["sessions"].append(session)
                    self.save_config()
                    
                    # Salva em arquivo separado para facilitar acesso
                    self._save_session_to_file(session)
                
                self.logger.info(f"Prompt enviado, {tokens_used} tokens usados, resposta em {round(end_time - start_time, 2)}s")
                return response_json, text
            else:
                error_msg = f"Erro API ({response.status_code}): {response.text}"
                self.logger.error(error_msg)
                return response, error_msg
        
        except Exception as e:
            error_msg = f"Erro ao enviar prompt: {str(e)}"
            self.logger.error(error_msg)
            return None, error_msg
    
    def _save_session_to_file(self, session):
        """Salva uma sessão em um arquivo separado para facilitar acesso."""
        sessions_dir = Path("sessions")
        sessions_dir.mkdir(exist_ok=True)
        
        # Cria subdiretórios por módulo se existir um módulo atual
        module_name = session.get("module", "general")
        if module_name:
            module_dir = sessions_dir / module_name
            module_dir.mkdir(exist_ok=True)
            file_path = module_dir / f"{session['id']}.json"
        else:
            file_path = sessions_dir / f"{session['id']}.json"
        
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(session, f, indent=4)
    
    def get_session_by_id(self, session_id):
        """Recupera uma sessão pelo ID."""
        for session in self.config["history"]["sessions"]:
            if session["id"] == session_id:
                return session
        return None
    
    def extract_code_from_response(self, response_text, file_path=None):
        """
        Extrai blocos de código de uma resposta e opcionalmente os salva em um arquivo.
        
        Args:
            response_text: Texto da resposta contendo blocos de código
            file_path: Caminho do arquivo para salvar o código extraído (opcional)
            
        Returns:
            Lista de blocos de código extraídos
        """
        # Regex simples para extrair código entre ```
        import re
        code_blocks = re.findall(r'```(?:\w+)?\n(.*?)```', response_text, re.DOTALL)
        
        if file_path and code_blocks:
            # Se um path for fornecido, salva o código no arquivo
            os.makedirs(os.path.dirname(file_path), exist_ok=True)
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(code_blocks[0])  # Salva apenas o primeiro bloco por padrão
            self.logger.info(f"Código extraído e salvo em '{file_path}'")
            
            # Registra o arquivo no módulo atual
            current_module = self.config["context"]["current_module"]
            if current_module:
                for module in self.config["project"]["modules"]:
                    if module["name"] == current_module:
                        if file_path not in module["files"]:
                            module["files"].append(file_path)
                            self.save_config()
        
        return code_blocks
    
    def extract_and_save_all_code(self, response_text, base_dir="restaurante-sistema"):
        """
        Extrai todos os blocos de código de uma resposta com seus caminhos e os salva.
        Procura por padrões como "```php\n// File: path/to/file.php" ou "Para o arquivo `path/to/file.php`:"
        
        Args:
            response_text: Texto da resposta contendo blocos de código
            base_dir: Diretório base para salvar os arquivos
            
        Returns:
            Lista de caminhos de arquivos criados
        """
        import re
        created_files = []
        
        # Padrão 1: ```language\n// File: path/to/file.php
        code_blocks_pattern1 = re.finditer(
            r'```(?:\w+)?\s*\n(?://|#)\s*File:\s*([\w\/\.-]+)\s*\n(.*?)```',
            response_text, 
            re.DOTALL
        )
        
        # Padrão 2: Para o arquivo `path/to/file.php`:
        # ```language
        # código...
        # ```
        code_blocks_pattern2 = re.finditer(
            r'(?:Para|Arquivo|No arquivo|Crie o arquivo|Vamos criar|Código para).*?[`"\']([^`"\']+\.\w+)[`"\'].*?:\s*```(?:\w+)?\s*\n(.*?)```',
            response_text,
            re.DOTALL
        )
        
        # Padrão 3: `path/to/file.php`
        # ```language
        # código...
        # ```
        code_blocks_pattern3 = re.finditer(
            r'[`"\']([^`"\']+\.\w+)[`"\']\s*:\s*```(?:\w+)?\s*\n(.*?)```',
            response_text,
            re.DOTALL
        )
        
        # Padrão 4: Formato usado pela última resposta (## titulo + arquivo)
        code_blocks_pattern4 = re.finditer(
            r'## \d+\. .*?\n\n```(?:\w+)?\n// File: ([\w\/\.-]+)\n(.*?)```',
            response_text,
            re.DOTALL
        )
        
        # Padrão 5: Para blocos que começam com ### `/caminho/do/arquivo.php`
        code_blocks_pattern5 = re.finditer(
            r'###\s*`?/?([^`\n]+)`?\s*\n```(?:\w+)?\s*\n(.*?)```',
            response_text,
            re.DOTALL
        )
        
        # Processa padrão 1
        for match in code_blocks_pattern1:
            file_path = match.group(1)
            code = match.group(2)
            full_path = self._normalize_file_path(file_path, base_dir)
            self._save_code_to_file(full_path, code)
            created_files.append(full_path)
        
        # Processa padrão 2
        for match in code_blocks_pattern2:
            file_path = match.group(1)
            code = match.group(2)
            full_path = self._normalize_file_path(file_path, base_dir)
            self._save_code_to_file(full_path, code)
            created_files.append(full_path)
        
        # Processa padrão 3
        for match in code_blocks_pattern3:
            file_path = match.group(1)
            code = match.group(2)
            full_path = self._normalize_file_path(file_path, base_dir)
            self._save_code_to_file(full_path, code)
            created_files.append(full_path)
        
        # Processa padrão 4
        for match in code_blocks_pattern4:
            file_path = match.group(1)
            code = match.group(2)
            full_path = self._normalize_file_path(file_path, base_dir)
            self._save_code_to_file(full_path, code)
            created_files.append(full_path)
            
        # Processa padrão 5
        for match in code_blocks_pattern5:
            file_path = match.group(1)
            code = match.group(2)
            full_path = self._normalize_file_path(file_path, base_dir)
            self._save_code_to_file(full_path, code)
            created_files.append(full_path)
        
        # Registra os arquivos no módulo atual
        current_module = self.config["context"]["current_module"]
        if current_module:
            for module in self.config["project"]["modules"]:
                if module["name"] == current_module:
                    for file_path in created_files:
                        if file_path not in module["files"]:
                            module["files"].append(file_path)
                    self.save_config()
        
        return created_files
    
    def _normalize_file_path(self, file_path, base_dir):
        """
        Normaliza o caminho do arquivo para o formato correto
        """
        # Remove a barra inicial se existir
        if file_path.startswith('/'):
            file_path = file_path[1:]
            
        # Remove prefixo restaurante-saas se existir
        if file_path.startswith('restaurante-saas/'):
            file_path = file_path[len('restaurante-saas/'):]
            
        # Evitar duplicação de restaurante-sistema
        file_path = re.sub(r'(restaurante-sistema/)+', 'restaurante-sistema/', file_path)
        
        # Garantir que o arquivo está no diretório correto
        if not file_path.startswith('restaurante-sistema') and not file_path.startswith(base_dir):
            file_path = os.path.join(base_dir, file_path)
            
        return file_path
    
    def _save_code_to_file(self, file_path, code):
        """Salva o código em um arquivo, criando os diretórios necessários."""
        try:
            # Normaliza o caminho (importante não usar os.path.normpath pois remove barras iniciais)
            # Remove caracteres estranhos no nome do arquivo
            file_path = re.sub(r'[^\w\-./\\]', '', file_path)
            
            # Convertendo para caminho absoluto dentro do projeto
            if not os.path.isabs(file_path):
                file_path = os.path.join(self.base_path, file_path)
                
            os.makedirs(os.path.dirname(file_path), exist_ok=True)
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(code)
            self.logger.info(f"Código salvo em '{file_path}'")
            return True
        except Exception as e:
            self.logger.error(f"Erro ao salvar código em '{file_path}': {str(e)}")
            return False
    
    def generate_module_prompt(self, module_name=None):
        """
        Gera um prompt para um módulo específico baseado no contexto do projeto.
        
        Args:
            module_name: Nome do módulo (se None, usa o módulo atual)
            
        Returns:
            Texto do prompt gerado
        """
        if not module_name:
            module_name = self.config["context"]["current_module"]
            if not module_name:
                self.logger.error("Nenhum módulo atual definido")
                return None
        
        # Encontra o módulo
        target_module = None
        for module in self.config["project"]["modules"]:
            if module["name"] == module_name:
                target_module = module
                break
        
        if not target_module:
            self.logger.error(f"Módulo '{module_name}' não encontrado")
            return None
        
        # Informa sobre módulos concluídos
        completed_modules = "\n".join([
            f"- {name}" for name in self.config["context"]["completed_modules"]
        ])
        if not completed_modules:
            completed_modules = "Nenhum módulo concluído ainda."
        
        # Informa sobre módulos em andamento
        in_progress_modules = "\n".join([
            f"- {name}" for name in self.config["context"]["in_progress_modules"] 
            if name != module_name
        ])
        if not in_progress_modules:
            in_progress_modules = "Nenhum outro módulo em andamento."
        
        # Lista arquivos já criados para este módulo
        module_files = "\n".join([
            f"- {file}" for file in target_module["files"]
        ])
        if not module_files:
            module_files = "Nenhum arquivo criado ainda para este módulo."
        
        # Carrega o contexto do projeto
        project_context = self._load_project_context()
        
        # Gera o prompt
        prompt = f"""
Estou desenvolvendo um sistema de gestão de restaurantes SaaS em PHP.
Módulo atual: {module_name}

## Contexto do Projeto
{project_context}

## Status do Desenvolvimento
- Progresso geral: {self.config["project"]["progress"]}%
- Módulos concluídos:
{completed_modules}

- Outros módulos em andamento:
{in_progress_modules}

## Sobre este Módulo
- Descrição: {target_module["description"]}
- Status: {target_module["status"]}
- Progresso: {target_module["progress"]}%
- Arquivos já criados:
{module_files}

## Requisitos para o Próximo Passo
[Descreva aqui os requisitos específicos para esta etapa do desenvolvimento]

Por favor, forneça:
1. Código para os próximos arquivos necessários para este módulo
2. Instruções de integração com os componentes existentes
3. Orientações para testes e validação
"""
        return prompt

    def backup_project(self):
        """Cria um backup do projeto e da configuração."""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_dir = f"backups/backup_{timestamp}"
        os.makedirs(backup_dir, exist_ok=True)
        
        # Copia o arquivo de configuração
        shutil.copy2(self.config_file, f"{backup_dir}/")
        
        # Copia os arquivos do projeto
        project_dir = os.path.join(self.base_path, self.config["project"]["name"])
        if os.path.exists(project_dir):
            shutil.copytree(
                project_dir, 
                f"{backup_dir}/{self.config['project']['name']}"
            )
        
        # Copia os logs e sessões
        if os.path.exists("logs"):
            shutil.copytree("logs", f"{backup_dir}/logs")
        if os.path.exists("sessions"):
            shutil.copytree("sessions", f"{backup_dir}/sessions")
        
        self.logger.info(f"Backup criado em '{backup_dir}'")
        return backup_dir
    
    def get_project_report(self):
        """Gera um relatório do estado atual do projeto."""
        # Estatísticas gerais
        modules_count = len(self.config["project"]["modules"])
        completed_modules_count = len(self.config["context"]["completed_modules"])
        in_progress_modules_count = len(self.config["context"]["in_progress_modules"])
        pending_modules_count = modules_count - completed_modules_count - in_progress_modules_count
        
        # Contagem de arquivos
        all_files = []
        for module in self.config["project"]["modules"]:
            all_files.extend(module["files"])
        
        # Relatório
        report = {
            "project_name": self.config["project"]["name"],
            "project_version": self.config["project"]["version"],
            "progress": self.config["project"]["progress"],
            "current_module": self.config["context"]["current_module"],
            "modules_statistics": {
                "total": modules_count,
                "completed": completed_modules_count,
                "in_progress": in_progress_modules_count,
                "pending": pending_modules_count
            },
            "files_count": len(all_files),
            "tokens_used": self.config["history"]["total_tokens_used"],
            "sessions_count": len(self.config["history"]["sessions"]),
            "last_updated": datetime.now().isoformat()
        }
        
        return report
    
    def print_project_report(self):
        """Imprime um relatório formatado do estado atual do projeto."""
        report = self.get_project_report()
        
        print("\n" + "="*50)
        print(f"RELATÓRIO DO PROJETO: {report['project_name']} v{report['project_version']}")
        print("="*50)
        print(f"Progresso Geral: {report['progress']}%")
        print(f"Módulo Atual: {report['current_module'] or 'Nenhum'}")
        print("-"*50)
        print("Estatísticas de Módulos:")
        print(f"  Total: {report['modules_statistics']['total']}")
        print(f"  Concluídos: {report['modules_statistics']['completed']}")
        print(f"  Em andamento: {report['modules_statistics']['in_progress']}")
        print(f"  Pendentes: {report['modules_statistics']['pending']}")
        print("-"*50)
        print(f"Total de Arquivos: {report['files_count']}")
        print(f"Total de Tokens Usados: {report['tokens_used']}")
        print(f"Total de Sessões com Claude: {report['sessions_count']}")
        print("-"*50)
        print(f"Última Atualização: {datetime.fromisoformat(report['last_updated']).strftime('%d/%m/%Y %H:%M:%S')}")
        print("="*50)


# Exemplo de uso
if __name__ == "__main__":
    manager = ClaudeProjectManager()
    
    # Configuração básica (verifica se existe um arquivo api.txt)
    if not manager.config["api"]["claude_api_key"]:
        manager._load_api_key_from_file()
    
    # Imprime relatório
    manager.print_project_report()