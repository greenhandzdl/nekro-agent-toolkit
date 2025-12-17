# Manuel d'utilisateur en français

<p align="center">
	<img src="../icons/nekro-agent-toolkit-icons.png" alt="Nekro Agent Toolkit吉祥物">
</p>

Nekro Agent Toolkit est un outil tout-en-un pour déployer, sauvegarder et restaurer Nekro Agent et les services associés, avec prise en charge de l'automatisation dans les environnements Docker.

## 🌐 Liens vers d'autres langues

| [Read in English](README-EN.md) | [اقرأ باللغة العربية](README-AR.md) | [Lire en français](README-FR.md) | [Читать на русском](README-RU.md) | [Leer en español](README-ES.md) | [日本語で読む](README-JP.md) |

## ✨ Fonctionnalités principales

- Installation, mise à jour, sauvegarde et restauration de Nekro Agent en un clic
- Détection intelligente et prise en charge multilingue
- Prise en charge de la sauvegarde et de la restauration automatiques des volumes Docker

## 🚀 Démarrage rapide

### Installation

```bash
pip install nekro-agent-toolkit
# Ou exécuter depuis le code source
git clone https://github.com/your-repo/nekro-agent-toolkit.git
cd nekro-agent-toolkit
```

### Commandes courantes

```bash
# Installation/Mise à jour/Sauvegarde/Restauration
nekro-agent-toolkit -i [PATH]
nekro-agent-toolkit -u [PATH]
nekro-agent-toolkit -b [DATA_DIR] BACKUP_DIR
nekro-agent-toolkit -r BACKUP_FILE [DATA_DIR]
```

### Gestion des dépendances avec uv (recommandé)

Ce projet prend désormais en charge l'utilisation de `uv` pour gérer les dépendances et générer des fichiers de verrouillage reproductibles `uv.lock`.

## Informations supplémentaires

- Exigences système : Python 3.6+, Docker, Docker Compose
- Licence : voir [LICENSE](../LICENSE)