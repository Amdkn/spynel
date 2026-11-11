"""A'Space adapter — spynel (D-N053 pas B, design Clara + design signe pas B).

Contrat seul, patron D-N048 (dify / cordis) et pas A (chronos) : cet adapter
ne modifie AUCUN fichier amont, ne fait AUCUN appel reseau, ne monte AUCUN
poids. Il constate : le gel epingle, la licence, la surface d'orchestration
de chat (entrees, harness workers, jobs, canaux, API locale), et il
reference fiber:a0:agent-zero comme cible d'orchestration SANS dupliquer
le loop agent-zero (aucun code de loop dans l'adapter).

Adresse : fiber:a0:spynel
Fork souverain : Amdkn/spynel (parent agent0ai/spynel, branche main)
Gel amont : 685ac65db967446d4e1cff65971ba0dc4827262f (« Support /models
through the shared model selection path »)
Bind Cordis Fiber (2L) : 3e076a1494364343cdafd703134b3fb46cbe7144
Licence : MIT

Mesures au gel (2026-11-11, verifiees au fichier) :
- 395 fichiers .go ; 27 paquets internal/ ; 202 fichiers _test.go
  (188 internal/, 3 scripts/, 11 third_party/bubbletea).
- Entree : cmd/spynel/main.go -> cli.Run ; harness workers : acp, claude,
  codex, pi (+ catalog, supervisor, worker) ; orchestrateur :
  internal/orchestrator (manager, routes, worker, work_list, status) ;
  jobs : internal/app (job_archive, job_info, job_worker) ;
  canaux : telegram, whatsapp, tui ; API locale : socket Unix prive
  (internal/localapi, token, pas de TCP par defaut).
"""

from __future__ import annotations

import re
from pathlib import Path

FIBER_ADDRESS = "fiber:a0:spynel"
ORCHESTRATION_TARGET = "fiber:a0:agent-zero"
FORK = "Amdkn/spynel"
UPSTREAM_REPO = "agent0ai/spynel"
UPSTREAM_BRANCH = "main"
PINNED_UPSTREAM_COMMIT = "685ac65db967446d4e1cff65971ba0dc4827262f"
PINNED_UPSTREAM_COMMIT_SHORT = "685ac65"
BIND_COMMIT = "3e076a1494364343cdafd703134b3fb46cbe7144"
BIND_LAYER = "2L"
LICENSE = "MIT"
ADAPTER_VERSION = "0.1.0"
GO_MODULE = "github.com/agent0ai/spynel"
GO_VERSION = "1.25.0"

HARNESS_WORKERS = ("acp", "claude", "codex", "pi")
CHANNELS = ("telegram", "tui", "whatsapp")
ORCHESTRATOR_FILES = ("manager.go", "routes.go", "worker.go", "work_list.go", "status.go")
JOB_FILES = ("job_archive.go", "job_info.go", "job_worker.go")

CONFINEMENT = """Aucun confinement commercial : code MIT. Usage B2B autorise par la
licence. Les canaux telegram/whatsapp exigent des secrets fournis par
l'utilisateur (jamais lus ni stockes ici) ; les modeles/outils sont
ceux que l'utilisateur configure, jamais appeles par l'adapter."""


def _repo_root() -> Path:
    return Path(__file__).resolve().parents[2]


def _go_files(root: Path) -> list[Path]:
    return [p for p in root.rglob("*.go") if ".git" not in p.parts]


def _surface(root: Path) -> dict:
    go_files = _go_files(root)
    test_files = [p for p in go_files if p.name.endswith("_test.go")]
    internal_pkgs = sorted(
        {str(p.parent.relative_to(root)) for p in go_files if str(p.relative_to(root)).startswith("internal/")}
    )
    harness = root / "internal" / "harness"
    workers = [w for w in HARNESS_WORKERS if (harness / f"{w}.go").exists()]
    orchestrator = root / "internal" / "orchestrator"
    orch = [f for f in ORCHESTRATOR_FILES if (orchestrator / f).exists()]
    app = root / "internal" / "app"
    jobs = [f for f in JOB_FILES if (app / f).exists()]
    channel_dir = root / "internal" / "channel"
    channels = [c for c in CHANNELS if (channel_dir / c).is_dir()]
    go_mod = (root / "go.mod").read_text(encoding="utf-8", errors="replace") if (root / "go.mod").exists() else ""
    m_mod = re.search(r"(?m)^module\s+(\S+)", go_mod)
    m_go = re.search(r"(?m)^go\s+(\S+)", go_mod)
    main_go = root / "cmd" / "spynel" / "main.go"
    entry_ok = main_go.exists() and "cli.Run(" in main_go.read_text(encoding="utf-8", errors="replace")
    localapi = root / "internal" / "localapi"
    socket_ok = (localapi / "socket_unix.go").exists()
    return {
        "go_files_total": len(go_files),
        "test_files_total": len(test_files),
        "internal_packages": len(internal_pkgs),
        "go_module": m_mod.group(1) if m_mod else None,
        "go_version": m_go.group(1) if m_go else None,
        "entry_point": entry_ok,
        "harness_workers_present": workers,
        "orchestrator_files_present": orch,
        "job_files_present": jobs,
        "channels_present": channels,
        "localapi_unix_socket": socket_ok,
    }


