def pregunta_08():
    """
    Repita la pregunta 7, pero ahora cada lista de letras debe contener cada
    letra una sola vez y estar ordenada alfabéticamente. Retorne una lista de
    tuplas `(valor, letras)` ordenada por el valor.

    Ejemplo del formato de la respuesta:

        [(0, ["C"]), (1, ["B", "E"]), (2, ["A", "E"]), ...]
    """

    from pathlib import Path

    import pandas as pd

    DATA_DIRECTORY = Path(__file__).resolve().parent.parent / "data"
    INPUT_FILE = DATA_DIRECTORY / "data.csv.gz"

    df = pd.read_csv(INPUT_FILE, compression="gzip", sep="\t", header=None)

    # Agrupar por valor y construir la lista de letras
    grouped = df.groupby(1)[0].apply(list)

    # Eliminar duplicados y ordenar alfabéticamente
    grouped = grouped.apply(lambda x: sorted(list(set(x))))

    result = [(value, letters) for value, letters in sorted(grouped.items())]

    return result

if __name__ == "__main__":
    print(pregunta_08())
