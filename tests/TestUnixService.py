# Copyright (c) 2025 Nelson Grey LLC
# Author: Nelson Grey LLC
#
# Licensed under the Nelson Grey LLC Community License 1.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
# https://github.com/mnelson3/sas-ci360-solutions/blob/main/LICENSE
#
from unittest.mock import MagicMock, patch

from UnixService import UnixService


def _service(tmp_path):
    return UnixService("test-sas-ci360-service", pid_dir=str(tmp_path))


def test_init_configures_syslog_handler(tmp_path):
    service = _service(tmp_path)

    assert any(
        handler.__class__.__name__ == "SysLogHandler"
        for handler in service.logger.handlers
    )


@patch("UnixService.time.sleep")
def test_run_polls_until_sigterm(mock_sleep, tmp_path):
    service = _service(tmp_path)
    fake_app = MagicMock()
    fake_main_cls = MagicMock(return_value=fake_app)
    got_sigterm = MagicMock(side_effect=[False, False, True])
    service.got_sigterm = got_sigterm

    with patch.dict(
        "sys.modules", {"sasci360solutions.main": MagicMock(CI360Main=fake_main_cls)}
    ):
        service.run()

    fake_main_cls.assert_called_once_with()
    assert fake_app.check_and_run.call_count == 2
    assert mock_sleep.call_count == 2
    mock_sleep.assert_called_with(UnixService.POLL_INTERVAL_SECONDS)


@patch("UnixService.time.sleep")
def test_run_logs_and_continues_when_a_cycle_raises(mock_sleep, tmp_path):
    service = _service(tmp_path)
    fake_app = MagicMock()
    fake_app.check_and_run.side_effect = [RuntimeError("boom"), None]
    fake_main_cls = MagicMock(return_value=fake_app)
    service.got_sigterm = MagicMock(side_effect=[False, False, True])
    service.logger = MagicMock()

    with patch.dict(
        "sys.modules", {"sasci360solutions.main": MagicMock(CI360Main=fake_main_cls)}
    ):
        service.run()

    service.logger.exception.assert_called_once()
    assert fake_app.check_and_run.call_count == 2
