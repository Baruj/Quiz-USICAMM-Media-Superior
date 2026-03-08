# Quiz-USICAMM-Media-Superior

Simulador web de preparación para admisión docente USICAMM en educación media superior.

## Descripción general

Este repositorio contiene una aplicación web para practicar quizzes de preparación docente. El sistema permite seleccionar un quiz, responder preguntas, registrar intentos y mostrar resultados detallados por pregunta, incluyendo respuesta elegida, respuesta correcta y explicación.

El proyecto está organizado para funcionar en desarrollo local y evolucionar hacia una arquitectura pública compuesta por:

- **GitHub Pages** para el frontend;
- **Azure App Service** para la API en FastAPI;
- **Azure Database for PostgreSQL** para la base de datos;
- **Azure VM** para Airflow + dbt como capa analítica separada.

## Regla central del proyecto

El quiz debe funcionar aunque Airflow no esté corriendo.

Airflow y dbt forman parte de la capa analítica y de automatización, pero no del flujo crítico del usuario al responder preguntas.

## Objetivo del proyecto

Construir una aplicación web que permita:

- responder quizzes temáticos e integradores;
- registrar intentos de usuario;
- guardar respuestas;
- calcular puntajes;
- mostrar retroalimentación por pregunta;
- generar posteriormente analítica sobre resultados mediante dbt y Airflow.

## Estado actual

El repositorio está orientado a cubrir las siguientes capacidades:

- ejecución local con Docker;
- inicialización reproducible de la base de datos;
- carga de preguntas desde JSON;
- soporte para múltiples quizzes;
- flujo completo de intento y envío;
- pruebas automáticas con `pytest`;
- validación analítica con `dbt`;
- integración continua con GitHub Actions;
- preparación para despliegue público.

## Funcionalidades de la primera versión

La primera versión del simulador contempla:

- quizzes temáticos, uno por cada `topic`;
- un quiz integrador con preguntas de todos los temas;
- listado de quizzes disponibles;
- selección de quiz desde el frontend;
- registro de respuestas por intento;
- cálculo de score;
- resultados correctos e incorrectos;
- explicación de la respuesta correcta.

## Stack tecnológico

- **Frontend:** HTML, CSS, JavaScript
- **Backend:** FastAPI
- **Base de datos:** PostgreSQL
- **Acceso a datos:** SQLAlchemy
- **Analítica:** dbt
- **Orquestación:** Airflow
- **Contenedores:** Docker / Docker Compose
- **CI:** GitHub Actions
- **Infraestructura objetivo:** GitHub Pages + Azure

## Estructura del repositorio

```text
.
├─ apps/
│  ├─ api/        # Backend FastAPI
│  └─ web/        # Frontend estático
├─ airflow/       # DAGs y configuración analítica
├─ data/          # Banco de preguntas en JSON
├─ dbt/           # Proyecto analítico
├─ infra/         # Docker Compose y Dockerfiles
├─ scripts/       # init.sql y seed.py
└─ tests/         # Pruebas automáticas
````

## Requisitos previos

Para trabajar en local se recomienda contar con lo siguiente:

* Git
* Docker y Docker Compose
* Python 3.12
* PowerShell 7 o superior en Windows
* Bash en Linux
* conexión a internet para instalar dependencias y descargar imágenes

## Variables y configuración importante

### Backend

La API usa principalmente estas variables de entorno:

* `DATABASE_URL`
* `CORS_ALLOWED_ORIGINS`

Ejemplo de valor local para `DATABASE_URL` fuera de Docker:

```text
postgresql+psycopg2://quiz:quiz@localhost:5432/quizops
```

Ejemplo de valor local dentro de Docker:

```text
postgresql+psycopg2://quiz:quiz@db:5432/quizops
```

### Frontend

El frontend obtiene la URL del backend desde `apps/web/config.js`.

Contenido local sugerido:

```javascript
window.APP_CONFIG = {
  API_URL: "http://localhost:8000"
};
```

Cuando el proyecto se publique en línea, este valor debe apuntar a la URL pública del backend.

## Ejecución local recomendada con Docker

La forma recomendada de desarrollo local es levantar base de datos y API con Docker, inicializar el esquema, correr el seed y después abrir el frontend estático.

### Opción A. Windows (PowerShell)

#### 1. Levantar servicios

```powershell
docker compose -f infra/docker-compose.yml up -d --build
```

#### 2. Inicializar la base de datos

```powershell
Get-Content .\scripts\init.sql -Raw | docker compose -f infra/docker-compose.yml exec -T db psql -U quiz -d quizops
```

#### 3. Ejecutar el seed

```powershell
docker compose -f infra/docker-compose.yml exec api python /app/scripts/seed.py
```

#### 4. Abrir el frontend local

```powershell
Set-Location .\apps\web
python -m http.server 5173
```

#### 5. Abrir las URLs de trabajo

* Frontend: `http://localhost:5173`
* API: `http://localhost:8000`
* Documentación FastAPI: `http://localhost:8000/docs`

