def pregunta_01():
    """
    El archivo `data/clusters_report.txt` es un reporte de clústeres de
    palabras clave pensado para ser leído por una persona, no por un programa:
    los encabezados ocupan varias líneas, las columnas están alineadas con
    espacios y la lista de palabras clave de un clúster continúa en las líneas
    siguientes.

    Su tarea es convertir ese reporte en un DataFrame de Pandas con una fila
    por clúster y las columnas:

    - `cluster`: número del clúster, como entero.
    - `cantidad_de_palabras_clave`: como entero.
    - `porcentaje_de_palabras_clave`: como número decimal; por ejemplo, el
      texto `15,9 %` debe quedar como `15.9`.
    - `principales_palabras_clave`: todas las palabras clave del clúster en un
      solo texto, separadas por una coma y un único espacio.

    Retorne el DataFrame.

    Ejemplo del formato de la respuesta (se omite la última columna):

           cluster  cantidad_de_palabras_clave  porcentaje_de_palabras_clave
        0        1                         105                          15.9
        1        2                         102                          15.4
        ...
    """

    import re
    from pathlib import Path

    import pandas as pd

    DATA_DIRECTORY = Path(__file__).resolve().parent.parent / "data"
    INPUT_FILE = DATA_DIRECTORY / "clusters_report.txt"

    lines = INPUT_FILE.read_text(encoding="utf-8").splitlines()

    # Línea inicial de un clúster: número, cantidad, porcentaje con coma y "%"
    row_pattern = re.compile(r"^\s*(\d+)\s+(\d+)\s+(\d+(?:[.,]\d+)?)\s*%\s*(.*)$")

    clusters = []

    for line in lines:
        match = row_pattern.match(line)

        if match:
            cluster, cantidad, porcentaje, palabras = match.groups()
            clusters.append(
                {
                    "cluster": int(cluster),
                    "cantidad_de_palabras_clave": int(cantidad),
                    "porcentaje_de_palabras_clave": float(porcentaje.replace(",", ".")),
                    "principales_palabras_clave": palabras.strip(),
                }
            )
        elif clusters and line.strip():
            # Continuación de la lista de palabras clave del clúster actual
            clusters[-1]["principales_palabras_clave"] += " " + line.strip()

    df = pd.DataFrame(clusters)

    # Normalizar espacios, dejar ", " entre palabras y quitar el punto final
    df["principales_palabras_clave"] = (
        df["principales_palabras_clave"]
        .str.replace(r"\s+", " ", regex=True)
        .str.replace(r"\s*,\s*", ", ", regex=True)
        .str.strip()
        .str.rstrip(".")
    )

    return df


if __name__ == "__main__":
    print(pregunta_01())