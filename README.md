# dice-roller
 # Desafio utilizando OTEL + LGTM
Este projeto demonstra um ambiente básico com uma aplicação python que gera números aleatórios, métricas e erros que foi instrumentada com Opentelemetry, Grafana, Loki e Tempo.

# Requisitos
- Docker instalado
- Docker compose instalado
- Loki docker driver

# Instruções
- Instalar Docker + Docker compose:
    - #sudo apt update 
    - #sudo apt install docker-ce  
    - #sudo apt install docker-compose
    - #sudo docker plugin install grafana/loki-docker-driver:latest --alias loki --grant-all-permissions

- Copiar repo observability:
  git clone https://github.com/danilopelisser/dice-roller.git

- Buildar aplicações:
  - #cd dice-roller/observability
  - #sudo docker-compose up --build -d 

# Testes de funcionamento (acesso URL via browser gera SPANS OTEL)
 - #sudo docker ps
 - http://ip_vm:5000/
 - http://ip_vm:5000/metrics
 - http://ip_vm:5000/fail

# Sobre
- Grafana frontend estará disponivel em http://ip_vm:3000
- Datasources e telemetria já configurados (para visualizar utilizar explorer)
  
