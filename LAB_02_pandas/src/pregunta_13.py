def pregunta_13():
    """
    Combine las tablas `data/tbl0.tsv` y `data/tbl2.tsv` usando la columna
    `c0`, que ambas comparten. Luego, sume los valores de la columna `c5b`
    para cada categoría de la columna `c1`. Retorne una Serie de Pandas cuyo
    índice son las categorías, en orden alfabético, y cuyos valores son las
    sumas.

    Ejemplo del formato de la respuesta:

        c1
        A    146
        B    134
        C     81
        ...
    """

    from pathlib import Path
    import pandas as pd

    DATA_DIRECTORY = Path(__file__).resolve().parent.parent / "data"
    INPUT_FILE = DATA_DIRECTORY / "tbl0.tsv"
    INPUT_FILE_2 = DATA_DIRECTORY / "tbl2.tsv"

    df = pd.read_csv(INPUT_FILE, sep="\t")
    df2 = pd.read_csv(INPUT_FILE_2, sep="\t")

    merged_df = pd.merge(df, df2, on="c0")
    result = merged_df.groupby("c1")["c5b"].sum().sort_index()

    return result

if __name__ == "__main__":
    print(pregunta_13())
