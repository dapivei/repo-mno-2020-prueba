"""Main module."""

manianeras = get_total_discourse()
manianeras.to_parquet('../data/raw/manianeras.parquet')
