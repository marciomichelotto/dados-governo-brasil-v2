"""Pipeline para leitura de CSV, limpeza de dados e carga no SQL Server."""

from __future__ import annotations

import argparse
import logging
import os
import re
import sys
import time
import unicodedata
from pathlib import Path

import pandas as pd
from sqlalchemy import create_engine, types

logger = logging.getLogger(__name__)


def configure_logging() -> None:
    """Configura logging padrão para execução via CLI."""
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s %(levelname)s %(name)s - %(message)s",
    )


def read_csv(path: Path, delimiter: str, encoding: str) -> pd.DataFrame:
    """Lê um arquivo CSV e retorna um DataFrame."""
    return pd.read_csv(path, sep=delimiter, encoding=encoding)


def normalize_column_name(column_name: str) -> str:
    """Normaliza nome de coluna para snake_case ASCII."""
    normalized = unicodedata.normalize("NFKD", str(column_name))
    normalized = normalized.encode("ascii", "ignore").decode("ascii")
    normalized = normalized.strip().lower()
    normalized = re.sub(r"[^a-z0-9]+", "_", normalized)
    normalized = re.sub(r"_+", "_", normalized).strip("_")
    return normalized or "coluna"


def deduplicate_column_names(column_names: list[str]) -> list[str]:
    """Garante nomes de coluna únicos preservando a ordem."""
    seen: dict[str, int] = {}
    unique_columns: list[str] = []

    for column_name in column_names:
        count = seen.get(column_name, 0) + 1
        seen[column_name] = count
        unique_columns.append(column_name if count == 1 else f"{column_name}_{count}")

    return unique_columns


def clean_dataframe(df: pd.DataFrame, drop_duplicates: bool = True) -> pd.DataFrame:
    """Aplica limpeza básica nos dados."""
    cleaned = df.copy()

    cleaned.columns = deduplicate_column_names(
        [normalize_column_name(column) for column in cleaned.columns]
    )

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
    logger.info(
        "Iniciando carga para %s.%s (registros=%s, chunksize=%s, if_exists=%s)",
        schema,
        table_name,
        len(df),
        chunksize,
        if_exists,
    )

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
    parser.add_argument(
        "--connection-string",
        default=os.getenv("DATABASE_URL"),
        help=(
            "String SQLAlchemy para SQL Server. "
            "Se omitida, usa a variável de ambiente DATABASE_URL"
        ),
    )
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


def validate_args(args: argparse.Namespace) -> None:
    """Valida argumentos antes da execução do pipeline."""
    if not args.csv_path.exists() or not args.csv_path.is_file():
        raise ValueError(f"CSV não encontrado: {args.csv_path}")

    if args.chunksize <= 0:
        raise ValueError("--chunksize deve ser maior que zero")

    if not args.connection_string:
        raise ValueError(
            "String de conexão não informada. Use --connection-string ou DATABASE_URL"
        )

    if not re.match(r"^[a-zA-Z_][a-zA-Z0-9_]*$", args.table):
        raise ValueError("--table deve conter apenas letras, números e underscore")

    if args.schema and not re.match(r"^[a-zA-Z_][a-zA-Z0-9_]*$", args.schema):
        raise ValueError("--schema deve conter apenas letras, números e underscore")


def main() -> None:
    configure_logging()
    start_time = time.perf_counter()

    try:
        args = parse_args()
        validate_args(args)

        logger.info(
            "Iniciando leitura do CSV: path=%s delimiter='%s' encoding=%s",
            args.csv_path,
            args.delimiter,
            args.encoding,
        )
        dataframe = read_csv(args.csv_path, delimiter=args.delimiter, encoding=args.encoding)

        initial_rows = len(dataframe)
        logger.info("Leitura concluída: registros=%s", initial_rows)

        dataframe = clean_dataframe(dataframe, drop_duplicates=not args.keep_duplicates)
        final_rows = len(dataframe)
        logger.info(
            "Limpeza concluída: registros_apos_limpeza=%s removidos=%s",
            final_rows,
            initial_rows - final_rows,
        )

        load_to_sql_server(
            df=dataframe,
            connection_string=args.connection_string,
            table_name=args.table,
            schema=args.schema,
            if_exists=args.if_exists,
            chunksize=args.chunksize,
        )

        elapsed = time.perf_counter() - start_time
        logger.info(
            "Carga concluída: %s registros enviados para %s.%s em %.2fs",
            len(dataframe),
            args.schema,
            args.table,
            elapsed,
        )
    except Exception as exc:  # noqa: BLE001
        logger.error("Falha na execução do pipeline: %s", exc)
        sys.exit(1)


if __name__ == "__main__":
    main()
