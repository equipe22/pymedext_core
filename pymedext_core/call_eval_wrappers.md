# Evaluation Imagerie

## Rappel 

### Avec getIMARecall.py

```bash
 python3 getIMARecall.py --inputFolder "../pymedext_annotations_results_examples/pymedext_regexp_examples/" --regexp "../doccano_config/regexp_type.csv" 
``` 

### Avec getEval.py
--> La précision sera aussi faite sur tous les items du fichier de couples regex,type

```bash
python3 getEval.py --inputFolder ../pymedext_annotations_results_examples/pymedext_regexp_examples/ --typeEval N --annotation ima --regexp ../doccano_config/regexp_type.csv --numbEval 2 --rappel
```

## Précision


### Avec un seul couple regex,type

```bash
python3 getEval.py --inputFolder ../pymedext_annotations_results_examples/pymedext_regexp_examples/ --typeEval N --annotation ima --regexp ISCOVID,motif --numbEval 4
```

### Avec un fichier de couples regex,type

```bash
python3 getEval.py --inputFolder ../pymedext_annotations_results_examples/pymedext_regexp_examples/ --typeEval N --annotation ima --regexp ../doccano_config/regexp_type.csv --numbEval 2 
```

# Évaluation DrWH

## Tirage aléatoire de N pymedext à évaluer dans chaque classe :

```bash
python3 getEval.py --inputFolder ../pymedext_annotations_results_examples/pymedext_neg_fam_hyp_examples/ --typeEval classes --annotation neg --numbEval 3
```
## Tirage aléatoire de N pymedext :

```bash
python3 getEval.py --inputFolder ../pymedext_annotations_results_examples/pymedext_neg_fam_hyp_examples/ --typeEval classes --annotation neg --numbEval 3
```