### Opción B. Linux (Bash)

#### 1. Levantar servicios

```bash
docker compose -f infra/docker-compose.yml up -d --build
```

#### 2. Inicializar la base de datos

```bash
cat scripts/init.sql | docker compose -f infra/docker-compose.yml exec -T db psql -U quiz -d quizops
```

#### 3. Ejecutar el seed

```bash
docker compose -f infra/docker-compose.yml exec api python /app/scripts/seed.py
```

#### 4. Abrir el frontend local

```bash
cd apps/web
python3 -m http.server 5173
```

#### 5. Abrir las URLs de trabajo

* Frontend: `http://localhost:5173`
* API: `http://localhost:8000`
* Documentación FastAPI: `http://localhost:8000/docs`

## Flujo mínimo de validación en local

Después de levantar el sistema, debe ser posible:

1. abrir el frontend;
2. ver el listado de quizzes;
3. seleccionar un quiz temático o integrador;
4. responder preguntas;
5. enviar el intento;
6. visualizar el puntaje;
7. revisar respuestas correctas e incorrectas;
8. consultar la API desde `/docs`.

## Desarrollo Python fuera de Docker (opcional)

Esta ruta es útil para correr pruebas desde la máquina anfitriona sin entrar al contenedor.

### Windows (PowerShell)

```powershell
py -3.12 -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
python -m pip install -r .\apps\api\requirements.txt
python -m pip install -r .\apps\api\requirements-dev.txt
$env:PYTHONPATH="apps/api"
$env:DATABASE_URL="postgresql+psycopg2://quiz:quiz@localhost:5432/quizops"
python -m pytest -q
```

### Linux (Bash)

```bash
python3.12 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install -r apps/api/requirements.txt
python -m pip install -r apps/api/requirements-dev.txt
export PYTHONPATH=apps/api
export DATABASE_URL=postgresql+psycopg2://quiz:quiz@localhost:5432/quizops
python -m pytest -q
```

## Pruebas automáticas

El proyecto incluye pruebas del flujo básico de la aplicación.

### Ejecutar pruebas del backend

```bash
python -m pytest -q
```

### Ejecutar pruebas específicas

```bash
python -m pytest tests/test_health.py -q
python -m pytest tests/test_quiz_flow.py -q
python -m pytest tests/test_submit_results.py -q
```

## Validación analítica con dbt

Una vez que la base y la API están funcionando, puede validarse la capa analítica.

### Con Docker

```bash
docker compose -f infra/docker-compose.yml run --rm dbt debug --profiles-dir /dbt
docker compose -f infra/docker-compose.yml run --rm dbt run --profiles-dir /dbt
docker compose -f infra/docker-compose.yml run --rm dbt test --profiles-dir /dbt
```

## Airflow en local (opcional)

Airflow no es necesario para ejecutar el flujo principal del simulador en desarrollo local. El quiz puede funcionar correctamente sin levantar Airflow, por lo que este componente debe considerarse opcional.

Solo conviene iniciarlo cuando se desea probar la capa de orquestación y automatización del proyecto, por ejemplo para validar DAGs, ejecutar tareas programadas o integrar procesos analíticos con `dbt`.

Para levantar Airflow en local debe usarse el perfil `airflow` definido en `infra/docker-compose.yml`:

Con tu `docker-compose.yml`, después de levantar Airflow con:

```bash
docker compose -f infra/docker-compose.yml --profile airflow up -d --build
```

la interfaz web queda en:

```text
http://localhost:8080
```

## Cómo entrar paso a paso

### 1. Levantar Airflow

```bash
docker compose -f infra/docker-compose.yml --profile airflow up -d --build
```

### 2. Verificar que los contenedores estén corriendo

```bash
docker compose -f infra/docker-compose.yml ps
```

Ahí debería aparecer al menos algo como:

* `airflow-webserver`
* `airflow-scheduler`
* `airflow-db`

### 3. Abrir el navegador

Entrar a:

```text
http://localhost:8080
```

### 4. Iniciar sesión

