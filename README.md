# It's most def...

`itsmostdef...` is a python package that fast and simple classifies the most likely content in a `.fastq|.fasta` file.

## Install

```bash
pip install itsmostdef
```


## Dependencies
* kraken2 (with DB)
* pyfastx 
* pandas

## USAGE

`itsmostdef... <fastq_file> <kraken_db> <n_threads> [kraken2_path (default = kraken2)]`
* `fastq_file`: path to the fastq file 
* `kraken_db`: path to the kraken database 
* `n_threads`: number of threads for kraken to use 
* `kraken2_path`: path to kraken2 executable. defaults to kraken2 

## Logic

Samples 5000 reads from the `fastq_file` using `pyfastx`. Classifies the reads with kraken2 and the database. Prints the most common species in the `fastq_file`.

## Example output

```bash

                    ..::RESULTS::..
---------------------------------------------------------
[PERCENT UNCLASSIFIED READS]:            18.08%
---------------------------------------------------------
                    ------------------
                    |IT'S MOST DEF...|
                    ------------------

[STAPHYLOCOCCUS AUREUS]:                 9.99%
[HOMO SAPIENS]:                          6.48%
[DIETZIA LUTEA]:                         0.42%
---------------------------------------------------------
                [NOTHING MORE WAS DETECTED]
---------------------------------------------------------
```
