import pandas as pd


def build_cohort_analysis() -> pd.DataFrame:
    """
    Una tienda quiere saber si sus clientes vuelven a comprar después de su
    primera compra. Para responder, agrupe a los clientes en cohortes según
    el mes de su primera compra y mida, mes a mes, qué proporción de cada
    cohorte vuelve a comprar. Use `data/sales.csv.gz`, que tiene una fila por
    orden con su cliente (`CustomerID`) y su fecha (`OrderDate`).

    Use estas definiciones:

    - `cohort_month`: el mes de la primera compra del cliente, escrito como
      `AAAA-MM`.
    - `period_index`: los meses transcurridos desde `cohort_month`; es 0 en el
      mes de la primera compra, 1 en el mes siguiente, y así sucesivamente.
    - `active_customers`: la cantidad de clientes distintos de la cohorte que
      compraron en ese período.
    - `cohort_size`: la cantidad de clientes de la cohorte, es decir, sus
      clientes activos en el período 0.
    - `retention_rate`: `active_customers` sobre `cohort_size`.

    Genere dos archivos en `submission/`:

    1. `cohort_retention.csv`, sin el índice de Pandas, con las columnas
       `cohort_month`, `period_index`, `active_customers`, `cohort_size` y
       `retention_rate`, y una fila por cada combinación cohorte–período
       observada, ordenadas por cohorte y período.

    2. `cohort_retention_heatmap.png`, un mapa de calor de `retention_rate`
       con una fila por cohorte (eje vertical) y una columna por período
       (eje horizontal). Muestre los valores como porcentajes. Los períodos
       que todavía no se pueden observar para una cohorte no significan
       retención cero: déjelos vacíos en el mapa.

    La función también debe retornar la tabla de retención.

    Ejemplo del formato de `cohort_retention.csv`:

        cohort_month,period_index,active_customers,cohort_size,retention_rate
        2022-01,0,100,100,1.0
        2022-01,1,26,100,0.26
        ...
    """
    from pathlib import Path

    BASE_DIRECTORY = Path(__file__).resolve().parent.parent
    INPUT_FILE = BASE_DIRECTORY / "data" / "sales.csv.gz"
    OUTPUT_DIRECTORY = BASE_DIRECTORY / "submission"

    # Leer los datos de ventas
    sales_df = pd.read_csv(INPUT_FILE, parse_dates=["OrderDate"])

    # Crear la columna cohort_month
    sales_df["cohort_month"] = sales_df.groupby("CustomerID")["OrderDate"].transform(
        lambda x: x.min().strftime("%Y-%m")
    )

    # Crear la columna period_index
    sales_df["period_index"] = (
        (sales_df["OrderDate"].dt.year - sales_df["cohort_month"].str[:4].astype(int)) * 12
        + (sales_df["OrderDate"].dt.month - sales_df["cohort_month"].str[5:7].astype(int))
    )

    # Calcular active_customers y cohort_size
    cohort_data = (
        sales_df.groupby(["cohort_month", "period_index"])["CustomerID"]
        .nunique()
        .reset_index(name="active_customers")
    )
    cohort_sizes = (
        cohort_data[cohort_data["period_index"] == 0][["cohort_month", "active_customers"]]
        .rename(columns={"active_customers": "cohort_size"})
    )
    cohort_data = cohort_data.merge(cohort_sizes, on="cohort_month")

    # Calcular retention_rate
    cohort_data["retention_rate"] = (
        cohort_data["active_customers"] / cohort_data["cohort_size"]
    )

    # Guardar el archivo CSV
    OUTPUT_CSV_FILE = OUTPUT_DIRECTORY / "cohort_retention.csv"
    cohort_data.to_csv(OUTPUT_CSV_FILE, index=False)

    # Crear el mapa de calor
    import matplotlib.pyplot as plt
    import seaborn as sns

    heatmap_data = cohort_data.pivot(
        index="cohort_month", columns="period_index", values="retention_rate"
    )
    
    plt.figure(figsize=(12, 8))
    sns.heatmap(
        heatmap_data,
        annot=True,
        fmt=".0%",
        cmap="YlGnBu",
        cbar_kws={"label": "Retention Rate"},
        linewidths=0.5,
        linecolor="gray",
        mask=heatmap_data.isnull(),
    )
    plt.title("Cohort Retention Rate Heatmap")
    plt.ylabel("Cohort Month")
    plt.xlabel("Period Index")

    # Guardar el mapa de calor como PNG
    OUTPUT_PNG_FILE = OUTPUT_DIRECTORY / "cohort_retention_heatmap.png"
    plt.savefig(OUTPUT_PNG_FILE, bbox_inches="tight")

    return cohort_data

if __name__ == "__main__":
    build_cohort_analysis()
