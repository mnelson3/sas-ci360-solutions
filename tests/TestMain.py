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

from sasci360solutions.main import CI360Main


def _standard(tmp_path, with_drop_file=False):
    export_path = tmp_path / "export"
    export_post_path = tmp_path / "post"
    export_path.mkdir()
    export_post_path.mkdir()
    if with_drop_file:
        (export_post_path / "export.csv").write_text("id\n1\n")

    return SimpleNamespace(
        export_file="export.csv",
        export_path="/{0}/".format(export_path.name),
        export_post_path=str(export_post_path),
    )


def _main(tmp_path, with_drop_file=False):
    standard = _standard(tmp_path, with_drop_file=with_drop_file)
    upload = MagicMock()
    upload.root_path = str(tmp_path)
    create_reports = MagicMock()
    send_status = MagicMock()
    send_support = MagicMock()

    app = CI360Main(
        standard=standard,
        upload=upload,
        create_reports=create_reports,
        send_status=send_status,
        send_support=send_support,
    )
    return app, upload, create_reports, send_status, send_support


def test_cycle_with_no_file_sends_status_only(tmp_path):
    app, upload, create_reports, send_status, send_support = _main(tmp_path)
    send_status.run.return_value = True

    result = app.run_identity_bridge_cycle(file_name=None)

    assert result is True
    send_status.run.assert_called_once_with()
    upload.run.assert_not_called()
    create_reports.run.assert_not_called()


def test_cycle_success(tmp_path):
    app, upload, create_reports, send_status, send_support = _main(tmp_path)
    upload.run.return_value = True
    create_reports.run.return_value = True

    result = app.run_identity_bridge_cycle(file_name="/tmp/chain.csv")

    assert result is True
    upload.run.assert_called_once_with(file_name="/tmp/chain.csv")
    create_reports.run.assert_called_once()
    _, kwargs = send_status.run.call_args
    assert kwargs["success"] is True


def test_cycle_upload_failure_short_circuits(tmp_path):
    app, upload, create_reports, send_status, send_support = _main(tmp_path)
    upload.run.return_value = False

    result = app.run_identity_bridge_cycle(file_name="/tmp/chain.csv")

    assert result is False
    create_reports.run.assert_not_called()
    _, kwargs = send_status.run.call_args
    assert kwargs["success"] is False


def test_cycle_report_failure_propagates(tmp_path):
    app, upload, create_reports, send_status, send_support = _main(tmp_path)
    upload.run.return_value = True
    create_reports.run.return_value = False

    result = app.run_identity_bridge_cycle(file_name="/tmp/chain.csv")

    assert result is False
    _, kwargs = send_status.run.call_args
    assert kwargs["success"] is False


def test_run_support_check_delegates():
    upload = MagicMock()
    create_reports = MagicMock()
    send_status = MagicMock()
    send_support = MagicMock()
    send_support.run.return_value = True
    standard = SimpleNamespace(
        export_file="export.csv", export_path="/export/", export_post_path="/tmp"
    )

    app = CI360Main(
        standard=standard,
        upload=upload,
        create_reports=create_reports,
        send_status=send_status,
        send_support=send_support,
    )

    assert app.run_support_check() is True
    send_support.run.assert_called_once()


def test_check_and_run_no_drop_file(tmp_path):
    app, upload, create_reports, send_status, send_support = _main(
        tmp_path, with_drop_file=False
    )
    send_status.run.return_value = True

    result = app.check_and_run()

    assert result is True
    upload.run.assert_not_called()


def test_check_and_run_moves_drop_file_and_runs_cycle(tmp_path):
    app, upload, create_reports, send_status, send_support = _main(
        tmp_path, with_drop_file=True
    )
    upload.run.return_value = True
    create_reports.run.return_value = True

    result = app.check_and_run()

    assert result is True
    upload.run.assert_called_once()
    # the original drop file must be gone
    assert not (tmp_path / "post" / "export.csv").exists()
    # an archived, timestamped copy must exist under export_path
    archived = list((tmp_path / "export").glob("export_*.CSV"))
    assert len(archived) == 1
