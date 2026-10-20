# Databricks notebook source
# /// script
# [tool.databricks.environment]
# environment_version = "6"
# ///
# MAGIC %md
# MAGIC # Customer 360 Intelligence - Ingestão Kaggle (Camada Bronze)
# MAGIC Ingestão do dataset público do Kaggle (vinaykandimalla/customer-360) para a camada Bronze.
# MAGIC
# MAGIC Dataset: https://www.kaggle.com/datasets/vinaykandimalla/customer-360
# MAGIC Licença: CC0: Public Domain

# COMMAND ----------

from pyspark.sql import functions as F

# Caminho dos arquivos CSV do Kaggle no Volume do Unity Catalog
# Atenção: baixe o dataset manualmente do Kaggle e faça upload para este caminho
INPUT_PATH = "/Volumes/customer_360/raw/kaggle"

# Catálogo e schema de destino (mesmo catálogo do pipeline principal)
BRONZE_CATALOG = "customer_360"
BRONZE_SCHEMA = "bronze"

# Garantir catálogo e schema
spark.sql(f"CREATE CATALOG IF NOT EXISTS {BRONZE_CATALOG}")
spark.sql(f"CREATE DATABASE IF NOT EXISTS {BRONZE_CATALOG}.{BRONZE_SCHEMA}")

# COMMAND ----------

# MAGIC %md
# MAGIC ## 1. CRM Customers (50.000 registros)
# MAGIC Colunas: customer_id (UUID), first_name, last_name, email, phone_number, gender, dob, signup_date, address, city, state, country, device_id(s), source

# COMMAND ----------

customers_kaggle_df = (
    spark.read.format("csv")
    .option("header", "true")
    .option("inferSchema", "true")
    .load(f"{INPUT_PATH}/customers.csv")
    .withColumn("_ingested_at", F.current_timestamp())
    .withColumn("_source_file", F.col("_metadata.file_path"))
    .withColumn("_source_system", F.lit("kaggle_customer_360"))
)

customers_kaggle_df.write.format("delta") \
    .mode("overwrite") \
    .saveAsTable(f"{BRONZE_CATALOG}.{BRONZE_SCHEMA}.kaggle_customers_raw")

print(f"✅ Tabela Bronze kaggle_customers_raw criada: {customers_kaggle_df.count()} registros")

# COMMAND ----------

# MAGIC %md
# MAGIC ## 2. Orders / Transactions (300.000 registros)
# MAGIC Colunas: order_id, customer_id, product_id, order_amount, order_date, payment_method, status, quantity

# COMMAND ----------

orders_kaggle_df = (
    spark.read.format("csv")
    .option("header", "true")
    .option("inferSchema", "true")
    .load(f"{INPUT_PATH}/orders.csv")
    .withColumn("_ingested_at", F.current_timestamp())
    .withColumn("_source_file", F.col("_metadata.file_path"))
    .withColumn("_source_system", F.lit("kaggle_customer_360"))
)

orders_kaggle_df.write.format("delta") \
    .mode("overwrite") \
    .saveAsTable(f"{BRONZE_CATALOG}.{BRONZE_SCHEMA}.kaggle_orders_raw")

print(f"✅ Tabela Bronze kaggle_orders_raw criada: {orders_kaggle_df.count()} registros")

# COMMAND ----------

# MAGIC %md
# MAGIC ## 3. Product Catalog (500 produtos)
# MAGIC Colunas: product_id, product_name, category, price

# COMMAND ----------

products_kaggle_df = (
    spark.read.format("csv")
    .option("header", "true")
    .option("inferSchema", "true")
    .load(f"{INPUT_PATH}/products.csv")
    .withColumn("_ingested_at", F.current_timestamp())
    .withColumn("_source_file", F.col("_metadata.file_path"))
    .withColumn("_source_system", F.lit("kaggle_customer_360"))
)

products_kaggle_df.write.format("delta") \
    .mode("overwrite") \
    .saveAsTable(f"{BRONZE_CATALOG}.{BRONZE_SCHEMA}.kaggle_products_raw")

print(f"✅ Tabela Bronze kaggle_products_raw criada: {products_kaggle_df.count()} registros")

# COMMAND ----------

# MAGIC %md
# MAGIC ## 4. Support Tickets (30.000 registros)
# MAGIC Colunas: ticket_id, customer_id, issue_type, ticket_created, ticket_resolved, resolution_time_hours, sentiment, support_agent

# COMMAND ----------

tickets_kaggle_df = (
    spark.read.format("csv")
    .option("header", "true")
    .option("inferSchema", "true")
    .load(f"{INPUT_PATH}/support_tickets.csv")
    .withColumn("_ingested_at", F.current_timestamp())
    .withColumn("_source_file", F.col("_metadata.file_path"))
    .withColumn("_source_system", F.lit("kaggle_customer_360"))
)

tickets_kaggle_df.write.format("delta") \
    .mode("overwrite") \
    .saveAsTable(f"{BRONZE_CATALOG}.{BRONZE_SCHEMA}.kaggle_support_tickets_raw")

print(f"✅ Tabela Bronze kaggle_support_tickets_raw criada: {tickets_kaggle_df.count()} registros")

# COMMAND ----------

# MAGIC %md
# MAGIC ## 5. Clickstream Events (2M ou 500K registros)
# MAGIC Colunas: event_id, session_id, customer_id (30% null), event_type, page_url, device_id, timestamp

# COMMAND ----------

clickstream_kaggle_df = (
    spark.read.format("csv")
    .option("header", "true")
    .option("inferSchema", "true")
    .load(f"{INPUT_PATH}/clickstream.csv")
    .withColumn("_ingested_at", F.current_timestamp())
    .withColumn("_source_file", F.col("_metadata.file_path"))
    .withColumn("_source_system", F.lit("kaggle_customer_360"))
)

clickstream_kaggle_df.write.format("delta") \
    .mode("overwrite") \
    .saveAsTable(f"{BRONZE_CATALOG}.{BRONZE_SCHEMA}.kaggle_clickstream_raw")

print(f"✅ Tabela Bronze kaggle_clickstream_raw criada: {clickstream_kaggle_df.count()} registros")

# COMMAND ----------

# MAGIC %md
# MAGIC ## Resumo das tabelas criadas
# MAGIC %sql
# MAGIC SHOW TABLES IN customer_360.bronze LIKE 'kaggle_%';
