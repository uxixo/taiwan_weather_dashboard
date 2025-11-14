# weather_dashboard.py
import requests
import streamlit as st
import pandas as pd  

st.title("台灣氣象資料 Dashboard")

API_KEY = "CWA-D099A3FC-C644-4A96-AFF0-365F65BD3B23"

LOCATION = st.selectbox("選擇城市", ['臺北市', '臺中市', '高雄市'])

url = f"https://opendata.cwa.gov.tw/api/v1/rest/datastore/F-C0032-001?Authorization={API_KEY}&locationName={LOCATION}"

res = requests.get(url)
data = res.json()

if data['records']['location']:
    location = data["records"]["location"][0]
    st.subheader(f"{location['locationName']} 36小時預報")

    for element in location["weatherElement"]:
        name = element["elementName"]
        value = element["time"][0]["parameter"]["parameterName"]
        st.write(f"{name}: {value}")
else:
    st.warning("查無資料，請確認城市名稱是否正確。")

