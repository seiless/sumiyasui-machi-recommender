import os

# --- フォルダーパス設定 ---
DATA_DIR = "data/"
RAW_DATA_DIR = os.path.join(DATA_DIR, "01_raw")
INTERMEDIATE_DATA_DIR = os.path.join(DATA_DIR, "02_intermediate")
PRIMARY_DATA_DIR = os.path.join(DATA_DIR, "03_primary")

# RAW`データ出力先設定
SUUMO = os.path.join(RAW_DATA_DIR, "suumo_scraping")
CRIME = os.path.join(RAW_DATA_DIR, "keisicho_crime_stats")

# --- ヘッダー情報設定 ---
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"  # noqa: E501
}
# --- [追加] スクレイピングする最大ページ数 ---
SCRAPING_MAX_PAGES = 5

# --- スクレイピング対象URL設定 ---
# 先に路線別から作業し、今後は地域別に拡張する予定
SUUMO_TARGETS = {
    "山手線": "https://suumo.jp/jj/chintai/ichiran/FR301FC005/?ar=030&bs=040&ra=013&rn=0005&cb=0.0&ct=9999999&mb=0&mt=9999999&et=9999999&cn=9999999&shkr1=03&shkr2=03&shkr3=03&shkr4=03&sngz=&po1=25&po2=99&pc=100",  # noqa: E501
}

# --- 犯罪関連統計URL ---
# まずは東京都だけ
CRILINAL_TARGETS = {
    "東京都": "https://www.keishicho.metro.tokyo.lg.jp/about_mpd/jokyo_tokei/jokyo/ninchikensu.html"  # noqa: E501
}
