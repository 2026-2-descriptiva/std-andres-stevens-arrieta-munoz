def pregunta_03():
    """
    Usando `data/tbl0.tsv`, cuente cuántos registros hay para cada categoría
    de la columna `c1`. Retorne una Serie de Pandas cuyo índice son las
    categorías, en orden alfabético, y cuyos valores son las cantidades.

    Ejemplo del formato de la respuesta:

        c1
        A     8
        B     7
        C     5
        ...
    """

    from pathlib import Path

    import pandas as pd

    DATA_DIRECTORY = Path(__file__).resolve().parent.parent / "data"
    INPUT_FILE = DATA_DIRECTORY / "tbl0.tsv"

    df = pd.read_csv(INPUT_FILE, sep="\t")

    result = df.groupby("c1").size()

    return result   

if __name__ == "__main__":
    print(pregunta_03())
