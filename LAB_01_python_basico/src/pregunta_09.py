def pregunta_09():
    """
    Cuente cuántas veces aparece cada clave en la quinta columna (`metrics`)
    de todo el archivo. Retorne un diccionario `{clave: cantidad}` con las
    claves en orden alfabético.

    Ejemplo del formato de la respuesta:

        {"aaa": 13, "bbb": 16, "ccc": 23, ...}
    """

    from pathlib import Path

    import pandas as pd

    DATA_DIRECTORY = Path(__file__).resolve().parent.parent / "data"
    INPUT_FILE = DATA_DIRECTORY / "data.csv.gz"

    df = pd.read_csv(INPUT_FILE, compression="gzip", sep="\t", header=None)

    # Extraer la columna de métricas y dividirla en pares clave:valor
    metrics_series = df[4].str.split(",", expand=True).stack()

    # Crear un DataFrame con las claves y valores
    metrics_df = metrics_series.str.split(":", expand=True)

    metrics_df.columns = ["key", "value"]

    # Contar la cantidad de veces que aparece cada clave
    key_counts = metrics_df["key"].value_counts().sort_index()

    # Convertir a diccionario
    result = key_counts.to_dict()

    return result

if __name__ == "__main__":
    print(pregunta_09())
