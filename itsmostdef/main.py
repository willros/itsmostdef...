from pathlib import Path
import subprocess
import sys
import pandas as pd
import numpy as np
import pyfastx
import tempfile

N_READS = 5000

def help() -> None:
    print("[USAGE]:    ", end="")
    print(f"{sys.argv[0]} <fastq_file> <kraken_db> <n_threads> [kraken2_path (default = kraken2)]")
    sys.exit(1)


def wrangle_kraken(kraken: str) -> pd.DataFrame:
    kraken_df = (
        pd.read_csv(
            kraken, sep="\t", header=None,
            names=["percent", "count_clades", "count", "tax_lvl", "taxonomy_id", "name"]
        )
        .assign(name=lambda x: x.name.str.strip())
        .assign(
            domain=lambda x: np.select(
                [x.tax_lvl.isin(["D", "U", "R"])],
                [x.name],
                default=pd.NA
            )
        )
        .fillna(method="ffill")
        .loc[lambda x: x.tax_lvl.str.contains("U|S|P|G")]
        .loc[lambda x: x["count"] > 20]
        .sort_values("percent", ascending=False)
    )
    
    return kraken_df
    
    
def kraken_classify(
    fastq_file: str,
    db: str,
    threads: int,
    kraken2: str = None
) -> None:
    if not Path(fastq_file).exists():
        print(f"[ERROR:]   FASTQFILE: {fastq_file}, does not exist. Exiting")
        sys.exit(1)
    if not Path(db).exists():
        print(f"[ERROR]   DATABASE: {db}, does not exist. Exiting")
        sys.exit(1)

    fastq_file = pyfastx.Fastx(fastq_file)
    kraken2 = kraken2 or "kraken2"

    counter = 0
    with tempfile.NamedTemporaryFile(mode='a+') as subsampled_fastq:
        for x in fastq_file:
            print(f"@{x[0]}", file=subsampled_fastq)
            print(f"{x[1]}", file=subsampled_fastq)
            print(f"+", file=subsampled_fastq)
            print(f"{x[2]}", file=subsampled_fastq)
            
            counter += 1
            if counter > N_READS:
                break
    
        subsampled_fastq = subsampled_fastq.name

        with tempfile.NamedTemporaryFile(mode="a+") as kraken_report:
            command = f"{kraken2} --db {db} --threads {threads} --use-names {subsampled_fastq} --report {kraken_report.name}"
            print(f"Running kraken on {str(fastq_file)}")
                
            subprocess.call(command, shell=True, stderr=subprocess.DEVNULL, stdout=subprocess.DEVNULL)
            kraken = wrangle_kraken(kraken_report.name)
    
    return kraken


def main() -> None:
    if len(sys.argv) < 4:
        help()

    kraken2 = sys.argv[4] if len(sys.argv) == 5 else "kraken2"

    df = kraken_classify(
        sys.argv[1],
        sys.argv[2],
        sys.argv[3],
        kraken2,
    )

    print("")
    print("                    ..::RESULTS::..")
    print("---------------------------------------------------------")
    unclassified = df.loc[lambda x: x.tax_lvl == "U"]
    if unclassified.shape[0] != 0:
        unclassified_reads = "[PERCENT UNCLASSIFIED READS]:"
        print(f"{unclassified_reads:<40} {unclassified.percent.squeeze()}%")
        print("---------------------------------------------------------")
    print("                    ------------------")
    print("                    |IT'S MOST DEF...|")
    print("                    ------------------")
    print("")
    species = df.loc[lambda x: x.tax_lvl != "U"]
    if species.shape[0] == 0:
        print("                [NOTHING MORE WAS DETECTED]")
        print("---------------------------------------------------------")
        sys.exit(0)
    for x in species.itertuples():
        name = f"[{str(x.name).upper()}]:"
        print(f"{name:<40} {x.percent}%")
    print("---------------------------------------------------------")
    print("                [NOTHING MORE WAS DETECTED]")
    print("---------------------------------------------------------")


    sys.exit(0)


if __name__ == "__main__":
    main()
