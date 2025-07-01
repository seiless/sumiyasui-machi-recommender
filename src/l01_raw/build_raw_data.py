from src.l01_raw.read_master_table import create_master_table_from_sqlserver

# SQLDBよりマスターテーブル読み込み
prefecture_master_table = create_master_table_from_sqlserver(
    "sumiyasui_machi_recommender", "prefecture_master"
)
prefecture_master_table.head()
