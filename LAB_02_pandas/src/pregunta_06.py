def pregunta_06():
    """
    Usando `data/tbl1.tsv`, obtenga los valores distintos de la columna `c4`,
    conviértalos a mayúsculas y retórnelos como una lista ordenada
    alfabéticamente.

    Ejemplo del formato de la respuesta:

        ["A", "B", "C", "D", "E", "F", "G"]
    """
    from pathlib import Path

    import pandas as pd

    DATA_DIRECTORY = Path(__file__).resolve().parent.parent / "data"
    INPUT_FILE = DATA_DIRECTORY / "tbl1.tsv"

    df = pd.read_csv(INPUT_FILE, sep="\t")

    result = df["c4"].str.upper().sort_values().unique().tolist()

    return result

if __name__ == "__main__":

    print(pregunta_06())

