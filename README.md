# sraScrape

Repository for scraping metadata from SRA run records. Utilizes the [Entrez Direct](https://www.ncbi.nlm.nih.gov/books/NBK179288/).

## Running

1. Set up a `params.json` in the upper directory. with the following attributes:

```json
{
    "entrez_email": "<your email>",
    "entrez_api": "<your NCBI API key>",
    "taxonomy_query": "<the taxonomy query for getting the correct organisms fro SRA search>",
    "addional_sra_query": "<additional search terms for SRA query>",
    "id_file": "<name.txt file for saving the SRA query ids>"
}
```

2. Set up the python env

```bash
uv venv name -python 3.12
uv source /path/to/venv/bin/activate
uv pip install -r requirements.txt
```

3.  Run the script.

```bash
python runner.py
```