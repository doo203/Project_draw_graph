import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from matplotlib.dates import DateFormatter, MinuteLocator
from datetime import datetime, timedelta

# ===== 한글 폰트 설정 =====
plt.rcParams['font.family'] = 'Malgun Gothic'  # 맑은 고딕
plt.rcParams['axes.unicode_minus'] = False  # 마이너스 기호 깨짐 방지
# =========================

# 저장 경로 설정
save_dir = r"C:\Users\h514790\Desktop\draw_graph\graph"

# today 변수 정의 = 파일명 때문에 지정
today = datetime.now()
date_folder = today.strftime("%y%m%d")
print(f"Processing date folder: {date_folder}")

# 공통 설정 - 시작과 끝 날짜가 모두 같은 경우
start_date_str = "2026-01-09"
end_date_str = today.strftime("%Y-%m-%d")

start_date = pd.to_datetime(start_date_str)
end_date = pd.to_datetime(end_date_str)
runtime_days = (end_date - start_date).days

# 겹침 방지용: start/end 근처 몇 분 이내 tick 제거
TOL_MIN = 13  # 13분 이내 겹치면 제거
tol_days = TOL_MIN / (24 * 60)


#================================#
#--- 샴시엘 - O2 graph (Param4) ---
print("Processing O2 logging...")
file_path = rf"E:\{date_folder}\packet_log_000_O2.csv"
print(f"Reading: {file_path}")
df = pd.read_csv(file_path)

"""
start_date_str = "2026-01-09"
end_date_str = today.strftime("%Y-%m-%d")

start_date = pd.to_datetime(start_date_str)
end_date = pd.to_datetime(end_date_str)
runtime_days = (end_date - start_date).days
"""
# --- 전처리 ---
df["date"] = df["date"].astype(str).str.strip().str.lstrip("'")
df["time"] = df["time"].astype(str).str.strip().str.lstrip("'")
df["time"] = df["time"].str.replace(",", "", regex=False)

t = df["time"].str.split(":", expand=True)
df["time_norm"] = (
    t[0].str.zfill(2) + ":" +
    t[1].str.zfill(2) + ":" +
    t[2].str.zfill(2)
)

df["datetime"] = pd.to_datetime(df["date"] + " " + df["time_norm"], errors="coerce")
df["Param4"] = pd.to_numeric(df["Param4"], errors="coerce")
df = df.dropna(subset=["datetime", "Param4"]).sort_values("datetime")

# --- 표시 개수 ---
N = 25
tail_df = df.tail(N)

# --- 그래프 ---
fig, ax = plt.subplots(figsize=(11, 5))
ax.plot(df["datetime"], df["Param4"])

# ===== 로깅 시작/끝 + x축 범위(약간 마진) =====
start_dt = df["datetime"].iloc[0]
end_dt   = df["datetime"].iloc[-1]
pad = pd.Timedelta(minutes=2)  # 좌우 여백(분)
ax.set_xlim(start_dt - pad, end_dt + pad)
# ============================================

ax.set_title(
    f"샴시엘 NI 9203 O2 "
    f"FW 1.4.0 Runtime {runtime_days}일차 + ver 3.40.10",
    fontsize=16,
    fontweight='bold'
)

# X축 시간 포맷
ax.xaxis.set_major_locator(MinuteLocator(interval=30))
ax.xaxis.set_major_formatter(DateFormatter('%H:%M'))
ax.tick_params(axis="x", rotation=90)
ax.set_ylim(0, 25)

# ===== start/end를 x축 tick에 포함 + 겹치는 tick 제거 =====
fig.canvas.draw()
start_num = mdates.date2num(start_dt)
end_num   = mdates.date2num(end_dt)

ticks = ax.get_xticks()
ticks = ticks[(np.abs(ticks - start_num) > tol_days) & (np.abs(ticks - end_num) > tol_days)]
ticks = np.unique(np.sort(np.append(ticks, [start_num, end_num])))
ax.set_xticks(ticks)

