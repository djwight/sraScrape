import os
import sys
import logging
import json
import time
from subprocess import run

with open("params.json") as handle:
    RUN_PARAMS: dict = json.load(handle)

logging.basicConfig(
    format="%(asctime)s [%(levelname)s] %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
    level=logging.DEBUG,
    stream=sys.stderr,
)


def main() -> None:
    begin = time.time()
    logging.info("Script Starting...")

    # get the metagenome taxonomies from NCBI
    logging.info("Getting metagenome taxonomies...")
    cmd_taxonomy = (
        f"export NCBI_API_KEY={RUN_PARAMS['entrez_api']}; "
        f"esearch -db taxonomy -query \"{RUN_PARAMS['taxonomy_query']}\" "
        "| efetch -format xml "
        "| xtract -pattern Taxon -element ScientificName"
    )
    taxonomy_lst = (
        run(cmd_taxonomy, shell=True, capture_output=True)
        .stdout.decode("utf-8")
        .rstrip()
        .split("\n")
    )

    # get the uids for the RNA-seq SRA records with metagenome organisms
    logging.info(
        "Getting SRA records with metagenome-associated entries and RNA-seq..."
    )
    rna_search_term = f"({'[ORGANISM] OR '.join(taxonomy_lst)}[ORGANISM]){RUN_PARAMS['additional_sra_query']}"

    cmd_sra_uid = (
        f"export NCBI_API_KEY={RUN_PARAMS['entrez_api']}; "
        f'esearch -db sra -query "{rna_search_term}" '
        f"| efetch -format uid > {RUN_PARAMS['id_file']}"
    )
    run(cmd_sra_uid, shell=True)

    # read id list and count
    with open(RUN_PARAMS["id_file"], "r") as handle:
        n_ids = len(handle.readlines())
    logging.info(f"{n_ids} ids to be retrieved from SRA...")

    # run the SRA query to get the full xml records for extraction and extract the data
    cmd_sra = (
        f"export NCBI_API_KEY={RUN_PARAMS['entrez_api']}; "
        f"efetch -db sra -input {RUN_PARAMS['id_file']} -format xml "
        "| python parser.py "
        f"> data__{time.strftime('%Y_%m_%d', time.gmtime())}.tsv"
    )
    run(cmd_sra, shell=True)

    # remove the ids file as not needed
    os.remove(RUN_PARAMS["id_file"])

    end = time.time()
    logging.info(f"Script Completed in {round(end-begin)}s")


if __name__ == "__main__":
    main()
