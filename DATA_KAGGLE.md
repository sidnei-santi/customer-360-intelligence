# Integração Dataset Kaggle - Customer 360

## 📋 Sobre o dataset

- **Fonte:** https://www.kaggle.com/datasets/vinaykandimalla/customer-360
- **Autor:** vinay kandimalla
- **Licença:** CC0: Public Domain (domínio público — uso livre, sem restrições)
- **Tamanho:** ~179 MB
- **Tabelas:** 5 (customers, orders, products, support_tickets, clickstream)

## 📥 Passo 1: Baixar o dataset

Acesse a página do Kaggle e faça o download manual:

```
https://www.kaggle.com/datasets/vinaykandimalla/customer-360/download
```

Ou via linha de comando (requer autenticação Kaggle configurada):

```bash
kaggle datasets download vinaykandimalla/customer-360
```

## 📁 Passo 2: Extrair e posicionar os arquivos

Extraia o arquivo ZIP e coloque os CSVs na pasta:

```
data/kaggle/
```

Estrutura esperada após extração:

```
data/kaggle/
├── customers.csv
├── orders.csv
├── products.csv
├── support_tickets.csv
└── clickstream.csv
```

> ⚠️ Os arquivos CSV e ZIP estão no `.gitignore` e não serão versionados. Cada desenvolvedor precisa baixar manualmente.

## ☁️ Passo 3: Upload para o Volume do Unity Catalog

O notebook `03_kaggle_bronze_ingestion.py` lê os dados deste caminho:

```
/Volumes/customer_360/raw/kaggle
```

Faça upload dos CSVs para esse Volume no Databricks (via UI do Databricks, Databricks CLI, ou Databricks SDK).

## 🚀 Passo 4: Executar o notebook

No Databricks Workspace, execute:

```
databricks/notebooks/03_kaggle_bronze_ingestion.py
```

Ou via job Databricks Bundle (já adicionado ao `databricks.yml` como tarefa `kaggle_bronze_ingestion`).

## 🔍 Diferenças em relação ao pipeline principal (`data/synthetic/`)

| Aspecto | Seu projeto (synthetic) | Dataset Kaggle |
|---------|------------------------|----------------|
| Contexto | B2B (Empresas) | B2C (Ecommerce varejo) |
| Idioma | Português | Inglês |
| customer_id | CUST-0001 (sequencial) | UUID |
| Qualidade | Limpo, controlado | Intencionalmente sujo (30% valores inconsistentes) |
| Oportunidades de venda | Sim | Não |
| Clickstream | Não | Sim (2M eventos) |
| Perfis de risco/churn | Sim | Não |

## 💡 Uso recomendado

Use este dataset como um **cenário secundário de teste** para validar que seu pipeline Silver consegue lidar com dados sujos, duplicatas e valores faltando. Mantenha o `data/synthetic/` como fonte principal para demos e casos de uso B2B.
