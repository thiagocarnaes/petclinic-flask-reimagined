# PetClinic API - Python/Flask Implementation

Este projeto é uma implementação da aplicação Spring PetClinic em Python usando Flask, baseada no repositório original [spring-projects/spring-petclinic](https://github.com/spring-projects/spring-petclinic).

## 🏗️ Arquitetura

O projeto segue uma arquitetura em camadas bem definida:

```
backend/
├── app/
│   ├── controllers/     # Controladores da API (rotas e validações)
│   ├── models/         # Modelos de dados (SQLAlchemy)
│   ├── services/       # Lógica de negócio
│   └── __init__.py     # Configuração da aplicação Flask
├── migrations/         # Migrações do banco de dados (Alembic)
├── config.py          # Configurações da aplicação
├── run.py             # Script de inicialização
└── requirements.txt   # Dependências Python
```

## 🚀 Tecnologias Utilizadas

- **Python 3.11**
- **Flask** - Framework web
- **SQLAlchemy** - ORM para banco de dados
- **Alembic** - Migrações de banco de dados
- **MySQL 8.0** - Banco de dados
- **Marshmallow** - Validação e serialização
- **Flasgger** - Documentação Swagger
- **Docker & Docker Compose** - Containerização

## 📊 Modelo de Dados

O sistema possui as seguintes entidades principais:

- **Owner** (Proprietário) - Donos dos pets
- **Pet** (Animal) - Animais de estimação
- **PetType** (Tipo de Pet) - Tipos de animais (gato, cachorro, etc.)
- **Visit** (Visita) - Consultas veterinárias
- **Vet** (Veterinário) - Profissionais veterinários
- **Specialty** (Especialidade) - Especialidades médicas

## 🔧 Configuração e Execução

### Pré-requisitos

- Docker e Docker Compose
- Git

### 1. Clone o repositório

```bash
git clone <seu-repositorio>
cd petclinic-flask
```

### 2. Configure as variáveis de ambiente

O arquivo `.env` já está configurado com valores padrão. Para produção, altere:

```bash
# Database Configuration
MYSQL_ROOT_PASSWORD=sua_senha_root_segura
MYSQL_DATABASE=petclinic
MYSQL_USER=petclinic_user
MYSQL_PASSWORD=sua_senha_segura

# Flask Configuration
SECRET_KEY=sua_chave_secreta_super_segura
```

### 3. Execute com Docker Compose

```bash
# Iniciar todos os serviços
docker-compose up -d

# Ver logs
docker-compose logs -f backend

# Parar os serviços
docker-compose down
```

### 4. Acesse a aplicação

- **API**: http://localhost:5000
- **Documentação Swagger**: http://localhost:5000/apidocs
- **Health Check**: http://localhost:5000/health

## 📚 API Endpoints

### Owners (Proprietários)
- `GET /api/owners` - Listar proprietários
- `POST /api/owners` - Criar proprietário
- `GET /api/owners/{id}` - Buscar proprietário por ID
- `PUT /api/owners/{id}` - Atualizar proprietário
- `DELETE /api/owners/{id}` - Deletar proprietário
- `GET /api/owners/search/lastname/{name}` - Buscar por sobrenome

### Pets (Animais)
- `GET /api/pets` - Listar pets
- `POST /api/pets` - Criar pet
- `GET /api/pets/{id}` - Buscar pet por ID
- `PUT /api/pets/{id}` - Atualizar pet
- `DELETE /api/pets/{id}` - Deletar pet
- `GET /api/pets/owner/{owner_id}` - Pets por proprietário

### Visits (Consultas)
- `GET /api/visits` - Listar consultas
- `POST /api/visits` - Criar consulta
- `GET /api/visits/{id}` - Buscar consulta por ID
- `PUT /api/visits/{id}` - Atualizar consulta
- `DELETE /api/visits/{id}` - Deletar consulta
- `GET /api/visits/pet/{pet_id}` - Consultas por pet
- `GET /api/visits/recent` - Consultas recentes

### Vets (Veterinários)
- `GET /api/vets` - Listar veterinários
- `POST /api/vets` - Criar veterinário
- `GET /api/vets/{id}` - Buscar veterinário por ID
- `PUT /api/vets/{id}` - Atualizar veterinário
- `DELETE /api/vets/{id}` - Deletar veterinário
- `POST /api/vets/{id}/specialties` - Adicionar especialidade
- `DELETE /api/vets/{id}/specialties/{specialty_id}` - Remover especialidade

### Specialties (Especialidades)
- `GET /api/specialties` - Listar especialidades
- `POST /api/specialties` - Criar especialidade
- `GET /api/specialties/{id}` - Buscar especialidade por ID
- `PUT /api/specialties/{id}` - Atualizar especialidade
- `DELETE /api/specialties/{id}` - Deletar especialidade

### Pet Types (Tipos de Pet)
- `GET /api/pet-types` - Listar tipos de pet
- `POST /api/pet-types` - Criar tipo de pet
- `GET /api/pet-types/{id}` - Buscar tipo por ID
- `PUT /api/pet-types/{id}` - Atualizar tipo
- `DELETE /api/pet-types/{id}` - Deletar tipo

### Authentication
- `POST /api/auth/login` - Login (usuário: admin, senha: admin123)
- `GET /api/auth/protected` - Rota protegida (requer token)
- `GET /api/auth/user` - Informações do usuário

## 🗄️ Migrações de Banco de Dados

O projeto usa Alembic para gerenciar migrações:

```bash
# Dentro do container backend
docker-compose exec backend bash

# Criar nova migração
flask db migrate -m "Descrição da migração"

# Aplicar migrações
flask db upgrade

# Ver histórico
flask db history
```

## 🔍 Validações Implementadas

### Controllers
- Validação de entrada com Marshmallow
- Validação de tipos de dados
- Validação de relacionamentos (FK)
- Validação de datas (não podem ser futuras)
- Validação de tamanhos de campos
- Tratamento de erros padronizado

### Regras de Negócio
- Proprietários não podem ser deletados se tiverem pets
- Pets não podem ser deletados se tiverem consultas
- Tipos de pet não podem ser deletados se tiverem pets associados
- Especialidades e tipos devem ser únicos
- Datas de nascimento e consultas não podem ser futuras

## 🧪 Testando a API

### Usando curl

```bash
# Listar proprietários
curl -X GET http://localhost:5000/api/owners

# Criar proprietário
curl -X POST http://localhost:5000/api/owners \
  -H "Content-Type: application/json" \
  -d '{
    "first_name": "João",
    "last_name": "Silva",
    "address": "Rua das Flores, 123",
    "city": "São Paulo",
    "telephone": "11999999999"
  }'

# Login
curl -X POST http://localhost:5000/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{"username": "admin", "password": "admin123"}'
```

### Usando Swagger UI

Acesse http://localhost:5000/apidocs para uma interface interativa completa.

## 🚀 Desenvolvimento

### Executar em modo desenvolvimento

```bash
# Clonar e entrar no diretório
cd backend

# Criar ambiente virtual
python -m venv venv
source venv/bin/activate  # Linux/Mac
# ou
venv\Scripts\activate  # Windows

# Instalar dependências
pip install -r requirements.txt

# Configurar variáveis de ambiente
export DATABASE_URL=mysql+pymysql://petclinic_user:petclinic_password123@localhost:3306/petclinic
export FLASK_ENV=development
export FLASK_DEBUG=1

# Executar migrações
flask db upgrade

# Iniciar servidor
python run.py
```

## 📝 Dados de Exemplo

O projeto vem com dados de exemplo que são inseridos automaticamente:

- 6 tipos de pets (Cat, Dog, Lizard, Snake, Bird, Hamster)
- 5 especialidades veterinárias
- 6 veterinários com especialidades
- 10 proprietários
- 13 pets
- 15 consultas de exemplo

## 🔧 Configurações Adicionais

### Logs
Os logs da aplicação são exibidos no console. Para produção, configure um sistema de logs apropriado.

### Segurança
- Configure senhas fortes no `.env`
- Use HTTPS em produção
- Configure CORS adequadamente
- Implemente autenticação robusta (o exemplo é simplificado)

### Performance
- Configure connection pooling para o banco
- Implemente cache onde necessário
- Configure índices apropriados no banco

## 🤝 Contribuindo

1. Fork o projeto
2. Crie uma branch para sua feature
3. Commit suas mudanças
4. Push para a branch
5. Abra um Pull Request

## 📄 Licença

Este projeto está sob a licença Apache 2.0 - veja o arquivo [LICENSE](LICENSE) para detalhes.

## 🆘 Suporte

Para suporte e dúvidas:
- Abra uma issue no GitHub
- Consulte a documentação Swagger em `/apidocs`
- Verifique os logs com `docker-compose logs backend`