# --- 오른쪽 텍스트 구성 ---
lines = [f"Date: {end_date_str}", "-" * 18]
lines += [f"{row['time_norm']}  {row['Param4']:.3f}" for _, row in tail_df.iterrows()]
text = "\n".join(lines)

ax.text(
    1.02, 0.5,
    text,
    transform=ax.transAxes,
    fontsize=9,
    va="center",
    family="monospace"
)

plt.tight_layout()
save_path = f"{save_dir}\\O2_logging_Param4.png"
plt.savefig(save_path, dpi=300, bbox_inches='tight')
print(f"Saved: {save_path}")
plt.close()

print(f"End date: {end_date_str}")
print(f"Runtime: {runtime_days}일차\n")


#================================#
#--- 샴시엘 - LEL (Param2) ---
print("Processing LEL logging...")
file_path = rf"E:\{date_folder}\packet_log_000_LEL.csv"
print(f"Reading: {file_path}")
df = pd.read_csv(file_path)
"""
start_date_str = "2026-01-09"
end_date_str = today.strftime("%Y-%m-%d")

start_date = pd.to_datetime(start_date_str)
end_date = pd.to_datetime(end_date_str)
runtime_days = (end_date - start_date).days
"""
# --- 전처리 ---
df["date"] = df["date"].astype(str).str.strip().str.lstrip("'")
df["time"] = df["time"].astype(str).str.strip().str.lstrip("'")
df["time"] = df["time"].str.replace(",", "", regex=False)

t = df["time"].str.split(":", expand=True)
df["time_norm"] = (
    t[0].str.zfill(2) + ":" +
    t[1].str.zfill(2) + ":" +
    t[2].str.zfill(2)
)

df["datetime"] = pd.to_datetime(df["date"] + " " + df["time_norm"], errors="coerce")
df["Param2"] = pd.to_numeric(df["Param2"], errors="coerce")
df = df.dropna(subset=["datetime", "Param2"]).sort_values("datetime")

# --- 표시 개수 ---
N = 25
tail_df = df.tail(N)

# --- 그래프 ---
fig, ax = plt.subplots(figsize=(11, 5))
ax.plot(df["datetime"], df["Param2"])

# ===== 로깅 시작/끝 + x축 범위(약간 마진) =====
start_dt = df["datetime"].iloc[0]
end_dt   = df["datetime"].iloc[-1]
pad = pd.Timedelta(minutes=2)
ax.set_xlim(start_dt - pad, end_dt + pad)
# ============================================

ax.set_title(
    f"샴시엘 NI 9227 LEL "
    f"FW 1.4.0 Runtime {runtime_days}일차 + ver 3.40.10",
    fontsize=16,
    fontweight='bold'
)

# X축 시간 포맷
ax.xaxis.set_major_locator(MinuteLocator(interval=30))
ax.xaxis.set_major_formatter(DateFormatter('%H:%M'))
ax.tick_params(axis="x", rotation=90)
ax.set_ylim(0, 25)

# ===== start/end를 x축 tick에 포함 + 겹치는 tick 제거 =====
fig.canvas.draw()
start_num = mdates.date2num(start_dt)
end_num   = mdates.date2num(end_dt)

ticks = ax.get_xticks()
ticks = ticks[(np.abs(ticks - start_num) > tol_days) & (np.abs(ticks - end_num) > tol_days)]
ticks = np.unique(np.sort(np.append(ticks, [start_num, end_num])))
ax.set_xticks(ticks)


# --- 오른쪽 텍스트 구성 ---
lines = [f"Date: {end_date_str}", "-" * 18]
lines += [f"{row['time_norm']}  {row['Param2']:.3f}" for _, row in tail_df.iterrows()]
text = "\n".join(lines)

ax.text(
    1.02, 0.5,
    text,
    transform=ax.transAxes,
    fontsize=9,
    va="center",
    family="monospace"
)

