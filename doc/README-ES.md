# Herramientas Nekro Agent

<p align="center">
  <img src="../icons/nekro-agent-toolkit-icons.png" alt="Mascota de las herramientas Nekro Agent">
</p>

Las herramientas Nekro Agent son una herramienta todo-en-uno para desplegar, respaldar y restaurar Nekro Agent y servicios relacionados. Soporta la gestión automatizada de Docker y proporciona un script de gestión de dependencias para añadir dependencias rápidamente.

## ✨ Características principales

- Instalación, actualización, respaldo y restauración con un solo clic para Nekro Agent
- Detección inteligente y soporte multilingüe
- Respaldo y restauración automáticos de volúmenes Docker
- Script de gestión de dependencias: añade dependencias fácilmente a requirements.txt y pyproject.toml

## 🚀 Inicio rápido

### Instalación

```bash
pip install nekro-agent-toolkit
# O ejecuta desde el código fuente
git clone https://github.com/your-repo/nekro-agent-toolkit.git
cd nekro-agent-toolkit
```

### Comandos comunes

```bash
# Instalar/Actualizar/Respaldar/Restaurar
nekro-agent-toolkit -i [PATH]
nekro-agent-toolkit -u [PATH]
nekro-agent-toolkit -b [DATA_DIR] BACKUP_DIR
nekro-agent-toolkit -r BACKUP_FILE [DATA_DIR]

# Añadir una dependencia a requirements.txt y pyproject.toml
./scripts/add-dependency.sh <package_name>
```

## 🌐 Para usuarios de otros idiomas

| [Leer en chino](../README.md) | [Read in English](./README-EN.md) | [اقرأ باللغة العربية](./README-AR.md) | [Lire en français](./README-FR.md) | [Читать на русском](./README-RU.md) |

## Información adicional

- Requisitos: Python 3.6+, Docker, Docker Compose
- Licencia: Ver [LICENSE](../LICENSE)