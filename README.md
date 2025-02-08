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
   git clone https://github.com/seu-usuario/m-task.git
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
