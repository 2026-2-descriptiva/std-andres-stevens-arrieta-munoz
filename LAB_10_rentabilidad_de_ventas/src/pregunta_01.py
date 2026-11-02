from zipfile import Path

import pandas as pd


def pregunta_01() -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    """
    Una cadena de suministros de oficina vende mucho, pero la gerencia
    sospecha que parte de esas ventas no deja utilidad. El archivo
    `data/superstore_orders.csv.gz` tiene una fila por línea de pedido, con
    el número de pedido (`Order ID`), las ventas (`Sales`), la utilidad
    (`Profit`), el descuento aplicado (`Discount`, como proporción), el
    segmento del cliente (`Customer Segment`) y la categoría del producto
    (`Product Category`). Una utilidad negativa significa que la línea se
    vendió con pérdida.

    Use estas definiciones:

    - Margen (`profit_margin`): utilidad sobre ventas.
    - Línea con pérdida: una línea cuya utilidad es negativa.
    - `loss_line_rate`: la proporción de líneas con pérdida.
    - `lost_profit`: la suma de las pérdidas de las líneas con pérdida,
      escrita como número positivo.
    - Rango de descuento (`discount_band`): `0%` si no hubo descuento,
      `1%-5%` si fue mayor que 0 y hasta 5 %, `6%-10%` si fue mayor que 5 % y
      hasta 10 %, y `más de 10%` en otro caso.

    Genere tres archivos en `submission/`, sin el índice de Pandas y con las
    columnas en el orden indicado:

    1. `profitability_summary.csv`, con una sola fila: `lines` (cantidad de
       líneas), `orders` (pedidos distintos), `sales`, `profit`,
       `profit_margin`, `loss_lines` (cantidad de líneas con pérdida),
       `loss_line_rate` y `lost_profit`.

    2. `discount_summary.csv`, con una fila por rango de descuento, en el
       orden en que se definieron arriba: `discount_band`, `lines`, `sales`,
       `profit`, `profit_margin`, `loss_line_rate` y `lost_profit`.

    3. `priority_segments.csv`, con los cinco segmentos segmento–categoría
       que más utilidad pierden: `Customer Segment`, `Product Category`,
       `lines`, `sales`, `profit`, `profit_margin` y `lost_profit`. Considere
       solamente segmentos con al menos 100 líneas y ordénelos por
       `lost_profit` de mayor a menor.

    La función también debe retornar las tres tablas, en el mismo orden.

    Ejemplo del formato de `discount_summary.csv`:

        discount_band,lines,sales,profit,profit_margin,loss_line_rate,...
        0%,166,170539.05,29472.3789,0.1728,0.488,...
        ...
    """
    
    from pathlib import Path
 
    import numpy as np
 
    BASE_DIRECTORY = Path(__file__).resolve().parent.parent
    INPUT_FILE = BASE_DIRECTORY / "data" / "superstore_orders.csv.gz"
    OUTPUT_DIRECTORY = BASE_DIRECTORY / "submission"
    OUTPUT_DIRECTORY.mkdir(parents=True, exist_ok=True)
 
    BAND_ORDER = ["0%", "1%-5%", "6%-10%", "más de 10%"]
 
    df = pd.read_csv(
        INPUT_FILE,
        compression="gzip",
        sep=";",
        decimal=",",
        encoding="utf-8-sig",
    )
 
    # Línea con pérdida y pérdida positiva por línea.
    df["is_loss"] = df["Profit"] < 0
    df["loss_amount"] = np.where(df["is_loss"], -df["Profit"], 0.0)
 
    # Rango de descuento (redondeo para evitar ruido de punto flotante).
    disc = df["Discount"].round(6)
    df["discount_band"] = np.select(
        [disc <= 0, disc <= 0.05, disc <= 0.10],
        ["0%", "1%-5%", "6%-10%"],
        default="más de 10%",
    )
 
    def summarize(group_cols):
        g = df.groupby(group_cols, sort=False, observed=True).agg(
            lines=("Profit", "size"),
            sales=("Sales", "sum"),
            profit=("Profit", "sum"),
            loss_lines=("is_loss", "sum"),
            lost_profit=("loss_amount", "sum"),
        )
        g["profit_margin"] = g["profit"] / g["sales"]
        g["loss_line_rate"] = g["loss_lines"] / g["lines"]
        return g.reset_index()
 
    def rounded(t):
        if "sales" in t.columns:
            t["sales"] = t["sales"].round(2)
        for col in ("profit", "lost_profit", "profit_margin", "loss_line_rate"):
            if col in t.columns:
                t[col] = t[col].round(4)
        return t
 
    # 1. Resumen general.
    lines = len(df)
    sales = df["Sales"].sum()
    profit = df["Profit"].sum()
    loss_lines = int(df["is_loss"].sum())
    profitability_summary = pd.DataFrame(
        [
            {
                "lines": lines,
                "orders": df["Order ID"].nunique(),
                "sales": sales,
                "profit": profit,
                "profit_margin": profit / sales,
                "loss_lines": loss_lines,
                "loss_line_rate": loss_lines / lines,
                "lost_profit": df["loss_amount"].sum(),
            }
        ]
    )
    profitability_summary = rounded(profitability_summary)
 
    # 2. Resumen por rango de descuento (siempre los cuatro rangos, en orden).
    discount_summary = summarize("discount_band").set_index("discount_band")
    discount_summary = discount_summary.reindex(BAND_ORDER)
    for col in ("lines", "sales", "profit", "loss_lines", "lost_profit"):
        discount_summary[col] = discount_summary[col].fillna(0)
    discount_summary["lines"] = discount_summary["lines"].astype(int)
    discount_summary = discount_summary.reset_index()[
        [
            "discount_band",
            "lines",
            "sales",
            "profit",
            "profit_margin",
            "loss_line_rate",
            "lost_profit",
        ]
    ]
    discount_summary = rounded(discount_summary)
 
    # 3. Cinco segmentos segmento–categoría que más utilidad pierden.
    seg = summarize(["Customer Segment", "Product Category"])
    seg = seg[seg["lines"] >= 100]
    priority_segments = (
        seg.sort_values("lost_profit", ascending=False, kind="mergesort")
        .head(5)[
            [
                "Customer Segment",
                "Product Category",
                "lines",
                "sales",
                "profit",
                "profit_margin",
                "lost_profit",
            ]
        ]
        .reset_index(drop=True)
    )
    priority_segments = rounded(priority_segments)
 
    profitability_summary.to_csv(
        OUTPUT_DIRECTORY / "profitability_summary.csv", index=False
    )
    discount_summary.to_csv(OUTPUT_DIRECTORY / "discount_summary.csv", index=False)
    priority_segments.to_csv(OUTPUT_DIRECTORY / "priority_segments.csv", index=False)
 
    return profitability_summary, discount_summary, priority_segments

if __name__ == "__main__":
    pregunta_01()