plt.tight_layout()
save_path = f"{save_dir}\\LEL_logging_Param2.png"
plt.savefig(save_path, dpi=300, bbox_inches='tight')
print(f"Saved: {save_path}")
plt.close()

print(f"End date: {end_date_str}")
print(f"Runtime: {runtime_days}일차\n")


#================================#
#--- 샴시엘 - LEL 200mA (Param2) ---
print("Processing LEL 200mA logging...")
file_path = rf"E:\{date_folder}\packet_log_000_200mA.csv"
print(f"Reading: {file_path}")
df = pd.read_csv(file_path)
"""
start_date_str = "2026-01-09"
end_date_str = today.strftime("%Y-%m-%d")

start_date = pd.to_datetime(start_date_str)
end_date = pd.to_datetime(end_date_str)
runtime_days = (end_date - start_date).days
"""
# --- 전처리 ---
df["date"] = df["date"].astype(str).str.strip().str.lstrip("'")
df["time"] = df["time"].astype(str).str.strip().str.lstrip("'")
df["time"] = df["time"].str.replace(",", "", regex=False)

t = df["time"].str.split(":", expand=True)
df["time_norm"] = (
    t[0].str.zfill(2) + ":" +
    t[1].str.zfill(2) + ":" +
    t[2].str.zfill(2)
)

df["datetime"] = pd.to_datetime(df["date"] + " " + df["time_norm"], errors="coerce")
df["Param2"] = pd.to_numeric(df["Param2"], errors="coerce")
df = df.dropna(subset=["datetime", "Param2"]).sort_values("datetime")

# --- 표시 개수 ---
N = 25
tail_df = df.tail(N)

# --- 그래프 ---
fig, ax = plt.subplots(figsize=(11, 5))
ax.plot(df["datetime"], df["Param2"])

# ===== 로깅 시작/끝 + x축 범위(약간 마진) =====
start_dt = df["datetime"].iloc[0]
end_dt   = df["datetime"].iloc[-1]
pad = pd.Timedelta(minutes=2)
ax.set_xlim(start_dt - pad, end_dt + pad)
# ============================================

ax.set_title(
    f"샴시엘 NI 9227 LEL 200mA "
    f"FW 1.4.0 Runtime {runtime_days}일차 + ver 3.40.10",
    fontsize=16,
    fontweight='bold'
)

# X축 시간 포맷
ax.xaxis.set_major_locator(MinuteLocator(interval=30))
ax.xaxis.set_major_formatter(DateFormatter('%H:%M'))
ax.tick_params(axis="x", rotation=90)
ax.set_ylim(0, 250)

# ===== start/end를 x축 tick에 포함 + 겹치는 tick 제거 =====
fig.canvas.draw()
start_num = mdates.date2num(start_dt)
end_num   = mdates.date2num(end_dt)

ticks = ax.get_xticks()
ticks = ticks[(np.abs(ticks - start_num) > tol_days) & (np.abs(ticks - end_num) > tol_days)]
ticks = np.unique(np.sort(np.append(ticks, [start_num, end_num])))
ax.set_xticks(ticks)

# --- 오른쪽 텍스트 구성 ---
lines = [f"Date: {end_date_str}", "-" * 18]
lines += [f"{row['time_norm']}  {row['Param2']:.3f}" for _, row in tail_df.iterrows()]
text = "\n".join(lines)

ax.text(
    1.02, 0.5,
    text,
    transform=ax.transAxes,
    fontsize=9,
    va="center",
    family="monospace"
)

plt.tight_layout()
save_path = f"{save_dir}\\LEL_200mA_Param2.png"
plt.savefig(save_path, dpi=300, bbox_inches='tight')
print(f"Saved: {save_path}")
plt.close()

print(f"End date: {end_date_str}")
print(f"Runtime: {runtime_days}일차\n")

print("\n=== All plots saved successfully! ===")
