#!/usr/bin/env python3
import os
import json
import shutil
from datetime import datetime
import re
import sys

class ProjectSetup:
    def __init__(self, base_dir="restaurante-sistema"):
        self.base_dir = base_dir
        self.created_dirs = []
        self.created_files = []
        
    def create_directory_structure(self):
        """
        Cria a estrutura completa de diretórios conforme especificada na documentação.
        """
        print("Criando estrutura completa de diretórios para o projeto RestauranteSaaS...\n")
        
        # Diretório base do projeto
        os.makedirs(self.base_dir, exist_ok=True)
        
        # Diretórios principais conforme a estrutura definida no project_context.txt
        directories = [
            # Diretórios raiz
            "config",
            "public",
            "public/assets/css",
            "public/assets/css/themes",
            "public/assets/js",
            "public/assets/images/logos",
            "public/assets/images/icons",
            "public/assets/images/backgrounds",
            "public/assets/images/placeholders",
            "public/assets/fonts",
            "public/assets/manifests",
            "public/uploads/tenants",
            "public/uploads/menus",
            "public/uploads/profiles",
            "public/uploads/qrcodes",
            "public/uploads/reports",
            
            # Recursos
            "resources/js/components",
            "resources/js/pages",
            "resources/js/libs",
            "resources/sass/components",
            "resources/sass/layout",
            "resources/sass/pages",
            "resources/sass/themes",
            "resources/lang/pt-br",
            "resources/lang/en",
            "resources/lang/es",
            "resources/lang/fr",
            "resources/views/admin",
            "resources/views/auth",
            "resources/views/pos",
            "resources/views/kitchen",
            "resources/views/client",
            "resources/views/waiter",
            "resources/views/manager",
            "resources/views/emails",
            "resources/views/pdf",
            "resources/views/components",
            "resources/views/errors",
            
            # Código fonte - Módulo Core
            "src/Core",
            "src/Core/Auth",
            "src/Core/Database",
            "src/Core/Cache",
            "src/Core/Tenant",
            "src/Core/HTTP",
            "src/Core/Security",
            "src/Core/Localization",
            "src/Core/Events",
            "src/Core/Queue",
            "src/Core/Validation",
            "src/Core/Helpers",
            "src/Core/Logger",
            "src/Core/Exceptions",
            
            # Outros módulos
            "src/Subscription/Controllers",
            "src/Subscription/Models",
            "src/Subscription/Services",
            "src/Subscription/Jobs",
            
            "src/Admin/Controllers",
            "src/Admin/Models",
            "src/Admin/Services",
            "src/Admin/Widgets",
            
            "src/Restaurant/Controllers",
            "src/Restaurant/Models",
            "src/Restaurant/Services",
            
            "src/Tables/Controllers",
            "src/Tables/Models",
            "src/Tables/Services",
            
            "src/Menu/Controllers",
            "src/Menu/Models",
            "src/Menu/Services",
            
            "src/Order/Controllers",
            "src/Order/Models",
            "src/Order/Services",
            "src/Order/Jobs",
            
            "src/Payment/Controllers",
            "src/Payment/Models",
            "src/Payment/Services",
            
            "src/Inventory/Controllers",
            "src/Inventory/Models",
            "src/Inventory/Services",
            
            "src/Analytics/Controllers",
            "src/Analytics/Models",
            "src/Analytics/Services",
            
            "src/Staff/Controllers",
            "src/Staff/Models",
            "src/Staff/Services",
            
            "src/Customer/Controllers",
            "src/Customer/Models",
            "src/Customer/Services",
            
            "src/Fiscal/Controllers",
            "src/Fiscal/Models",
            "src/Fiscal/Services",
            
            "src/Delivery/Controllers",
            "src/Delivery/Models",
            "src/Delivery/Services",
            
            "src/Integration/Controllers",
            "src/Integration/Models",
            "src/Integration/Services",
            
            "src/API/Controllers",
            "src/API/Middlewares",
            "src/API/Resources",
            
            # Banco de dados
            "database/migrations",
            "database/seeders",
            "database/backup",
            
            # Testes
            "tests/Unit/Models",
            "tests/Unit/Services",
            "tests/Unit/Helpers",
            "tests/Integration/Controllers",
            "tests/Integration/API",
            "tests/Integration/Services",
            "tests/Feature/Order",
            "tests/Feature/Payment",
            "tests/Feature/Auth",
            "tests/Browser/Admin",
            "tests/Browser/Client",
            "tests/Browser/Waiter",
            
            # Armazenamento
            "storage/app/private",
            "storage/app/public",
            "storage/framework/cache",
            "storage/framework/sessions",
            "storage/framework/views",
            "storage/logs",
            
            # Documentação
            "docs/api",
            "docs/user",
            "docs/admin",
            "docs/developer",
            
            # Scripts
            "scripts/cron",
            
            # Vendor (vazio, será preenchido pelo Composer)
            "vendor"
        ]
        
        # Criar diretórios
        for directory in directories:
            full_path = os.path.join(self.base_dir, directory)
            os.makedirs(full_path, exist_ok=True)
            self.created_dirs.append(full_path)
            print(f"  Criado: {full_path}")
            
        return self.created_dirs
    
    def create_config_files(self):
        """
        Cria arquivos de configuração básicos.
        """
        print("\nCriando arquivos de configuração...")
        
        config_files = {
            "config/app.php": """<?php
/**
 * Configurações gerais da aplicação
 */
return [
    'name' => 'Sistema de Gestão de Restaurantes',
    'version' => '1.0.0',
    'environment' => 'development', // development, production, testing
    'debug' => true,
    'timezone' => 'America/Sao_Paulo',
    'locale' => 'pt_BR',
    'url' => 'http://localhost/restaurante-sistema',
    'encryption_key' => 'sua_chave_de_encriptacao_segura_aqui',
    'session' => [
        'lifetime' => 120, // em minutos
        'secure_cookies' => false, // true em produção
        'same_site' => 'lax', // none, lax, strict
        'http_only' => true,
    ],
    'security' => [
        'password_min_length' => 8,
        'password_requires_special' => true,
        'password_requires_number' => true,
        'password_requires_uppercase' => true,
        'max_login_attempts' => 5,
        'lockout_time' => 15, // em minutos
    ],
    'logs' => [
        'enabled' => true,
        'path' => 'storage/logs',
        'level' => 'debug', // debug, info, notice, warning, error, critical, alert, emergency
    ],
    'tenant' => [
        'column' => 'tenant_id',
        'header' => 'X-Tenant',
        'validate_all_routes' => true,
        'exempt_routes' => ['/auth/login', '/auth/register', '/auth/reset-password']
    ]
];
""",
            "config/database.php": """<?php
/**
 * Configurações de banco de dados
 */
return [
    'default' => 'mysql',
    
    'connections' => [
        'mysql' => [
            'driver' => 'mysql',
            'host' => getenv('DB_HOST') ?: 'localhost',
            'port' => getenv('DB_PORT') ?: '3306',
            'database' => getenv('DB_DATABASE') ?: 'restaurante_saas',
            'username' => getenv('DB_USERNAME') ?: 'root',
            'password' => getenv('DB_PASSWORD') ?: '',
            'charset' => 'utf8mb4',
            'collation' => 'utf8mb4_unicode_ci',
            'prefix' => '',
            'strict' => true,
            'engine' => 'InnoDB',
        ],
        
        'tenant' => [
            'driver' => 'mysql',
            'host' => getenv('DB_HOST') ?: 'localhost',
            'port' => getenv('DB_PORT') ?: '3306',
            'database' => null, // Será preenchido dinamicamente
            'username' => getenv('DB_USERNAME') ?: 'root',
            'password' => getenv('DB_PASSWORD') ?: '',
            'charset' => 'utf8mb4',
            'collation' => 'utf8mb4_unicode_ci',
            'prefix' => '',
            'strict' => true,
            'engine' => 'InnoDB',
        ],
    ],
    
    'migrations' => 'migrations',
    
    'redis' => [
        'client' => 'predis',
        'default' => [
            'host' => getenv('REDIS_HOST') ?: '127.0.0.1',
            'password' => getenv('REDIS_PASSWORD') ?: null,
            'port' => getenv('REDIS_PORT') ?: 6379,
            'database' => 0,
        ],
        'cache' => [
            'host' => getenv('REDIS_HOST') ?: '127.0.0.1',
            'password' => getenv('REDIS_PASSWORD') ?: null,
            'port' => getenv('REDIS_PORT') ?: 6379,
            'database' => 1,
        ],
        'session' => [
            'host' => getenv('REDIS_HOST') ?: '127.0.0.1',
            'password' => getenv('REDIS_PASSWORD') ?: null,
            'port' => getenv('REDIS_PORT') ?: 6379,
            'database' => 2,
        ],
    ],
];
""",
            "config/cache.php": """<?php
/**
 * Configurações de cache
 */
return [
    'default' => 'file', // file, redis, memcached
    
    'stores' => [
        'file' => [
            'driver' => 'file',
            'path' => 'storage/framework/cache',
        ],
        'redis' => [
            'driver' => 'redis',
            'connection' => 'cache',
        ],
        'memcached' => [
            'driver' => 'memcached',
            'servers' => [
                [
                    'host' => getenv('MEMCACHED_HOST') ?: '127.0.0.1',
                    'port' => getenv('MEMCACHED_PORT') ?: 11211,
                    'weight' => 100,
                ],
            ],
        ],
    ],
    
    'prefix' => 'restaurante_',
    'ttl' => 3600, // Tempo padrão de cache em segundos (1 hora)
];
""",
            "config/mail.php": """<?php
/**
 * Configurações de email
 */
return [
    'driver' => 'smtp', // smtp, sendmail, mailgun, ses, postmark
    
    'smtp' => [
        'host' => getenv('MAIL_HOST') ?: 'smtp.mailtrap.io',
        'port' => getenv('MAIL_PORT') ?: 2525,
        'encryption' => getenv('MAIL_ENCRYPTION') ?: 'tls',
        'username' => getenv('MAIL_USERNAME') ?: '',
        'password' => getenv('MAIL_PASSWORD') ?: '',
    ],
    
    'from' => [
        'address' => getenv('MAIL_FROM_ADDRESS') ?: 'noreply@restaurantesaas.com',
        'name' => getenv('MAIL_FROM_NAME') ?: 'Sistema de Gestão de Restaurantes',
    ],
    
    'markdown' => [
        'theme' => 'default',
        'paths' => [
            'resources/views/emails',
        ],
    ],
];
""",
            "config/payment.php": """<?php
/**
 * Configurações de pagamento
 */
return [
    'default' => 'stripe',
    
    'providers' => [
        'stripe' => [
            'key' => getenv('STRIPE_KEY') ?: '',
            'secret' => getenv('STRIPE_SECRET') ?: '',
            'webhook_secret' => getenv('STRIPE_WEBHOOK_SECRET') ?: '',
        ],
        'paypal' => [
            'client_id' => getenv('PAYPAL_CLIENT_ID') ?: '',
            'client_secret' => getenv('PAYPAL_CLIENT_SECRET') ?: '',
            'environment' => getenv('PAYPAL_ENVIRONMENT') ?: 'sandbox', // sandbox, production
        ],
        'mercadopago' => [
            'public_key' => getenv('MP_PUBLIC_KEY') ?: '',
            'access_token' => getenv('MP_ACCESS_TOKEN') ?: '',
        ],
        'pix' => [
            'key_type' => getenv('PIX_KEY_TYPE') ?: 'cpf', // cpf, cnpj, email, phone, random
            'key' => getenv('PIX_KEY') ?: '',
            'merchant_name' => getenv('PIX_MERCHANT_NAME') ?: '',
            'merchant_city' => getenv('PIX_MERCHANT_CITY') ?: '',
        ],
    ],
    
    'currency' => 'BRL',
    'decimal_precision' => 2,
];
""",
            "config/routes.php": """<?php
/**
 * Configuração de rotas
 */
return [
    'web' => 'routes/web.php',
    'api' => 'routes/api.php',
    'admin' => 'routes/admin.php',
    'tenant' => 'routes/tenant.php',
    'middleware' => [
        'web' => [
            'session',
            'csrf',
            'auth',
        ],
        'api' => [
            'throttle:60,1',
            'auth:api',
        ],
        'admin' => [
            'session',
            'csrf',
            'auth',
            'admin',
        ],
    ],
];
""",
            "config/logging.php": """<?php
/**
 * Configurações de logging
 */
return [
    'default' => 'file',
    
    'channels' => [
        'file' => [
            'driver' => 'file',
            'path' => 'storage/logs/app.log',
            'level' => 'debug',
            'days' => 14,
        ],
        'database' => [
            'driver' => 'database',
            'table' => 'activity_logs',
            'level' => 'info',
        ],
        'slack' => [
            'driver' => 'slack',
            'url' => getenv('LOG_SLACK_WEBHOOK_URL') ?: '',
            'username' => 'RestauranteSaaS Log',
            'emoji' => ':boom:',
            'level' => 'critical',
        ],
    ],
];
""",
        }
        
        for file_path, content in config_files.items():
            full_path = os.path.join(self.base_dir, file_path)
            os.makedirs(os.path.dirname(full_path), exist_ok=True)
            
            with open(full_path, 'w', encoding='utf-8') as f:
                f.write(content)
            
            self.created_files.append(full_path)
            print(f"  Criado: {full_path}")
            
        return self.created_files
    
    def create_core_files(self):
        """
        Cria os arquivos principais do núcleo do sistema.
        """
        print("\nCriando arquivos do núcleo (Core)...")
        
        core_files = {
            "src/Core/App.php": """<?php
namespace RestauranteSaas\\Core;

/**
 * Classe principal da aplicação
 */
class App
{
    private static $instance = null;
    private $config = [];
    private $container = [];
    private $currentTenant = null;

    /**
     * Construtor privado (Singleton)
     */
    private function __construct()
    {
        $this->loadConfigurations();
        $this->setupErrorHandling();
        $this->initializeContainer();
    }

    /**
     * Obtém a instância única da aplicação
     */
    public static function getInstance()
    {
        if (self::$instance === null) {
            self::$instance = new self();
        }
        return self::$instance;
    }

    /**
     * Carrega todos os arquivos de configuração
     */
    private function loadConfigurations()
    {
        $configFiles = glob(__DIR__ . '/../../config/*.php');
        foreach ($configFiles as $file) {
            $key = basename($file, '.php');
            $this->config[$key] = require $file;
        }
    }

    /**
     * Configura o tratamento de erros e exceções
     */
    private function setupErrorHandling()
    {
        $errorHandler = new ErrorHandler($this->config['app']['debug']);
        $errorHandler->register();
    }

    /**
     * Inicializa o container de serviços
     */
    private function initializeContainer()
    {
        // Registra os serviços principais
        $this->bind('db', function() {
            return new Database\\Connection($this->config['database']);
        });
        
        $this->bind('router', function() {
            return new Router();
        });
        
        $this->bind('request', function() {
            return new HTTP\\Request();
        });
        
        $this->bind('response', function() {
            return new HTTP\\Response();
        });
        
        $this->bind('session', function() {
            return new Auth\\Session($this->config['app']['session']);
        });
        
        $this->bind('auth', function() {
            return new Auth\\Auth($this->get('db'), $this->get('session'));
        });
        
        $this->bind('tenant', function() {
            return new Tenant\\TenantManager($this->config['app']['tenant']);
        });
        
        $this->bind('cache', function() {
            return new Cache\\CacheManager($this->config['cache']);
        });
        
        $this->bind('logger', function() {
            return new Logger\\Logger($this->config['logging']);
        });
    }

    /**
     * Executa a aplicação
     */
    public function run()
    {
        // Inicia a sessão
        $this->get('session')->start();
        
        // Resolve o tenant atual
        $tenantManager = $this->get('tenant');
        $this->currentTenant = $tenantManager->resolveTenant();
        
        // Configura o banco de dados com o contexto do tenant
        if ($this->currentTenant) {
            $this->get('db')->setTenant($this->currentTenant->id);
        }
        
        // Processa a requisição através do roteador
        $router = $this->get('router');
        $router->loadRoutes();
        
        $request = $this->get('request');
        $response = $router->dispatch($request);
        
        // Envia a resposta
        $response->send();
    }

    /**
     * Obtém um valor de configuração
     */
    public function config($key, $default = null)
    {
        $parts = explode('.', $key);
        $value = $this->config;
        
        foreach ($parts as $part) {
            if (!isset($value[$part])) {
                return $default;
            }
            $value = $value[$part];
        }
        
        return $value;
    }

    /**
     * Registra um serviço no container
     */
    public function bind($name, $resolver)
    {
        $this->container[$name] = [
            'resolver' => $resolver,
            'instance' => null
        ];
    }

    /**
     * Obtém um serviço do container
     */
    public function get($name)
    {
        if (!isset($this->container[$name])) {
            throw new Exceptions\\AppException("Serviço '$name' não encontrado no container");
        }
        
        if ($this->container[$name]['instance'] === null) {
            $resolver = $this->container[$name]['resolver'];
            $this->container[$name]['instance'] = $resolver();
        }
        
        return $this->container[$name]['instance'];
    }

    /**
     * Obtém o tenant atual
     */
    public function getCurrentTenant()
    {
        return $this->currentTenant;
    }

    /**
     * Define o tenant atual
     */
    public function setCurrentTenant($tenant)
    {
        $this->currentTenant = $tenant;
        
        if ($tenant) {
            $this->get('db')->setTenant($tenant->id);
        }
    }
}
""",
            "src/Core/Router.php": """<?php
namespace RestauranteSaas\\Core;

use RestauranteSaas\\Core\\Exceptions\\AppException;

/**
 * Sistema de roteamento
 */
class Router
{
    private $routes = [
        'GET' => [],
        'POST' => [],
        'PUT' => [],
        'DELETE' => [],
        'PATCH' => []
    ];
    
    private $namedRoutes = [];
    private $middlewares = [];
    private $globalMiddlewares = [];
    private $routeGroups = [];
    private $currentGroup = null;
    
    /**
     * Carrega as rotas dos arquivos
     */
    public function loadRoutes()
    {
        require_once __DIR__ . '/../../routes/web.php';
        
        if (file_exists(__DIR__ . '/../../routes/api.php')) {
            require_once __DIR__ . '/../../routes/api.php';
        }
        
        if (file_exists(__DIR__ . '/../../routes/admin.php')) {
            require_once __DIR__ . '/../../routes/admin.php';
        }
        
        if (file_exists(__DIR__ . '/../../routes/tenant.php')) {
            require_once __DIR__ . '/../../routes/tenant.php';
        }
    }
    
    /**
     * Registra uma rota GET
     */
    public function get($uri, $handler, $name = null)
    {
        return $this->addRoute('GET', $uri, $handler, $name);
    }
    
    /**
     * Registra uma rota POST
     */
    public function post($uri, $handler, $name = null)
    {
        return $this->addRoute('POST', $uri, $handler, $name);
    }
    
    /**
     * Registra uma rota PUT
     */
    public function put($uri, $handler, $name = null)
    {
        return $this->addRoute('PUT', $uri, $handler, $name);
    }
    
    /**
     * Registra uma rota DELETE
     */
    public function delete($uri, $handler, $name = null)
    {
        return $this->addRoute('DELETE', $uri, $handler, $name);
    }
    
    /**
     * Registra uma rota PATCH
     */
    public function patch($uri, $handler, $name = null)
    {
        return $this->addRoute('PATCH', $uri, $handler, $name);
    }
    
    /**
     * Adiciona uma rota ao roteador
     */
    private function addRoute($method, $uri, $handler, $name = null)
    {
        // Aplica o prefixo do grupo, se estiver em um grupo
        if ($this->currentGroup) {
            $uri = $this->routeGroups[$this->currentGroup]['prefix'] . $uri;
        }
        
        // Substitui parâmetros nomeados por regex
        $pattern = preg_replace('/\{([a-zA-Z0-9_]+)\}/', '(?P<$1>[^/]+)', $uri);
        $pattern = "#^{$pattern}$#";
        
        $this->routes[$method][$pattern] = [
            'uri' => $uri,
            'handler' => $handler,
            'middlewares' => $this->currentGroup 
                ? array_merge($this->routeGroups[$this->currentGroup]['middlewares'], $this->middlewares) 
                : $this->middlewares
        ];
        
        // Reseta middlewares para a próxima rota
        $this->middlewares = [];
        
        // Armazena rota nomeada
        if ($name) {
            $this->namedRoutes[$name] = $uri;
        }
        
        return $this;
    }
    
    /**
     * Aplica middleware à próxima rota registrada
     */
    public function middleware($middleware)
    {
        if (is_array($middleware)) {
            $this->middlewares = array_merge($this->middlewares, $middleware);
        } else {
            $this->middlewares[] = $middleware;
        }
        
        return $this;
    }
    
    /**
     * Adiciona um middleware global
     */
    public function addGlobalMiddleware($middleware)
    {
        $this->globalMiddlewares[] = $middleware;
    }
    
    /**
     * Cria um grupo de rotas
     */
    public function group(array $attributes, callable $callback)
    {
        $groupId = uniqid('group_');
        
        $this->routeGroups[$groupId] = [
            'prefix' => $attributes['prefix'] ?? '',
            'middlewares' => $attributes['middleware'] ?? []
        ];
        
        $previousGroup = $this->currentGroup;
        $this->currentGroup = $groupId;
        
        call_user_func($callback, $this);
        
        $this->currentGroup = $previousGroup;
    }
    
    /**
     * Gera URL para uma rota nomeada
     */
    public function url($name, $parameters = [])
    {
        if (!isset($this->namedRoutes[$name])) {
            throw new AppException("Rota com nome '{$name}' não encontrada");
        }
        
        $uri = $this->namedRoutes[$name];
        
        // Substitui parâmetros na URI
        foreach ($parameters as $key => $value) {
            $uri = str_replace("{{$key}}", $value, $uri);
        }
        
        return $uri;
    }
    
    /**
     * Despacha a requisição para o handler apropriado
     */
    public function dispatch($request)
    {
        $method = $request->getMethod();
        $uri = $request->getUri();
        
        // Remove string de consulta
        $uri = explode('?', $uri)[0];
        
        // Remove barra final
        $uri = rtrim($uri, '/');
        
        // Rota padrão se vazia
        if ($uri === '') {
            $uri = '/';
        }
        
        // Encontra rota correspondente
        foreach ($this->routes[$method] as $pattern => $route) {
            if (preg_match($pattern, $uri, $matches)) {
                // Extrai parâmetros da rota
                $params = array_filter($matches, function($key) {
                    return !is_numeric($key);
                }, ARRAY_FILTER_USE_KEY);
                
                $request->setParams($params);
                
                // Processa middlewares globais
                foreach ($this->globalMiddlewares as $middleware) {
                    $middlewareInstance = $this->resolveMiddleware($middleware);
                    $response = $middlewareInstance->handle($request, function ($request) {
                        return null;
                    });
                    
                    if ($response) {
                        return $response;
                    }
                }
                
                // Processa middlewares da rota
                $middlewares = $route['middlewares'];
                return $this->processMiddlewares($middlewares, $request, function ($request) use ($route) {
                    return $this->callRouteHandler($route['handler'], $request);
                });
            }
        }
        
        // Nenhuma rota correspondente encontrada
        $response = new HTTP\\Response();
        return $response->setStatus(404)->setContent([
            'error' => true,
            'message' => 'Rota não encontrada'
        ]);
    }
    
    /**
     * Processa a pilha de middlewares
     */
    private function processMiddlewares(array $middlewares, $request, callable $target)
    {
        if (empty($middlewares)) {
            return $target($request);
        }
        
        $middleware = array_shift($middlewares);
        $middlewareInstance = $this->resolveMiddleware($middleware);
        
        return $middlewareInstance->handle($request, function ($request) use ($middlewares, $target) {
            return $this->processMiddlewares($middlewares, $request, $target);
        });
    }
    
    /**
     * Resolve a classe de middleware
     */
    private function resolveMiddleware($middleware)
    {
        // Mapeamento de aliases de middleware
        $middlewareMap = [
            'auth' => \\RestauranteSaas\\Core\\HTTP\\Middleware\\AuthMiddleware::class,
            'guest' => \\RestauranteSaas\\Core\\HTTP\\Middleware\\GuestMiddleware::class,
            'tenant' => \\RestauranteSaas\\Core\\HTTP\\Middleware\\TenantMiddleware::class,
            'api' => \\RestauranteSaas\\Core\\HTTP\\Middleware\\ApiMiddleware::class,
            'throttle' => \\RestauranteSaas\\Core\\HTTP\\Middleware\\ThrottleMiddleware::class,
        ];
        
        $class = isset($middlewareMap[$middleware]) ? $middlewareMap[$middleware] : $middleware;
        
        if (!class_exists($class)) {
            throw new AppException("Classe de middleware '{$class}' não encontrada");
        }
        
        return new $class();
    }
    
    /**
     * Chama o handler da rota
     */
    private function callRouteHandler($handler, $request)
    {
        if (is_callable($handler)) {
            return $handler($request);
        }
        
        if (is_string($handler)) {
            // Resolve Controller@method
            if (strpos($handler, '@') !== false) {
                list($controller, $method) = explode('@', $handler);
                
                $controllerClass = "\\RestauranteSaas\\Controllers\\{$controller}";
                
                if (!class_exists($controllerClass)) {
                    throw new AppException("Controller '{$controllerClass}' não encontrado");
                }
                
                $controllerInstance = new $controllerClass();
                
                if (!method_exists($controllerInstance, $method)) {
                    throw new AppException("Método '{$method}' não encontrado no controller '{$controllerClass}'");
                }
                
                return $controllerInstance->$method($request);
            }
        }
        
        if (is_array($handler) && count($handler) === 2) {
            list($controller, $method) = $handler;
            
            if (is_string($controller)) {
                $controller = new $controller();
            }
            
            return $controller->$method($request);
        }
        
        throw new AppException("Handler de rota inválido");
    }
}
""",
            "src/Core/Controller.php": """<?php
namespace RestauranteSaas\\Core;

use RestauranteSaas\\Core\\HTTP\\Request;
use RestauranteSaas\\Core\\HTTP\\Response;

/**
 * Controlador base para todos os controladores da aplicação
 */
abstract class Controller
{
    protected $app;
    protected $request;
    protected $response;
    protected $view;
    
    /**
     * Construtor
     */
    public function __construct()
    {
        $this->app = App::getInstance();
        $this->request = new Request();
        $this->response = new Response();
        $this->view = new View();
    }
    
    /**
     * Renderiza uma view
     */
    protected function view($template, $data = [])
    {
        return $this->view->render($template, $data);
    }
    
    /**
     * Retorna uma resposta JSON
     */
    protected function json($data, $status = 200, $headers = [])
    {
        return $this->response
            ->setContent($data)
            ->setContentType('application/json')
            ->setStatus($status)
            ->setHeaders($headers);
    }
    
    /**
     * Redireciona para outra URL
     */
    protected function redirect($url, $status = 302)
    {
        return $this->response
            ->setStatus($status)
            ->setHeader('Location', $url);
    }
    
    /**
     * Redireciona para uma rota nomeada
     */
    protected function redirectToRoute($name, $params = [], $status = 302)
    {
        $router = $this->app->get('router');
        $url = $router->url($name, $params);
        
        return $this->redirect($url, $status);
    }
    
    /**
     * Valida os dados da requisição
     */
    protected function validate($rules, $messages = [])
    {
        $validator = new Validation\\Validator();
        $data = $this->request->all();
        
        $result = $validator->validate($data, $rules, $messages);
        
        if (!$result->isValid()) {
            throw new Exceptions\\ValidationException('Erro de validação', $result->getErrors());
        }
        
        return $data;
    }
    
    /**
     * Obtém o modelo pelo ID ou lança exceção
     */
    protected function findModelOrFail($modelClass, $id)
    {
        $model = new $modelClass();
        return $model->findOrFail($id);
    }
    
    /**
     * Verifica se o usuário tem permissão
     */
    protected function authorize($permission)
    {
        $auth = $this->app->get('auth');
        
        if (!$auth->check()) {
            throw new Exceptions\\AuthException('Não autenticado');
        }
        
        if (!$auth->hasPermission($permission)) {
            throw new Exceptions\\AuthException('Acesso não autorizado');
        }
        
        return true;
    }
}
""",
            "src/Core/Model.php": """<?php
namespace RestauranteSaas\\Core;

use RestauranteSaas\\Core\\Exceptions\\ModelException;

/**
 * Modelo base para todos os modelos da aplicação
 */
abstract class Model
{
    protected $table;
    protected $primaryKey = 'id';
    protected $fillable = [];
    protected $guarded = ['id'];
    protected $db;
    protected $attributes = [];
    protected $original = [];
    protected $relations = [];
    protected $exists = false;
    protected $timestamps = true;
    
    /**
     * Construtor
     */
    public function __construct(array $attributes = [])
    {
        $this->db = App::getInstance()->get('db');
        
        if (!$this->table) {
            // Deriva o nome da tabela a partir do nome da classe, se não definido
            $reflection = new \\ReflectionClass($this);
            $this->table = strtolower($reflection->getShortName()) . 's';
        }
        
        $this->fill($attributes);
    }
    
    /**
     * Preenche o modelo com atributos
     */
    public function fill(array $attributes)
    {
        foreach ($attributes as $key => $value) {
            if ($this->isFillable($key)) {
                $this->setAttribute($key, $value);
            }
        }
        
        return $this;
    }
    
    /**
     * Verifica se um atributo é preenchível
     */
    public function isFillable($key)
    {
        if (in_array($key, $this->guarded)) {
            return false;
        }
        
        return empty($this->fillable) || in_array($key, $this->fillable);
    }
    
    /**
     * Define um atributo
     */
    public function setAttribute($key, $value)
    {
        $this->attributes[$key] = $value;
        return $this;
    }
    
    /**
     * Obtém um atributo
     */
    public function getAttribute($key)
    {
        if (!isset($this->attributes[$key])) {
            return null;
        }
        
        return $this->attributes[$key];
    }
    
    /**
     * Método mágico para obter atributos
     */
    public function __get($key)
    {
        return $this->getAttribute($key);
    }
    
    /**
     * Método mágico para definir atributos
     */
    public function __set($key, $value)
    {
        $this->setAttribute($key, $value);
    }
    
    /**
     * Método mágico para verificar se existe um atributo
     */
    public function __isset($key)
    {
        return isset($this->attributes[$key]);
    }
    
    /**
     * Obtém todos os atributos
     */
    public function getAttributes()
    {
        return $this->attributes;
    }
    
    /**
     * Encontra um registro pelo ID
     */
    public function find($id)
    {
        $result = $this->db->select($this->table, '*', "{$this->primaryKey} = ?", [$id]);
        
        if ($result->rowCount() === 0) {
            return null;
        }
        
        $model = new static($result->fetch());
        $model->exists = true;
        $model->original = $model->attributes;
        
        return $model;
    }
    
    /**
     * Encontra um registro ou falha
     */
    public function findOrFail($id)
    {
        $model = $this->find($id);
        
        if ($model === null) {
            throw new ModelException("Registro com ID {$id} não encontrado na tabela {$this->table}");
        }
        
        return $model;
    }
    
    /**
     * Obtém todos os registros
     */
    public function all()
    {
        $result = $this->db->select($this->table);
        
        $models = [];
        foreach ($result->fetchAll() as $attributes) {
            $model = new static($attributes);
            $model->exists = true;
            $model->original = $model->attributes;
            $models[] = $model;
        }
        
        return $models;
    }
    
    /**
     * Salva o modelo
     */
    public function save()
    {
        if ($this->exists) {
            return $this->update();
        }
        
        return $this->insert();
    }
    
    /**
     * Insere um novo registro
     */
    private function insert()
    {
        // Preenche timestamps se habilitado
        if ($this->timestamps) {
            $now = date('Y-m-d H:i:s');
            $this->attributes['created_at'] = $now;
            $this->attributes['updated_at'] = $now;
        }
        
        // Filtra atributos não preenchíveis
        $attributes = array_filter($this->attributes, function($key) {
            return $this->isFillable($key);
        }, ARRAY_FILTER_USE_KEY);
        
        $id = $this->db->insert($this->table, $attributes);
        
        $this->attributes[$this->primaryKey] = $id;
        $this->exists = true;
        $this->original = $this->attributes;
        
        return true;
    }
    
    /**
     * Atualiza um registro existente
     */
    private function update()
    {
        if (!isset($this->attributes[$this->primaryKey])) {
            throw new ModelException("Não é possível atualizar o modelo sem chave primária");
        }
        
        // Atualiza timestamp se habilitado
        if ($this->timestamps) {
            $this->attributes['updated_at'] = date('Y-m-d H:i:s');
        }
        
        // Obtém apenas atributos modificados
        $dirty = array_diff_assoc($this->attributes, $this->original);
        
        // Filtra chave primária e atributos não preenchíveis
        $dirty = array_filter($dirty, function($key) {
            return $key !== $this->primaryKey && $this->isFillable($key);
        }, ARRAY_FILTER_USE_KEY);
        
        if (empty($dirty)) {
            return true; // Nenhuma alteração para salvar
        }
        
        $this->db->update($this->table, $dirty, "{$this->primaryKey} = ?", [$this->attributes[$this->primaryKey]]);
        
        $this->original = $this->attributes;
        
        return true;
    }
    
    /**
     * Exclui o modelo
     */
    public function delete()
    {
        if (!$this->exists) {
            throw new ModelException("Não é possível excluir o modelo que não existe");
        }
        
        if (!isset($this->attributes[$this->primaryKey])) {
            throw new ModelException("Não é possível excluir o modelo sem chave primária");
        }
        
        $this->db->delete($this->table, "{$this->primaryKey} = ?", [$this->attributes[$this->primaryKey]]);
        
        $this->exists = false;
        
        return true;
    }
    
    /**
     * Cria uma nova instância do modelo
     */
    public static function create(array $attributes)
    {
        $model = new static($attributes);
        $model->save();
        
        return $model;
    }
    
    /**
     * Executa uma consulta where
     */
    public function where($column, $operator, $value = null)
    {
        // Trata sintaxe de dois argumentos: where('coluna', 'valor')
        if ($value === null) {
            $value = $operator;
            $operator = '=';
        }
        
        $result = $this->db->select($this->table, '*', "$column $operator ?", [$value]);
        
        $models = [];
        foreach ($result->fetchAll() as $attributes) {
            $model = new static($attributes);
            $model->exists = true;
            $model->original = $model->attributes;
            $models[] = $model;
        }
        
        return $models;
    }
    
    /**
     * Obtém o primeiro registro que corresponde aos critérios
     */
    public function firstWhere($column, $operator, $value = null)
    {
        $models = $this->where($column, $operator, $value);
        
        return !empty($models) ? $models[0] : null;
    }
    
    /**
     * Conta registros
     */
    public function count()
    {
        $result = $this->db->select($this->table, 'COUNT(*) as count');
        return (int) $result->fetch()['count'];
    }
}
""",
            "src/Core/View.php": """<?php
namespace RestauranteSaas\\Core;

use RestauranteSaas\\Core\\Exceptions\\AppException;

/**
 * Sistema de renderização de views
 */
class View
{
    private $layout = 'layouts/app';
    private $sections = [];
    private $sectionStack = [];
    private $viewPath = 'resources/views';
    
    /**
     * Renderiza uma view
     */
    public function render($template, $data = [])
    {
        $app = App::getInstance();
        $response = new HTTP\\Response();
        
        // Extrai os dados para a view
        extract($data);
        
        // Inicia o buffer de saída
        ob_start();
        
        // Inclui o template
        $templatePath = $this->resolvePath($template);
        
        if (!file_exists($templatePath)) {
            throw new AppException("View não encontrada: {$template}");
        }
        
        include $templatePath;
        
        // Captura o conteúdo do template
        $content = ob_get_clean();
        
        // Se temos um layout, renderiza o layout com o conteúdo
        if ($this->layout) {
            $this->sections['content'] = $content;
            
            ob_start();
            
            $layoutPath = $this->resolvePath($this->layout);
            
            if (!file_exists($layoutPath)) {
                throw new AppException("Layout não encontrado: {$this->layout}");
            }
            
            include $layoutPath;
            
            $content = ob_get_clean();
        }
        
        return $response->setContent($content)->setContentType('text/html');
    }
    
    /**
     * Define o layout a ser usado
     */
    public function setLayout($layout)
    {
        $this->layout = $layout;
        return $this;
    }
    
    /**
     * Desativa o uso de layout
     */
    public function withoutLayout()
    {
        $this->layout = null;
        return $this;
    }
    
    /**
     * Inicia uma seção
     */
    public function section($name)
    {
        $this->sectionStack[] = $name;
        ob_start();
    }
    
    /**
     * Finaliza a seção atual
     */
    public function endSection()
    {
        if (empty($this->sectionStack)) {
            throw new AppException("Não há seção para finalizar");
        }
        
        $name = array_pop($this->sectionStack);
        $this->sections[$name] = ob_get_clean();
    }
    
    /**
     * Exibe uma seção
     */
    public function yield($name)
    {
        echo $this->sections[$name] ?? '';
    }
    
    /**
     * Inclui outra view
     */
    public function include($template, $data = [])
    {
        extract($data);
        
        $templatePath = $this->resolvePath($template);
        
        if (!file_exists($templatePath)) {
            throw new AppException("View incluída não encontrada: {$template}");
        }
        
        include $templatePath;
    }
    
    /**
     * Resolve o caminho completo para um template
     */
    private function resolvePath($template)
    {
        return BASE_PATH . '/' . $this->viewPath . '/' . $template . '.php';
    }
    
    /**
     * Escapa string HTML para segurança
     */
    public function e($value)
    {
        return htmlspecialchars($value, ENT_QUOTES, 'UTF-8');
    }
    
    /**
     * Gera uma URL completa
     */
    public function url($path)
    {
        $app = App::getInstance();
        $baseUrl = $app->config('app.url');
        
        return rtrim($baseUrl, '/') . '/' . ltrim($path, '/');
    }
    
    /**
     * Gera uma URL para asset
     */
    public function asset($path)
    {
        return $this->url('assets/' . ltrim($path, '/'));
    }
}
""",
            "src/Core/Exceptions/AppException.php": """<?php
namespace RestauranteSaas\\Core\\Exceptions;

/**
 * Exceção base da aplicação
 */
class AppException extends \\Exception
{
    protected $context = [];
    
    /**
     * Construtor
     */
    public function __construct($message = "", $code = 0, \\Throwable $previous = null, array $context = [])
    {
        parent::__construct($message, $code, $previous);
        $this->context = $context;
    }
    
    /**
     * Obtém o contexto da exceção
     */
    public function getContext()
    {
        return $this->context;
    }
    
    /**
     * Define o contexto da exceção
     */
    public function setContext(array $context)
    {
        $this->context = $context;
        return $this;
    }
}
""",
            "src/Core/Database/Connection.php": """<?php
namespace RestauranteSaas\\Core\\Database;

use RestauranteSaas\\Core\\Exceptions\\DatabaseException;
use RestauranteSaas\\Core\\App;

/**
 * Gerencia conexões com o banco de dados
 */
class Connection
{
    private $pdo;
    private $tenantId = null;
    private $config;
    private $queryLog = [];
    private $isLoggingEnabled = false;
    
    /**
     * Construtor
     */
    public function __construct(array $config)
    {
        $this->config = $config;
        $this->connect();
        
        $app = App::getInstance();
        $this->isLoggingEnabled = $app->config('app.environment') === 'development';
    }
    
    /**
     * Estabelece a conexão com o banco de dados
     */
    private function connect()
    {
        $dsn = "mysql:host={$this->config['connections']['mysql']['host']};dbname={$this->config['connections']['mysql']['database']};charset=utf8mb4";
        
        $options = [
            \\PDO::ATTR_ERRMODE => \\PDO::ERRMODE_EXCEPTION,
            \\PDO::ATTR_DEFAULT_FETCH_MODE => \\PDO::FETCH_ASSOC,
            \\PDO::ATTR_EMULATE_PREPARES => false,
            \\PDO::MYSQL_ATTR_INIT_COMMAND => "SET NAMES utf8mb4 COLLATE utf8mb4_unicode_ci"
        ];
        
        try {
            $this->pdo = new \\PDO(
                $dsn,
                $this->config['connections']['mysql']['username'],
                $this->config['connections']['mysql']['password'],
                $options
            );
        } catch (\\PDOException $e) {
            throw new DatabaseException("Falha na conexão com o banco de dados: " . $e->getMessage());
        }
    }
    
    /**
     * Define o ID do tenant atual
     */
    public function setTenant($tenantId)
    {
        $this->tenantId = $tenantId;
    }
    
    /**
     * Executa uma consulta SELECT
     */
    public function select($table, $columns = '*', $where = null, $params = [], $orderBy = null, $limit = null, $offset = null)
    {
        $query = "SELECT $columns FROM $table";
        
        // Aplica filtro de tenant se o ID do tenant estiver definido e a tabela tiver uma coluna de tenant
        if ($this->tenantId && $this->tableHasTenantColumn($table)) {
            $query .= $where ? " WHERE tenant_id = ? AND $where" : " WHERE tenant_id = ?";
            array_unshift($params, $this->tenantId);
        } elseif ($where) {
            $query .= " WHERE $where";
        }
        
        if ($orderBy) {
            $query .= " ORDER BY $orderBy";
        }
        
        if ($limit) {
            $query .= " LIMIT $limit";
            
            if ($offset) {
                $query .= " OFFSET $offset";
            }
        }
        
        return $this->query($query, $params);
    }
    
    /**
     * Executa uma consulta INSERT
     */
    public function insert($table, $data)
    {
        // Adiciona o ID do tenant aos dados se o ID do tenant estiver definido e a tabela tiver uma coluna de tenant
        if ($this->tenantId && $this->tableHasTenantColumn($table)) {
            $data['tenant_id'] = $this->tenantId;
        }
        
        $columns = implode(', ', array_keys($data));
        $placeholders = implode(', ', array_fill(0, count($data), '?'));
        
        $query = "INSERT INTO $table ($columns) VALUES ($placeholders)";
        
        $this->query($query, array_values($data));
        
        return $this->pdo->lastInsertId();
    }
    
    /**
     * Executa uma consulta UPDATE
     */
    public function update($table, $data, $where = null, $params = [])
    {
        $sets = [];
        foreach (array_keys($data) as $column) {
            $sets[] = "$column = ?";
        }
        
        $query = "UPDATE $table SET " . implode(', ', $sets);
        
        // Aplica filtro de tenant se o ID do tenant estiver definido e a tabela tiver uma coluna de tenant
        if ($this->tenantId && $this->tableHasTenantColumn($table)) {
            $query .= $where ? " WHERE tenant_id = ? AND $where" : " WHERE tenant_id = ?";
            array_push($params, $this->tenantId);
        } elseif ($where) {
            $query .= " WHERE $where";
        }
        
        return $this->query($query, array_merge(array_values($data), $params))->rowCount();
    }
    
    /**
     * Executa uma consulta DELETE
     */
    public function delete($table, $where = null, $params = [])
    {
        $query = "DELETE FROM $table";
        
        // Aplica filtro de tenant se o ID do tenant estiver definido e a tabela tiver uma coluna de tenant
        if ($this->tenantId && $this->tableHasTenantColumn($table)) {
            $query .= $where ? " WHERE tenant_id = ? AND $where" : " WHERE tenant_id = ?";
            array_unshift($params, $this->tenantId);
        } elseif ($where) {
            $query .= " WHERE $where";
        }
        
        return $this->query($query, $params)->rowCount();
    }
    
    /**
     * Executa uma consulta bruta
     */
    public function query($query, $params = [])
    {
        $startTime = microtime(true);
        
        try {
            $stmt = $this->pdo->prepare($query);
            $stmt->execute($params);
            
            if ($this->isLoggingEnabled) {
                $endTime = microtime(true);
                $executionTime = round(($endTime - $startTime) * 1000, 2); // em milissegundos
                $this->logQuery($query, $params, $executionTime);
            }
            
            return $stmt;
        } catch (\\PDOException $e) {
            throw new DatabaseException("Falha na execução da consulta: " . $e->getMessage() . "\\nConsulta: $query");
        }
    }
    
    /**
     * Inicia uma transação
     */
    public function beginTransaction()
    {
        return $this->pdo->beginTransaction();
    }
    
    /**
     * Confirma uma transação
     */
    public function commit()
    {
        return $this->pdo->commit();
    }
    
    /**
     * Reverte uma transação
     */
    public function rollback()
    {
        return $this->pdo->rollBack();
    }
    
    /**
     * Obtém a instância do PDO
     */
    public function getPdo()
    {
        return $this->pdo;
    }
    
    /**
     * Verifica se uma tabela tem uma coluna de tenant
     */
    private function tableHasTenantColumn($table)
    {
        // Lista de tabelas que não possuem coluna tenant_id
        $tablesWithoutTenant = ['tenants', 'plans', 'permissions', 'platform_admins'];
        
        return !in_array($table, $tablesWithoutTenant);
    }
    
    /**
     * Registra uma consulta para depuração
     */
    private function logQuery($query, $params, $executionTime)
    {
        $this->queryLog[] = [
            'query' => $query,
            'params' => $params,
            'execution_time' => $executionTime . 'ms',
            'time' => date('Y-m-d H:i:s')
        ];
        
        // Mantém apenas as últimas 100 consultas no log
        if (count($this->queryLog) > 100) {
            array_shift($this->queryLog);
        }
    }
    
    /**
     * Obtém o log de consultas
     */
    public function getQueryLog()
    {
        return $this->queryLog;
    }
}
""",
            "src/Core/ErrorHandler.php": """<?php
namespace RestauranteSaas\\Core;

use RestauranteSaas\\Core\\Exceptions\\AppException;
use RestauranteSaas\\Core\\Exceptions\\ValidationException;
use RestauranteSaas\\Core\\HTTP\\Response;

/**
 * Sistema de tratamento de erros e exceções
 */
class ErrorHandler
{
    private $debug;
    
    /**
     * Construtor
     */
    public function __construct($debug = false)
    {
        $this->debug = $debug;
    }
    
    /**
     * Registra os handlers de erro e exceção
     */
    public function register()
    {
        error_reporting(E_ALL);
        set_error_handler([$this, 'handleError']);
        set_exception_handler([$this, 'handleException']);
        register_shutdown_function([$this, 'handleShutdown']);
    }
    
    /**
     * Trata erros de PHP
     */
    public function handleError($level, $message, $file, $line)
    {
        if (!(error_reporting() & $level)) {
            // Este código de erro não está incluído em error_reporting
            return;
        }
        
        throw new \\ErrorException($message, 0, $level, $file, $line);
    }
    
    /**
     * Trata exceções não capturadas
     */
    public function handleException($exception)
    {
        $this->logException($exception);
        
        if (php_sapi_name() === 'cli') {
            $this->renderCliException($exception);
        } else {
            $this->renderHttpException($exception);
        }
    }
    
    /**
     * Trata erros fatais
     */
    public function handleShutdown()
    {
        $error = error_get_last();
        
        if ($error !== null && in_array($error['type'], [E_ERROR, E_PARSE, E_CORE_ERROR, E_COMPILE_ERROR])) {
            $this->handleError($error['type'], $error['message'], $error['file'], $error['line']);
        }
    }
    
    /**
     * Registra a exceção
     */
    private function logException($exception)
    {
        $message = sprintf(
            "[%s] %s in %s on line %d\\n%s\\n",
            get_class($exception),
            $exception->getMessage(),
            $exception->getFile(),
            $exception->getLine(),
            $exception->getTraceAsString()
        );
        
        error_log($message);
        
        // Registro adicional para tipos específicos de exceção
        if ($exception instanceof ValidationException) {
            error_log("Erros de validação: " . json_encode($exception->getErrors()));
        }
    }
    
    /**
     * Renderiza a exceção para CLI
     */
    private function renderCliException($exception)
    {
        echo "\\033[31mErro: " . $exception->getMessage() . "\\033[0m\\n";
        
        if ($this->debug) {
            echo "\\nArquivo: " . $exception->getFile() . " (Linha: " . $exception->getLine() . ")\\n";
            echo "\\nStack Trace:\\n" . $exception->getTraceAsString() . "\\n";
        }
    }
    
    /**
     * Renderiza a exceção para HTTP
     */
    private function renderHttpException($exception)
    {
        $statusCode = 500;
        
        // Determina o código de status com base no tipo de exceção
        if ($exception instanceof ValidationException) {
            $statusCode = 422;
        } elseif ($exception instanceof \\RestauranteSaas\\Core\\Exceptions\\ModelException) {
            $statusCode = 404;
        } elseif ($exception instanceof \\RestauranteSaas\\Core\\Exceptions\\AuthException) {
            $statusCode = 401;
        }
        
        // Define cabeçalhos de resposta HTTP
        $response = new Response();
        $response->setStatus($statusCode);
        
        // Verifica se a requisição espera JSON
        $acceptHeader = $_SERVER['HTTP_ACCEPT'] ?? '';
        $isJsonRequest = strpos($acceptHeader, 'application/json') !== false;
        
        if ($isJsonRequest) {
            $this->renderJsonException($exception, $response);
        } else {
            $this->renderHtmlException($exception, $response);
        }
        
        $response->send();
    }
    
    /**
     * Renderiza exceção como JSON
     */
    private function renderJsonException($exception, $response)
    {
        $responseData = [
            'error' => true,
            'message' => $exception->getMessage()
        ];
        
        // Adiciona informações de depuração se estiver no modo debug
        if ($this->debug) {
            $responseData['debug'] = [
                'type' => get_class($exception),
                'file' => $exception->getFile(),
                'line' => $exception->getLine(),
                'trace' => explode("\\n", $exception->getTraceAsString())
            ];
        }
        
        // Adiciona erros de validação se disponíveis
        if ($exception instanceof ValidationException) {
            $responseData['errors'] = $exception->getErrors();
        }
        
        $response->setContentType('application/json');
        $response->setContent($responseData);
    }
    
    /**
     * Renderiza exceção como HTML
     */
    private function renderHtmlException($exception, $response)
    {
        $statusCode = $response->getStatusCode();
        
        // Tenta encontrar uma view de erro personalizada
        $errorView = "errors/{$statusCode}";
        $genericErrorView = "errors/generic";
        
        $view = new View();
        
        try {
            $content = $view->render($errorView, [
                'exception' => $exception,
                'debug' => $this->debug
            ])->getContent();
        } catch (\\Exception $e) {
            // Fallback para a view de erro genérica
            try {
                $content = $view->render($genericErrorView, [
                    'exception' => $exception,
                    'statusCode' => $statusCode,
                    'debug' => $this->debug
                ])->getContent();
            } catch (\\Exception $e) {
                // Fallback para HTML simples se as views não estiverem disponíveis
                $content = $this->getBasicErrorHtml($exception, $statusCode);
            }
        }
        
        $response->setContentType('text/html');
        $response->setContent($content);
    }
    
    /**
     * Gera HTML básico para erro quando as views não estão disponíveis
     */
    private function getBasicErrorHtml($exception, $statusCode)
    {
        $title = $statusCode . ' - ' . $this->getStatusText($statusCode);
        $message = $this->debug ? $exception->getMessage() : 'Ocorreu um erro na aplicação.';
        
        $html = "<!DOCTYPE html>
<html>
<head>
    <meta charset='UTF-8'>
    <meta name='viewport' content='width=device-width, initial-scale=1.0'>
    <title>{$title}</title>
    <style>
        body { font-family: Arial, sans-serif; line-height: 1.6; color: #333; margin: 0; padding: 20px; }
        .container { max-width: 800px; margin: 0 auto; }
        .error-code { font-size: 72px; color: #e74c3c; margin: 0; }
        .error-title { margin-top: 0; color: #555; }
        .error-message { background: #f8f8f8; padding: 15px; border-radius: 3px; }
        .error-stack { background: #f1f1f1; padding: 15px; font-family: monospace; font-size: 14px; overflow-x: auto; }
    </style>
</head>
<body>
    <div class='container'>
        <h1 class='error-code'>{$statusCode}</h1>
        <h2 class='error-title'>{$this->getStatusText($statusCode)}</h2>
        <div class='error-message'>{$message}</div>";
        
        if ($this->debug) {
            $html .= "
        <p><strong>Arquivo:</strong> {$exception->getFile()} (Linha: {$exception->getLine()})</p>
        <div class='error-stack'>
            <strong>Stack Trace:</strong><br>
            " . nl2br(htmlspecialchars($exception->getTraceAsString())) . "
        </div>";
        }
        
        $html .= "
    </div>
</body>
</html>";
        
        return $html;
    }
    
    /**
     * Obtém o texto correspondente ao código de status HTTP
     */
    private function getStatusText($statusCode)
    {
        $statusTexts = [
            400 => 'Bad Request',
            401 => 'Unauthorized',
            403 => 'Forbidden',
            404 => 'Not Found',
            422 => 'Unprocessable Entity',
            500 => 'Internal Server Error',
        ];
        
        return $statusTexts[$statusCode] ?? 'Error';
    }
}
""",
            "src/Core/Auth/Auth.php": """<?php
namespace RestauranteSaas\\Core\\Auth;

use RestauranteSaas\\Core\\Exceptions\\AuthException;
use RestauranteSaas\\Core\\App;
use RestauranteSaas\\Core\\Database\\Connection;

/**
 * Sistema de autenticação
 */
class Auth
{
    private $db;
    private $session;
    private $user = null;
    
    /**
     * Construtor
     */
    public function __construct(Connection $db, Session $session)
    {
        $this->db = $db;
        $this->session = $session;
        
        // Carrega o usuário da sessão, se estiver autenticado
        $this->loadUser();
    }
    
    /**
     * Carrega o usuário da sessão
     */
    private function loadUser()
    {
        $userId = $this->session->get('auth_user_id');
        
        if ($userId) {
            $result = $this->db->select('users', '*', "id = ?", [$userId]);
            
            if ($result->rowCount() > 0) {
                $this->user = $result->fetch();
            } else {
                // Usuário não encontrado, limpa a sessão
                $this->logout();
            }
        }
    }
    
    /**
     * Tenta autenticar um usuário com email e senha
     */
    public function attempt($email, $password, $remember = false)
    {
        $result = $this->db->select('users', '*', "email = ? AND active = 1", [$email]);
        
        if ($result->rowCount() === 0) {
            return false;
        }
        
        $user = $result->fetch();
        
        // Verifica se a conta está bloqueada
        if (!empty($user['locked_until']) && new \\DateTime($user['locked_until']) > new \\DateTime()) {
            throw new AuthException("Conta bloqueada temporariamente devido a tentativas de login mal-sucedidas");
        }
        
        // Verifica a senha
        if (!password_verify($password, $user['password'])) {
            // Incrementa o contador de tentativas de login
            $this->incrementLoginAttempts($user['id']);
            return false;
        }
        
        // Redefine as tentativas de login
        $this->resetLoginAttempts($user['id']);
        
        // Atualiza a hash da senha se necessário
        if (password_needs_rehash($user['password'], PASSWORD_DEFAULT)) {
            $this->updatePassword($user['id'], $password);
        }
        
        // Registra o login
        $this->registerLogin($user['id']);
        
        // Armazena o ID do usuário na sessão
        $this->session->set('auth_user_id', $user['id']);
        
        // Define o token de lembrete, se solicitado
        if ($remember) {
            $this->setRememberToken($user['id']);
        }
        
        $this->user = $user;
        
        return true;
    }
    
    /**
     * Incrementa o contador de tentativas de login
     */
    private function incrementLoginAttempts($userId)
    {
        $result = $this->db->select('users', 'login_attempts', "id = ?", [$userId]);
        $user = $result->fetch();
        
        $attempts = $user['login_attempts'] + 1;
        $app = App::getInstance();
        $maxAttempts = $app->config('app.security.max_login_attempts', 5);
        
        if ($attempts >= $maxAttempts) {
            // Bloqueia a conta temporariamente
            $lockoutTime = $app->config('app.security.lockout_time', 15);
            $lockedUntil = date('Y-m-d H:i:s', strtotime("+{$lockoutTime} minutes"));
            
            $this->db->update('users', [
                'login_attempts' => 0,
                'locked_until' => $lockedUntil
            ], "id = ?", [$userId]);
        } else {
            $this->db->update('users', [
                'login_attempts' => $attempts
            ], "id = ?", [$userId]);
        }
    }
    
    /**
     * Redefine o contador de tentativas de login
     */
    private function resetLoginAttempts($userId)
    {
        $this->db->update('users', [
            'login_attempts' => 0,
            'locked_until' => null
        ], "id = ?", [$userId]);
    }
    
    /**
     * Atualiza a senha do usuário
     */
    private function updatePassword($userId, $password)
    {
        $this->db->update('users', [
            'password' => password_hash($password, PASSWORD_DEFAULT)
        ], "id = ?", [$userId]);
    }
    
    /**
     * Registra o login do usuário
     */
    private function registerLogin($userId)
    {
        $this->db->update('users', [
            'last_login' => date('Y-m-d H:i:s'),
            'last_ip' => $_SERVER['REMOTE_ADDR'] ?? null
        ], "id = ?", [$userId]);
    }
    
    /**
     * Define o token de lembrete para o usuário
     */
    private function setRememberToken($userId)
    {
        $token = bin2hex(random_bytes(32));
        
        $this->db->update('users', [
            'remember_token' => $token
        ], "id = ?", [$userId]);
        
        // Define o cookie de lembrete (30 dias)
        setcookie('remember_token', $token, time() + 60 * 60 * 24 * 30, '/', '', false, true);
    }
    
    /**
     * Efetua o logout do usuário
     */
    public function logout()
    {
        // Limpa o token de lembrete, se existir
        if ($this->user) {
            $this->db->update('users', [
                'remember_token' => null
            ], "id = ?", [$this->user['id']]);
            
            // Remove o cookie de lembrete
            setcookie('remember_token', '', time() - 3600, '/', '', false, true);
        }
        
        // Limpa a sessão
        $this->session->remove('auth_user_id');
        
        $this->user = null;
    }
    
    /**
     * Verifica se o usuário está autenticado
     */
    public function check()
    {
        return $this->user !== null;
    }
    
    /**
     * Verifica se o usuário não está autenticado
     */
    public function guest()
    {
        return !$this->check();
    }
    
    /**
     * Obtém o usuário autenticado
     */
    public function user()
    {
        return $this->user;
    }
    
    /**
     * Obtém o ID do usuário autenticado
     */
    public function id()
    {
        return $this->user ? $this->user['id'] : null;
    }
    
    /**
     * Verifica se o usuário tem uma determinada função
     */
    public function hasRole($role)
    {
        if (!$this->check()) {
            return false;
        }
        
        // Verifica função direta no campo 'role'
        if ($this->user['role'] === $role) {
            return true;
        }
        
        // Verifica nas funções relacionadas
        $userId = $this->user['id'];
        $result = $this->db->query(
            "SELECT r.name FROM roles r
             JOIN user_roles ur ON r.id = ur.role_id
             WHERE ur.user_id = ? AND r.name = ?",
            [$userId, $role]
        );
        
        return $result->rowCount() > 0;
    }
    
    /**
     * Verifica se o usuário tem uma determinada permissão
     */
    public function hasPermission($permission)
    {
        if (!$this->check()) {
            return false;
        }
        
        // Usuários administradores têm todas as permissões
        if ($this->user['role'] === 'admin') {
            return true;
        }
        
        // Verifica nas permissões relacionadas
        $userId = $this->user['id'];
        $tenantId = App::getInstance()->getCurrentTenant() ? App::getInstance()->getCurrentTenant()->id : null;
        
        $query = "
            SELECT p.name FROM permissions p
            JOIN role_permissions rp ON p.id = rp.permission_id
            JOIN roles r ON rp.role_id = r.id
            JOIN user_roles ur ON r.id = ur.role_id
            WHERE ur.user_id = ? AND p.name = ?
        ";
        
        $params = [$userId, $permission];
        
        if ($tenantId) {
            $query .= " AND (rp.tenant_id IS NULL OR rp.tenant_id = ?)";
            $params[] = $tenantId;
        }
        
        $result = $this->db->query($query, $params);
        
        return $result->rowCount() > 0;
    }
}
""",
        }
        
        for file_path, content in core_files.items():
            full_path = os.path.join(self.base_dir, file_path)
            os.makedirs(os.path.dirname(full_path), exist_ok=True)
            
            with open(full_path, 'w', encoding='utf-8') as f:
                f.write(content)
            
            self.created_files.append(full_path)
            print(f"  Criado: {full_path}")
            
        return self.created_files
    
    def create_database_files(self):
        """
        Cria os arquivos de migrações de banco de dados.
        """
        print("\nCriando arquivos de migração de banco de dados...")
        
        migrations = {
            "database/migrations/001_create_tenants_table.php": """<?php
/**
 * Migração para criar a tabela de tenants (restaurantes)
 */

namespace RestauranteSaas\\Database\\Migrations;

use RestauranteSaas\\Core\\Database\\Migration;

class CreateTenantsTable extends Migration
{
    /**
     * Executa a migração
     */
    public function up()
    {
        $this->db->query("
            CREATE TABLE IF NOT EXISTS tenants (
                id INT UNSIGNED PRIMARY KEY AUTO_INCREMENT,
                name VARCHAR(100) NOT NULL,
                slug VARCHAR(100) NOT NULL UNIQUE,
                domain VARCHAR(255) UNIQUE,
                custom_domain VARCHAR(255) UNIQUE,
                logo VARCHAR(255),
                favicon VARCHAR(255),
                primary_color VARCHAR(20) DEFAULT '#3490dc',
                secondary_color VARCHAR(20) DEFAULT '#38c172',
                phone VARCHAR(20),
                email VARCHAR(100) NOT NULL,
                address TEXT,
                city VARCHAR(100),
                state VARCHAR(100),
                postal_code VARCHAR(20),
                country VARCHAR(100) DEFAULT 'Brasil',
                timezone VARCHAR(50) DEFAULT 'America/Sao_Paulo',
                currency VARCHAR(10) DEFAULT 'BRL',
                locale VARCHAR(20) DEFAULT 'pt_BR',
                tax_id VARCHAR(20),
                tax_regime VARCHAR(50),
                legal_name VARCHAR(100),
                restaurant_type_id INT UNSIGNED,
                subscription_id INT UNSIGNED,
                features JSON,
                settings JSON,
                onboarding_completed BOOLEAN DEFAULT 0,
                active BOOLEAN DEFAULT 1,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
            );
        ");
    }

    /**
     * Reverte a migração
     */
    public function down()
    {
        $this->db->query("DROP TABLE IF EXISTS tenants;");
    }
}
""",
            "database/migrations/002_create_users_table.php": """<?php
/**
 * Migração para criar a tabela de usuários
 */

namespace RestauranteSaas\\Database\\Migrations;

use RestauranteSaas\\Core\\Database\\Migration;

class CreateUsersTable extends Migration
{
    /**
     * Executa a migração
     */
    public function up()
    {
        $this->db->query("
            CREATE TABLE IF NOT EXISTS users (
                id INT UNSIGNED PRIMARY KEY AUTO_INCREMENT,
                tenant_id INT UNSIGNED NULL,
                username VARCHAR(50) NOT NULL UNIQUE,
                email VARCHAR(100) NOT NULL UNIQUE,
                password VARCHAR(255) NOT NULL,
                name VARCHAR(100) NOT NULL,
                first_name VARCHAR(50),
                last_name VARCHAR(50),
                role VARCHAR(30) NOT NULL DEFAULT 'user',
                profile_photo VARCHAR(255),
                phone VARCHAR(20),
                address TEXT,
                birthday DATE,
                gender ENUM('M', 'F', 'O'),
                notes TEXT,
                preferences JSON,
                last_login DATETIME,
                last_ip VARCHAR(45),
                login_attempts TINYINT DEFAULT 0,
                locked_until DATETIME,
                remember_token VARCHAR(100),
                email_verified_at DATETIME,
                two_factor_secret VARCHAR(255),
                two_factor_recovery_codes TEXT,
                active BOOLEAN DEFAULT 1,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
                FOREIGN KEY (tenant_id) REFERENCES tenants(id) ON DELETE CASCADE
            );
        ");
    }

    /**
     * Reverte a migração
     */
    public function down()
    {
        $this->db->query("DROP TABLE IF EXISTS users;");
    }
}
""",
            "database/migrations/003_create_roles_table.php": """<?php
/**
 * Migração para criar a tabela de papéis (roles)
 */

namespace RestauranteSaas\\Database\\Migrations;

use RestauranteSaas\\Core\\Database\\Migration;

class CreateRolesTable extends Migration
{
    /**
     * Executa a migração
     */
    public function up()
    {
        $this->db->query("
            CREATE TABLE IF NOT EXISTS roles (
                id INT UNSIGNED PRIMARY KEY AUTO_INCREMENT,
                tenant_id INT UNSIGNED NULL,
                name VARCHAR(50) NOT NULL,
                description TEXT,
                is_system BOOLEAN DEFAULT 0,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
                UNIQUE KEY role_tenant_unique (name, tenant_id),
                FOREIGN KEY (tenant_id) REFERENCES tenants(id) ON DELETE CASCADE
            );
        ");
    }

    /**
     * Reverte a migração
     */
    public function down()
    {
        $this->db->query("DROP TABLE IF EXISTS roles;");
    }
}
""",
            "database/migrations/004_create_permissions_table.php": """<?php
/**
 * Migração para criar a tabela de permissões
 */

namespace RestauranteSaas\\Database\\Migrations;

use RestauranteSaas\\Core\\Database\\Migration;

class CreatePermissionsTable extends Migration
{
    /**
     * Executa a migração
     */
    public function up()
    {
        $this->db->query("
            CREATE TABLE IF NOT EXISTS permissions (
                id INT UNSIGNED PRIMARY KEY AUTO_INCREMENT,
                name VARCHAR(100) NOT NULL,
                description TEXT,
                module VARCHAR(50) NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
                UNIQUE KEY permission_unique (name)
            );
        ");
    }

    /**
     * Reverte a migração
     */
    public function down()
    {
        $this->db->query("DROP TABLE IF EXISTS permissions;");
    }
}
""",
            "database/migrations/005_create_role_permissions_table.php": """<?php
/**
 * Migração para criar a tabela de relacionamento entre papéis e permissões
 */

namespace RestauranteSaas\\Database\\Migrations;

use RestauranteSaas\\Core\\Database\\Migration;

class CreateRolePermissionsTable extends Migration
{
    /**
     * Executa a migração
     */
    public function up()
    {
        $this->db->query("
            CREATE TABLE IF NOT EXISTS role_permissions (
                role_id INT UNSIGNED NOT NULL,
                permission_id INT UNSIGNED NOT NULL,
                tenant_id INT UNSIGNED NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                PRIMARY KEY (role_id, permission_id, tenant_id),
                FOREIGN KEY (role_id) REFERENCES roles(id) ON DELETE CASCADE,
                FOREIGN KEY (permission_id) REFERENCES permissions(id) ON DELETE CASCADE,
                FOREIGN KEY (tenant_id) REFERENCES tenants(id) ON DELETE CASCADE
            );
        ");
    }

    /**
     * Reverte a migração
     */
    public function down()
    {
        $this->db->query("DROP TABLE IF EXISTS role_permissions;");
    }
}
""",
            "database/migrations/006_create_plans_table.php": """<?php
/**
 * Migração para criar a tabela de planos
 */

namespace RestauranteSaas\\Database\\Migrations;

use RestauranteSaas\\Core\\Database\\Migration;

class CreatePlansTable extends Migration
{
    /**
     * Executa a migração
     */
    public function up()
    {
        $this->db->query("
            CREATE TABLE IF NOT EXISTS plans (
                id INT UNSIGNED PRIMARY KEY AUTO_INCREMENT,
                name VARCHAR(50) NOT NULL,
                description TEXT,
                price DECIMAL(10,2) NOT NULL,
                setup_fee DECIMAL(10,2) DEFAULT 0,
                trial_days INT DEFAULT 0,
                billing_cycle ENUM('monthly', 'quarterly', 'semiannual', 'yearly') DEFAULT 'monthly',
                max_tables INT,
                max_users INT,
                max_items INT,
                max_orders INT,
                features JSON,
                limits JSON,
                stripe_plan_id VARCHAR(100),
                is_public BOOLEAN DEFAULT 1,
                is_custom BOOLEAN DEFAULT 0,
                is_default BOOLEAN DEFAULT 0,
                sort_order INT DEFAULT 0,
                active BOOLEAN DEFAULT 1,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
            );
        ");
    }

    /**
     * Reverte a migração
     */
    public function down()
    {
        $this->db->query("DROP TABLE IF EXISTS plans;");
    }
}
""",
            "database/migrations/007_create_subscriptions_table.php": """<?php
/**
 * Migração para criar a tabela de assinaturas
 */

namespace RestauranteSaas\\Database\\Migrations;

use RestauranteSaas\\Core\\Database\\Migration;

class CreateSubscriptionsTable extends Migration
{
    /**
     * Executa a migração
     */
    public function up()
    {
        $this->db->query("
            CREATE TABLE IF NOT EXISTS subscriptions (
                id INT UNSIGNED PRIMARY KEY AUTO_INCREMENT,
                tenant_id INT UNSIGNED NOT NULL,
                plan_id INT UNSIGNED NOT NULL,
                status ENUM('pending', 'trial', 'active', 'past_due', 'cancelled', 'suspended') DEFAULT 'pending',
                starts_at DATETIME NOT NULL,
                trial_ends_at DATETIME,
                ends_at DATETIME,
                next_billing_date DATETIME,
                last_payment_date DATETIME,
                cancellation_date DATETIME,
                cancellation_reason TEXT,
                payment_method ENUM('credit_card', 'bank_slip', 'pix', 'bank_transfer', 'other') DEFAULT 'credit_card',
                payment_details JSON,
                coupon_code VARCHAR(50),
                coupon_discount DECIMAL(10,2) DEFAULT 0,
                stripe_subscription_id VARCHAR(100),
                stripe_customer_id VARCHAR(100),
                renewal_reminder_sent BOOLEAN DEFAULT 0,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
                FOREIGN KEY (tenant_id) REFERENCES tenants(id) ON DELETE CASCADE,
                FOREIGN KEY (plan_id) REFERENCES plans(id)
            );
        ");
        
        // Atualizar a tabela tenants para adicionar a chave estrangeira
        $this->db->query("
            ALTER TABLE tenants
            ADD CONSTRAINT fk_tenants_subscription
            FOREIGN KEY (subscription_id)
            REFERENCES subscriptions(id);
        ");
    }

    /**
     * Reverte a migração
     */
    public function down()
    {
        // Remover a chave estrangeira da tabela tenants
        $this->db->query("
            ALTER TABLE tenants
            DROP FOREIGN KEY fk_tenants_subscription;
        ");
        
        $this->db->query("DROP TABLE IF EXISTS subscriptions;");
    }
}
"""
        }
        
        for file_path, content in migrations.items():
            full_path = os.path.join(self.base_dir, file_path)
            os.makedirs(os.path.dirname(full_path), exist_ok=True)
            
            with open(full_path, 'w', encoding='utf-8') as f:
                f.write(content)
            
            self.created_files.append(full_path)
            print(f"  Criado: {full_path}")
            
        return self.created_files
        
    def create_root_files(self):
        """
        Cria os arquivos na raiz do projeto.
        """
        print("\nCriando arquivos na raiz do projeto...")
        
        root_files = {
            ".htaccess": """
# Prevent directory listing
Options -Indexes

# Redirect all requests to index.php (except for existing files)
<IfModule mod_rewrite.c>
    RewriteEngine On
    RewriteBase /
    
    # Allow direct access to files in these directories
    RewriteCond %{REQUEST_URI} !^/public/
    
    # If the requested file exists, serve it directly
    RewriteCond %{REQUEST_FILENAME} !-f
    RewriteCond %{REQUEST_FILENAME} !-d
    
    # Otherwise, redirect to index.php
    RewriteRule ^(.*)$ public/index.php [QSA,L]
</IfModule>

# Protect sensitive files
<FilesMatch "^\.env|composer\.json|composer\.lock">
    Order allow,deny
    Deny from all
</FilesMatch>

# Setup proper MIME types
<IfModule mod_mime.c>
    AddType application/javascript .js
    AddType text/css .css
    AddType image/svg+xml .svg
    AddType image/webp .webp
    AddType font/woff .woff
    AddType font/woff2 .woff2
</IfModule>

# Compress output
<IfModule mod_deflate.c>
    AddOutputFilterByType DEFLATE text/html text/plain text/xml text/css application/javascript application/json
</IfModule>

# Set security headers
<IfModule mod_headers.c>
    Header set X-Content-Type-Options "nosniff"
    Header set X-XSS-Protection "1; mode=block"
    Header set X-Frame-Options "SAMEORIGIN"
    Header set Referrer-Policy "strict-origin-when-cross-origin"
</IfModule>
""",
            "index.php": """<?php
/**
 * RestauranteSaaS - Sistema de Gestão de Restaurantes
 *
 * Este é o ponto de entrada principal da aplicação.
 * Redireciona todas as requisições para o front controller em /public/index.php
 */

// Redireciona para o diretório public
header('Location: public/index.php');
exit;
""",
            "composer.json": """{
    "name": "restaurantesaas/sistema",
    "description": "Sistema de Gestão de Restaurantes SaaS",
    "type": "project",
    "license": "proprietary",
    "authors": [
        {
            "name": "Restaurant SaaS Team",
            "email": "contato@restaurantesaas.com"
        }
    ],
    "require": {
        "php": "^8.1",
        "ext-pdo": "*",
        "ext-json": "*",
        "ext-mbstring": "*",
        "ext-gd": "*",
        "vlucas/phpdotenv": "^5.5",
        "stripe/stripe-php": "^10.0",
        "symfony/mailer": "^6.0",
        "endroid/qr-code": "^4.0",
        "nesbot/carbon": "^2.0",
        "filp/whoops": "^2.0",
        "monolog/monolog": "^3.0"
    },
    "require-dev": {
        "phpunit/phpunit": "^10.0",
        "fakerphp/faker": "^1.0",
        "symfony/var-dumper": "^6.0",
        "squizlabs/php_codesniffer": "^3.0"
    },
    "autoload": {
        "psr-4": {
            "RestauranteSaas\\\\": "src/"
        },
        "files": [
            "src/Core/Helpers/functions.php"
        ]
    },
    "autoload-dev": {
        "psr-4": {
            "Tests\\\\": "tests/"
        }
    },
    "scripts": {
        "test": "phpunit",
        "cs": "phpcs --standard=PSR12 src tests",
        "cs-fix": "phpcbf --standard=PSR12 src tests"
    },
    "config": {
        "sort-packages": true,
        "optimize-autoloader": true
    },
    "minimum-stability": "dev",
    "prefer-stable": true
}
""",
            ".env.example": """# Environment: development, production, testing
APP_ENV=development
APP_DEBUG=true
APP_URL=http://localhost/restaurante-sistema
APP_KEY=

# Database Configuration
DB_HOST=localhost
DB_PORT=3306
DB_DATABASE=restaurante_saas
DB_USERNAME=root
DB_PASSWORD=

# Redis Configuration (optional)
REDIS_HOST=127.0.0.1
REDIS_PASSWORD=null
REDIS_PORT=6379

# Email Configuration
MAIL_DRIVER=smtp
MAIL_HOST=mailhog
MAIL_PORT=1025
MAIL_USERNAME=null
MAIL_PASSWORD=null
MAIL_ENCRYPTION=null
MAIL_FROM_ADDRESS=noreply@restaurantesaas.com
MAIL_FROM_NAME="Sistema de Gestão de Restaurantes"

# Stripe Integration
STRIPE_KEY=
STRIPE_SECRET=
STRIPE_WEBHOOK_SECRET=

# PayPal Integration
PAYPAL_CLIENT_ID=
PAYPAL_CLIENT_SECRET=
PAYPAL_ENVIRONMENT=sandbox

# MercadoPago Integration
MP_PUBLIC_KEY=
MP_ACCESS_TOKEN=

# PIX Configuration
PIX_KEY_TYPE=
PIX_KEY=
PIX_MERCHANT_NAME=
PIX_MERCHANT_CITY=

# Logging
LOG_CHANNEL=file
LOG_LEVEL=debug

# Session
SESSION_DRIVER=file
SESSION_LIFETIME=120

# Timezone
TIMEZONE=America/Sao_Paulo
""",
            "public/index.php": """<?php
/**
 * RestauranteSaaS - Sistema de Gestão de Restaurantes
 *
 * Front Controller - Todas as requisições passam por aqui
 */

// Define o caminho base da aplicação
define('BASE_PATH', dirname(__DIR__));

// Carrega o autoloader do Composer
require BASE_PATH . '/vendor/autoload.php';

// Carrega as variáveis de ambiente
if (file_exists(BASE_PATH . '/.env')) {
    $dotenv = \\Dotenv\\Dotenv::createImmutable(BASE_PATH);
    $dotenv->load();
}

// Define o ambiente da aplicação
$environment = getenv('APP_ENV') ?: 'production';

// Configura o tratamento de erros
if ($environment === 'development') {
    error_reporting(E_ALL);
    ini_set('display_errors', 1);
    
    // Usar Whoops para erros em desenvolvimento
    if (class_exists('\\Whoops\\Run')) {
        $whoops = new \\Whoops\\Run;
        $whoops->pushHandler(new \\Whoops\\Handler\\PrettyPageHandler);
        $whoops->register();
    }
} else {
    error_reporting(0);
    ini_set('display_errors', 0);
}

// Inicializa a aplicação
$app = \\RestauranteSaas\\Core\\App::getInstance();

// Executa a aplicação
$app->run();
""",
            "public/.htaccess": """
# Prevent directory listing
Options -Indexes

# Enable rewrite engine
<IfModule mod_rewrite.c>
    RewriteEngine On
    RewriteBase /
    
    # Redirect trailing slashes if not a folder
    RewriteCond %{REQUEST_FILENAME} !-d
    RewriteCond %{REQUEST_URI} (.+)/$
    RewriteRule ^ %1 [L,R=301]
    
    # Allow direct access to asset files
    RewriteCond %{REQUEST_URI} !^/assets/
    
    # If the requested file exists, serve it directly
    RewriteCond %{REQUEST_FILENAME} !-f
    RewriteCond %{REQUEST_FILENAME} !-d
    
    # Otherwise, redirect to index.php
    RewriteRule ^ index.php [L]
</IfModule>

# Cache Control
<IfModule mod_expires.c>
    ExpiresActive On
    
    # Images
    ExpiresByType image/jpeg "access plus 1 year"
    ExpiresByType image/gif "access plus 1 year"
    ExpiresByType image/png "access plus 1 year"
    ExpiresByType image/webp "access plus 1 year"
    ExpiresByType image/svg+xml "access plus 1 year"
    ExpiresByType image/x-icon "access plus 1 year"
    
    # CSS, JavaScript
    ExpiresByType text/css "access plus 1 month"
    ExpiresByType text/javascript "access plus 1 month"
    ExpiresByType application/javascript "access plus 1 month"
    
    # Fonts
    ExpiresByType font/woff "access plus 1 year"
    ExpiresByType font/woff2 "access plus 1 year"
    ExpiresByType application/font-woff "access plus 1 year"
    ExpiresByType application/font-woff2 "access plus 1 year"
</IfModule>

# Set security headers
<IfModule mod_headers.c>
    Header set X-Content-Type-Options "nosniff"
    Header set X-XSS-Protection "1; mode=block"
    Header set X-Frame-Options "SAMEORIGIN"
    Header set Referrer-Policy "strict-origin-when-cross-origin"
    Header set Content-Security-Policy "default-src 'self'; script-src 'self' 'unsafe-inline' 'unsafe-eval' https://js.stripe.com; style-src 'self' 'unsafe-inline'; img-src 'self' data:; font-src 'self' data:; connect-src 'self' https://api.stripe.com;"
</IfModule>
""",
            "routes/web.php": """<?php
/**
 * Rotas web da aplicação
 */

use RestauranteSaas\\Core\\Router;

$router = Router::getInstance();

// Página inicial
$router->get('/', 'HomeController@index', 'home');
$router->get('/about', 'HomeController@about', 'about');
$router->get('/contact', 'HomeController@contact', 'contact');

// Autenticação
$router->get('/login', 'AuthController@showLoginForm', 'login');
$router->post('/login', 'AuthController@login');
$router->get('/register', 'AuthController@showRegistrationForm', 'register');
$router->post('/register', 'AuthController@register');
$router->get('/password/reset', 'AuthController@showLinkRequestForm', 'password.request');
$router->post('/password/email', 'AuthController@sendResetLinkEmail', 'password.email');
$router->get('/password/reset/{token}', 'AuthController@showResetForm', 'password.reset');
$router->post('/password/reset', 'AuthController@reset', 'password.update');
$router->get('/logout', 'AuthController@logout', 'logout');

// Verificação de email
$router->get('/email/verify', 'AuthController@showVerificationNotice', 'verification.notice');
$router->get('/email/verify/{id}/{hash}', 'AuthController@verify', 'verification.verify');
$router->post('/email/resend', 'AuthController@resend', 'verification.resend');

// Registro de tenant/restaurante
$router->get('/register-restaurant', 'RestaurantController@showRegistrationForm', 'restaurant.register');
$router->post('/register-restaurant', 'RestaurantController@register');

// Área do usuário (protegida por autenticação)
$router->group(['prefix' => '/account', 'middleware' => 'auth'], function ($router) {
    $router->get('/', 'AccountController@index', 'account');
    $router->get('/profile', 'AccountController@profile', 'account.profile');
    $router->post('/profile', 'AccountController@updateProfile');
    $router->get('/password', 'AccountController@showPasswordForm', 'account.password');
    $router->post('/password', 'AccountController@updatePassword');
    $router->get('/subscription', 'AccountController@subscription', 'account.subscription');
});

// Área administrativa (protegida por autenticação e permissão admin)
$router->group(['prefix' => '/admin', 'middleware' => ['auth', 'admin']], function ($router) {
    $router->get('/', 'Admin\\DashboardController@index', 'admin.dashboard');
    
    // Gerenciamento de usuários
    $router->get('/users', 'Admin\\UserController@index', 'admin.users');
    $router->get('/users/create', 'Admin\\UserController@create', 'admin.users.create');
    $router->post('/users', 'Admin\\UserController@store', 'admin.users.store');
    $router->get('/users/{id}', 'Admin\\UserController@show', 'admin.users.show');
    $router->get('/users/{id}/edit', 'Admin\\UserController@edit', 'admin.users.edit');
    $router->put('/users/{id}', 'Admin\\UserController@update', 'admin.users.update');
    $router->delete('/users/{id}', 'Admin\\UserController@destroy', 'admin.users.destroy');
    
    // Gerenciamento de restaurantes/tenants
    $router->get('/restaurants', 'Admin\\RestaurantController@index', 'admin.restaurants');
    $router->get('/restaurants/create', 'Admin\\RestaurantController@create', 'admin.restaurants.create');
    $router->post('/restaurants', 'Admin\\RestaurantController@store', 'admin.restaurants.store');
    $router->get('/restaurants/{id}', 'Admin\\RestaurantController@show', 'admin.restaurants.show');
    $router->get('/restaurants/{id}/edit', 'Admin\\RestaurantController@edit', 'admin.restaurants.edit');
    $router->put('/restaurants/{id}', 'Admin\\RestaurantController@update', 'admin.restaurants.update');
    $router->delete('/restaurants/{id}', 'Admin\\RestaurantController@destroy', 'admin.restaurants.destroy');
    
    // Gerenciamento de planos
    $router->get('/plans', 'Admin\\PlanController@index', 'admin.plans');
    $router->get('/plans/create', 'Admin\\PlanController@create', 'admin.plans.create');
    $router->post('/plans', 'Admin\\PlanController@store', 'admin.plans.store');
    $router->get('/plans/{id}', 'Admin\\PlanController@show', 'admin.plans.show');
    $router->get('/plans/{id}/edit', 'Admin\\PlanController@edit', 'admin.plans.edit');
    $router->put('/plans/{id}', 'Admin\\PlanController@update', 'admin.plans.update');
    $router->delete('/plans/{id}', 'Admin\\PlanController@destroy', 'admin.plans.destroy');
    
    // Configurações do sistema
    $router->get('/settings', 'Admin\\SettingsController@index', 'admin.settings');
    $router->post('/settings', 'Admin\\SettingsController@update', 'admin.settings.update');
    
    // Logs do sistema
    $router->get('/logs', 'Admin\\LogController@index', 'admin.logs');
    $router->get('/logs/{id}', 'Admin\\LogController@show', 'admin.logs.show');
});