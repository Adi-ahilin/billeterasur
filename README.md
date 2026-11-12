# BilleteraSur

Billetera digital de prepago con transferencias entre personas y pagos mediante código QR
dinámico. Proyecto de la asignatura **Desarrollo Seguro (CI3V64)** de INACAP, desarrollado con
enfoque DevSecOps: la seguridad es un requisito de diseño, no una etapa final.

| | |
|---|---|
| **Equipo** | Adilén Reyes (Desarrolladora · DevOps y QA) · Mario Campos (Scrum Master · Security Champion) |
| **Tablero** | [Azure Boards](https://dev.azure.com/mariocampos18/BilleteraSur) |
| **Informe** | [`docs/S1_informe_planificacion.pdf`](docs/) |

## Tecnología

| Capa | Elección |
|---|---|
| Backend | Python 3.13 · Django 5.2 LTS · Django REST Framework |
| Base de datos | PostgreSQL 17 (Docker en local) |
| Frontend | React · Vite · pnpm |
| Contraseñas | Argon2id |
| Planificación | Azure Boards (proceso Agile) |

Cada elección está justificada desde la seguridad en la sección 2.5 del informe.

## Requisitos

- Python 3.13
- Docker Desktop
- Node.js y pnpm 10.26 o superior

## Puesta en marcha

### 1. Clonar e instalar el backend

```bash
git clone https://github.com/Adi-ahilin/billeterasur.git
cd billeterasur/backend
python -m venv .venv
.venv\Scripts\activate          # en Linux o macOS: source .venv/bin/activate
pip install -r requirements/base.txt
```

### 2. Configurar las variables de entorno

Copia la plantilla y completa los valores. **El archivo `.env` nunca se sube al repositorio.**

```bash
copy .env.example .env          # en Linux o macOS: cp .env.example .env
```

Variables necesarias: `SECRET_KEY`, `DEBUG`, `DB_NAME`, `DB_USER`, `DB_PASSWORD`, `DB_HOST`,
`DB_PORT`.

### 3. Levantar la base de datos

Desde la raíz del repositorio:

```bash
docker compose --env-file backend/.env up -d
docker compose --env-file backend/.env ps
```

El contenedor publica PostgreSQL en `127.0.0.1:5432`, accesible solo desde la propia máquina.

### 4. Migrar y verificar

```bash
cd backend
python manage.py migrate
python manage.py test           # 23 pruebas
python manage.py runserver
```

La API queda en `http://127.0.0.1:8000/`. El endpoint de registro es
`POST /api/v1/registro/` y responde 405 a un GET, porque solo acepta POST.

### 5. Levantar el frontend

En otra terminal, desde la raíz:

```bash
cd frontend
pnpm install
pnpm dev
```

La aplicación queda en `http://localhost:5173/`. Requiere el backend corriendo.

## Estructura