def main():
    """
    Antes de limpiar o analizar un conjunto de datos, un analista debe
    documentar qué problemas tiene. En este laboratorio usted no va a limpiar
    `data/ventas.csv.gz`: va a construir un reporte de calidad que deje evidencia
    de sus problemas, tal como están en el archivo.

    Lea `data/ventas.csv.gz` sin modificar sus valores. Para trabajar con los
    encabezados, normalícelos: páselos a minúsculas, elimine los espacios al
    inicio y al final (y cualquier marca BOM) y reemplace los espacios
    internos por `_`. Las columnas requeridas son `supplier_id`, `supplier`,
    `country`, `city`, `purchase_date`, `amount`, `discount`, `weight`,
    `units`, `unit_price` y `contact_email`.

    Escriba el reporte en `submission/data_quality_report.json` con estas
    claves:

    - `row_count`: cantidad de filas de datos.
    - `column_count`: cantidad de columnas.
    - `missing_required_columns`: lista ordenada de columnas requeridas que no
      están en el archivo.
    - `unexpected_columns`: lista ordenada de columnas del archivo que no son
      requeridas.
    - `duplicate_row_count`: cantidad de filas idénticas a una fila anterior.
    - `duplicate_supplier_id_row_count`: cantidad de filas cuyo `supplier_id`
      aparece más de una vez (cuente todas esas filas, no solo las
      repetidas).
    - `missing_value_count_by_column`: diccionario con la cantidad de valores
      faltantes de cada columna. Considere faltantes las celdas vacías y las
      que contienen `N/A`.
    - `invalid_email_count`: cantidad de valores de `contact_email` que no
      tienen la forma `usuario@dominio.extension`.
    - `invalid_unit_count`: cantidad de valores numéricos de `units` que no son
      enteros positivos. Los valores faltantes no se cuentan aquí.
    - `country_values`: lista ordenada de los valores distintos de `country`,
      escritos exactamente como aparecen en el archivo.

    La función también debe retornar el reporte como un diccionario.

    Ejemplo del formato del reporte:

        {
          "row_count": 103,
          "column_count": 11,
          "missing_required_columns": [],
          ...
          "country_values": [" Colombia ", "CO", ...]
        }
    """
    import json
    import re
    from pathlib import Path

    import pandas as pd

    BASE_DIRECTORY = Path(__file__).resolve().parent.parent
    INPUT_FILE = BASE_DIRECTORY / "data" / "ventas.csv.gz"
    OUTPUT_FILE = BASE_DIRECTORY / "submission" / "data_quality_report.json"

    # Leer sin modificar valores: todo como texto y sin que pandas convierta
    # "N/A", "NA", "" u otros textos en NaN. utf-8-sig elimina el BOM.
    df = pd.read_csv(
        INPUT_FILE,
        compression="gzip",
        dtype=str,
        keep_default_na=False,
        na_filter=False,
        encoding="utf-8-sig",
    )

    # Normalizar encabezados
    df.columns = (
        df.columns.str.replace("\ufeff", "", regex=False)
        .str.strip()
        .str.lower()
        .str.replace(" ", "_", regex=False)
    )

    required_columns = [
        "supplier_id", "supplier", "country", "city", "purchase_date",
        "amount", "discount", "weight", "units", "unit_price", "contact_email",
    ]

    # Faltante = celda vacía o "N/A"
    es_faltante = df.isin(["", "N/A"])

    # Correos inválidos (los faltantes no se cuentan)
    patron_email = re.compile(r"[^@\s]+@[^@\s]+\.[^@\s]+")
    if "contact_email" in df.columns:
        emails = df.loc[~es_faltante["contact_email"], "contact_email"]
        invalid_email_count = int((~emails.apply(lambda x: bool(patron_email.fullmatch(x)))).sum())
    else:
        invalid_email_count = 0

    # Unidades inválidas: valores numéricos que no son enteros positivos
    if "units" in df.columns:
        units = pd.to_numeric(
            df.loc[~es_faltante["units"], "units"], errors="coerce"
        ).dropna()
        invalid_unit_count = int(((units <= 0) | (units != units.round())).sum())
    else:
        invalid_unit_count = 0

    if "supplier_id" in df.columns:
        duplicate_supplier_id_row_count = int(df.duplicated(subset=["supplier_id"], keep=False).sum())
    else:
        duplicate_supplier_id_row_count = 0

    report = {
        "row_count": int(len(df)),
        "column_count": int(len(df.columns)),
        "missing_required_columns": sorted(c for c in required_columns if c not in df.columns),
        "unexpected_columns": sorted(c for c in df.columns if c not in required_columns),
        "duplicate_row_count": int(df.duplicated().sum()),
        "duplicate_supplier_id_row_count": duplicate_supplier_id_row_count,
        "missing_value_count_by_column": {
            col: int(es_faltante[col].sum()) for col in df.columns
        },
        "invalid_email_count": invalid_email_count,
        "invalid_unit_count": invalid_unit_count,
        "country_values": sorted(df["country"].unique().tolist()) if "country" in df.columns else [],
    }

    OUTPUT_FILE.parent.mkdir(parents=True, exist_ok=True)
    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        json.dump(report, f, ensure_ascii=False, indent=2)

    return report


if __name__ == "__main__":
    main()