En tu configuración actual, el usuario inicial se crea aquí:

```yaml
_AIRFLOW_WWW_USER_USERNAME: admin
_AIRFLOW_WWW_USER_PASSWORD: admin
```

Entonces, las credenciales serían:

* **usuario:** `admin`
* **contraseña:** `admin`

## Si no abre de inmediato

A veces Airflow tarda un poco en inicializarse, sobre todo la primera vez. Si `localhost:8080` no responde todavía, revisa logs con:

```bash
docker compose -f infra/docker-compose.yml logs airflow-webserver
```

y también:

```bash
docker compose -f infra/docker-compose.yml logs airflow-init
```

## Qué pasa al entrar

Una vez dentro, verás la interfaz de Airflow, donde normalmente podrás:

* ver DAGs;
* activarlos o pausarlos;
* lanzarlos manualmente;
* revisar ejecuciones;
* consultar logs de tareas.

## Texto para tu README

Puedes ponerlo así:

````text
### Cómo entrar a Airflow en local

Después de levantar Airflow con el perfil `airflow`, la interfaz web queda disponible en:

```text
http://localhost:8080
````

Para acceder, abrir esa URL en el navegador. Con la configuración actual del proyecto, el usuario inicial es:

* usuario: `admin`
* contraseña: `admin`

Si la página no responde inmediatamente, conviene revisar que los contenedores estén activos con:

```bash
docker compose -f infra/docker-compose.yml ps
```

y, en caso necesario, revisar logs del webserver o del proceso de inicialización:

```bash
docker compose -f infra/docker-compose.yml logs airflow-webserver
docker compose -f infra/docker-compose.yml logs airflow-init
```

La interfaz de Airflow permite revisar DAGs, ejecutar flujos manualmente y consultar logs de ejecución.




## Integración continua

El repositorio está preparado para validarse automáticamente con GitHub Actions. La idea del flujo de CI es comprobar, en cada `push` o `pull request`, que:

* PostgreSQL puede levantarse;
* `scripts/init.sql` aplica correctamente el esquema;
* `scripts/seed.py` puebla la base;
* `pytest` pasa sin errores;
* `dbt debug`, `dbt run` y `dbt test` funcionan.

## Arquitectura objetivo

La arquitectura pública del proyecto es la siguiente:

* **GitHub Pages:** frontend estático
* **Azure App Service:** backend FastAPI
* **Azure Database for PostgreSQL:** base de datos
* **Azure VM:** Airflow + dbt

## Guía para poner el proyecto en línea

El despliegue recomendado debe hacerse por capas y en este orden:

1. base de datos;
2. backend;
3. frontend;
4. validación de conexión;
5. capa analítica separada.

### 1. Desplegar PostgreSQL en Azure

Objetivo: sacar la base de datos del entorno local y alojarla en un servicio administrado.

Pasos recomendados:

1. crear un recurso de **Azure Database for PostgreSQL**;
2. definir nombre del servidor, usuario administrador y contraseña;
3. crear la base de datos del proyecto;
4. habilitar acceso desde la IP necesaria o ajustar firewall;
5. obtener la cadena de conexión;
6. aplicar `scripts/init.sql`;
7. correr `scripts/seed.py` contra la base pública.

Ejemplo conceptual de conexión para producción:

```text
postgresql+psycopg2://USUARIO:PASSWORD@SERVIDOR.postgres.database.azure.com:5432/quizops?sslmode=require
```

### 2. Aplicar `init.sql` y correr `seed.py` en la base pública

Una vez creada la base pública, deben cargarse el esquema y los datos iniciales.

#### Windows (PowerShell)

```powershell
Get-Content .\scripts\init.sql -Raw | psql "host=SERVIDOR.postgres.database.azure.com port=5432 dbname=quizops user=USUARIO password=PASSWORD sslmode=require"
$env:DATABASE_URL="postgresql+psycopg2://USUARIO:PASSWORD@SERVIDOR.postgres.database.azure.com:5432/quizops?sslmode=require"
python .\scripts\seed.py
```

#### Linux (Bash)

```bash
cat scripts/init.sql | psql "host=SERVIDOR.postgres.database.azure.com port=5432 dbname=quizops user=USUARIO password=PASSWORD sslmode=require"
export DATABASE_URL="postgresql+psycopg2://USUARIO:PASSWORD@SERVIDOR.postgres.database.azure.com:5432/quizops?sslmode=require"
python scripts/seed.py
```

Resultado esperado:

* tablas creadas;
* quizzes temáticos creados;
* quiz integrador creado;
* preguntas y relaciones cargadas.

### 3. Desplegar el backend en Azure App Service

Objetivo: publicar la API en una URL pública.

Pasos recomendados:

1. crear una aplicación en **Azure App Service** con runtime de Python;
2. desplegar el contenido de `apps/api`;
3. configurar variables de entorno;
4. verificar que la app arranque;
5. probar `/health`;
6. probar `/quizzes` y `/docs`.

Variables mínimas:

* `DATABASE_URL`
* `CORS_ALLOWED_ORIGINS`

Ejemplo de `CORS_ALLOWED_ORIGINS`:

```text
https://TU-USUARIO.github.io/Quiz-USICAMM-Media-Superior
```

URL pública esperada del backend:

```text
https://tu-api.azurewebsites.net
```

### 4. Publicar el frontend en GitHub Pages

Objetivo: exponer la interfaz web en una URL pública.

Pasos recomendados:

1. editar `apps/web/config.js`;
2. cambiar `API_URL` para que use la URL pública del backend;
3. publicar `apps/web` con GitHub Pages, idealmente mediante GitHub Actions;
4. abrir la URL pública del frontend;
5. comprobar que el frontend consume la API pública.

Ejemplo de `config.js` para producción:

```javascript
window.APP_CONFIG = {
  API_URL: "https://tu-api.azurewebsites.net"
};
```

URL pública esperada del frontend:

```text
https://TU-USUARIO.github.io/Quiz-USICAMM-Media-Superior
```

### 5. Validar la conexión entre frontend y backend

Esta parte debe comprobarse con un flujo real de usuario.

Checklist mínima:

* el frontend carga el listado de quizzes;
* el usuario puede seleccionar un quiz;
* el frontend obtiene preguntas desde la API pública;
* el usuario puede responder;
* el intento se guarda;
* el `submit` calcula el score;
* la interfaz muestra resultados;
* no existen errores de CORS en la consola del navegador.

### 6. Desplegar Airflow + dbt en una VM de Azure

Objetivo: mover la capa analítica fuera de la máquina local.

Pasos recomendados:

1. crear una VM Linux en Azure;
2. instalar Docker y Docker Compose;
3. subir configuración de Airflow;
4. copiar DAGs;
5. copiar proyecto dbt;
6. configurar conexión a PostgreSQL;
7. inicializar Airflow;
8. levantar webserver y scheduler;
9. ejecutar un DAG inicial de validación.

Primer uso recomendado de Airflow:

* `dbt run`
* `dbt test`

## Qué debe verificar una versión pública profesional

Para considerar que el proyecto está correctamente presentado y listo para mostrarse, deben cumplirse estas condiciones:

* el README explica claramente qué hace el proyecto;
* existe una ruta reproducible para correrlo en local;
* Windows y Linux tienen instrucciones explícitas;
* el backend expone `/health` y `/docs`;
* la aplicación puede ejecutarse desde cero sin improvisaciones;
* las pruebas automáticas funcionan;
* CI valida el flujo mínimo;
* el frontend público consume la API pública;
* Airflow y dbt están desacoplados del flujo principal.

## Solución de problemas comunes

### El frontend abre pero no aparecen quizzes

Verificar:

* que la base haya sido inicializada con `init.sql`;
* que `seed.py` se haya ejecutado correctamente;
* que `apps/web/config.js` apunte a la URL correcta del backend.

### Hay errores de CORS

Verificar:

* que `CORS_ALLOWED_ORIGINS` incluya exactamente la URL pública del frontend;
* que no se esté mezclando `localhost` con la URL pública por error.

### La API no conecta con PostgreSQL en Azure

Verificar:

* usuario y contraseña;
* firewall del servidor;
* nombre correcto del host;
* uso de `sslmode=require`.

### PowerShell no deja activar el entorno virtual

Abrir PowerShell como usuario normal y, si es necesario, ajustar la política de ejecución para la sesión actual antes de activar `.venv`.

## Criterio de cierre del proyecto

Se considera que el proyecto ya quedó bien cuando una persona externa puede:

1. entrar a la URL pública del frontend;
2. elegir un quiz;
3. responder preguntas;
4. enviar el intento;
5. ver resultados;
6. mientras la capa analítica permanece separada y no bloquea el uso principal.

## Nota final

Este repositorio no busca quedarse como demo técnica. Su objetivo es consolidarse como una aplicación funcional, documentada, reproducible y desplegable, con valor tanto académico como profesional.
