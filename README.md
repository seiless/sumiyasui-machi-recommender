🏠 自分だけの条件で探す「住みやすい街」推薦システム

単に家賃だけで家を探すのではなく、ユーザーのライフスタイルに合わせた最適な街を推薦するウェブアプリケーションです。
家賃、治安、施設の利便性など多様なデータを総合し、個人の好みに応じた重み付けを適用することで、データに基づいた合理的な居住地の選択をサポートします。

(ここに実際のプロジェクト実行画面のスクリーンショットや GIF を追加することを強く推奨します。)

🚀 主な機能
カスタマイズ可能な条件設定: 希望家賃、路線、施設の利便性など、様々な条件をスライダーやメニューで直接設定
重み付けによるスコアリング: 治安、家賃、利便性など、各項目に対する個人の好みを重みとして付与し、最終的な「住みやすさスコア」を計算
データ統合分析: 不動産物件情報（SUUMO など）と公共データ（治安、インフラなど）を組み合わせ、多角的な分析を提供
インタラクティブな地図での可視化: 推薦された街の位置と情報を地図上で直感的に確認
🛠️ 技術スタックと開発環境
区分 技術
バックエンド Python 3.11+
ウェブフレームワーク Streamlit
データハンドリング Pandas
機械学習 Scikit-learn
ウェブスクレイピング Requests, BeautifulSoup4, lxml
地図可視化 Folium
テスト Pytest
コード品質管理 Black, Flake8
CI/CD GitHub Actions
依存関係管理 venv, requirements.txt, requirements-dev.txt

フォルダ構成
sumiyasui-machi-recommender/
├── .github/workflows/ # GitHub Actions (CI/CD) ワークフロー
│ └── run-tests.yml
├── data/ # データ保存用フォルダ (Git 追跡対象外)
├── scraper/ # データ収集(スクレイピング)モジュール
│ └── suumo_scraper.py
├── processor/ # データ加工・統合モジュール
│ └── data_processor.py
├── recommender/ # 推薦エンジンのロジックモジュール
│ └── engine.py
├── tests/ # Pytest テストコード
│ └── test_recommender.py
├── .env.example # 環境変数のサンプルファイル
├── .gitignore # Git 追跡除外リスト
├── app.py # Streamlit ウェブアプリケーション実行ファイル
├── config.py # プロジェクト設定値の管理
├── requirements.txt # 実行環境の依存関係
├── requirements-dev.txt # 開発環境の依存関係
└── README.md # プロジェクト説明書 (このファイル)
⚙️ 導入と実行方法
リポジトリのクローン

Bash

仮想環境の作成と有効化

Bash

# 仮想環境の作成 (初回のみ)

python -m venv venv

# 仮想環境の有効化 (Windows)

venv\Scripts\activate

# (macOS/Linux の場合: source venv/bin/activate)

依存ライブラリのインストール

Bash

# 実行用・開発用のライブラリを全てインストール

pip install -r requirements.txt
pip install -r requirements-dev.txt
環境変数の設定 (.env ファイル)
.env.example ファイルをコピーして .env ファイルを作成し、必要な API キーなどの値を入力します。(現在のプロジェクトでは、特別なキーは不要な場合があります。)

アプリケーションの実行

Bash

streamlit run app.py
ターミナルに表示される URL (通常 http://localhost:8501) をウェブブラウザで開いてください。

✅ テスト方法
プロジェクトの主要なロジックが正常に動作するかを確認するために、以下のコマンドを実行してください。

Bash

pytest
📝 今後の改善計画 (To-Do)
[ ] 分析対象エリアの拡大 (例: 大阪、福岡)
[ ] 追加データソースの結合 (例: 学区情報、周辺の飲食店レビュー)
[ ] 推薦アルゴリズムの高度化 (機械学習モデルの導入)
[ ] クラウドプラットフォームへのデプロイ (AWS, GCP など)
📄 ライセンス
このプロジェクトは MIT ライセンスの下で配布されています。
