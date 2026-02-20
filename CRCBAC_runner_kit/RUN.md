# CRCBAC_code – guia rápido de execução (smoke test)

Este kit ajuda a rodar um **teste mínimo** do repo `krishnasreeja/CRCBAC_code` (gateway CoAP + cliente), sem depender de datasets grandes.

## 0) Pré-requisitos

- Python 3.10+ (recomendado) + `pip`
- Git
- MongoDB rodando em `mongodb://localhost:27017`

> Alternativa simples para MongoDB: Docker
>
> `docker run --name mongo-crcbac -p 27017:27017 -d mongo:6`

## 1) Baixar o repositório

```
git clone https://github.com/krishnasreeja/CRCBAC_code
cd CRCBAC_code
```

## 2) (Opcional) Normalizar newlines

Se os arquivos `.py` aparecerem “em uma linha só” no editor, ou der erro de sintaxe, rode:

```
python /caminho/para/CRCBAC_runner_kit/fix_newlines.py CRBAC_GRT_dataset_code_result/CODE
```

## 3) Criar ambiente Python

No diretório do repo:

```
python -m venv .venv
# Windows:
.venv\Scripts\activate
# Linux/Mac:
source .venv/bin/activate

pip install -r /caminho/para/CRCBAC_runner_kit/requirements.txt
```

## 4) Seed do MongoDB (dataset mínimo)

```
python /caminho/para/CRCBAC_runner_kit/seed_mongo.py
```

## 5) Rodar o gateway (servidor CoAP)

Terminal 1:

```
python CRBAC_GRT_dataset_code_result/CODE/CRBAC_Gateway_Grant_transfer.py
```

Ele deve imprimir algo como **"CoAP server started."**.

## 6) Rodar o cliente (device)

Edite `CRBAC_Device.py` e troque a variável `csv_file` para apontar para `test_requests.tsv` (deste kit).

Depois, Terminal 2:

```
python CRBAC_GRT_dataset_code_result/CODE/CRBAC_Device.py
```

## O que esperar

- O servidor deve imprimir logs/linhas de decisão
- O cliente deve receber e imprimir o `response` decodificado

Se quiser testar o ramo **AC** (access check), crie um TSV com 4 colunas e `request_type = AC`.
