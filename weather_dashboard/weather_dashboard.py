import requests
import streamlit as st
import pandas as pd

# -----------------------------
# App 標題
# -----------------------------
st.title("台灣氣象資料 Dashboard")

# -----------------------------
# 選城市
# -----------------------------
LOCATION = st.selectbox("選擇城市", ['臺北市', '臺中市', '高雄市'])


API_KEY = "CWA-D099A3FC-C644-4A96-AFF0-365F65BD3B23"

# -----------------------------
# API URL
# -----------------------------
url = f"https://opendata.cwa.gov.tw/api/v1/rest/datastore/F-C0032-001?Authorization={API_KEY}&locationName={LOCATION}"

# -----------------------------
# 抓取資料（暫時忽略 SSL 驗證）
# -----------------------------
try:
    res = requests.get(url, verify=False)
    data = res.json()
except requests.exceptions.SSLError:
    st.error("SSL 驗證失敗，請檢查網路或部署環境")
    st.stop()
except Exception as e:
    st.error(f"取得資料失敗: {e}")
    st.stop()

# -----------------------------
# 顯示資料
# -----------------------------
if data['records']['location']:
    location = data["records"]["location"][0]
    st.subheader(f"{location['locationName']} 36小時預報")

    # 建立表格資料
    weather_dict = {}
    for element in location["weatherElement"]:
        name = element["elementName"]
        times = [t["startTime"] for t in element["time"]]
        values = [t["parameter"]["parameterName"] for t in element["time"]]
        weather_dict[name] = values
        # 顯示即時數值（第一筆）
        st.write(f"{name}: {values[0]}")

    # 折線圖：以最高溫、最低溫呈現
    if "MaxT" in weather_dict and "MinT" in weather_dict:
        df_temp = pd.DataFrame({
            "時間": times,
            "最高溫": list(map(int, weather_dict["MaxT"])),
            "最低溫": list(map(int, weather_dict["MinT"]))
        })
        df_temp = df_temp.set_index("時間")
        st.line_chart(df_temp)

else:
    st.warning("查無資料，請確認城市名稱是否正確。")
