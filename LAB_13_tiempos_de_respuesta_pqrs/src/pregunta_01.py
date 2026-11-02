import pandas as pd


def pregunta_01() -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    """
    Una entidad pública recibe peticiones, quejas, reclamos y sugerencias
    (PQRS) por dos canales, la página web y las cartas, y la ley le da 15 días
    hábiles para responder cada una. Su tarea es medir si la entidad cumple
    ese plazo.

    Los archivos `data/historical_requests_web.csv.gz` y
    `data/historical_requests_letter.csv.gz` tienen una fila por solicitud
    recibida entre 2016 y 2021 por cada canal, con su identificador
    (`record_id`), la fecha de entrada (`in_date`), el día de la semana de
    entrada (`day_name`) y la fecha de respuesta (`out_date`). Si `out_date`
    está vacía, la solicitud todavía no ha sido respondida.

    Tenga en cuenta lo siguiente:

    - Algunas solicitudes aparecen repetidas: elimine las filas idénticas
      dentro de cada canal, para contar cada solicitud una sola vez. Las
      filas sin `record_id` son solicitudes válidas.
    - Llame `letter` al canal de las cartas y `web` al de la página web.
    - Los días hábiles de respuesta son los días de lunes a viernes
      posteriores a la fecha de entrada, hasta la fecha de respuesta
      incluida. Por ejemplo, una solicitud que entra un viernes y se responde
      el lunes siguiente tardó 1 día hábil. No considere los festivos.
    - Los días calendario de respuesta son la diferencia entre la fecha de
      respuesta y la de entrada.
    - Una solicitud cumple el plazo si fue respondida en 15 días hábiles o
      menos. Una solicitud pendiente no ha cumplido el plazo.
    - `on_time_rate` es la proporción de solicitudes que cumplen el plazo,
      sobre el total de solicitudes, incluidas las pendientes.
    - Las medianas de días se calculan solamente con las solicitudes
      respondidas.

    Genere tres archivos en `submission/`, sin el índice de Pandas y con las
    columnas en el orden indicado:

    1. `channel_summary.csv`, con una fila por canal, en orden alfabético:
       `channel`, `requests`, `answered`, `pending`,
       `median_business_days` y `on_time_rate`.

    2. `yearly_summary.csv`, con una fila por año de entrada y canal,
       ordenada por año y luego por canal: `year`, `channel`, `requests`,
       `pending` y `on_time_rate`.

    3. `entry_day_summary.csv`, con una fila por día de entrada, de lunes a
       domingo, con los dos canales juntos: `day_name`, `requests`,
       `median_calendar_days` y `median_business_days`.

    Observe en el tercer archivo cómo cambia la lectura del tiempo de
    respuesta según se cuenten días calendario o días hábiles.

    La función también debe retornar las tres tablas, en el mismo orden.

    Ejemplo del formato de `channel_summary.csv`:

        channel,requests,answered,pending,median_business_days,on_time_rate
        letter,28138,...
        ...
    """
    from pathlib import Path
 
    import numpy as np
 
    BASE_DIRECTORY = Path(__file__).resolve().parent.parent
    DATA_DIRECTORY = BASE_DIRECTORY / "data"
    OUTPUT_DIRECTORY = BASE_DIRECTORY / "submission"
    OUTPUT_DIRECTORY.mkdir(parents=True, exist_ok=True)
 
    # Leer cada canal, eliminar filas idénticas y asignar el nombre del canal
    channels = {
        "web": "historical_requests_web.csv.gz",
        "letter": "historical_requests_letter.csv.gz",
    }
    frames = []
    for channel, file_name in channels.items():
        data = pd.read_csv(DATA_DIRECTORY / file_name).drop_duplicates()
        data["channel"] = channel
        frames.append(data)
 
    combined_data = pd.concat(frames, ignore_index=True)
    combined_data["in_date"] = pd.to_datetime(combined_data["in_date"])
    combined_data["out_date"] = pd.to_datetime(
        combined_data["out_date"], errors="coerce"
    )
 
    # Días calendario y días hábiles (lunes a viernes, sin festivos)
    answered = combined_data["out_date"].notna()
    combined_data["calendar_days"] = (
        combined_data["out_date"] - combined_data["in_date"]
    ).dt.days
 
    combined_data["business_days"] = np.nan
    combined_data.loc[answered, "business_days"] = np.busday_count(
        (combined_data.loc[answered, "in_date"] + pd.Timedelta(days=1))
        .to_numpy(dtype="datetime64[D]"),
        (combined_data.loc[answered, "out_date"] + pd.Timedelta(days=1))
        .to_numpy(dtype="datetime64[D]"),
    )
 
    # Cumple el plazo: respondida en 15 días hábiles o menos
    combined_data["on_time"] = answered & (combined_data["business_days"] <= 15)
    combined_data["year"] = combined_data["in_date"].dt.year
 
    # Resumen por canal (orden alfabético: letter, web)
    channel_summary = (
        combined_data.groupby("channel")
        .agg(
            requests=("in_date", "size"),
            answered=("out_date", "count"),
            median_business_days=("business_days", "median"),
            on_time_rate=("on_time", "mean"),
        )
        .reset_index()
    )
    channel_summary["pending"] = (
        channel_summary["requests"] - channel_summary["answered"]
    )
    channel_summary = channel_summary[
        [
            "channel",
            "requests",
            "answered",
            "pending",
            "median_business_days",
            "on_time_rate",
        ]
    ]
 
    # Resumen por año de entrada y canal
    yearly_summary = (
        combined_data.groupby(["year", "channel"])
        .agg(
            requests=("in_date", "size"),
            answered=("out_date", "count"),
            on_time_rate=("on_time", "mean"),
        )
        .reset_index()
    )
    yearly_summary["pending"] = yearly_summary["requests"] - yearly_summary["answered"]
    yearly_summary = yearly_summary[
        ["year", "channel", "requests", "pending", "on_time_rate"]
    ].sort_values(["year", "channel"])
 
    # Resumen por día de entrada, de lunes a domingo, con los dos canales juntos
    day_order = [
        "Monday",
        "Tuesday",
        "Wednesday",
        "Thursday",
        "Friday",
        "Saturday",
        "Sunday",
    ]
    entry_day_summary = (
        combined_data.groupby("day_name")
        .agg(
            requests=("in_date", "size"),
            median_calendar_days=("calendar_days", "median"),
            median_business_days=("business_days", "median"),
        )
        .reindex(day_order)
        .reset_index()
    )
 
    # Guardar los resultados
    channel_summary.to_csv(OUTPUT_DIRECTORY / "channel_summary.csv", index=False)
    yearly_summary.to_csv(OUTPUT_DIRECTORY / "yearly_summary.csv", index=False)
    entry_day_summary.to_csv(OUTPUT_DIRECTORY / "entry_day_summary.csv", index=False)
 
    return channel_summary, yearly_summary, entry_day_summary
 
 
if __name__ == "__main__":
    pregunta_01()


