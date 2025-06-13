import requests
from bs4 import BeautifulSoup
import pandas as pd
import time
import random
from urllib.parse import urljoin
from typing import List, Tuple, Dict
import config


def scrape_single_page(page_url: str) -> Tuple[List[Dict], str]:
    """
    指定された単一ページのURLから物件情報をスクレイピングし、
    「次のページ」のURLを返します。
    """
    response = requests.get(page_url, headers=config.HEADERS)
    response.raise_for_status()  # リクエストが失敗した場合、エラーを発生させます。
    soup = BeautifulSoup(response.content, "lxml")
    page_properties = []
    listings = soup.find_all(
        "div", class_="property property--highlight js-property js-cassetLink"
    )

    for listing in listings:
        # 各項目を抽出する前に、デフォルト値を設定します。
        (
            title,
            address,
            transport_str,
            rent,
            admin_fee,
            deposit,
            key_money,
            layout,
            area,
            building_type,
            age,
        ) = ["N/A"] * 11

        try:
            # タイトルを抽出します（最上位のコンテナにのみ存在）。
            title_element = listing.find("a", class_="js-cassetLinkHref")
            if title_element:
                title = title_element.text.strip()

            # 詳細情報が含まれる「detailbox」コンテナを探します。
            detailbox = listing.find("div", class_="detailbox")
            if detailbox:
                # 「detailbox」内部の情報をパースします。

                # 1. 価格や面積などが含まれるメインテーブル
                property_table = detailbox.find(
                    "div", class_="detailbox-property"
                )  # noqa: E501
                if property_table:
                    cols = property_table.find_all("td")

                    if len(cols):
                        # 1番目のセル：賃料、管理費
                        rent_div = cols[0].find(
                            "div", class_="detailbox-property-point"
                        )
                        if rent_div:
                            rent = rent_div.text.strip()

                        admin_fee_div = (
                            rent_div.find_next_sibling("div")
                            if rent_div
                            else None  # noqa: E501
                        )
                        if admin_fee_div:
                            admin_fee = admin_fee_div.text.strip()

                        # 2番目のセル：敷金、礼金
                        for div in cols[1].find_all("div"):
                            span = div.find("span", class_="square_pct")
                            if span:
                                label_text = span.text.strip()
                                if "敷" in label_text:
                                    deposit = (
                                        div.text.strip()
                                        .replace(label_text, "")
                                        .strip()  # noqa: E501
                                    )
                                elif "礼" in label_text:
                                    key_money = (
                                        div.text.strip()
                                        .replace(label_text, "")
                                        .strip()  # noqa: E501
                                    )

                        # 3番目のセル：間取り、面積 (向きは除外)
                        madori_divs = cols[2].find_all("div")
                        if len(madori_divs) >= 2:
                            layout = madori_divs[0].text.strip()
                            area = madori_divs[1].text.strip()

                        # 4番目のセル：種別、築年数
                        type_divs = cols[3].find_all("div")
                        if len(type_divs) >= 2:
                            building_type = type_divs[0].text.strip()
                            age = type_divs[1].text.strip()

                        # 5番目のセル：住所
                        address = cols[4].text.strip()

                # 2. 交通情報の抽出
                transport_box = detailbox.find("div", class_="detailnote-box")
                if transport_box:
                    transport_divs = transport_box.find_all("div")
                    transport_list = [
                        t.text.strip()
                        for t in transport_divs
                        if t.text.strip() and "お電話" not in t.text
                    ]
                    transport_str = " | ".join(transport_list)

            # 抽出した情報を辞書として整理します。
            property_info = {
                "物件名": title,
                "住所": address,
                "交通": transport_str,
                "賃料": rent,
                "管理費": admin_fee,
                "敷金": deposit,
                "礼金": key_money,
                "間取り": layout,
                "専有面積": area,
                "種別": building_type,
                "築年数": age,
            }
            page_properties.append(property_info)

        except Exception as e:
            print(
                f"データ抽出中にエラーが発生: {e}。この物件({title})はスキップします。"
            )
            continue

    # 「次のページ」へのリンクを探します。
    next_page_link_element = soup.find("a", string="次へ")

    next_page_url = (
        urljoin(page_url, next_page_link_element["href"])
        if next_page_link_element
        else None
    )

    return page_properties, next_page_url


if __name__ == "__main__":
    # configファイルから設定値を取得
    start_url = config.SUUMO_TARGETS["山手線"]
    MAX_PAGES = config.SCRAPING_MAX_PAGES

    current_url = start_url
    all_results = []
    page_count = 1

    # 最後のページまでループを続けます
    while current_url:
        if page_count > MAX_PAGES:
            print(f"最大設定ページ数 {MAX_PAGES} に到達したため、処理を終了します。")
            break

        print(f"--- {page_count}ページ目: スクレイピング中...")

        page_data, next_url = scrape_single_page(current_url)
        if page_data:
            print(f"  -> {len(page_data)}件の情報を取得しました。")
        else:
            print(
                "このページで物件が見つからなかったため、スクレイピングを終了します。"
            )
            break

        all_results.extend(page_data)
        current_url = next_url
        page_count += 1

        if current_url:
            # 次のページをリクエストする前に、サーバーに負荷をかけないようランダムな時間待機します。
            sleep_time = random.uniform(1.0, 2.5)
            print(f"次のページに移動する前に{sleep_time:.2f}秒待機します...")
            time.sleep(sleep_time)

    # 最終結果の処理
    final_df = pd.DataFrame(all_results)

    print("\n" + "=" * 50)
    print("スクレイピング完了！")
    print(f"合計{len(final_df)}件の物件情報を収集しました。")

    output_filename = "suumo_listings.csv"
    final_df.to_csv(
        config.DATA_DIR + output_filename, index=False, encoding="utf-8-sig"
    )
    print(f"\n結果は'{output_filename}'ファイルに保存されました。")