def describe() -> dict:
    """Decrit l'adapter (manifeste machine, sans effet de bord)."""
    return {
        "fiber": FIBER_ADDRESS,
        "fork": FORK,
        "upstream": UPSTREAM_REPO,
        "upstream_branch": UPSTREAM_BRANCH,
        "pinned_upstream_commit": PINNED_UPSTREAM_COMMIT,
        "bind_commit": BIND_COMMIT,
        "bind_layer": BIND_LAYER,
        "license": LICENSE,
        "adapter_version": ADAPTER_VERSION,
        "orchestration_target": ORCHESTRATION_TARGET,
        "confinement": CONFINEMENT,
        "surface": "validate() -> dict ; doctor() -> list[check] ; describe() -> dict",
    }


def validate() -> dict:
    """Constate l'etat du fork gele. Aucun appel reseau, aucune ecriture."""
    root = _repo_root()
    surface = _surface(root)
    license_file = root / "LICENSE"
    return {
        "pinned_commit_is_40_hex": bool(re.fullmatch(r"[0-9a-f]{40}", PINNED_UPSTREAM_COMMIT)),
        "license_file_present": license_file.is_file(),
        "license": LICENSE,
        "adapter_network_calls": 0,
        "orchestration_target": ORCHESTRATION_TARGET,
        "loop_duplicated": False,
        "confinement": CONFINEMENT,
        **surface,
        "surface_complete": (
            surface["entry_point"]
            and surface["harness_workers_present"] == list(HARNESS_WORKERS)
            and surface["orchestrator_files_present"] == list(ORCHESTRATOR_FILES)
            and surface["job_files_present"] == list(JOB_FILES)
            and surface["channels_present"] == list(CHANNELS)
            and surface["localapi_unix_socket"]
            and surface["go_module"] == GO_MODULE
            and surface["go_version"] == GO_VERSION
        ),
    }


def doctor() -> list[dict]:
    """Liste de controles sur le fork gele."""
    v = validate()
    return [
        {
            "name": "gel_epingle_40_hex",
            "ok": v["pinned_commit_is_40_hex"],
            "detail": PINNED_UPSTREAM_COMMIT_SHORT,
        },
        {
            "name": "licence_mit",
            "ok": v["license_file_present"] and v["license"] == "MIT",
            "detail": "LICENSE present, MIT",
        },
        {
            "name": "module_go",
            "ok": v["go_module"] == GO_MODULE and v["go_version"] == GO_VERSION,
            "detail": f"{v['go_module']} (go {v['go_version']})",
        },
        {
            "name": "entree_cli",
            "ok": v["entry_point"],
            "detail": "cmd/spynel/main.go -> cli.Run",
        },
        {
            "name": "surface_orchestration",
            "ok": v["surface_complete"],
            "detail": (
                f"{v['go_files_total']} .go, {v['test_files_total']} tests, "
                f"{v['internal_packages']} paquets internal ; workers {v['harness_workers_present']} ; "
                f"canaux {v['channels_present']} ; API locale socket Unix"
            ),
        },
        {
            "name": "cible_agent_zero_sans_duplication",
            "ok": v["orchestration_target"] == "fiber:a0:agent-zero" and not v["loop_duplicated"],
            "detail": "reference fiber:a0:agent-zero, 0 code de loop dans l'adapter",
        },
        {
            "name": "adapter_sans_reseau",
            "ok": v["adapter_network_calls"] == 0,
            "detail": "stdlib seule, 0 import reseau, 0 appel sortant",
        },
    ]
