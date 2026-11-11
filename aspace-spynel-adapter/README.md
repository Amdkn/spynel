# A'Space adapter — spynel

**Adresse :** `fiber:a0:spynel` — D-N053 pas B (design Clara, design signé pas B D-B0..D-B3).
**Fork souverain :** `Amdkn/spynel` (parent `agent0ai/spynel`, branche `main`).
**Gel amont :** `685ac65db967446d4e1cff65971ba0dc4827262f` (« Support /models through the shared model selection path »).
**Bind Cordis Fiber (2L) :** `3e076a1494364343cdafd703134b3fb46cbe7144` — `aspace-plugin.json`, re-appliqué VERBATIM sur `main` au-dessus de l'adapter (F8 D2).
**Licence :** `MIT`.
**Version adapter :** 0.1.0 — contrat seul, patron D-N048 (dify / cordis) et pas A (chronos).

## Ce que fait l'adapter

Spynel is a classic, non-AI program that coordinates and oversees external
AI/coding harnesses. "Simplicity at scale." One human → one agent →
infinite agents. L'adapter couvre l'interface d'orchestration complète
(D10) : entrée `cmd/spynel/main.go` → `cli.Run`, harness workers (acp,
claude, codex, pi + catalog, supervisor, worker), orchestrateur
(`internal/orchestrator` : manager, routes, worker, work_list, status),
jobs (`internal/app` : job_archive, job_info, job_worker), canaux
(telegram, whatsapp, tui), API locale (socket Unix privé, token, pas de
TCP par défaut). Il référence `fiber:a0:agent-zero` comme cible
d'orchestration **sans dupliquer le loop agent-zero** (0 code de loop
dans l'adapter).

Surface : `validate()` (constate : gel, licence, module Go, surface
d'orchestration mesurée au fichier, zéro appel réseau), `doctor()` (liste
de contrôles), `describe()` (manifeste machine). **Aucun fichier amont
touché** (hors la ligne d'index DOX requise par le contrat du repo, voir
la fiche), **aucun appel réseau, aucun poids monté dans le fork.**

Mesures au gel : 395 fichiers `.go`, 27 paquets `internal/`, 202 fichiers
`_test.go` (188 `internal/`, 3 `scripts/`, 11 `third_party/bubbletea`).

## Confinement

Aucun confinement commercial : code MIT. Usage B2B autorisé par la
licence. Les canaux telegram/whatsapp exigent des secrets fournis par
l'utilisateur (jamais lus ni stockés ici).

## Tests

```bash
python -m pytest aspace-spynel-adapter/tests/test_smoke.py -v
```

Smoke : constantes (gel 40-hex, adresse fiber, cible agent-zero,
licence, module Go), `validate()` vert (surface complète mesurée),
`doctor()` tout ok, zéro import réseau dans l'adapter. La suite amont
est celle du module au gel (`go test ./...`, voir la fiche d'adaptation :
`spynel-ADAPTATION.md`, évidence D-N053/b/spynel/).
