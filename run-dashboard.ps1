# run-dashboard.ps1
Set-Location "D:\tp-kafka-spark"

Write-Host "DASHBOARD DELTA LAKE - CA EN TEMPS RÉEL" -ForegroundColor Cyan

$env:PYSPARK_PYTHON = "C:\Users\pc\AppData\Local\Programs\Python\Python310\python.exe"
$env:PYSPARK_DRIVER_PYTHON = "C:\Users\pc\AppData\Local\Programs\Python\Python310\python.exe"
$env:HADOOP_HOME = "C:\hadoop"
$env:PATH = "$env:HADOOP_HOME\bin;" + $env:PATH

# Lancer et GARDER LA FENÊTRE OUVERTE
spark-submit --packages io.delta:delta-spark_2.12:3.2.0 dashbord_query.py

# Empêche la fermeture
Write-Host "Appuie sur une touche pour fermer..." -ForegroundColor Yellow
$null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")