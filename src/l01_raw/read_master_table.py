import pandas as pd
import os
from sqlalchemy import create_engine, text
import logging
import traceback
from dotenv import load_dotenv
from src.config import PROJECT_ROOT

env_path = PROJECT_ROOT / ".env"
load_dotenv(dotenv_path=env_path)

logger = logging.getLogger(__name__)

DB_CONNECTION_STR = os.getenv("DB_CONNECTION_STR")
CONNECTION = create_engine(DB_CONNECTION_STR) if DB_CONNECTION_STR else None


def create_master_table_from_sqlserver(
    schema_name: str, table_name: str
) -> pd.DataFrame:
    if not CONNECTION:
        logger.error("DB_CONNECTION_STR variable not setted.")
        return None

    conn = None
    try:
        conn = CONNECTION.connect()
        logger.info("connection is succed")
        sql_query = text(f"SELECT * FROM {schema_name}.{table_name}")

        df_from_db = pd.read_sql(sql_query, conn)

        return df_from_db

    except Exception as e:
        logger.error(e)
        logger.error(traceback.format_exc())

    finally:
        if conn is not None:
            conn.close()
            logger.info("DB Connection is closed")


if __name__ == "__main__":
    schema = "sumiyasui_machi_recommender"
    table = "prefecture_master"

    print(f"'{schema}.{table}' 테이블을 읽어옵니다...")

    # 2. 위에서 정의한 함수를 호출합니다.
    master_df = create_master_table_from_sqlserver(schema, table)

    # 3. 결과를 확인합니다.
    if master_df is not None:
        print("데이터 로딩 성공! 상위 5개 행:")
        print(master_df.head())
    else:
        print("데이터 로딩에 실패했습니다. 로그를 확인하세요.")
