# Copyright (c) 2025 Nelson Grey LLC
# Author: Nelson Grey LLC
#
# Licensed under the Nelson Grey LLC Community License 1.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
# https://github.com/mnelson3/sas-ci360-solutions/blob/main/LICENSE
#
"""
SASCI360Service.py imports pywin32 (win32event, win32service,
win32serviceutil, servicemanager) at module level - real dependencies
of the deployed Windows service, but genuinely unavailable outside
Windows, including in this CI (ubuntu-latest). Following the same
sys.modules-stubbing convention this project family already uses for
an uninstalled private dependency (see sas-ci360-sdk's sol-identity
tests), we register minimal fakes so the module can be imported and
its own logic exercised without a Windows install providing the real
packages.
"""
import sys
import types
from unittest.mock import MagicMock, patch


def _install_fake_module(dotted_name):
    if dotted_name in sys.modules:
        return sys.modules[dotted_name]
    module = types.ModuleType(dotted_name)
    sys.modules[dotted_name] = module
    if "." in dotted_name:
        parent_name, attr = dotted_name.rsplit(".", 1)
        parent = _install_fake_module(parent_name)
        setattr(parent, attr, module)
    return module


_servicemanager = _install_fake_module("servicemanager")
if not hasattr(_servicemanager, "LogMsg"):
    _servicemanager.LogMsg = MagicMock(name="LogMsg")
    _servicemanager.EVENTLOG_INFORMATION_TYPE = 1
    _servicemanager.PYS_SERVICE_STARTED = 1

_win32 = _install_fake_module("win32")
_win32event = _install_fake_module("win32.win32event")
if not hasattr(_win32event, "CreateEvent"):
    _win32event.CreateEvent = MagicMock(name="CreateEvent", return_value="hWaitStop")
    _win32event.SetEvent = MagicMock(name="SetEvent")
    _win32event.WaitForSingleObject = MagicMock(name="WaitForSingleObject")
    _win32event.WAIT_OBJECT_0 = 0
_win32.win32event = _win32event

_win32service = _install_fake_module("win32.win32service")
if not hasattr(_win32service, "SERVICE_STOP_PENDING"):
    _win32service.SERVICE_STOP_PENDING = 3
_win32.win32service = _win32service

_win32_lib = _install_fake_module("win32.lib")
_win32serviceutil = _install_fake_module("win32.lib.win32serviceutil")


class _FakeServiceFramework:
    def __init__(self, name):
        self._svc_name_arg = name

    def ReportServiceStatus(self, *args, **kwargs):
        pass


if not hasattr(_win32serviceutil, "ServiceFramework"):
    _win32serviceutil.ServiceFramework = _FakeServiceFramework
    _win32serviceutil.HandleCommandLine = MagicMock(name="HandleCommandLine")
_win32_lib.win32serviceutil = _win32serviceutil

import SASCI360Service  # noqa: E402


def _service():
    with patch.object(
        SASCI360Service.win32event, "CreateEvent", return_value="hWaitStop"
    ):
        return SASCI360Service.SASCI360Service("test-service")


def test_init_creates_stop_event():
    service = _service()

    assert service.hWaitStop == "hWaitStop"


def test_svc_stop_reports_pending_and_sets_event():
    service = _service()
    with patch.object(SASCI360Service.win32event, "SetEvent") as mock_set_event:
        service.SvcStop()

    mock_set_event.assert_called_once_with(service.hWaitStop)


def test_svc_stop_logs_and_returns_none_on_failure():
    service = _service()
    with patch.object(service, "ReportServiceStatus", side_effect=RuntimeError("boom")):
        result = service.SvcStop()

    assert result is None


def test_svc_do_run_logs_start_and_calls_main():
    service = _service()
    with patch.object(service, "main") as mock_main:
        service.SvcDoRun()

    mock_main.assert_called_once_with()


def test_svc_do_run_logs_and_returns_none_on_failure():
    service = _service()
    with patch.object(service, "main", side_effect=RuntimeError("boom")):
        result = service.SvcDoRun()

    assert result is None


def test_main_polls_until_stop_signal():
    service = _service()
    fake_app = MagicMock()
    fake_main_cls = MagicMock(return_value=fake_app)

    with patch.dict(
        "sys.modules", {"sasci360solutions.main": MagicMock(CI360Main=fake_main_cls)}
    ), patch.object(
        SASCI360Service.win32event, "WaitForSingleObject", side_effect=[1, 1, 0]
    ), patch.object(
        SASCI360Service.win32event, "WAIT_OBJECT_0", 0
    ):
        service.main()

    fake_main_cls.assert_called_once_with()
    assert fake_app.check_and_run.call_count == 3


def test_main_logs_and_returns_none_on_failure():
    service = _service()
    fake_main_cls = MagicMock(side_effect=RuntimeError("boom"))

    with patch.dict(
        "sys.modules", {"sasci360solutions.main": MagicMock(CI360Main=fake_main_cls)}
    ):
        result = service.main()

    assert result is None
