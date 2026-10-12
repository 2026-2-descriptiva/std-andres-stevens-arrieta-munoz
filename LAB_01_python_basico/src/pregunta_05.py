def pregunta_05():
    """
    Para cada letra de la primera columna (`letter`), encuentre el valor
    máximo y el valor mínimo de la segunda columna (`value`). Retorne una lista
    de tuplas `(letra, máximo, mínimo)` ordenada alfabéticamente por la letra.

    Ejemplo del formato de la respuesta:

        [("A", 9, 2), ("B", 9, 1), ...]
    """

    from pathlib import Path

    import pandas as pd

    DATA_DIRECTORY = Path(__file__).resolve().parent.parent / "data"
    INPUT_FILE = DATA_DIRECTORY / "data.csv.gz"

    df = pd.read_csv(INPUT_FILE, compression="gzip", sep="\t", header=None)

    max_values = df.groupby(0)[1].max()
    min_values = df.groupby(0)[1].min()

    result = [(letter, int(max_values[letter]), int(min_values[letter])) for letter in sorted(max_values.index)]

    return result

if __name__ == "__main__":
    print(pregunta_05())


