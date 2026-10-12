def pregunta_02():
    """
    Cuente cuántos registros hay para cada letra de la primera columna
    (`letter`). Retorne una lista de tuplas `(letra, cantidad)` ordenada
    alfabéticamente por la letra.

    Ejemplo del formato de la respuesta:

        [("A", 8), ("B", 7), ("C", 5), ...]
    """
    from pathlib import Path

    import pandas as pd

    DATA_DIRECTORY = Path(__file__).resolve().parent.parent / "data"
    INPUT_FILE = DATA_DIRECTORY / "data.csv.gz"

    df = pd.read_csv(INPUT_FILE, compression="gzip", sep="\t", header=None)

    counts = df.iloc[:, 0].value_counts().sort_index()

    return list(counts.items())

if __name__ == "__main__":
    print(pregunta_02())
