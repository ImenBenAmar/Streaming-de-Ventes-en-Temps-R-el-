# dashboard_query.py
from pyspark.sql import SparkSession
import time

spark = SparkSession.builder \
    .appName("DashboardVentes") \
    .config("spark.sql.extensions", "io.delta.sql.DeltaSparkSessionExtension") \
    .config("spark.sql.catalog.spark_catalog", "org.apache.spark.sql.delta.catalog.DeltaCatalog") \
    .getOrCreate()

print("DASHBOARD EN TEMPS RÉEL - CA PAR PAYS/SEGMENT")
print("=" * 80)

while True:
    try:
        df = spark.read.format("delta").load("C:/tmp/delta/silver/ventes_agg")
        
        print(f"\nMISE À JOUR : {time.strftime('%H:%M:%S')}")
        print("-" * 80)
        
        df.groupBy("pays", "segment") \
          .sum("total_depense") \
          .withColumnRenamed("sum(total_depense)", "ca_total") \
          .orderBy("ca_total", ascending=False) \
          .show(15, truncate=False)
          
    except Exception as e:
        print(f"Attente des données... ({e})")
    
    time.sleep(30)