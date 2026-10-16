# Databricks notebook source
# /// script
# [tool.databricks.environment]
# environment_version = "6"
# ///
# MAGIC %md
# MAGIC # Customer 360 Intelligence - Ingestão Camada Bronze
# MAGIC Ingestão dos dados sintéticos a partir do volume do Unity Catalog.

# COMMAND ----------

# Caminho correto descoberto no seu volume
INPUT_PATH = "/Volumes/customer_360/raw/main" 

# Vamos criar o schema/database de destino no Unity Catalog (ex: bronze)
BRONZE_CATALOG = "customer_360"
BRONZE_SCHEMA = "bronze"

spark.sql(f"CREATE CATALOG IF NOT EXISTS {BRONZE_CATALOG}")
spark.sql(f"CREATE DATABASE IF NOT EXISTS {BRONZE_CATALOG}.{BRONZE_SCHEMA}")

# COMMAND ----------

# 1. Ingestão Customers Raw
from pyspark.sql import functions as F

customers_df = (
    spark.read.format("csv")
    .option("header", "true")
    .option("inferSchema", "true")
    .load(f"{INPUT_PATH}/customers_raw.csv")
    .withColumn("_ingested_at", F.current_timestamp())
    .withColumn("_source_file", F.col("_metadata.file_path"))
)

customers_df.write.format("delta") \
    .mode("overwrite") \
    .saveAsTable(f"{BRONZE_CATALOG}.{BRONZE_SCHEMA}.customers_raw")

print("✅ Tabela Bronze customers_raw criada com sucesso!")

# COMMAND ----------

# 2. Ingestão Orders Raw
orders_df = (
    spark.read.format("csv")
    .option("header", "true")
    .option("inferSchema", "true")
    .load(f"{INPUT_PATH}/orders_raw.csv")
    .withColumn("_ingested_at", F.current_timestamp())
    .withColumn("_source_file", F.col("_metadata.file_path"))
)

orders_df.write.format("delta") \
    .mode("overwrite") \
    .saveAsTable(f"{BRONZE_CATALOG}.{BRONZE_SCHEMA}.orders_raw")

print("✅ Tabela Bronze orders_raw criada com sucesso!")

# COMMAND ----------

# 3. Ingestão Interactions Raw
interactions_df = (
    spark.read.format("csv")
    .option("header", "true")
    .option("inferSchema", "true")
    .load(f"{INPUT_PATH}/interactions_raw.csv")
    .withColumn("_ingested_at", F.current_timestamp())
    .withColumn("_source_file", F.col("_metadata.file_path"))
)

interactions_df.write.format("delta") \
    .mode("overwrite") \
    .saveAsTable(f"{BRONZE_CATALOG}.{BRONZE_SCHEMA}.interactions_raw")

print("✅ Tabela Bronze interactions_raw criada com sucesso!")

# COMMAND ----------

# 4. Ingestão Opportunities Raw
opportunities_df = (
    spark.read.format("csv")
    .option("header", "true")
    .option("inferSchema", "true")
    .load(f"{INPUT_PATH}/opportunities_raw.csv")
    .withColumn("_ingested_at", F.current_timestamp())
    .withColumn("_source_file", F.col("_metadata.file_path"))
)

opportunities_df.write.format("delta") \
    .mode("overwrite") \
    .saveAsTable(f"{BRONZE_CATALOG}.{BRONZE_SCHEMA}.opportunities_raw")

print("✅ Tabela Bronze opportunities_raw criada com sucesso!")

# COMMAND ----------

# MAGIC %sql
# MAGIC SELECT * FROM customer_360.bronze.customers_raw LIMIT 5;