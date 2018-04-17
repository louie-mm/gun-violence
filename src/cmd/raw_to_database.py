from src.facades.data_enrichment_facade.add_geocode_to_raw import AddGeoCodesToDb
from src.facades.download_facade.raw_download import CsvToDb

CsvToDb().run()
AddGeoCodesToDb().run()
