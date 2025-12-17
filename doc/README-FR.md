# Outils Nekro Agent

<p align="center">
  <img src="../icons/nekro-agent-toolkit-icons.png" alt="Mascotte des outils Nekro Agent">
</p>

Les outils Nekro Agent sont un outil tout-en-un pour déployer, sauvegarder et restaurer Nekro Agent et les services associés. Ils prennent en charge la gestion automatisée de Docker et fournissent un script de gestion des dépendances pour ajouter rapidement des dépendances.

## ✨ Fonctionnalités principales

- Installation, mise à niveau, sauvegarde et restauration en un clic pour Nekro Agent
- Détection intelligente et prise en charge multilingue
- Sauvegarde et restauration automatiques des volumes Docker
- Script de gestion des dépendances : ajoutez facilement des dépendances à requirements.txt et pyproject.toml

## 🚀 Démarrage rapide

### Installation

```bash
pip install nekro-agent-toolkit
# Ou exécuter depuis la source
git clone https://github.com/your-repo/nekro-agent-toolkit.git
cd nekro-agent-toolkit
```

### Commandes courantes

```bash
# Installer/Mettre à jour/Sauvegarder/Restaurer
nekro-agent-toolkit -i [PATH]
nekro-agent-toolkit -u [PATH]
nekro-agent-toolkit -b [DATA_DIR] BACKUP_DIR
nekro-agent-toolkit -r BACKUP_FILE [DATA_DIR]

# Ajouter une dépendance à requirements.txt et pyproject.toml
./scripts/add-dependency.sh <package_name>
```

## Informations supplémentaires

- Exigences : Python 3.6+, Docker, Docker Compose
- Licence : Voir [LICENSE](../LICENSE)

## 🌐 Pour les utilisateurs d'autres langues

| [Lire en chinois](../README.md) | [Read in English](./README-EN.md) | [اقرأ باللغة العربية](./README-AR.md) | [Читать на русском](./README-RU.md) | [Leer en español](./README-ES.md) |