"""記事001: 「雨が多い県」は雨量で見るか、日数で見るかで変わる"""
import pandas as pd
from estat_dashboard import PREFS
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
RAW = ROOT / "data" / "raw"
OUT = ROOT / "data" / "processed"
OUT.mkdir(parents=True, exist_ok=True)
Y0, Y1 = 2015, 2024

def avg(name):
    df = pd.read_csv(RAW / f"{name}.csv")
    df = df[(df.year >= Y0) & (df.year <= Y1)]
    n = df.groupby("pref").size()
    assert len(n) == 47 and n.min() >= Y1 - Y0, name  # 欠測は1年まで許容（記事で明記）
    return df.groupby("pref")["value"].mean()

df = pd.DataFrame({"rain_mm": avg("rain_mm"), "rain_days": avg("rain_days"), "sunshine_hours": avg("sunshine_hours")})
df["mm_per_rain_day"] = df.rain_mm / df.rain_days
for c in ["rain_mm", "rain_days", "sunshine_hours", "mm_per_rain_day"]:
    df[c + "_rank"] = df[c].rank(ascending=False, method="min").astype(int)
df = df.reindex(PREFS).round(1)  # JISコード順
df.to_csv(OUT / "a001_rain.csv", encoding="utf-8")
with open(OUT / "a001_summary.txt", "w", encoding="utf-8") as f:
    for c in ["rain_mm", "rain_days", "mm_per_rain_day", "sunshine_hours"]:
        s = df.sort_values(c, ascending=False)[c]
        f.write(f"== {c} top10\n{s.head(10).to_string()}\n-- bottom5\n{s.tail(5).to_string()}\n\n")
    f.write(f"corr rain_mm vs rain_days: {df.rain_mm.corr(df.rain_days):.2f}\n")
    f.write(f"corr rain_days vs sunshine: {df.rain_days.corr(df.sunshine_hours):.2f}\n")
    f.write(f"corr rain_mm vs sunshine: {df.rain_mm.corr(df.sunshine_hours):.2f}\n")
    df["gap"] = df.rain_mm_rank - df.rain_days_rank
    f.write("\n== 雨量順位と日数順位のギャップ（正=日数の方が上位）\n" + df.sort_values("gap")[["rain_mm","rain_mm_rank","rain_days","rain_days_rank","gap"]].to_string())

# サイト用JSON
SITE = ROOT / "src" / "data"
SITE.mkdir(parents=True, exist_ok=True)
df.drop(columns=["gap"]).rename_axis("pref").reset_index().to_json(SITE / "a001_rain.json", orient="records", force_ascii=False, indent=1)
