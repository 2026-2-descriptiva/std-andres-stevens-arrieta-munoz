def pregunta_12():
    """
    Para cada letra de la primera columna (`letter`), sume todos los valores
    numéricos de los pares `clave:valor` de la quinta columna (`metrics`).
    Retorne un diccionario `{letra: suma}` con las letras en orden alfabético.

    Ejemplo del formato de la respuesta:

        {"A": 177, "B": 187, "C": 114, ...}
    """

    from pathlib import Path

    import pandas as pd

    DATA_DIRECTORY = Path(__file__).resolve().parent.parent / "data"
    INPUT_FILE = DATA_DIRECTORY / "data.csv.gz"

    df = pd.read_csv(INPUT_FILE, compression="gzip", sep="\t", header=None)

    # Una fila por cada par clave:valor, conservando la letra de la fila
    pairs_df = pd.DataFrame(
        {
            "letter": df[0],
            "pair": df[4].str.split(","),
        }
    ).explode("pair")

    # Tomar la parte numérica de cada par "clave:valor"
    pairs_df["value"] = pairs_df["pair"].str.split(":").str[1].astype(int)

    # Agrupar por letra y sumar
    letter_sums = pairs_df.groupby("letter")["value"].sum().sort_index()

    return {k: int(v) for k, v in letter_sums.items()}


if __name__ == "__main__":
    print(pregunta_12())