import streamlit as st
import joblib

# モデル読み込み
model_g = joblib.load("model_g.pkl")
model_r = joblib.load("model_r.pkl")

st.title("🎰 スロットAI予測アプリ")
st.write("現在の台の状態を入力して、次の当たりG数と連チャン数を予測します。")

# 選択肢用マップ
店舗マップ = {'梅坪': 0, '豊田': 1, '安城': 2}
台マップ = {'北斗の拳': 0, 'バジリスク絆2': 1, '番長ZERO': 2}

with st.form("predict_form"):
    st.subheader("📝 台情報の入力")

    col1, col2 = st.columns(2)

    with col1:
        店舗選択 = st.selectbox("店舗", list(店舗マップ.keys()))
        台選択 = st.selectbox("台の種類", list(台マップ.keys()))
        総回転数 = st.text_input("総回転数（例: 3500）")
        現在G = st.text_input("現在のゲーム数（例: 200）")
        差枚 = st.text_input("差枚（例: -500）")

    with col2:
        前回当選G = st.text_input("前回の当選ゲーム数")
        平均当選G = st.text_input("平均当選ゲーム数")
        連チャン = st.text_input("3連以上の連チャン回数")
        駆け抜け = st.text_input("駆け抜け回数")
        当たり回数 = st.text_input("当たり回数")

    submitted = st.form_submit_button("🔮 予測する")

if submitted:
    def safe_int(value):
        try:
            return int(value)
        except:
            return 0

    店舗 = 店舗マップ[店舗選択]
    台の種類 = 台マップ[台選択]
    総回転数 = safe_int(総回転数)
    現在G = safe_int(現在G)
    前回当選G = safe_int(前回当選G)
    平均当選G = safe_int(平均当選G)
    差枚 = safe_int(差枚)
    連チャン = safe_int(連チャン)
    駆け抜け = safe_int(駆け抜け)
    当たり回数 = safe_int(当たり回数)

    input_data = [[店舗, 台の種類, 総回転数, 現在G, 前回当選G,
                   平均当選G, 差枚, 連チャン, 駆け抜け, 当たり回数]]

    pred_g = model_g.predict(input_data)[0]
    pred_r = model_r.predict(input_data)[0]

    st.success(f"🎯 次の当たりまでの予想G数: {pred_g:.0f}G")
    st.success(f"🔥 次の連チャン予想: {pred_r:.1f}連")
