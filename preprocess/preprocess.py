import re
import unicodedata
from datetime import datetime

import jageocoder
import numpy as np
import pandas as pd
from jp_pref.prefecture import code2name, name2code

pd.options.mode.copy_on_write = True


def get_inside_par(s: str) -> str:
    regex = r"（.+\）"
    return re.search(regex, s).group().strip("（）")


def add_datetime_tz(data):
    # title_detailの前半と後半を分離する
    data[["content", "incident_date"]] = data["title_detail"].str.split(
        "　", expand=True
    )

    # incident_dateの[解決]を消す
    data["incident_date"] = data["incident_date"].apply(
        lambda x: x.replace("［解決］", "")
    )

    # 日付がないレコードを捨てる
    data = data[data["incident_date"].apply(lambda s: "日" in s)]

    # incident_dateに含まれる「からX月Y日」を削除
    data.loc[:, "incident_date"] = data["incident_date"].apply(
        lambda s: re.sub(r"から.*", "", s)
    )

    # タイムゾーン取得
    def get_tz(s):
        regex = r"(?<=日)(.*)"
        return re.search(regex, s).group()

    data["tz"] = data["incident_date"].apply(get_tz)

    # incident_dateから日付を抽出
    def get_date(s):
        regex = r".+日"
        return re.search(regex, s).group()

    data["incident_date"] = (
        data["incident_date"]
        .apply(lambda s: get_date(s))
        .apply(lambda s: unicodedata.normalize("NFKC", s))
    )

    # date列、incident_date列をdatetimeに
    data["incident_date"] = pd.to_datetime(data["incident_date"], format="%m月%d日")
    data["date"] = pd.to_datetime(data["date"], format="%Y/%m/%d")

    def get_year(article_date: datetime, incident_date: datetime) -> datetime:
        if int(incident_date.month) == 1 and int(incident_date.month) == 12:
            new_incident_date = incident_date.replace(year=article_date.year + 1)
        else:
            new_incident_date = incident_date.replace(year=article_date.year)
        return new_incident_date

    data["incident_date"] = data.apply(
        lambda row: get_year(row.date, row.incident_date), axis=1
    )

    return data


### 住所の加工


def add_address(data):

    # 県名を取得
    data["prefecture"] = (
        data["content"].apply(get_inside_par).apply(lambda s: code2name(name2code(s)))
    )

    # contentから県名より下位の住所取得
    def get_address_post(s):
        s = s.split("で")[0]
        res = re.sub(r"（.+）", "", s)
        return res

    data["address_post"] = data["content"].apply(get_address_post)

    data["address"] = data["prefecture"] + data["address_post"]

    return data


# 事件の内容
def add_incident(data):
    data["incident"] = data["title"].apply(get_inside_par)
    data.rename(columns={"date": "article_date"}, inplace=True)
    data["animal"] = data["incident"].apply(
        lambda s: True if ("出没" in s or "脱走" in s) else False
    )
    return data


def get_coordinate(s):
    """地名に対して経度と緯度を返す"""
    res = jageocoder.search(s)
    if len(res) > 0:
        lon = res["candidates"][0]["x"]
        lat = res["candidates"][0]["y"]
    else:
        lon, lat = np.nan, np.nan
    return lon, lat


def add_coordinate(data):
    """データフレームのaddress列を参照してlon, lat列を追加"""
    data[["lon", "lat"]] = data.apply(
        lambda r: get_coordinate(r["address"]), axis=1, result_type="expand"
    )
    return data


data = pd.read_csv("./output.csv", encoding="utf_8")
data = add_datetime_tz(data)
data = add_address(data)
data = add_incident(data)
jageocoder.init()
data = add_coordinate(data)
data.to_csv("./data_processed_dev.csv", index=False)
