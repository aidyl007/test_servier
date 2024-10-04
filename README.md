# Servier Test

This is a little project containing :
- `Dataflow pipeline`: to process raw layer data (csv & json formats)
this pipeline will:
     - read 4 source files in the servierconfigs bucket
     - clean data with appropriate transformations 
     - store the data in the destination tables 
     - create end process file in servierdataextract bucket, so that the data extractor module will be notified , and start the processing
- `Data Extractor module`: a cloud function tiggered by a pubsub message, to use a BQ job  in order to run a query on the previus raw layer tables, and store data in json result file . It will first read the file and search in firestore the query to exec accoding to the name file. A BQ job will run the query and save the result in both result table and result.json file under output folder



## Terraform

Here are the resources created by terraform:
 - `bigquery.tf`:  `drugs` , `pubmed` , `clinicaltrials` and `result` tables
 - `cloudfunction.tf`: Cloud function used in the data extractor module
 - `iam.tf`: service account, binding and roles
 - `notification.tf`:  pubsub topic and subscription
 - `storage.tf`: buckets to store source and output data



## Input parameters

In order to run the Servier technical test:
- Upload `drugs.csv`, `pubmed.csv`, `pubmed.json` and `clinical_trials.csv` to `gs://servierconfigs`
- Create a firestore collection named `config` with a document `servier_pipeline` containing this query:

```
WITH
  preprocessed_pubmed AS (
  SELECT
    id,
    journal,
    date,
    REGEXP_EXTRACT_ALL(LOWER(REGEXP_REPLACE(title, r'[^\w\s]', ' ')), r'\w+') AS word_list
  FROM
    `eco-watch-430116-g6.servier_test_dataset.pubmed` ),
  preprocessed_clinical_trials AS (
  SELECT
    id,
    journal,
    date,
    REGEXP_EXTRACT_ALL(LOWER(REGEXP_REPLACE(scientific_title, r'[^\w\s]', ' ')), r'\w+') AS word_list
  FROM
    `eco-watch-430116-g6.servier_test_dataset.clinicaltrials` )
SELECT
  DISTINCT drugs.drug AS drug,
  CAST(pubmed.id AS STRING) AS id,
  pubmed.journal AS journal,
  pubmed.date AS date
FROM
  `eco-watch-430116-g6.servier_test_dataset.drugs` AS drugs
JOIN
  preprocessed_pubmed AS pubmed
ON
  LOWER(drugs.drug) IN UNNEST(pubmed.word_list)
UNION ALL
SELECT
  DISTINCT drugs.drug AS drug,
  clinical_trials.id AS id,
  clinical_trials.journal AS journal,
  clinical_trials.date AS date
FROM
  `eco-watch-430116-g6.servier_test_dataset.drugs` AS drugs
JOIN
  preprocessed_clinical_trials AS clinical_trials
ON
  LOWER(drugs.drug) IN UNNEST(clinical_trials.word_list);
```

## Output
You can find the output data in this file after the end of processing `gs://servierdataextract/output/result.json`.

````
{"drug":"ETHANOL","id":"6","journal":"Psychopharmacology","date":"2020-01-01"}
{"drug":"TETRACYCLINE","id":"6","journal":"Psychopharmacology","date":"2020-01-01"}
{"drug":"TETRACYCLINE","id":"4","journal":"Journal of food protection","date":"2020-01-01"}
{"drug":"DIPHENHYDRAMINE","id":"NCT01967433","journal":"Journal of emergency nursing","date":"2020-01-01"}
{"drug":"DIPHENHYDRAMINE","id":"NCT04189588","journal":"Journal of emergency nursing","date":"2020-01-01"}
{"drug":"DIPHENHYDRAMINE","id":"NCT04237091","journal":"Journal of emergency nursing","date":"2020-01-01"}
{"drug":"BETAMETHASONE","id":"NCT04153396","journal":"Hôpitaux Universitaires de Genève","date":"2020-01-01"}
{"drug":"BETAMETHASONE","id":"10","journal":"The journal of maternal-fetal \u0026 neonatal medicine","date":"2020-01-01"}
{"drug":"BETAMETHASONE","id":"11","journal":"Journal of back and musculoskeletal rehabilitation","date":"2020-01-01"}
{"drug":"ISOPRENALINE","id":"9","journal":"Journal of photochemistry and photobiology. B, Biology","date":"2020-01-01"}
{"drug":"TETRACYCLINE","id":"5","journal":"American journal of veterinary research","date":"2020-01-02"}
{"drug":"EPINEPHRINE","id":"7","journal":"The journal of allergy and clinical immunology. In practice","date":"2020-02-01"}
{"drug":"ATROPINE","journal":"The journal of maternal-fetal \u0026 neonatal medicine","date":"2020-03-01"}
{"drug":"BETAMETHASONE","journal":"The journal of maternal-fetal \u0026 neonatal medicine","date":"2020-03-01"}
{"drug":"EPINEPHRINE","id":"8","journal":"The journal of allergy and clinical immunology. In practice","date":"2020-03-01"}
{"drug":"EPINEPHRINE","id":"NCT04188184","journal":"Journal of emergency nursing\\xc3\\x28","date":"2020-04-27"}
{"drug":"DIPHENHYDRAMINE","id":"1","journal":"Journal of emergency nursing","date":"2019-01-01"}
{"drug":"DIPHENHYDRAMINE","id":"2","journal":"Journal of emergency nursing","date":"2019-01-01"}
{"drug":"DIPHENHYDRAMINE","id":"3","journal":"The Journal of pediatrics","date":"2019-01-02"}

````

##  BONUS

Here you can find the first function of the bonus: get_journal_with_max_unique_drugs
used to retreive the journal which menstioned the most unique drugs.


 ##  SQL

Here you can fin two sql files (query_01, query_02) used to answer the relative 2 questions of the test

