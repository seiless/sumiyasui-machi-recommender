import requests
from bs4 import BeautifulSoup
import pandas as pd
from urllib.parse import urljoin, urlparse
from src import config
from sqlalchemy import create_engine
import logging
import os
import traceback
from dotenv import load_dotenv
from src.config import PROJECT_ROOT, SCHEMA_NAME

env_path = PROJECT_ROOT / ".env"
load_dotenv(dotenv_path=env_path)

logger = logging.getLogger(__name__)

DB_CONNECTION_STR = os.getenv("DB_CONNECTION_STR")
CONNECTION = create_engine(DB_CONNECTION_STR) if DB_CONNECTION_STR else None


def extract_csv_links(base_url: str) -> list[str]:
    response = requests.get(base_url, headers=config.HEADERS)
    response.raise_for_status()
    soup = BeautifulSoup(response.content, "html.parser")

    links = soup.find_all("a", class_="csv")
    full_links = [urljoin(base_url, link.get("href")) for link in links]

    return full_links


def process_and_return_df(csv_url: str) -> pd.DataFrame:
    """_summary_

    Args:
        csv_url (str): _description_

    Returns:
        pd.DataFrame: _description_
    """
    relative_path = urlparse(csv_url).path.split("/")[-1]
    filename = relative_path.replace(".csv", "").replace(".", "_").lower()
    df = pd.read_csv(csv_url, encoding="sjis")
    return df, filename


def save_pandas_df_to_sqlserver(
    df: pd.DataFrame, schema_name: str, table_name: str
) -> None:
    if not CONNECTION:
        logger.error("DB_CONNECTION_STR variable not setted.")
        return None
    conn = None
    try:
        df.to_sql(
            schema=schema_name,
            name=table_name,
            con=CONNECTION,
            if_exists="replace",
            index=False,
        )
        logger.info("connection is succed")
        logger.info(f"{schema_name}.{table_name} is created")
    except Exception as e:
        logger.error(e)
        logger.error(traceback.format_exc())

    finally:
        if conn is not None:
            conn.close()
            logger.info("DB Connection is closed")


if __name__ == "__main__":
    PAGE_URL = config.CRILINAL_TARGETS["東京都"]
    OUTPUT_DIR = config.CRIME

    print("1. CSVリンクの抽出を始めます...")
    csv_urls = extract_csv_links(PAGE_URL)
    print(f"合計 {len(csv_urls)}個のリンクを見つけました。")

    print("\n2. 各CSVファイルをSQLサーバへ保存します...")
    saved_files = []
    downloaded_files = 0
    for url in csv_urls:
        try:
            logger.info(f"{downloaded_files}件目ダウンロード中")
            temp_df, filename = process_and_return_df(url)
            save_pandas_df_to_sqlserver(temp_df, SCHEMA_NAME, filename)
            downloaded_files = downloaded_files + 1
        except Exception as e:
            print(f"エラー発生: {url} 処理中問題が発生しました- {e}")

    print(f"\n計 {downloaded_files}個のファイルが保存されました。")
