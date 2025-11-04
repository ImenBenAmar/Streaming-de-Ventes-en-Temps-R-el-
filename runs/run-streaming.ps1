# run-streaming.ps1
Set-Location "D:\tp-kafka-spark"

Write-Host "DÉMARRAGE SPARK STREAMING + DELTA LAKE" -ForegroundColor Green

# Python 3.10
$env:PYSPARK_PYTHON = "C:\Users\pc\AppData\Local\Programs\Python\Python310\python.exe"
$env:PYSPARK_DRIVER_PYTHON = "C:\Users\pc\AppData\Local\Programs\Python\Python310\python.exe"

# Hadoop / winutils
$env:HADOOP_HOME = "C:\hadoop"
$env:PATH = "$env:HADOOP_HOME\bin;" + $env:PATH

# Lancement
spark-submit --packages org.apache.spark:spark-sql-kafka-0-10_2.12:3.5.3,io.delta:delta-spark_2.12:3.2.0 spark_streaming_delta.py