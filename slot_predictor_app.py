import streamlit as st
import joblib
import matplotlib.pyplot as plt

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

    店舗選択 = st.selectbox("店舗", list(店舗マップ.keys()))
    台選択 = st.selectbox("台の種類", list(台マップ.keys()))
    総回転数 = st.number_input("総回転数", min_value=0)
    現在G = st.number_input("現在のゲーム数", min_value=0)
    前回当選G = st.number_input("前回の当選ゲーム数", min_value=0)
    平均当選G = st.number_input("平均当選ゲーム数", min_value=0)
    差枚 = st.number_input("差枚", min_value=-5000, max_value=5000)
    連チャン = st.number_input("3連以上の連チャン回数", min_value=0)
    駆け抜け = st.number_input("駆け抜け回数", min_value=0)
    当たり回数 = st.number_input("当たり回数", min_value=0)

    submitted = st.form_submit_button("🔮 予測する")

if submitted:
    # 入力を数値に変換
    店舗 = 店舗マップ[店舗選択]
    台の種類 = 台マップ[台選択]

    # モデル入力
    input_data = [[店舗, 台の種類, 総回転数, 現在G, 前回当選G,
                   平均当選G, 差枚, 連チャン, 駆け抜け, 当たり回数]]

    # 予測
    pred_g = model_g.predict(input_data)[0]
    pred_r = model_r.predict(input_data)[0]

    # 結果表示
    st.success(f"🎯 次の当たりまでの予想G数: {pred_g:.0f}G")
    st.success(f"🔥 次の連チャン予想: {pred_r:.1f}連")

    # グラフ表示
    fig, ax = plt.subplots()
    ax.bar(['当たりG数', '連チャン数'], [pred_g, pred_r], color=['skyblue', 'salmon'])
    ax.set_ylabel('予測値')
    ax.set_title('予測結果の可視化')
    st.pyplot(fig)
