# Instruções para Rodar a Aplicação com Docker

Este projeto, **m-task**, é um gerenciador de tarefas (Task Manager) construído com Django usando o template [Cookiecutter Django](https://github.com/cookiecutter/cookiecutter-django). Abaixo estão as instruções para rodar a aplicação em ambientes local e produção utilizando Docker.

## Estrutura de Arquivos

- **`docker-compose.local.yml`**: Configuração do Docker Compose para ambiente de desenvolvimento local.
- **`docker-compose.production.yml`**: Configuração do Docker Compose para ambiente de produção.
- **`Dockerfile`**: Arquivo de configuração do Docker para construir a imagem da aplicação.

## Como Rodar a Aplicação

### 1. Ambiente de Desenvolvimento Local

Para rodar a aplicação localmente com Docker, siga os passos abaixo:

1. **Clone o repositório**:
   ```bash
   git clone https://github.com/MeninoNias/m-task.git
   cd m-task
   ```

2. **Crie um arquivo `.env`**:
   Crie um arquivo `.env` na raiz do projeto com as variáveis de ambiente necessárias. Você pode usar o arquivo `.env.example` como base.

3. **Suba os containers**:
   Utilize o `docker-compose.local.yml` para subir os containers:
   ```bash
   docker-compose -f docker-compose.local.yml up --build
   ```

4. **Acesse a aplicação**:
   Após os containers estarem rodando, acesse a aplicação no navegador em:
   ```
   http://localhost:8000
   ```

5. **Crie um superusuário**:
   Para acessar o painel administrativo, crie um superusuário:
   ```bash
   docker-compose -f docker-compose.local.yml exec web python manage.py createsuperuser
   ```

6. **Execute migrações**:
   Certifique-se de que as migrações do banco de dados foram aplicadas:
   ```bash
   docker-compose -f docker-compose.local.yml exec web python manage.py migrate
   ```

### 2. Ambiente de Produção

Para rodar a aplicação em produção, siga os passos abaixo:

1. **Crie um arquivo `.env.production`**:
   Crie um arquivo `.env.production` com as variáveis de ambiente específicas para produção.

2. **Suba os containers**:
   Utilize o `docker-compose.production.yml` para subir os containers em produção:
   ```bash
   docker-compose -f docker-compose.production.yml up --build -d
   ```

3. **Execute migrações**:
   Aplique as migrações do banco de dados:
   ```bash
   docker-compose -f docker-compose.production.yml exec web python manage.py migrate
   ```

4. **Colete arquivos estáticos**:
   Colete os arquivos estáticos para servir em produção:
   ```bash
   docker-compose -f docker-compose.production.yml exec web python manage.py collectstatic --noinput
   ```

5. **Acesse a aplicação**:
   A aplicação estará disponível no endereço configurado no seu servidor (por exemplo, `http://seu-dominio.com`).

## Deploy em Produção

### Pré-requisitos

- Servidor Linux com Docker e Docker Compose instalados
- Domínio configurado apontando para o IP do servidor
- Certificado SSL (Let's Encrypt será configurado automaticamente)

### 1. Preparação do Ambiente

1. **Configure as variáveis de ambiente**:
   Crie os arquivos de ambiente em `.envs/.production/`:

   ```bash
   .envs/
   └── .production/
       ├── .django
       └── .postgres
   ```

   `.django` deve conter:
   ```env
   DJANGO_SETTINGS_MODULE=config.settings.production
   DJANGO_SECRET_KEY=sua-chave-secreta-aqui
   DJANGO_ADMIN_URL=admin/
   DJANGO_ALLOWED_HOSTS=seu-dominio.com
   DJANGO_SERVER_EMAIL=noreply@seu-dominio.com
   
   # AWS
   DJANGO_AWS_ACCESS_KEY_ID=
   DJANGO_AWS_SECRET_ACCESS_KEY=
   DJANGO_AWS_STORAGE_BUCKET_NAME=
   ```

   `.postgres` deve conter:
   ```env
   POSTGRES_HOST=postgres
   POSTGRES_PORT=5432
   POSTGRES_DB=m_task
   POSTGRES_USER=seu-usuario
   POSTGRES_PASSWORD=sua-senha-segura
   ```

2. **Configure o Traefik**:
   Atualize o arquivo `compose/production/traefik/traefik.yml`:
   ```yaml
   # Altere estas configurações
   email: 'seu-email@dominio.com'
   rule: 'Host(`seu-dominio.com`)'
   ```

### 2. Deploy

1. **Clone o repositório no servidor**:
   ```bash
   git clone https://github.com/seu-usuario/m-task.git
   cd m-task
   ```

2. **Construa e inicie os containers**:
   ```bash
   docker-compose -f docker-compose.production.yml up --build -d
   ```

3. **Execute as migrações**:
   ```bash
   docker-compose -f docker-compose.production.yml exec django python manage.py migrate
   ```

4. **Colete arquivos estáticos**:
   ```bash
   docker-compose -f docker-compose.production.yml exec django python manage.py collectstatic --noinput
   ```

5. **Crie um superusuário**:
   ```bash
   docker-compose -f docker-compose.production.yml exec django python manage.py createsuperuser
   ```

### 3. Configurações de Segurança

1. **Firewall**:
   Configure o firewall permitindo apenas as portas necessárias:
   ```bash
   sudo ufw allow 80/tcp
   sudo ufw allow 443/tcp
   sudo ufw enable
   ```

2. **Backup do Banco de Dados**:
   Configure backups automáticos usando o serviço AWS:
   ```bash
   # Backup manual
   docker-compose -f docker-compose.production.yml run --rm awscli upload_db_backup
   ```

### 4. Monitoramento

1. **Logs dos Containers**:
   ```bash
   # Visualizar logs
   docker-compose -f docker-compose.production.yml logs -f

   # Logs específicos
   docker-compose -f docker-compose.production.yml logs -f django
   ```

2. **Status dos Serviços**:
   ```bash
   docker-compose -f docker-compose.production.yml ps
   ```

### 5. Manutenção

1. **Atualização da Aplicação**:
   ```bash
   git pull origin main
   docker-compose -f docker-compose.production.yml up --build -d
   docker-compose -f docker-compose.production.yml exec django python manage.py migrate
   docker-compose -f docker-compose.production.yml exec django python manage.py collectstatic --noinput
   ```

2. **Backup e Restore**:
   ```bash
   # Backup
   docker-compose -f docker-compose.production.yml exec postgres backup

   # Restore
   docker-compose -f docker-compose.production.yml exec postgres restore <backup-file>
   ```

### Troubleshooting

1. **Verificar Logs**:
   ```bash
   docker-compose -f docker-compose.production.yml logs -f service_name
   ```

2. **Reiniciar Serviços**:
   ```bash
   docker-compose -f docker-compose.production.yml restart service_name
   ```

3. **Verificar Certificados SSL**:
   ```bash
   docker-compose -f docker-compose.production.yml exec traefik cat /etc/traefik/acme/acme.json
   ```

## Detalhes do Projeto

### Tecnologias Utilizadas

- **Django**: Framework web para desenvolvimento rápido e seguro.
- **Docker**: Para containerização da aplicação e dependências.
- **PostgreSQL**: Banco de dados relacional utilizado para armazenar dados.
- **Redis**: Utilizado para cache e filas de tarefas.
- **Webpack**: Para compilação de assets estáticos (CSS, JavaScript).

### Funcionalidades Principais

- Gerenciamento de tarefas (criação, edição, exclusão).
- Autenticação de usuários (registro, login, recuperação de senha).
- Painel administrativo para superusuários.
- Integração com Docker para fácil deploy em diferentes ambientes.

### Licença

Este projeto está licenciado sob a licença **MIT**. Para mais detalhes, consulte o arquivo `LICENSE`.

### Links Úteis

- [Documentação do Cookiecutter Django](https://cookiecutter-django.readthedocs.io/en/latest/)
- [Documentação do Docker](https://docs.docker.com/)
- [Documentação do Django](https://docs.djangoproject.com/)

Se tiver dúvidas ou problemas, sinta-se à vontade para abrir uma issue no repositório do projeto.
