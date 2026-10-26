import pandas as pd


def clean_campaign_data() -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    """
    Los datos de una campaña de mercadeo bancario llegaron repartidos en diez
    archivos comprimidos, `data/bank-marketing-campaing-*.csv.gz`, con
    información mezclada del cliente, de la campaña y del contexto económico.
    Su tarea es leerlos directamente desde los archivos comprimidos, sin
    descomprimirlos a mano, y separarlos en tres tablas limpias.

    Guarde cada tabla como un CSV sin comprimir en `submission/`, sin el índice
    de Pandas y con las columnas en el orden indicado:

    1. `client.csv`: `client_id`, `age`, `job`, `marital`, `education`,
       `credit_default` y `mortgage`.
       - En `job`, elimine los puntos y cambie los guiones por guiones bajos.
       - En `education`, cambie los puntos por guiones bajos y deje el valor
         `unknown` como faltante.
       - En `credit_default` y `mortgage`, escriba 1 si el valor es `yes` y 0
         en cualquier otro caso.

    2. `campaign.csv`: `client_id`, `number_contacts`, `contact_duration`,
       `previous_campaign_contacts`, `previous_outcome`, `campaign_outcome` y
       `last_contact_date`.
       - En `previous_outcome`, escriba 1 si el valor es `success` y 0 en
         cualquier otro caso.
       - En `campaign_outcome`, escriba 1 si el valor es `yes` y 0 en
         cualquier otro caso.
       - Construya `last_contact_date` a partir de las columnas `month` y
         `day`, usando el año 2022 y el formato `AAAA-MM-DD`.

    3. `economics.csv`: `client_id`, `cons_price_idx` y
       `euribor_three_months`.

    La función también debe retornar las tres tablas, en el orden `client`,
    `campaign` y `economics`.

    Ejemplo del formato de `campaign.csv`:

        client_id,number_contacts,contact_duration,...,last_contact_date
        0,1,261,...,2022-05-13
        ...
    """

    from pathlib import Path
    import pandas as pd

    BASE_DIRECTORY = Path(__file__).resolve().parent.parent
    INPUT_FILE = BASE_DIRECTORY / "data" 
    OUTPUT_FILE = BASE_DIRECTORY / "submission"

    # Leer todos los archivos comprimidos y concatenarlos en un solo DataFrame
    all_files = list(INPUT_FILE.glob("bank-marketing-campaing-*.csv.gz"))

    df = pd.concat((pd.read_csv(f, compression='gzip') for f in all_files), ignore_index=True)

    # Crear la tabla client
    client = df[['client_id', 'age', 'job', 'marital', 'education', 'credit_default', 'mortgage']].copy() 

    client['job'] = client['job'].str.replace('.', '', regex=False).str.replace('-', '_', regex=False)
    client['education'] = client['education'].str.replace('.', '_', regex=False).replace('unknown', pd.NA)
    client['credit_default'] = client['credit_default'].apply(lambda x: 1 if x == 'yes' else 0)
    client['mortgage'] = client['mortgage'].apply(lambda x: 1 if x == 'yes' else 0) 

    # Crear la tabla campaign
    campaign = df[['client_id', 'number_contacts', 'contact_duration', 'previous_campaign_contacts', 'previous_outcome', 'campaign_outcome', 'month', 'day']].copy()  

    campaign['previous_outcome'] = campaign['previous_outcome'].apply(lambda x: 1 if x == 'success' else 0)
    campaign['campaign_outcome'] = campaign['campaign_outcome'].apply(lambda x: 1 if x == 'yes' else 0)
    campaign['last_contact_date'] = pd.to_datetime(campaign['month'].astype(str) + '-' + campaign['day'].astype(str) + '-2022', format='%b-%d-%Y')    

    campaign = campaign.drop(columns=['month', 'day'])

    # Crear la tabla economics
    economics = df[['client_id', 'cons_price_idx', 'euribor_three_months']].copy()

    # Guardar las tablas como CSV sin comprimir en submission/
    client.to_csv(OUTPUT_FILE / 'client.csv', index=False)

    campaign.to_csv(OUTPUT_FILE / 'campaign.csv', index=False)

    economics.to_csv(OUTPUT_FILE / 'economics.csv', index=False)

    return client, campaign, economics

if __name__ == "__main__":
    clean_campaign_data()


