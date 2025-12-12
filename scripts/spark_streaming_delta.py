from pyspark.sql import SparkSession
from pyspark.sql.functions import col, from_json, current_timestamp
from pyspark.sql.types import StructType, StructField, StringType, IntegerType, DoubleType

# Initialiser Spark avec Delta et Kafka
spark = SparkSession.builder \
    .appName("VentesStreamingDelta") \
    .config("spark.sql.extensions", "io.delta.sql.DeltaSparkSessionExtension") \
    .config("spark.sql.catalog.spark_catalog", "org.apache.spark.sql.delta.catalog.DeltaCatalog") \
    .getOrCreate()

# Schéma des données ventes
schema = StructType([
    StructField("id_vente", IntegerType(), True),
    StructField("produit", StringType(), True),
    StructField("quantite", IntegerType(), True),
    StructField("prix_unitaire", DoubleType(), True),
    StructField("pays", StringType(), True),
    StructField("segment", StringType(), True),
    StructField("timestamp", StringType(), True)
])

# Lire le stream Kafka
df = spark.readStream \
    .format("kafka") \
    .option("kafka.bootstrap.servers", "localhost:9092") \
    .option("subscribe", "ventes_stream") \
    .option("startingOffsets", "earliest") \
    .load()

# Parser les données JSON
df_parsed = df.selectExpr("CAST(value AS STRING)") \
    .select(from_json(col("value"), schema).alias("data")) \
    .select("data.*") \
    .withColumn("processing_time", current_timestamp())

# Écrire en Bronze (données brutes)
bronze_path = r"C:/tmp/delta/bronze/ventes"
query_bronze = df_parsed.writeStream \
    .format("delta") \
    .outputMode("append") \
    .option("checkpointLocation", "C:/tmp/delta/bronze/checkpoint") \
    .start(bronze_path)

# Enrichir pour Silver (e.g., calcul total_depense)
df_enriched = df_parsed.withColumn("total_depense", col("quantite") * col("prix_unitaire"))

# Agrégation pour Silver (micro-batch)
silver_path = "C:/tmp/delta/silver/ventes_agg"
query_silver = df_enriched.writeStream \
    .format("delta") \
    .outputMode("append") \
    .option("checkpointLocation", "C:/tmp/delta/silver/checkpoint") \
    .start(silver_path)

# Attendre la fin (pour test, Ctrl+C pour arrêter)
query_bronze.awaitTermination()
query_silver.awaitTermination()