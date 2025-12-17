# Manual del usuario en español

<p align="center">
	<img src="https://cdn.jsdelivr.net/gh/greenhandzdl/nekro-agent-toolkit@main/icons/nekro-agent-toolkit-icons.png" alt="Nekro Agent Toolkit吉祥物">
</p>

Nekro Agent Toolkit es una herramienta todo en uno para implementar, respaldar y restaurar Nekro Agent y servicios relacionados, con soporte de automatización en entornos Docker.

## 🌐 Enlaces a otros idiomas

| [Read in English](https://cdn.jsdelivr.net/gh/greenhandzdl/nekro-agent-toolkit@main/doc/README/README-EN.md) | [اقرأ باللغة العربية](https://cdn.jsdelivr.net/gh/greenhandzdl/nekro-agent-toolkit@main/doc/README/README-AR.md) | [Lire en français](https://cdn.jsdelivr.net/gh/greenhandzdl/nekro-agent-toolkit@main/doc/README/README-FR.md) | [Читать на русском](https://cdn.jsdelivr.net/gh/greenhandzdl/nekro-agent-toolkit@main/doc/README/README-RU.md) | [Leer en español](https://cdn.jsdelivr.net/gh/greenhandzdl/nekro-agent-toolkit@main/doc/README/README-ES.md) | [日本語で読む](https://cdn.jsdelivr.net/gh/greenhandzdl/nekro-agent-toolkit@main/doc/README/README-JP.md) |

## ✨ Características principales

- Instalación, actualización, respaldo y restauración de Nekro Agent con un solo clic
- Detección inteligente y soporte multilingüe
- Soporte para respaldo y restauración automáticos de volúmenes Docker

## 🚀 Inicio rápido

### Instalación

```bash
pip install nekro-agent-toolkit
# O ejecutar desde el código fuente
git clone https://github.com/your-repo/nekro-agent-toolkit.git
cd nekro-agent-toolkit
```

### Comandos comunes

```bash
# Instalación/Actualización/Respaldo/Restauración
nekro-agent-toolkit -i [PATH]
nekro-agent-toolkit -u [PATH]
nekro-agent-toolkit -b [DATA_DIR] BACKUP_DIR
nekro-agent-toolkit -r BACKUP_FILE [DATA_DIR]
```

### Gestión de dependencias con uv (recomendado)

Este proyecto ahora admite el uso de `uv` para gestionar dependencias y generar archivos de bloqueo reproducibles `uv.lock`.

## Información adicional

- Requisitos del sistema: Python 3.6+, Docker, Docker Compose
- Licencia: ver [LICENSE](https://cdn.jsdelivr.net/gh/greenhandzdl/nekro-agent-toolkit@main/LICENSE)