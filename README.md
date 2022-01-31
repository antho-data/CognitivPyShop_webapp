# CognitivPyShop_webapp

![Capture](https://user-images.githubusercontent.com/83237498/128639441-84ef5164-f10b-483c-8993-e4681c9ed578.JPG)



## 1- Description du projet
Le projet s’inscrit dans le cadre d’un challenge proposé par « Rakuten Institute of Technology » et a comme objectif de permettre de prédire la catégorie d’un objet lors de sa mise en vente sur la plateforme de e-commerce Rakuten à partir de son titre, de sa description et de son visuel.

## 2- Source du Dataset
Pour réaliser ce projet, nous utiliserons les datasets X_train et y_train disponibles sur le site du challenge ainsi que les images associées aux articles présents dans le dataset également mis à disposition.

Ces datasets sont mis à disposition par Rakuten, et sont issues du site internet de ecommerce https://fr.shopping.rakuten.com/



## 3- Structure et éléments du dataset
Le dataset Rakuten est constitué de :
-	Trois fichiers csv : un jeu de features d‘entrainement, un jeu avec les catégories associées et un jeu contenant des features pour tests
-	Un dossier « Images » contenant lui-même deux dossiers nommés respectivement « image_train » et « image_test » dans lesquels sont rangés les images des produits (qui ont été rangés dans des sous répertoires associés aux catégories des objets dans la phase de preprocessing)

Ci-dessous, vous trouverez une vision graphique de la structure globale des données :
![image](https://user-images.githubusercontent.com/83237498/128336530-d47f7ac6-d56a-4562-a573-aafec78fad14.png)


## 4 - Représentation des données (X, y)

La première étape de la modélisation du problème consiste à mettre en forme les données fournies afin de produire des premières visualisations et de préparer le set d’entrainement qui sera ensuite utilisé par les modèles de datascience.

Nous avons ainsi constitué deux sets de données, l’un permettant d’analyser les données textuelles, et le second permettant d’analyser les données visuelles. Ces deux sets de données ont été créés à partir d’une jointure entre les données X_train et y_train fournies par Rakuten.

- Analyse globale :
Chaque article a un unique product_id et une unique image_id, et ces id ne sont liés qu’à un article.

Un set global a été constitué en :
- Ajoutant une colonne reconstituant un lien relatif vers l’image associé à l’article
- Supprimant les colonnes product_id et image_id qui sont intégrés dans la colonne
précédemment ajoutée
- Remplaçant la colonne prdtypecode par un label chronologique et ajoutant sa
description

![Capture](https://user-images.githubusercontent.com/83237498/128639397-010c927e-3d72-42eb-b698-994a683d514a.JPG)



