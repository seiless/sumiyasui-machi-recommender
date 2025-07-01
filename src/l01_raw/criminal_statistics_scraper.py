import requests
from bs4 import BeautifulSoup
import pandas as pd
from urllib.parse import urljoin, urlparse
from src import config


def extract_csv_links(base_url: str) -> list[str]:
    response = requests.get(base_url, headers=config.HEADERS)
    response.raise_for_status()
    soup = BeautifulSoup(response.content, "html.parser")

    links = soup.find_all("a", class_="csv")
    full_links = [urljoin(base_url, link.get("href")) for link in links]

    return full_links


def process_and_save_csv(csv_url: str, output_dir: str) -> str:
    relative_path = urlparse(csv_url).path.split("/")[-1]
    filename_stem = relative_path.replace(".csv", "").replace(".", "_")
    output_filename = f"{filename_stem}.csv"
    output_path = f"{output_dir}/{output_filename}"

    df = pd.read_csv(csv_url, encoding="sjis")
    df.to_csv(output_path, index=False, encoding="utf-8-sig")

    print(f"'{output_filename}'ファイルに保存されました。.")
    return output_path


if __name__ == "__main__":
    PAGE_URL = config.CRILINAL_TARGETS["東京都"]
    OUTPUT_DIR = config.CRIME

    print("1. CSVリンクの抽出を始めます...")
    csv_urls = extract_csv_links(PAGE_URL)
    print(f"총 {len(csv_urls)}個のリンクを見つけました。")

    print("\n2. 各CSVファイルをダウンロードし保存します...")
    saved_files = []
    for url in csv_urls:
        try:
            saved_path = process_and_save_csv(url, OUTPUT_DIR)
            saved_files.append(saved_path)
        except Exception as e:
            print(f"エラー発生: {url} 処理中問題が発生しました- {e}")

    print(f"\n총 {len(saved_files)}個のファイルが保存されました。")
