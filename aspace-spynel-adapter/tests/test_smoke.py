"""Smoke tests de l'adapter spynel (D-N053 pas B).

Roules avec le venv du pas : `python -m pytest aspace-spynel-adapter/tests/test_smoke.py -v`.
Ne touchent pas l'amont, ne font aucun appel reseau.
"""

import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

import aspace_spynel_adapter as adapter  # noqa: E402


def test_constants():
    assert re.fullmatch(r"[0-9a-f]{40}", adapter.PINNED_UPSTREAM_COMMIT)
    assert adapter.FIBER_ADDRESS == "fiber:a0:spynel"
    assert adapter.ORCHESTRATION_TARGET == "fiber:a0:agent-zero"
    assert adapter.LICENSE == "MIT"
    assert adapter.FORK == "Amdkn/spynel"
    assert adapter.UPSTREAM_REPO == "agent0ai/spynel"
    assert adapter.ADAPTER_VERSION == "0.1.0"
    assert adapter.BIND_COMMIT == "3e076a1494364343cdafd703134b3fb46cbe7144"
    assert adapter.GO_MODULE == "github.com/agent0ai/spynel"
    assert adapter.GO_VERSION == "1.25.0"


def test_validate_surface():
    v = adapter.validate()
    assert v["pinned_commit_is_40_hex"] is True
    assert v["license_file_present"] is True
    assert v["go_files_total"] == 395
    assert v["test_files_total"] == 202
    assert v["internal_packages"] == 27
    assert v["go_module"] == "github.com/agent0ai/spynel"
    assert v["go_version"] == "1.25.0"
    assert v["entry_point"] is True
    assert v["harness_workers_present"] == ["acp", "claude", "codex", "pi"]
    assert v["orchestrator_files_present"] == ["manager.go", "routes.go", "worker.go", "work_list.go", "status.go"]
    assert v["job_files_present"] == ["job_archive.go", "job_info.go", "job_worker.go"]
    assert v["channels_present"] == ["telegram", "tui", "whatsapp"]
    assert v["localapi_unix_socket"] is True
    assert v["loop_duplicated"] is False
    assert v["surface_complete"] is True
    assert v["adapter_network_calls"] == 0
    assert v["confinement"]


def test_doctor_all_pass():
    checks = adapter.doctor()
    assert checks, "doctor() vide"
    failed = [c for c in checks if not c["ok"]]
    assert not failed, failed


def test_no_network_import_in_adapter():
    import ast

    src = (Path(adapter.__file__).parent / "__init__.py").read_text()
    tree = ast.parse(src)
    imported = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            imported.update(a.name.split(".")[0] for a in node.names)
        elif isinstance(node, ast.ImportFrom) and node.module:
            imported.add(node.module.split(".")[0])
    # L'adapter nomme le socket Unix de l'API locale (fichier socket_unix.go)
    # sans jamais l'importer ni l'appeler : le controle porte sur les imports.
    for banned in ("requests", "httpx", "urllib", "socket", "huggingface_hub", "aiohttp", "http"):
        assert banned not in imported, banned
    assert imported <= {"re", "pathlib", "__future__", "annotations"}, imported


def test_describe():
    d = adapter.describe()
    assert d["fiber"] == "fiber:a0:spynel"
    assert d["orchestration_target"] == "fiber:a0:agent-zero"
    assert d["pinned_upstream_commit"] == adapter.PINNED_UPSTREAM_COMMIT
    assert d["license"] == "MIT"
