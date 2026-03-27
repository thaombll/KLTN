import pandas as pd
import numpy as np


# =========================
# 1. PROFILE COLUMN
# =========================
def profile_column(col_data):

    stats = {
        "count": int(col_data.count()),
        "null_count": int(col_data.isnull().sum()),
        "unique_count": int(col_data.nunique())
    }

    # Try convert datetime nếu có thể
    col_data_dt = pd.to_datetime(col_data, errors='coerce')

    # =====================
    # DATETIME
    # =====================
    if col_data_dt.notnull().sum() > 0.8 * len(col_data):
        col_data = col_data_dt
        stats["type"] = "datetime"

        stats["min"] = str(col_data.min())
        stats["max"] = str(col_data.max())
        stats["time_span"] = str(col_data.max() - col_data.min())

        # Distribution
        stats["by_day"] = col_data.dt.date.value_counts().head(10).to_dict()
        stats["by_month"] = col_data.dt.to_period("M").value_counts().to_dict()
        stats["by_hour"] = col_data.dt.hour.value_counts().to_dict()

        # Interval
        diff = col_data.sort_values().diff().dropna()
        if not diff.empty:
            stats["avg_interval"] = str(diff.mean())
            stats["max_gap"] = str(diff.max())

            threshold = diff.mean() + 3 * diff.std()
            stats["time_gap_outliers"] = int((diff > threshold).sum())

    # =====================
    # NUMERIC
    # =====================
    elif np.issubdtype(col_data.dtype, np.number):
        stats["type"] = "numeric"

        stats["mean"] = float(col_data.mean())
        stats["std"] = float(col_data.std())
        stats["min"] = float(col_data.min())
        stats["max"] = float(col_data.max())

        # Mode
        if not col_data.mode().empty:
            stats["mode"] = float(col_data.mode().iloc[0])

        # IQR outlier
        q1 = col_data.quantile(0.25)
        q3 = col_data.quantile(0.75)
        iqr = q3 - q1

        lower = q1 - 1.5 * iqr
        upper = q3 + 1.5 * iqr

        outliers = col_data[(col_data < lower) | (col_data > upper)]
        stats["outlier_count"] = int(len(outliers))

        # Histogram
        try:
            bins = pd.cut(col_data, bins=5)
            stats["distribution"] = bins.value_counts().to_dict()
        except:
            stats["distribution"] = {}

    # =====================
    # CATEGORICAL
    # =====================
    else:
        stats["type"] = "categorical"

        if not col_data.mode().empty:
            stats["mode"] = str(col_data.mode().iloc[0])

        # Frequency
        stats["value_distribution"] = col_data.value_counts().head(10).to_dict()

        # Imbalance
        vc = col_data.value_counts(normalize=True)
        if not vc.empty:
            stats["top_1_ratio"] = float(vc.iloc[0])

    return stats


# =========================
# 2. ROW COUNT
# =========================
def get_row_count(conn, schema, table):
    query = f'SELECT COUNT(*) FROM "{schema}"."{table}"'
    return int(pd.read_sql(query, conn).iloc[0, 0])


# =========================
# 3. MAIN FUNCTION
# =========================
def information_database(conn):

    result = {}

    # Tables
    tables_df = pd.read_sql("""
    SELECT table_schema, table_name
    FROM information_schema.tables
    WHERE table_type = 'BASE TABLE'
    AND table_schema NOT IN ('information_schema', 'pg_catalog');
    """, conn)

    # Columns
    columns_df = pd.read_sql("""
    SELECT table_schema, table_name, column_name, data_type
    FROM information_schema.columns
    WHERE table_schema NOT IN ('information_schema', 'pg_catalog');
    """, conn)

    # PK
    pk_df = pd.read_sql("""
    SELECT tc.table_schema, tc.table_name, kc.column_name
    FROM information_schema.table_constraints tc
    JOIN information_schema.key_column_usage kc
        ON tc.constraint_name = kc.constraint_name
    WHERE tc.constraint_type = 'PRIMARY KEY';
    """, conn)

    # FK
    fk_df = pd.read_sql("""
    SELECT
        tc.table_schema AS source_schema,
        tc.table_name AS source_table,
        kcu.column_name AS source_column,
        ccu.table_schema AS target_schema,
        ccu.table_name AS target_table,
        ccu.column_name AS target_column
    FROM information_schema.table_constraints tc
    JOIN information_schema.key_column_usage kcu
        ON tc.constraint_name = kcu.constraint_name
    JOIN information_schema.constraint_column_usage ccu
        ON ccu.constraint_name = tc.constraint_name
    WHERE tc.constraint_type = 'FOREIGN KEY';
    """, conn)

    # LOOP TABLE
    for _, row in tables_df.iterrows():
        schema = row['table_schema']
        table = row['table_name']
        key = f"{schema}.{table}"

        try:
            # Load sample data
            df = pd.read_sql(f'SELECT * FROM "{schema}"."{table}" LIMIT 10000', conn)

            table_info = {
                "row_count": get_row_count(conn, schema, table),
                "columns": [],
                "primary_keys": [],
                "foreign_keys": [],
                "profile": {}
            }

            # Columns
            cols = columns_df[
                (columns_df['table_schema'] == schema) &
                (columns_df['table_name'] == table)
            ]
            table_info["columns"] = cols.to_dict('records')

            # PK
            pks = pk_df[
                (pk_df['table_schema'] == schema) &
                (pk_df['table_name'] == table)
            ]
            table_info["primary_keys"] = pks['column_name'].tolist()

            # FK
            fks = fk_df[
                (fk_df['source_schema'] == schema) &
                (fk_df['source_table'] == table)
            ]
            table_info["foreign_keys"] = fks.to_dict('records')

            # PROFILE
            for col in df.columns:
                table_info["profile"][col] = profile_column(df[col])

            result[key] = table_info

        except Exception as e:
            print(f"Error processing {key}: {e}")

    return result