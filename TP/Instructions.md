## 🗓️ **Jour 1 – Introduction DevOps + Pipelines de base (GitHub + GitLab)**

### Démo 1 : Création d’un projet Java API + client lourd (JavaFX), découpage
1. **Création du projet API Java :**
   - Ouvrir IntelliJ IDEA ou Eclipse.
   - Créer un nouveau projet Java.
   - Ajouter une classe principale pour exposer des endpoints via un framework comme **Spring Boot** ou **JAX-RS**.
   
2. **Création de l’application client JavaFX :**
   - Créer un projet JavaFX dans le même repository.
   - Ajouter une fenêtre basique qui consomme les APIs créées.
   
3. **Découpage du projet en modules :**
   - Organiser l'API et l'application client JavaFX dans deux modules séparés mais dans le même repository.

### Démo 2 : Création du pipeline GitHub Actions
1. **Créer un dépôt GitHub :**
   - Allez sur GitHub, créez un nouveau repository pour l'API Java et le client JavaFX.
   
2. **Configurer le workflow GitHub Actions :**
   - Créez un fichier `.github/workflows/build.yml`.
   - Ajouter des étapes de build et de tests dans le fichier YAML. Exemple :
     ```yaml
     name: CI Pipeline
     on: [push, pull_request]
     jobs:
       build:
         runs-on: ubuntu-latest
         steps:
           - name: Checkout code
             uses: actions/checkout@v2
           - name: Set up JDK 11
             uses: actions/setup-java@v2
             with:
               java-version: 11
           - name: Build and Test
             run: ./mvnw clean install
     ```

---

## 🗓️ **Jour 2 – Docker + CI conditionnelle**

### Démo 1 : Création d’un Dockerfile pour l’API Java
1. **Création du Dockerfile :**
   - Créez un fichier `Dockerfile` à la racine du projet.
   - Exemple de contenu pour une application Java :
     ```dockerfile
     FROM openjdk:11-jre-slim
     COPY target/myapp.jar /app/myapp.jar
     WORKDIR /app
     ENTRYPOINT ["java", "-jar", "myapp.jar"]
     ```

2. **Construire l'image Docker localement :**
   - Exécutez la commande suivante dans le terminal :
     ```bash
     docker build -t myapp .
     ```

3. **Lancer l’application Docker :**
   - Après la construction de l'image, lancez le conteneur :
     ```bash
     docker run -p 8080:8080 myapp
     ```

### Démo 2 : Pipeline conditionnel dans GitHub Actions
1. **Modifier le pipeline GitHub pour ajouter la condition Docker :**
   - Ajoutez un job Docker dans le pipeline, qui se déclenche uniquement si les tests sont réussis :
     ```yaml
     jobs:
       build:
         runs-on: ubuntu-latest
         steps:
           - name: Checkout code
             uses: actions/checkout@v2
           - name: Set up JDK 11
             uses: actions/setup-java@v2
           - name: Build and Test
             run: ./mvnw clean test
       docker:
         if: success()
         runs-on: ubuntu-latest
         steps:
           - name: Build Docker image
             run: docker build -t myapp .
           - name: Push Docker image
             run: docker push myapp
     ```

---

## 🗓️ **Jour 3 – Qualité, changelog, matrice de build**

### Démo 1 : Création d’un job de changelog dans GitHub/GitLab
1. **Utiliser un outil comme `semantic-release` ou `github-changelog-generator` pour générer un changelog automatiquement.**
   - Ajouter le job de génération du changelog dans `.github/workflows/changelog.yml` :
     ```yaml
     jobs:
       changelog:
         runs-on: ubuntu-latest
         steps:
           - name: Checkout code
             uses: actions/checkout@v2
           - name: Install dependencies
             run: npm install
           - name: Generate Changelog
             run: github-changelog-generator
     ```

2. **Exécuter le job et vérifier le changelog généré.**

