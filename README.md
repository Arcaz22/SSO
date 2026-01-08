version: '3.8'

services:
  postgres:
    image: postgres:16-alpine
    container_name: sso_postgres
    restart: always
    environment:
      POSTGRES_USER: postgres
      POSTGRES_PASSWORD: password
      POSTGRES_DB: sso
    ports:
      - "5432:5432"
    volumes:
      - ./pg_data:/var/lib/postgresql/data
      - ./init-db.sh:/docker-entrypoint-initdb.d/init-db.sh
    networks:
      - sso_network

  keycloak:
    image: quay.io/keycloak/keycloak:24.0.1
    container_name: sso_keycloak
    restart: always
    command: start-dev
    environment:
      KC_DB: postgres
      KC_DB_URL: "jdbc:postgresql://sso_postgres:5432/sso"
      KC_DB_USERNAME: postgres
      KC_DB_PASSWORD: password

      KEYCLOAK_ADMIN: admin
      KEYCLOAK_ADMIN_PASSWORD: password

      KC_PROXY: edge
      KC_HOSTNAME_STRICT: "false"
      KC_HTTP_ENABLED: "true"
      KC_TRANSACTION_XA_ENABLED: "false"

      KC_LOG_LEVEL: info
    depends_on:
      - postgres
    ports:
      - "8080:8080"
    networks:
      - sso_network
    deploy:
      resources:
        limits:
          memory: 1024M

networks:
  sso_network:
    name: sso_network
    driver: bridge
