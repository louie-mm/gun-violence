from src.data_enrichment import AddGeoCodesToDb
from src.etl import CsvToDb

CsvToDb().run()
AddGeoCodesToDb().run()
