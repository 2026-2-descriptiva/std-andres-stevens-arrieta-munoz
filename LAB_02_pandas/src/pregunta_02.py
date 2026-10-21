def pregunta_02():
    """
    ¿Cuántas columnas tiene la tabla `data/tbl0.tsv`? Retorne la cantidad
    como un número entero.

    Ejemplo del formato de la respuesta:

        4
    """

    from pathlib import Path

    import pandas as pd

    DATA_DIRECTORY = Path(__file__).resolve().parent.parent / "data"
    INPUT_FILE = DATA_DIRECTORY / "tbl0.tsv"

    df = pd.read_csv(INPUT_FILE, sep="\t")
    result = len(df.columns)

    return result

if __name__ == "__main__":
    print(pregunta_02())

