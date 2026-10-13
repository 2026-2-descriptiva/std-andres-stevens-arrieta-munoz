def pregunta_11():
    """
    La cuarta columna (`codes`) contiene letras minúsculas separadas por
    comas. Para cada una de esas letras, sume los valores de la segunda
    columna (`value`) de los registros en los que aparece. Retorne un
    diccionario `{letra: suma}` con las letras en orden alfabético.

    Ejemplo del formato de la respuesta:

        {"a": 122, "b": 49, "c": 91, ...}
    """

    from pathlib import Path

    import pandas as pd

    DATA_DIRECTORY = Path(__file__).resolve().parent.parent / "data"
    INPUT_FILE = DATA_DIRECTORY / "data.csv.gz"

    df = pd.read_csv(INPUT_FILE, compression="gzip", sep="\t", header=None)

    # Una fila por cada letra, conservando el valor de la segunda columna
    codes_df = pd.DataFrame(
        {
            "letter": df[3].str.split(","),
            "value": df[1],
        }
    ).explode("letter")

    # Agrupar por letra y sumar los valores
    letter_sums = codes_df.groupby("letter")["value"].sum().sort_index()

    return letter_sums.to_dict()


if __name__ == "__main__":
    print(pregunta_11())