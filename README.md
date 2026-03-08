# Quiz-USICAMM-Media-Superior

Simulador web de preparación para admisión docente USICAMM en educación media superior.

## Objetivo

Construir una aplicación web que permita a los usuarios responder cuestionarios de práctica, obtener retroalimentación sobre respuestas correctas e incorrectas, guardar intentos y, en una etapa posterior, generar analítica de resultados mediante dbt y Airflow.

## Estado del proyecto

Versión inicial en construcción.

Este repositorio surge a partir de un proyecto demo técnico y se encuentra en proceso de adaptación hacia un producto real orientado a simulación y práctica de preguntas para admisión docente.

## Alcance de la primera versión

La primera versión del proyecto busca cubrir lo siguiente:

- ejecución local funcional;
- carga de preguntas desde archivos JSON;
- visualización de preguntas en una interfaz web;
- registro de respuestas;
- cálculo de resultados;
- retroalimentación de respuestas correctas e incorrectas.

## Stack tecnológico

- **Frontend:** HTML, CSS, JavaScript
- **Backend:** FastAPI
- **Base de datos:** PostgreSQL
- **Analítica:** dbt
- **Orquestación:** Airflow
- **Contenedores:** Docker / Docker Compose
- **Arquitectura objetivo:** GitHub Pages + Azure

## Estructura general del proyecto

```text
.
├─ apps/
│  ├─ api/
│  └─ web/
├─ data/
├─ dbt/
├─ airflow/
├─ infra/
├─ scripts/
└─ tests/
````

## Ejecución local

### 1. Levantar servicios

```powershell
docker compose -f infra/docker-compose.yml up -d --build
```

### 2. Inicializar la base de datos

```powershell
Get-Content .\scripts\init.sql -Raw | docker exec -i infra-db-1 psql -U quiz -d quizops
```

### 3. Cargar preguntas de ejemplo

```powershell
docker compose -f infra/docker-compose.yml exec api python /app/scripts/seed.py
```

### 4. Ejecutar el frontend local

```powershell
cd .\apps\web
python -m http.server 5173
```

### 5. Abrir en navegador

* [http://localhost:5173](http://localhost:5173)

## Objetivo de arquitectura

La arquitectura objetivo del proyecto es:

* **GitHub Pages** para el frontend;
* **Azure App Service** para FastAPI;
* **Azure Database for PostgreSQL** para la base de datos;
* **Azure VM** para Airflow + dbt.

## Regla importante del proyecto

El quiz debe funcionar aunque Airflow no corra.

Airflow quedará reservado para tareas de analítica, validación y automatización, pero no será parte del flujo crítico del usuario al responder preguntas.

## Hoja de ruta inicial

* [ ] Crear el nuevo repositorio de trabajo
* [ ] Dejar funcional el flujo completo en local
* [ ] Mostrar resultados por pregunta en la interfaz
* [ ] Agregar pruebas automáticas
* [ ] Configurar CI
* [ ] Desplegar frontend en GitHub Pages
* [ ] Desplegar backend y base de datos en Azure
* [ ] Subir Airflow + dbt a una VM en Azure

## Nota

Este proyecto se encuentra en evolución. El objetivo es convertir una base técnica de portafolio en una aplicación real y pública orientada a la preparación académica y profesional.
