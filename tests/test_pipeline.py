from __future__ import annotations

from pathlib import Path

import pandas as pd
import pytest
from sqlalchemy import types

from pipeline.csv_to_sqlserver_pipeline import (
    clean_dataframe,
    deduplicate_column_names,
    infer_sqlalchemy_types,
    normalize_column_name,
    read_csv,
    validate_args,
)


def test_clean_dataframe_normaliza_colunas_trim_e_remove_duplicatas() -> None:
    df = pd.DataFrame(
        {
            " Nome Coluna ": ["  Ana ", "Ana", None],
            "Valor ": [1, 1, None],
        }
    )

    cleaned = clean_dataframe(df)

    assert list(cleaned.columns) == ["nome_coluna", "valor"]
    assert cleaned.iloc[0]["nome_coluna"] == "Ana"
    assert len(cleaned) == 1


def test_clean_dataframe_preserva_duplicatas_quando_configurado() -> None:
    df = pd.DataFrame({"nome": ["A", "A"], "valor": [1, 1]})

    cleaned = clean_dataframe(df, drop_duplicates=False)

    assert len(cleaned) == 2


def test_normalize_column_name_remove_acentos_e_simbolos() -> None:
    assert normalize_column_name(" Órgão/Unidade (R$) ") == "orgao_unidade_r"


def test_deduplicate_column_names_adiciona_sufixo_para_colisoes() -> None:
    result = deduplicate_column_names(["valor", "valor", "valor", "data"])

    assert result == ["valor", "valor_2", "valor_3", "data"]


def test_clean_dataframe_normaliza_colunas_com_acentos_e_colisoes() -> None:
    df = pd.DataFrame(
        {
            "Órgão": ["A"],
            "Orgao": ["B"],
            "Valor (R$)": [10],
        }
    )

    cleaned = clean_dataframe(df, drop_duplicates=False)

    assert list(cleaned.columns) == ["orgao", "orgao_2", "valor_r"]


def test_infer_sqlalchemy_types_mapeia_tipos_basicos() -> None:
    df = pd.DataFrame(
        {
            "inteiro": pd.Series([1, 2], dtype="int64"),
            "decimal": pd.Series([1.1, 2.2], dtype="float64"),
            "booleano": pd.Series([True, False], dtype="bool"),
            "data": pd.to_datetime(["2024-01-01", "2024-01-02"]),
            "texto": pd.Series(["a", "b"], dtype="string"),
        }
    )

    dtype_map = infer_sqlalchemy_types(df)

    assert isinstance(dtype_map["inteiro"], types.BigInteger)
    assert isinstance(dtype_map["decimal"], types.Float)
    assert isinstance(dtype_map["booleano"], types.Boolean)
    assert isinstance(dtype_map["data"], types.DateTime)
    assert isinstance(dtype_map["texto"], types.UnicodeText)


def test_read_csv_suporta_delimitador_e_encoding(tmp_path: Path) -> None:
    csv_path = tmp_path / "arquivo.csv"
    csv_path.write_text("nome;cidade\nJoão;São Paulo\n", encoding="latin-1")

    df = read_csv(csv_path, delimiter=";", encoding="latin-1")

    assert list(df.columns) == ["nome", "cidade"]
    assert df.iloc[0]["cidade"] == "São Paulo"


def test_validate_args_falha_quando_chunksize_invalido(tmp_path: Path) -> None:
    csv_path = tmp_path / "dados.csv"
    csv_path.write_text("coluna\nvalor\n", encoding="utf-8")

    args = type(
        "Args",
        (),
        {
            "csv_path": csv_path,
            "chunksize": 0,
            "connection_string": "sqlite://",
            "table": "tabela",
            "schema": "dbo",
        },
    )

    with pytest.raises(ValueError, match="chunksize"):
        validate_args(args)


def test_validate_args_falha_sem_connection_string(tmp_path: Path) -> None:
    csv_path = tmp_path / "dados.csv"
    csv_path.write_text("coluna\nvalor\n", encoding="utf-8")

    args = type(
        "Args",
        (),
        {
            "csv_path": csv_path,
            "chunksize": 100,
            "connection_string": None,
            "table": "tabela",
            "schema": "dbo",
        },
    )

    with pytest.raises(ValueError, match="String de conexão"):
        validate_args(args)
