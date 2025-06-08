# Exchange Rate ETL Pipeline:
An automated Exchange Rate ETL Pipeline that **extracts** exchange rate data from an API, cleans it and stores it in a postgres database on Render.
The pipeline is automated using cron scheduler that updates the database at 0430 UTC everyday.
