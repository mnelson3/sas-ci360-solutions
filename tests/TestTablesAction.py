# Copyright (c) 2025 Nelson Grey LLC
# Author: Nelson Grey LLC
#
# Licensed under the Nelson Grey LLC Community License 1.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
# https://github.com/mnelson3/sas-ci360-solutions/blob/main/LICENSE
#
from types import SimpleNamespace
from unittest.mock import MagicMock

import pytest

from sasci360solutions.marketing_data.TablesAction import TableActions


def _standard():
    return SimpleNamespace(
        algorithm="HS256",
        encoding="UTF-8",
        external_gateway_path="extapigwservice-test.ci360.sas.com",
        secret_key="example-secret-key",
        tenant_id="example-tenant-id",
        gDirDataResponseTablesGet="/data/response/tables/",
    )


def test_tables_get_persists_and_returns_result(tmp_path):
    standard = _standard()
    client = MagicMock()
    client.get_tables.return_value = {"items": [{"id": "table-1"}]}
    reporter = MagicMock()

    custom = TableActions(
        standard=standard, client=client, reporter=reporter, root_path=str(tmp_path)
    )
    result = custom.tables_get()

    assert result == {"items": [{"id": "table-1"}]}
    client.get_tables.assert_called_once()
    reporter.save.assert_called_once()


def test_tables_by_id_get_persists_and_returns_result(tmp_path):
    standard = _standard()
    client = MagicMock()
    client.get_table.return_value = {"id": "table-1", "name": "identityBridge"}
    reporter = MagicMock()

    custom = TableActions(
        standard=standard, client=client, reporter=reporter, root_path=str(tmp_path)
    )
    result = custom.tables_by_id_get(table_id="table-1")

    assert result == {"id": "table-1", "name": "identityBridge"}
    client.get_table.assert_called_once_with("table-1")
    reporter.save.assert_called_once()


def test_tables_by_id_get_requires_table_id():
    standard = _standard()
    client = MagicMock()
    reporter = MagicMock()

    custom = TableActions(standard=standard, client=client, reporter=reporter)

    with pytest.raises(ValueError):
        custom.tables_by_id_get()


def test_tables_get_returns_none_on_error():
    from sasci360soldata.base import CI360DataConnectionError

    standard = _standard()
    client = MagicMock()
    client.get_tables.side_effect = CI360DataConnectionError("boom")
    reporter = MagicMock()

    custom = TableActions(standard=standard, client=client, reporter=reporter)
    result = custom.tables_get()

    assert result is None
