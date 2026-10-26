def pregunta_01():
    """
    El archivo `data/solicitudes_de_credito.csv.gz` contiene las solicitudes de
    un programa de crédito, pero llegó sucio: tiene una columna de índice que
    no pertenece a los datos, registros duplicados, registros incompletos y
    valores que representan lo mismo escritos de formas distintas en los
    campos de texto, las fechas, el estrato y el monto.

    Su tarea es limpiarlo y guardar el resultado en
    `submission/solicitudes_de_credito.csv`, usando punto y coma (`;`) como
    separador y sin el índice de Pandas.

    El archivo limpio debe cumplir lo siguiente:

    - Contiene solamente las nueve columnas `sexo`, `tipo_de_emprendimiento`,
      `idea_negocio`, `barrio`, `estrato`, `comuna_ciudadano`,
      `fecha_de_beneficio`, `monto_del_credito` y `línea_credito`, en ese
      orden.
    - Los campos de texto están en minúsculas y sus palabras separadas por
      espacios.
    - `estrato` y `monto_del_credito` son números enteros, sin símbolos ni
      separadores de miles.
    - Todas las fechas de `fecha_de_beneficio` usan un mismo formato, por
      ejemplo `AAAA-MM-DD`.
    - No hay registros incompletos. La única excepción es
      `comuna_ciudadano`: sus valores faltantes son parte de los datos
      originales y deben conservarse.
    - No hay registros duplicados.

    Ejemplo del formato del archivo:

        sexo;tipo_de_emprendimiento;idea_negocio;barrio;estrato;...
        femenino;comercio;almacen de ropa en;los cerros el vergel;2;...
        ...
    """
    from pathlib import Path

    import pandas as pd

    BASE_DIRECTORY = Path(__file__).resolve().parent.parent
    INPUT_FILE = BASE_DIRECTORY / "data" / "solicitudes_de_credito.csv.gz"
    OUTPUT_FILE = BASE_DIRECTORY / "submission" / "solicitudes_de_credito.csv"

    # Todo como texto y sin convertir valores a NaN automáticamente
    df = pd.read_csv(
        INPUT_FILE, sep=";", dtype=str, compression="gzip", keep_default_na=False
    )

    # Eliminar la columna de índice que no pertenece a los datos
    df = df.iloc[:, 1:]

    df.columns = [
        "sexo",
        "tipo_de_emprendimiento",
        "idea_negocio",
        "barrio",
        "estrato",
        "comuna_ciudadano",
        "fecha_de_beneficio",
        "monto_del_credito",
        "línea_credito",
    ]

    # Texto: minúsculas, guiones como separadores, espacios únicos, sin bordes
    text_columns = [
        "sexo",
        "tipo_de_emprendimiento",
        "idea_negocio",
        "barrio",
        "comuna_ciudadano",
        "línea_credito",
    ]
    for column in text_columns:
        df[column] = (
            df[column]
            .str.lower()
            .str.replace(r"[_\-]+", " ", regex=True)
            .str.replace(r"\s+", " ", regex=True)
            .str.strip()
            .replace("", pd.NA)
        )

    # Estrato: entero ("02" -> 2)
    df["estrato"] = pd.to_numeric(df["estrato"].str.strip(), errors="coerce").astype("Int64")

    # Monto: "$ 1,200,000.00" -> 1200000
    monto = (
        df["monto_del_credito"]
        .str.replace(r"[^\d.,]", "", regex=True)
        .str.replace(",", "", regex=False)
        .str.replace(r"\.\d{1,2}$", "", regex=True)  # decimales
        .str.replace(".", "", regex=False)  # separadores de miles restantes
        .replace("", pd.NA)
    )
    
    df["monto_del_credito"] = pd.to_numeric(monto, errors="coerce").astype("Int64")

    # Fechas: cada formato por separado (dayfirst alteraría aaaa/mm/dd)
    fecha = df["fecha_de_beneficio"].str.strip().str.replace("-", "/", regex=False)
    es_anio_primero = fecha.str.match(r"^\d{4}/")
    fecha_a = pd.to_datetime(
        fecha.where(es_anio_primero), format="%Y/%m/%d", errors="coerce"
    )
    fecha_b = pd.to_datetime(
        fecha.where(~es_anio_primero), format="%d/%m/%Y", errors="coerce"
    )
    df["fecha_de_beneficio"] = fecha_a.fillna(fecha_b).dt.strftime("%Y-%m-%d")

    # Eliminar registros incompletos, excepto comuna_ciudadano
    df = df.dropna(subset=[c for c in df.columns if c != "comuna_ciudadano"])

    # Eliminar duplicados
    df = df.drop_duplicates()

    OUTPUT_FILE.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(OUTPUT_FILE, sep=";", index=False, encoding="utf-8")


if __name__ == "__main__":
    pregunta_01()


if __name__ == "__main__":
    pregunta_01()


