"""Pipeline para leitura de CSV, limpeza de dados e carga no SQL Server."""

from __future__ import annotations

import argparse
from pathlib import Path

import pandas as pd
from sqlalchemy import create_engine, types


def read_csv(path: Path, delimiter: str, encoding: str) -> pd.DataFrame:
    """Lê um arquivo CSV e retorna um DataFrame."""
    return pd.read_csv(path, sep=delimiter, encoding=encoding)


def clean_dataframe(df: pd.DataFrame, drop_duplicates: bool = True) -> pd.DataFrame:
    """Aplica limpeza básica nos dados."""
    cleaned = df.copy()

    cleaned.columns = [column.strip().lower().replace(" ", "_") for column in cleaned.columns]

    object_columns = cleaned.select_dtypes(include=["object"]).columns
    for column in object_columns:
        cleaned[column] = cleaned[column].astype("string").str.strip()

    cleaned = cleaned.dropna(axis=0, how="all")

    if drop_duplicates:
        cleaned = cleaned.drop_duplicates()

    return cleaned


def infer_sqlalchemy_types(df: pd.DataFrame) -> dict[str, types.TypeEngine]:
    """Infere tipos SQLAlchemy para escrita no SQL Server."""
    dtype_map: dict[str, types.TypeEngine] = {}

    for column_name, dtype in df.dtypes.items():
        if pd.api.types.is_integer_dtype(dtype):
            dtype_map[column_name] = types.BigInteger()
        elif pd.api.types.is_float_dtype(dtype):
            dtype_map[column_name] = types.Float(precision=53)
        elif pd.api.types.is_bool_dtype(dtype):
            dtype_map[column_name] = types.Boolean()
        elif pd.api.types.is_datetime64_any_dtype(dtype):
            dtype_map[column_name] = types.DateTime()
        else:
            dtype_map[column_name] = types.UnicodeText()

    return dtype_map


def load_to_sql_server(
    df: pd.DataFrame,
    connection_string: str,
    table_name: str,
    schema: str,
    if_exists: str,
    chunksize: int,
) -> None:
    """Carrega DataFrame em tabela SQL Server."""
    engine = create_engine(connection_string, fast_executemany=True)
    dtype_map = infer_sqlalchemy_types(df)

    with engine.begin() as connection:
        df.to_sql(
            name=table_name,
            con=connection,
            schema=schema,
            if_exists=if_exists,
            index=False,
            chunksize=chunksize,
            method="multi",
            dtype=dtype_map,
        )


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Pipeline ETL: CSV -> limpeza -> SQL Server"
    )
    parser.add_argument("--csv-path", required=True, type=Path, help="Caminho do CSV")
    parser.add_argument("--connection-string", required=True, help="String SQLAlchemy para SQL Server")
    parser.add_argument("--table", required=True, help="Nome da tabela de destino")
    parser.add_argument("--schema", default="dbo", help="Schema de destino")
    parser.add_argument(
        "--if-exists",
        default="append",
        choices=["fail", "replace", "append"],
        help="Comportamento caso tabela exista",
    )
    parser.add_argument("--delimiter", default=",", help="Delimitador do CSV")
    parser.add_argument("--encoding", default="utf-8", help="Encoding do CSV")
    parser.add_argument("--chunksize", type=int, default=1000, help="Linhas por lote")
    parser.add_argument(
        "--keep-duplicates",
        action="store_true",
        help="Mantém duplicatas ao invés de removê-las",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()

    dataframe = read_csv(args.csv_path, delimiter=args.delimiter, encoding=args.encoding)
    dataframe = clean_dataframe(dataframe, drop_duplicates=not args.keep_duplicates)

    load_to_sql_server(
        df=dataframe,
        connection_string=args.connection_string,
        table_name=args.table,
        schema=args.schema,
        if_exists=args.if_exists,
        chunksize=args.chunksize,
    )

    print(
        f"Carga concluída: {len(dataframe)} registros enviados para "
        f"{args.schema}.{args.table}."
    )


if __name__ == "__main__":
    main()
