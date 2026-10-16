# Databricks notebook source
# MAGIC %md
# MAGIC # Customer 360 Intelligence - Transformations (Camada Silver)

# COMMAND ----------

from pyspark.sql import functions as F
from pyspark.sql.window import Window

CATALOG = "customer_360"
BRONZE_SCHEMA = "bronze"
SILVER_SCHEMA = "silver"

# Garantir catálogo e schema
spark.sql(f"CREATE CATALOG IF NOT EXISTS {CATALOG}")
spark.sql(f"CREATE DATABASE IF NOT EXISTS {CATALOG}.{SILVER_SCHEMA}")

# COMMAND ----------

# 1. Silver Customers
print("Processando Customers Silver...")
customers_bronze = spark.read.table(f"{CATALOG}.{BRONZE_SCHEMA}.customers_raw")

window_customers = Window.partitionBy("customer_id").orderBy(F.col("_ingested_at").desc())

customers_silver = (
    customers_bronze
    .withColumn("row_num", F.row_number().over(window_customers))
    .filter(F.col("row_num") == 1)
    .drop("row_num")
    .select(
        F.trim(F.col("customer_id")).alias("customer_id"),
        F.trim(F.col("company_name")).alias("company_name"),
        F.trim(F.col("segment")).alias("segment"),
        F.trim(F.col("industry")).alias("industry"),
        F.trim(F.col("status")).alias("status"),
        F.trim(F.col("risk_profile")).alias("risk_profile"),
        F.col("created_at").cast("timestamp").alias("created_at"),
        F.col("_ingested_at")
    )
)

customers_silver.write.format("delta") \
    .mode("overwrite") \
    .option("overwriteSchema", "true") \
    .saveAsTable(f"{CATALOG}.{SILVER_SCHEMA}.customers")

print("✅ Tabela Silver 'customers' criada!")

# COMMAND ----------

# 2. Silver Orders
print("Processando Orders Silver...")
orders_bronze = spark.read.table(f"{CATALOG}.{BRONZE_SCHEMA}.orders_raw")

window_orders = Window.partitionBy("order_id").orderBy(F.col("_ingested_at").desc())

orders_silver = (
    orders_bronze
    .withColumn("row_num", F.row_number().over(window_orders))
    .filter(F.col("row_num") == 1)
    .drop("row_num")
    .select(
        F.trim(F.col("order_id")).alias("order_id"),
        F.trim(F.col("customer_id")).alias("customer_id"),
        F.trim(F.col("product_name")).alias("product_name"),
        F.col("quantity").cast("integer").alias("quantity"),
        F.col("total_amount").cast("double").alias("total_amount"),
        F.trim(F.col("status")).alias("status"),
        F.col("order_date").cast("timestamp").alias("order_date"),
        F.col("_ingested_at")
    )
    .filter(F.col("customer_id").isNotNull())
)

orders_silver.write.format("delta") \
    .mode("overwrite") \
    .option("overwriteSchema", "true") \
    .saveAsTable(f"{CATALOG}.{SILVER_SCHEMA}.orders")

print("✅ Tabela Silver 'orders' criada!")

# COMMAND ----------

# 3. Silver Interactions
print("Processando Interactions Silver...")
interactions_bronze = spark.read.table(f"{CATALOG}.{BRONZE_SCHEMA}.interactions_raw")

window_interactions = Window.partitionBy("interaction_id").orderBy(F.col("_ingested_at").desc())

interactions_silver = (
    interactions_bronze
    .withColumn("row_num", F.row_number().over(window_interactions))
    .filter(F.col("row_num") == 1)
    .drop("row_num")
    .select(
        F.trim(F.col("interaction_id")).alias("interaction_id"),
        F.trim(F.col("customer_id")).alias("customer_id"),
        F.trim(F.col("channel")).alias("channel"),
        F.trim(F.col("sentiment")).alias("sentiment"),
        F.trim(F.col("notes")).alias("notes"),
        F.col("created_at").cast("timestamp").alias("created_at"),
        F.col("_ingested_at")
    )
)

interactions_silver.write.format("delta") \
    .mode("overwrite") \
    .option("overwriteSchema", "true") \
    .saveAsTable(f"{CATALOG}.{SILVER_SCHEMA}.interactions")

print("✅ Tabela Silver 'interactions' criada!")

# COMMAND ----------

# 4. Silver Opportunities
print("Processando Opportunities Silver...")
opps_bronze = spark.read.table(f"{CATALOG}.{BRONZE_SCHEMA}.opportunities_raw")

window_opps = Window.partitionBy("opportunity_id").orderBy(F.col("_ingested_at").desc())

opps_silver = (
    opps_bronze
    .withColumn("row_num", F.row_number().over(window_opps))
    .filter(F.col("row_num") == 1)
    .drop("row_num")
    .select(
        F.trim(F.col("opportunity_id")).alias("opportunity_id"),
        F.trim(F.col("customer_id")).alias("customer_id"),
        F.trim(F.col("title")).alias("title"),
        F.trim(F.col("stage")).alias("stage"),
        F.col("estimated_value").cast("double").alias("estimated_value"),
        F.col("created_at").cast("timestamp").alias("created_at"),
        F.col("_ingested_at")
    )
)

opps_silver.write.format("delta") \
    .mode("overwrite") \
    .option("overwriteSchema", "true") \
    .saveAsTable(f"{CATALOG}.{SILVER_SCHEMA}.opportunities")

print("✅ Tabela Silver 'opportunities' criada!")
