Ce README détaille d'une part les différents appels aux wrappers getEval, getDrWHEval, getIMAPrecision et getIMARappel, qui permettent de créer des fichiers-projets lisibles sur Doccano.
Une fois les fichiers créés, il faut faire appel au wrapper sendProjectToDoccano pour créer les projets correspondants sur Doccano.
Les wrappers ont été créés pour évaluer la performance des extracteurs des compte-rendus d'imagerie (section Évaluation Imagerie), et les API de DrWH pour l'hypothèse, la négation et le contexte familial (section Évaluation DrWH).

D'autre part, il détaille les wrappers d'interactions avec l'API Doccano comme sendProjectToDoccano, addDocumentsToDoccanoProjects, addUsersRolesToDoccanoProjects.


# Préparation de fichiers-projets Doccano d'intérêt

## Évaluation Imagerie

### Rappel 

##### Avec getIMARecall.py :

```bash
 python3 getIMARecall.py --inputFolder "pymedext_annotations_results_examples/pymedext_regexp_examples/" --regexp "doccano_config/regexp_type.csv" 
``` 

##### Avec getEval.py :

--> La précision sera aussi faite sur tous les items du fichier de couples regex,type

```bash
python3 getEval.py --inputFolder pymedext_annotations_results_examples/pymedext_regexp_examples/ --typeEval N --annotation ima --regexp doccano_config/regexp_type.csv --numbEval 2 --rappel
```

### Précision

#### Avec un seul couple regex,type

##### Avec getIMAPrecision :

```bash 
python3 getIMAPrecision.py --inputFolder pymedext_annotations_results_examples/pymedext_regexp_examples/ --regexp ISCOVID,motif --numbEval 2 --rappel
```

##### Avec getEval.py :

```bash
python3 getEval.py --inputFolder pymedext_annotations_results_examples/pymedext_regexp_examples/ --typeEval N --annotation ima --regexp ISCOVID,motif --numbEval 4
```

#### Avec un fichier de couples regex,type

##### Avec getIMAPrecision :

```bash
python3 getIMAPrecision.py --inputFolder pymedext_annotations_results_examples/pymedext_regexp_examples/ --regexp doccano_config/regexp_type.csv --numbEval 2 
```

```bash
python3 getIMAPrecision.py --inputFolder pymedext_annotations_results_examples/pymedext_regexp_examples/ --regexp doccano_config/regexp_type.csv --numbEval 2 --rappel
```
Le rappel est fait sur le fichier

##### Avec getEval.py :

```bash
python3 getEval.py --inputFolder pymedext_annotations_results_examples/pymedext_regexp_examples/ --typeEval N --annotation ima --regexp doccano_config/regexp_type.csv --numbEval 2 
```



## Évaluation DrWH

#### Tirage aléatoire de N fichiers pymedexts à évaluer dans chaque classe :

##### Avec getDrWHeval :

```bash
python3 getDrWHEval.py --inputFolder pymedext_annotations_results_examples/pymedext_neg_fam_hyp_examples/ --typeEval classes --annotation neg --numbEval 3
```

##### Avec getEval.py :

```bash
python3 getEval.py --inputFolder pymedext_annotations_results_examples/pymedext_neg_fam_hyp_examples/ --typeEval classes --annotation hyp --numbEval 3
```

### Tirage aléatoire de N fichiers pymedexts :

##### Avec getDrWHeval :

```bash
python3 getDrWHEval.py --inputFolder pymedext_annotations_results_examples/pymedext_neg_fam_hyp_examples/ --typeEval N --annotation fam --numbEval 3
```

##### Avec getEval.py :

```bash
python3 getEval.py --inputFolder pymedext_annotations_results_examples/pymedext_neg_fam_hyp_examples/ --typeEval N --annotation neg --numbEval 3
```


# Intéractions avec l'API Doccano


## Envoie d'un projet sur Doccano

```bash
python3 getEval.py --inputFolder pymedext_annotations_results_examples/pymedext_neg_fam_hyp_examples/ --typeEval classes --annotation neg --numbEval 3
python3 sendProjectToDoccano.py -pro "Projet_TEST_Name" -fname "20200729-195332_3_classes_neg.jsonl" -dir . -format json -labels "correct;vert,c|incorrect;rouge,i|probleme;orange,o"
```

## Ajout d'utilisateurs et de leurs rôles

```bash
python3 addUsersRolesToDoccanoProjects.py -roles Hippolyte:annotation_approver;Laure:annotation_approver --project_names "Projet_TEST_Name"
```

## Partictulier à l'imagerie 

### Sélectionner les texts des documents annotés "probleme" dans les projets Doccano et les renvoyer sur Doccano dans des nouveaux projets 

```bash
selectProblemAnnotedDocumentsFromDoccanoProjects.py
```

### Ajout de documents à des projets existants sur Doccano (les recherche avec la regex)

```bash
python3 addDocumentsToDoccanoProjects.py -regex "ISCOVID" -dir <dir with the new files>
```


