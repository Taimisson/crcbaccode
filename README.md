# CRCBAC_code – Setup de Reprodução

> Baseline **CRCBAC** (Context-aware Role-Capability-Based Access Control).
> Repo original: https://github.com/krishnasreeja/CRCBAC_code

---

## Pré-requisitos

| Requisito | Versão testada |
|-----------|---------------|
| Python | 3.10.x |
| Docker Desktop | qualquer |
| Git | qualquer |

---

## 1. Clonar e criar venv

```powershell
git clone https://github.com/krishnasreeja/CRCBAC_code
cd CRCBAC_code
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r CRCBAC_runner_kit\requirements.txt
```

## 2. Subir MongoDB

```powershell
docker run --name mongo-crcbac -p 27017:27017 -d mongo:6
```

Verificar:

```powershell
docker exec -it mongo-crcbac mongosh --eval "db.runCommand({ ping: 1 })"
# Esperado: { ok: 1 }
```

## 3. Seed do banco

```powershell
python CRCBAC_runner_kit\seed_mongo.py
```

Saída esperada:

```
Seed complete.
DB: CRBAC_Policies
Collections seeded: GRT_Role_ctx_policy4000, GRT_Role_ctx_policy500, GRT_Role_ctx_policy5000, GRT_dev500_R100_20ctx, p1k_rolectx_res10, throughput_file1
```

## 4. Rodar o gateway (Terminal 1 — deixar aberto)

```powershell
python .\CRBAC_GRT_dataset_code_result\CODE\CRBAC_Gateway_Grant_transfer.py
```

Saída: `CoAP server started.`

## 5. Smoke test (Terminal 2)

```powershell
python .\send_test_coap.py
```

Saída esperada:

```
=== Response (decoded) ===
Role_n: R6, Role_t: R1
Role hierarchy satisfied
Capability matched,permission:allow
T2: HH:MM:SS
```

## 6. Benchmark (Terminal 2)

```powershell
python .\bench_coap.py
```

Gera `bench_processing_time_ms.csv` (50 amostras, mediana ~5–7 ms).

---

## Troubleshooting rápido

| Problema | Solução |
|----------|---------|
| `ConnectionRefusedError` | `docker start mongo-crcbac` |
| `Required collection does not exist` | Rodar o seed (passo 3) |
| Porta 5683 ocupada | `Get-Process python \| Stop-Process` |
| `ModuleNotFoundError` | Ativar venv + `pip install -r CRCBAC_runner_kit\requirements.txt` |
| Timeout no smoke test | Verificar se o gateway está rodando (passo 4) |
