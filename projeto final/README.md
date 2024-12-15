# Projeto: Gerenciamento de Tarefas Seguro e Escalável

## Objetivo

O objetivo deste projeto é desenvolver uma aplicação web segura e escalável para o gerenciamento de tarefas. O sistema permite aos usuários criar, ler, atualizar e deletar tarefas de forma rápida e fácil, utilizando uma API REST simples. A aplicação foi construída com ênfase em infraestrutura de rede, segurança (HTTPS) e balanceamento de carga, utilizando Docker, NGINX e FastAPI.

## Estrutura do Projeto

```
.
├── Dockerfile
├── Makefile
├── README.md
├── app
│   └── index.html
├── docker-compose.yaml
├── main.py
├── proxy
│   └── nginx.conf
├── requirements.txt
├── ssl-certs
│   ├── localhost.crt
│   └── localhost.key
└── tasks.json
```

## Componentes do Projeto

### 1. **Dockerfile**

Define a configuração do container para a aplicação FastAPI, incluindo a instalação de dependências necessárias, cópia de arquivos e a execução do servidor.

### 2. **Makefile**

Automatiza a execução de comandos, como a construção dos containers Docker, reinício da aplicação, e verificação de redes e balanceamento de carga.

### 3. **Docker Compose**

O arquivo `docker-compose.yaml` define os serviços necessários para rodar a aplicação, incluindo o NGINX como proxy reverso e o container da aplicação `tasks` com duas réplicas para balanceamento de carga. Além disso, configura redes isoladas para garantir a segurança e a segmentação da infraestrutura.

### 4. **NGINX (nginx.conf)**

O NGINX é utilizado para realizar o balanceamento de carga entre as réplicas do serviço `tasks`. Além disso, ele é responsável por redirecionar o tráfego HTTP para HTTPS, garantindo comunicação segura entre o cliente e o servidor.

### 5. **FastAPI (main.py)**

A aplicação FastAPI é responsável por fornecer a API que permite operações CRUD (Criar, Ler, Atualizar e Deletar) nas tarefas. Ela lida com os status codes HTTP de forma apropriada para cada operação.

### 6. **Certificados SSL (ssl-certs)**

Os certificados SSL garantem que a comunicação entre o cliente e o servidor seja feita de forma segura, utilizando HTTPS.

### 7. **Arquivo de Tarefas (tasks.json)**

Armazena os dados das tarefas em formato JSON. A aplicação carrega e salva os dados no arquivo sempre que uma operação CRUD é realizada.

## Funcionalidades

### 1. **Infraestrutura de Rede**

- **Balanceamento de Carga**: O NGINX distribui o tráfego entre as duas réplicas do serviço `tasks` para garantir alta disponibilidade.
- **Segurança de Rede**: Utiliza o Docker para isolar os containers em redes específicas, protegendo serviços sensíveis.

### 2. **Segurança**

- **HTTPS**: A aplicação utiliza SSL/TLS para criptografar a comunicação entre o cliente e o servidor, protegendo os dados transmitidos.
- **Certificados Autoassinados**: Certificados SSL são gerados para garantir a comunicação segura.

### 3. **API REST**

- **Operações CRUD**: A API permite a criação, leitura, atualização e exclusão de tarefas.
- **Códigos de Status HTTP**: A aplicação retorna os códigos de status HTTP apropriados para cada operação, como `200 OK`, `201 Created`, `400 Bad Request`, etc.

## Como Funciona

### 1. **NGINX Proxy Reverso**

O NGINX é configurado para:

- Redirecionar o tráfego HTTP para HTTPS.
- Realizar o balanceamento de carga entre as réplicas do serviço `tasks`.

### 2. **Docker Compose**

- Define e inicializa os containers necessários:
    - `nginx-proxy`: O container NGINX, que lida com o balanceamento de carga e redirecionamento de tráfego.
    - `tasks`: O container da aplicação FastAPI, que gerencia as tarefas.

O arquivo `docker-compose.yaml` também configura redes isoladas para garantir segurança entre os serviços.

### 3. **FastAPI e CRUD**

A API da FastAPI oferece os seguintes endpoints:

- **GET /tasks**: Retorna todas as tarefas.
- **POST /tasks**: Cria uma nova tarefa.
- **PUT /tasks/{taskId}**: Atualiza uma tarefa existente.
- **DELETE /tasks/{taskId}**: Deleta uma tarefa.

## Como Rodar o Projeto

### 1. **Instalar Dependências**

Para instalar as dependências do Python:
`pip install -r requirements.txt`

### 2. **Iniciar os Containers**

Para iniciar os containers, execute o seguinte comando no terminal:
`make up`

Para reiniciar os containers:
`make restart`

Para parar os containers:
`make down`

Para verificar o balanceamento de carga:
`make stats`

Para testar o CRUD localmente:
`make crud`

Instalando o ping dentro do container 

`apt update`
 
`apt install -y iputils-ping`

### 3. **Acessar a Aplicação**

Abra um navegador e vá até [https://tasks.local](https://tasks.local) para interagir com a API.

## Arquivos Importantes

### **nginx.conf**

Este arquivo configura o NGINX para:

- Redirecionar o tráfego HTTP para HTTPS.
- Realizar o balanceamento de carga entre as réplicas do serviço `tasks`.

Exemplo de configuração do NGINX:

```
events {}

http {
    server {
        listen 80;
        server_name tasks.local;
        return 301 https://$host$request_uri;
    }

    upstream backend {
        server tasks:80;
    }

    server {
        listen 443 ssl;
        server_name tasks.local;

        ssl_certificate /etc/nginx/ssl/localhost.crt;
        ssl_certificate_key /etc/nginx/ssl/localhost.key;

        location / {
            proxy_pass http://tasks;
            proxy_set_header Host $host;
            proxy_set_header X-Real-IP $remote_addr;
            proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
            proxy_set_header X-Forwarded-Proto $scheme;
        }
    }
}
```


### **docker-compose.yaml**

Define os serviços e redes da aplicação. O NGINX é configurado para escutar nas portas 80 (HTTP) e 443 (HTTPS), e o serviço `tasks` é configurado com 2 réplicas para balanceamento de carga.

Exemplo de configuração do Docker Compose:

```
services:
  nginx-proxy:
    image: nginx:latest
    ports:
      - "80:80"
      - "443:443"
    networks:
      - net11
      - net13
    volumes:
      - ./proxy/nginx.conf:/etc/nginx/nginx.conf:ro
      - ./ssl-certs:/etc/nginx/ssl:ro
    depends_on:
      - tasks

  tasks:
    image: nginx:latest
    volumes:
      - ./app:/usr/share/nginx/html:ro
    expose:
      - "80"
    networks:
      - net12
      - net13
    deploy:
      replicas: 2


```
## Conclusão

Este projeto demonstra a criação de uma aplicação web escalável e segura, utilizando Docker, NGINX, FastAPI e HTTPS. O sistema foi projetado para ser resiliente e capaz de lidar com um grande volume de tráfego, ao mesmo tempo em que garante a segurança dos dados com a criptografia SSL/TLS. A aplicação de balanceamento de carga e redes isoladas assegura a alta disponibilidade e a segurança da infraestrutura.