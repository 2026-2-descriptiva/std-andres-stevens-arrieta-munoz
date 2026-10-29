def pregunta_01():
    """
    Una aseguradora quiere publicar datos de sus afiliados para que un grupo
    de investigación estudie el costo de los seguros, sin que nadie pueda
    reconocer a una persona. El archivo `data/insurance.csv.gz` tiene una fila
    por afiliado con su edad (`age`), sexo (`sex`), índice de masa corporal
    (`bmi`), número de hijos (`children`), si fuma (`smoker`), región
    (`region`) y el costo de su seguro (`charges`).

    El archivo no tiene nombres ni documentos, pero eso no basta: la edad, el
    sexo, el índice de masa corporal, el número de hijos y la región son
    cuasi-identificadores, porque combinados pueden señalar a una persona.
    `smoker` es el atributo sensible que se quiere proteger.

    En este laboratorio usted va a medir el riesgo de reidentificación y a
    decidir qué publicar. Use estas definiciones:

    - Una clase de equivalencia es un grupo de registros con los mismos
      valores en todos los cuasi-identificadores. Un conjunto de datos cumple
      k-anonimato si toda clase tiene al menos k registros. Use k = 5.
    - `age_group`: `18-29`, `30-39`, `40-49` o `50-64`.
    - `bmi_group`: `bajo peso` (menos de 18.5), `normal` (desde 18.5 y menos
      de 25), `sobrepeso` (desde 25 y menos de 30) u `obesidad` (30 o más).
    - `children_group`: `0`, `1-2` o `3+`.

    Evalúe dos esquemas de generalización:

    - `with_children`: `age_group`, `sex`, `bmi_group`, `children_group` y
      `region`.
    - `without_children`: `age_group`, `sex`, `bmi_group` y `region`; el
      número de hijos no se publica.

    En cada esquema, suprima (no publique) los registros de las clases con
    menos de 5 registros. Luego, entre las clases publicadas, identifique las
    que no tienen diversidad en el atributo sensible, es decir, aquellas en
    las que todos los afiliados fuman o ninguno fuma: en esas clases, saber
    que alguien pertenece a ellas revela si fuma.

    Escriba `submission/privacy_report.json` con estas claves:

    - `original_k`: el menor tamaño de clase usando los cuasi-identificadores
      originales, sin generalizar.
    - `original_unique_records`: cuántos registros son los únicos de su clase
      con los cuasi-identificadores originales.
    - `schemes`: un diccionario con una entrada por esquema (`with_children` y
      `without_children`), cada una con las claves `quasi_identifiers` (la
      lista de columnas del esquema), `equivalence_classes` (clases antes de
      suprimir), `k_before_suppression`, `suppressed_records`,
      `published_records`, `published_classes`,
      `classes_without_smoker_diversity` y
      `records_without_smoker_diversity`.
    - `selected_scheme`: el esquema que suprime menos registros.
    - `mean_charges_original` y `mean_charges_published`: el costo promedio
      de todos los afiliados y el de los registros publicados con el esquema
      seleccionado.
    - `smoker_rate_original` y `smoker_rate_published`: la proporción de
      fumadores en ambos casos.

    Escriba también `submission/insurance_published.csv`, sin el índice de
    Pandas, con los registros publicados del esquema seleccionado, en el
    mismo orden del archivo original, y las columnas del esquema seguidas de
    `smoker` y `charges`.

    La función también debe retornar el reporte como un diccionario.

    Ejemplo del formato del reporte:

        {
          "original_k": 1,
          "original_unique_records": 1330,
          "schemes": {
            "with_children": {
              "quasi_identifiers": ["age_group", "sex", ...],
              "equivalence_classes": 278,
              ...
            },
            ...
          },
          ...
        }
    """

    import json
    from pathlib import Path
 
    import numpy as np
    import pandas as pd
 
    BASE_DIRECTORY = Path(__file__).resolve().parent.parent
    INPUT_FILE = BASE_DIRECTORY / "data" / "insurance.csv.gz"
    OUTPUT_DIRECTORY = BASE_DIRECTORY / "submission"
    OUTPUT_FILE = OUTPUT_DIRECTORY / "insurance_published.csv"
    REPORT_FILE = OUTPUT_DIRECTORY / "privacy_report.json"
 
    K = 5
    COLUMNS = ["age", "sex", "bmi", "children", "smoker", "region", "charges"]
 
    # Cargar los datos (con o sin fila de encabezado)
    df = pd.read_csv(INPUT_FILE, compression="gzip")
    if "age" not in df.columns:
        df = pd.read_csv(INPUT_FILE, compression="gzip", header=None, names=COLUMNS)
    df = df.reset_index(drop=True)
 
    # Cuasi-identificadores originales, sin generalizar
    original_qi = ["age", "sex", "bmi", "children", "region"]
    original_sizes = df.groupby(original_qi, observed=True).size()
    original_k = int(original_sizes.min())
    original_unique_records = int((original_sizes == 1).sum())
 
    # Generalización
    df["age_group"] = pd.cut(
        df["age"],
        bins=[-np.inf, 30, 40, 50, np.inf],
        labels=["18-29", "30-39", "40-49", "50-64"],
        right=False,
    ).astype(str)
 
    df["bmi_group"] = pd.cut(
        df["bmi"],
        bins=[-np.inf, 18.5, 25, 30, np.inf],
        labels=["bajo peso", "normal", "sobrepeso", "obesidad"],
        right=False,
    ).astype(str)
 
    df["children_group"] = pd.cut(
        df["children"],
        bins=[-np.inf, 1, 3, np.inf],
        labels=["0", "1-2", "3+"],
        right=False,
    ).astype(str)
 
    df["is_smoker"] = df["smoker"].astype(str).str.lower().eq("yes")
 
    schemes_definition = {
        "with_children": ["age_group", "sex", "bmi_group", "children_group", "region"],
        "without_children": ["age_group", "sex", "bmi_group", "region"],
    }
 
    schemes = {}
    published_masks = {}
 
    for name, quasi_identifiers in schemes_definition.items():
        grouped = df.groupby(quasi_identifiers, observed=True)
        class_size = grouped["is_smoker"].transform("size")
        class_smokers = grouped["is_smoker"].transform("sum")
 
        published = class_size >= K
        no_diversity = published & ((class_smokers == 0) | (class_smokers == class_size))
 
        sizes = grouped.size()
        published_sizes = sizes[sizes >= K]
 
        smoker_per_class = grouped["is_smoker"].agg(["size", "sum"])
        smoker_per_class = smoker_per_class[smoker_per_class["size"] >= K]
        classes_without_diversity = (
            (smoker_per_class["sum"] == 0)
            | (smoker_per_class["sum"] == smoker_per_class["size"])
        ).sum()
 
        schemes[name] = {
            "quasi_identifiers": quasi_identifiers,
            "equivalence_classes": int(len(sizes)),
            "k_before_suppression": int(sizes.min()),
            "suppressed_records": int((~published).sum()),
            "published_records": int(published.sum()),
            "published_classes": int(len(published_sizes)),
            "classes_without_smoker_diversity": int(classes_without_diversity),
            "records_without_smoker_diversity": int(no_diversity.sum()),
        }
        published_masks[name] = published
 
    selected_scheme = min(
        schemes, key=lambda name: schemes[name]["suppressed_records"]
    )
    mask = published_masks[selected_scheme]
    published_df = df.loc[mask]
 
    report = {
        "original_k": original_k,
        "original_unique_records": original_unique_records,
        "schemes": schemes,
        "selected_scheme": selected_scheme,
        "mean_charges_original": float(df["charges"].mean()),
        "mean_charges_published": float(published_df["charges"].mean()),
        "smoker_rate_original": float(df["is_smoker"].mean()),
        "smoker_rate_published": float(published_df["is_smoker"].mean()),
    }
 
    OUTPUT_DIRECTORY.mkdir(parents=True, exist_ok=True)
 
    output_columns = schemes_definition[selected_scheme] + ["smoker", "charges"]
    published_df[output_columns].to_csv(OUTPUT_FILE, index=False)
 
    with open(REPORT_FILE, "w", encoding="utf-8") as file:
        json.dump(report, file, ensure_ascii=False, indent=2)
 
    return report

if __name__ == "__main__":
    report = pregunta_01()
