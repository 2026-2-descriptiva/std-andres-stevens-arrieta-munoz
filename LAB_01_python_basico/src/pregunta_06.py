def pregunta_06():
    """
    La quinta columna (`metrics`) contiene pares `clave:valor` separados por
    comas. Para cada clave, encuentre el valor mínimo y el valor máximo que
    aparecen en todo el archivo. Retorne una lista de tuplas
    `(clave, mínimo, máximo)` ordenada alfabéticamente por la clave.

    Observe que el orden es mínimo y luego máximo, al contrario de la
    pregunta 5.

    Ejemplo del formato de la respuesta:

        [("aaa", 1, 9), ("bbb", 1, 9), ...]
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
    metrics_df["value"] = pd.to_numeric(metrics_df["value"], errors="coerce")
    # Agrupar por clave y encontrar el mínimo y máximo
    min_values = metrics_df.groupby("key")["value"].min()
    max_values = metrics_df.groupby("key")["value"].max()

    result = [(key, int(min_values[key]), int(max_values[key])) for key in sorted(min_values.index)]

    return result

if __name__ == "__main__":
    print(pregunta_06())