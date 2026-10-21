"""統計ダッシュボードAPI（APIキー不要）から都道府県別データを取得してCSV化する。"""
import csv, json, sys, urllib.request, urllib.parse
from pathlib import Path

BASE = "https://dashboard.e-stat.go.jp/api/1.0/Json/"
ROOT = Path(__file__).resolve().parent.parent
RAW = ROOT / "data" / "raw"

PREFS = ["北海道","青森県","岩手県","宮城県","秋田県","山形県","福島県","茨城県","栃木県","群馬県","埼玉県","千葉県","東京都","神奈川県","新潟県","富山県","石川県","福井県","山梨県","長野県","岐阜県","静岡県","愛知県","三重県","滋賀県","京都府","大阪府","兵庫県","奈良県","和歌山県","鳥取県","島根県","岡山県","広島県","山口県","徳島県","香川県","愛媛県","高知県","福岡県","佐賀県","長崎県","熊本県","大分県","宮崎県","鹿児島県","沖縄県"]

def _get(endpoint, **params):
    url = BASE + endpoint + "?" + urllib.parse.urlencode({"Lang": "JP", **params})
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
    with urllib.request.urlopen(req, timeout=60) as r:
        return json.loads(r.read().decode("utf-8"))

def fetch_pref(code):
    """指標コード -> [{pref, year, value}]（都道府県・年次）"""
    d = _get("getData", IndicatorCode=code, RegionalRank=3, IsSeasonalAdjustment=1)
    objs = d["GET_STATS"]["STATISTICAL_DATA"]["DATA_INF"]["DATA_OBJ"]
    rows = []
    for o in objs:
        v = o["VALUE"]
        rc = int(v["@regionCode"][:2])
        if not 1 <= rc <= 47 or v["@time"][4:6] != "CY" or v["$"] in ("-", "", "…", "***"):
            continue
        rows.append({"pref": PREFS[rc - 1], "year": int(v["@time"][:4]), "value": float(v["$"])})
    return rows

def save(code, name):
    rows = fetch_pref(code)
    RAW.mkdir(parents=True, exist_ok=True)
    path = RAW / f"{name}.csv"
    with open(path, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=["pref", "year", "value"])
        w.writeheader(); w.writerows(rows)
    return path, len(rows)

if __name__ == "__main__":
    for arg in sys.argv[1:]:
        code, name = arg.split("=")
        print(save(code, name))