### Démo 2 : Création d’une matrice de build dans GitHub/GitLab
1. **Utiliser une matrice pour tester plusieurs versions Java :**
   - Exemple de configuration dans GitHub Actions pour tester avec Java 11 et Java 17 :
     ```yaml
     jobs:
       build:
         runs-on: ubuntu-latest
         strategy:
           matrix:
             java-version: [11, 17]
         steps:
           - name: Checkout code
             uses: actions/checkout@v2
           - name: Set up JDK
             uses: actions/setup-java@v2
             with:
               java-version: ${{ matrix.java-version }}
           - name: Build and Test
             run: ./mvnw clean install
     ```

2. **Vérifier que le pipeline s'exécute pour chaque version de Java définie dans la matrice.**

Voici la démo ajoutée pour la gestion du **code coverage** dans les pipelines CI, à insérer dans le **Jour 3 – Qualité, changelog, matrice de build** :


### Démo 3 : Ajout de la couverture de code (Code Coverage) dans le pipeline CI

1. **Installer un outil de couverture de code :**
   - Pour une application Java, nous allons utiliser **JaCoCo** pour générer un rapport de couverture de code.
   - Assurez-vous que JaCoCo est ajouté à votre fichier `pom.xml` (si vous utilisez Maven) ou `build.gradle` (si vous utilisez Gradle).

   **Exemple pour Maven :**
   Ajoutez la dépendance JaCoCo dans la section `plugins` de votre fichier `pom.xml` :
   ```xml
   <build>
     <plugins>
       <plugin>
         <groupId>org.jacoco</groupId>
         <artifactId>jacoco-maven-plugin</artifactId>
         <version>0.8.7</version>
         <executions>
           <execution>
             <goals>
               <goal>prepare-agent</goal>
               <goal>report</goal>
             </goals>
           </execution>
         </executions>
       </plugin>
     </plugins>
   </build>
   ```

   **Exemple pour Gradle :**
   Ajoutez ce code à votre fichier `build.gradle` :
   ```gradle
   plugins {
     id 'jacoco'
   }

   jacoco {
     toolVersion = "0.8.7"
   }

   test {
     useJUnitPlatform()
     finalizedBy jacocoTestReport
   }

   jacocoTestReport {
     dependsOn test
     reports {
       xml.enabled true
       html.enabled true
     }
   }
   ```

2. **Générer le rapport de couverture :**
   - Pour Maven, exécutez la commande suivante pour générer le rapport de couverture de code :
     ```bash
     mvn clean test
     ```
   - Le rapport sera généré dans le répertoire `target/site/jacoco/`.

   - Pour Gradle, exécutez :
     ```bash
     ./gradlew test jacocoTestReport
     ```

3. **Afficher le badge de couverture de code dans le pipeline :**
   - Une fois que le rapport de couverture est généré, nous allons l'ajouter au pipeline CI pour qu'il soit visible dans GitHub ou GitLab.
   - Ajoutez une étape dans le pipeline GitHub Actions pour télécharger et afficher le badge de couverture.
   
   **Exemple d'intégration dans `.github/workflows/ci.yml` :**
   ```yaml
   jobs:
     build:
       runs-on: ubuntu-latest
       steps:
         - name: Checkout code
           uses: actions/checkout@v2
         - name: Set up JDK 11
           uses: actions/setup-java@v2
           with:
             java-version: 11
         - name: Build and Test with JaCoCo
           run: mvn clean test
         - name: Upload code coverage to Coveralls
           uses: coverallsapp/github-action@v2
           with:
             github-token: ${{ secrets.GITHUB_TOKEN }}
   ```

4. **Vérifier le badge de couverture :**
   - Une fois le pipeline exécuté avec succès, vous pouvez intégrer le badge de couverture de code dans votre README ou tableau de bord de projet.
   - Utilisez un service comme **Coveralls** ou **Codecov** pour héberger et afficher les rapports de couverture.

   Exemple d'intégration du badge dans le `README.md` :
   ```markdown
   ![Coverage Badge](https://coveralls.io/repos/github/username/repository/badge.svg)
   ```

5. **Vérifier le rapport HTML localement :**
   - Le rapport HTML généré par JaCoCo peut être ouvert dans un navigateur pour vérifier la couverture de chaque classe et méthode.
   - Ouvrez `target/site/jacoco/index.html` (pour Maven) dans un navigateur pour consulter le rapport.

