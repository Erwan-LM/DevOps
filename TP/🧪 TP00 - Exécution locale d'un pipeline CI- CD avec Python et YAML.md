# 🛠️ Exécution locale d'un pipeline CI/CD avec Python et YAML

## Étape 1 – Construction d’un pipeline

Ce projet propose une approche simple pour exécuter un pipeline CI/CD localement en utilisant un script Python (`runner.py`) qui lit et exécute les étapes définies dans un fichier YAML (`pipeline.yaml`). Cela permet de simuler un processus d'intégration et de déploiement continu sans recourir à des outils externes.

---

## 📁 Structure du projet

```
.
├── runner.py
├── pipeline.yaml
└── output/
    ├── test_result.txt
    └── build_artifact.txt
```

---

### 📄 Contenu de `pipeline.yaml`

Le fichier `pipeline.yaml` définit les différentes étapes (`stages`) du pipeline et les tâches (`jobs`) associées à chaque étape. Exemple :

```yaml
stages:
  - preparation
  - test
  - build
  - deploy

jobs:
  preparation_job:
    stage: preparation
    script:
      - echo "Préparation de l'environnement..."

  test_job:
    stage: test
    script:
      - echo "Exécution des tests..."
      - echo "Test réussi" > output/test_result.txt

  build_job:
    stage: build
    script:
      - echo "Construction du projet..."
      - echo "Fichier de build" > output/build_artifact.txt

  deploy_job:
    stage: deploy
    script:
      - echo "Déploiement de l'application..."
```

---

### 🐍 Script Python `runner.py`

Le script `runner.py` lit le fichier `pipeline.yaml` et exécute les commandes définies dans chaque tâche, en respectant l'ordre des étapes. Exemple :

```python
import yaml
import subprocess

# Charger le fichier YAML
with open('pipeline.yaml', 'r') as file:
    pipeline = yaml.safe_load(file)

stages = pipeline.get('stages', [])
jobs = pipeline.get('jobs', {})

for stage in stages:
    print(f"\n🔹 Stage : {stage}")
    for job_name, job in jobs.items():
        if job.get('stage') == stage:
            print(f"  ▶️ Job : {job_name}")
            for command in job.get('script', []):
                print(f"    $ {command}")
                subprocess.run(command, shell=True, check=True)
```

---

### ✅ Prérequis

* Python 3 installé sur votre système.
* Module `PyYAML` installé :

```bash
pip install pyyaml
```

---

### 🚀 Exécution du pipeline

1. Assurez-vous que les fichiers `runner.py` et `pipeline.yaml` sont dans le même répertoire.
2. Ouvrez un terminal et naviguez jusqu'à ce répertoire.
3. Exécutez le script Python :

```bash
python runner.py
```

---

### ⚠️ Résultat attendu (avec un 🐛 volontaire)

> Vous pourrez lancer le script, mais une erreur va intervenir. À vous de la corriger (soit dans le YAML, soit dans le script Python).

```bash
Création du répertoire : output

🔹 Stage : preparation
  ▶️ Job : preparation_job
    $ echo "Préparation de l'environnement..."
Préparation de l'environnement...

🔹 Stage : test
  ▶️ Job : test_job
    $ echo "Exécution des tests..."
Exécution des tests...
    $ echo "Test réussi" > output/test_result.txt

🔹 Stage : build
  ▶️ Job : build_job
    $ echo "Construction du projet..."
Construction du projet...
    $ echo "Fichier de build" > output/build_artifact.txt

🔹 Stage : deploy
  ▶️ Job : deploy_job
    $ echo "Déploiement de l'application..."
Déploiement de l'application...
```

---

## 📝 Étape suivante : créer et builder une application .NET

### 0. Prérequis

Vérifiez que **.NET SDK** est installé :

```bash
dotnet --version
```


### 1. Créer un projet console

```bash
dotnet new console -o DemoApp
```


### 2. Explorer le projet

```bash
cd DemoApp
dir  # ou ls sur Linux/Mac
```


### 3. Compiler l’application

```bash
dotnet build
```


### 4. Exécuter l’application

```bash
dotnet run
```

Vous devriez voir :

```
Hello, World!
```

### 5. Modifier le message

Ouvrez `Program.cs` et changez :

```csharp
Console.WriteLine("Hello, World CI-CD!");
```

Puis recompilez et relancez :

```bash
dotnet run
```


### 6. Adapter le pipeline

Intégrez ces commandes dans les étapes appropriées (`create`, `build`, `deploy`).

## 📝 Étape suivante : créer et tester un projet xUnit .NET

### 1. Créer un projet xUnit

```bash
dotnet new xunit -o Demo.Tests
cd Demo.Tests
```

### 2. Exécuter les tests

```bash
dotnet test
```

Résultat attendu :

```
Passed!  - Failed: 0, Passed: 1, Skipped: 0
```

### 3. Modifier un test

```csharp
[Fact]
public void AlwaysPass()
{
    Assert.True(true);
}
```

Puis relancer :

```bash
dotnet test
```

### 4. Adapter le pipeline

Intégrez ces commandes dans les étapes appropriées (`create`, `build`, `deploy`).

---

## 🧩 Personnalisation

Vous pouvez adapter le fichier `pipeline.yaml` pour inclure des étapes supplémentaires ou modifier les commandes exécutées dans chaque tâche selon les besoins spécifiques de votre projet.

---

## 📚 Ressources supplémentaires

* Documentation PyYAML : [https://pyyaml.org/wiki/PyYAMLDocumentation](https://pyyaml.org/wiki/PyYAMLDocumentation)
* Guide sur les pipelines CI/CD : [https://about.gitlab.com/stages-devops-lifecycle/continuous-integration/](https://about.gitlab.com/stages-devops-lifecycle/continuous-integration/)

