# Sistema de Votaciones

Sistema web para gestionar procesos de votación de manera ordenada, rápida y confiable.

## Tecnologías
- **Backend:** Python + Flask
- **Base de datos:** MySQL 
- **Frontend:** HTML + CSS + Bootstrap 5
- **Deploy:** Git

## Instalación local

### Requisitos
- Python 3.10+
- pip

### Pasos

```bash
# 1. Clonar el repositorio
git clone https://github.com/DanielChitay/SistemaVotaciones
cd sistema-votaciones

# 2. Crear entorno virtual
python -m venv venv

# En Windows:
venv\Scripts\activate

# En Mac/Linux:
source venv/bin/activate

# 3. Instalar dependencias
pip install -r requirements.txt

# 4. Ejecutar la aplicación
python run.py
```

### Acceso
- URL: `http://localhost:5000`
- Usuario: `admin@votaciones.gt`
- Contraseña: `admin123`

## Estructura del proyecto

```
sistema-votaciones/
├── app/
│   ├── __init__.py         # App factory
│   ├── models.py           # Modelos de BD
│   ├── routes/
│   │   ├── auth.py         # Login / logout
│   │   ├── usuarios.py     # CRUD usuarios
│   │   ├── votaciones.py   # Gestión votaciones
│   │   ├── mesas.py        # Gestión mesas
│   │   └── resultados.py   # Registro y consulta
│   └── templates/          # HTML
├── requirements.txt
├── config.py
├── run.py
├── Procfile
└── README.md
```

## Equipo
- **Project Manager:** FRANCISCO ESTRADA - 7690 23 22940
- **Analista:** NERY OSORIO - 7690 23 5339
- **Desarrollador:** JOSUE VELASQUEZ  - 7690 23 13042
- **QA / Tester:** MELVIN RAMOS - 7690 23 17316

## GRUPO 1
Análisis de Sistemas 1
