import logging
import pandas as pd

logging.basicConfig(
    format="%(asctime)s [%(levelname)s] %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
    level=logging.DEBUG,
)

# triaged list of metagenomes from Hiu et al. 2024 (https://www.cell.com/cell/fulltext/S0092-8674(24)01085-7)
EXCEL_PATH = "data/mmc1.xlsx"
OUTPATH = "data/metagenomics_20200814.tsv"


def get_top_n(df: pd.DataFrame, col: str, top_n: int) -> dict:
    """Generates count statistics on the top n occuring instances in a df column.

    Args:
        df (pd.DataFrame): dataframe where the stats should be generated.
        col (str): name of the column to be analysed.
        top_n (int): number of top counts to be returned.

    Returns:
        dict:   dictionary containing the counts of the instances and proportion of all instances form top n
                most frequently occuring instances
    """
    df_top_n = pd.DataFrame(df[col].value_counts()[:top_n])
    df_top_n["prop"] = df_top_n["count"] / len(df)
    return df_top_n.to_dict(orient="index")


def main() -> None:
    logging.info("Script starting...")
    df = pd.read_excel(EXCEL_PATH, skiprows=2)

    # stats- dup SRA runs
    logging.info(f"Number of entries = {df.shape[0]}")
    dup_runs = df.duplicated(subset="Run").sum()
    logging.info(f"Number of duplicated SRA runs = {dup_runs}")

    # stats- top 10s
    logging.info(
        f"Top 10 sample sources: {get_top_n(df, col='ScientificName', top_n=10)}"
    )
    logging.info(f"Top 10 BioSamples: {get_top_n(df, col='BioSample', top_n=10)}")
    logging.info(
        f"Top 10 library types: {get_top_n(df, col='LibraryStrategy', top_n=10)}"
    )

    df.to_csv(OUTPATH, sep="\t", index=False)
    logging.info(f"File saves as tsv = '{OUTPATH}'")

    logging.info("Script completed!")


if __name__ == "__main__":
    main()
