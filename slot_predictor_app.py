import streamlit as st
import pandas as pd
import joblib
import os
import uuid
from datetime import datetime

# ファイル設定
LOG_FILE = "user_input_log.csv"

# モデル読み込み
model_g = joblib.load("model_g.pkl")
model_r = joblib.load("model_r.pkl")

st.title("🎰 スロットAI予測アプリ（結果追記機能付き）")

# カテゴリ変換用
店舗マップ = {'梅坪': 0, '豊田': 1, '安城': 2}
台マップ = {'北斗の拳': 0, 'バジリスク絆2': 1, '番長ZERO': 2}

# タブ分け
tab1, tab2 = st.tabs(["📊 台の入力・予測", "📝 結果を後から追記"])

# 入力補助
def safe_int(val):
    try:
        return int(val)
    except:
        return 0

with tab1:
    with st.form("predict_form"):
        st.subheader("📝 台情報の入力")

        col1, col2 = st.columns(2)
        with col1:
            店舗選択 = st.selectbox("店舗", list(店舗マップ.keys()))
            台選択 = st.selectbox("台の種類", list(台マップ.keys()))
            総回転数 = st.text_input("総回転数")
            現在G = st.text_input("現在のゲーム数")
            差枚 = st.text_input("差枚")

        with col2:
            前回当選G = st.text_input("前回の当選ゲーム数")
            平均当選G = st.text_input("平均当選ゲーム数")
            連チャン = st.text_input("3連以上の連チャン回数")
            駆け抜け = st.text_input("駆け抜け回数")
            当たり回数 = st.text_input("当たり回数")

        submitted = st.form_submit_button("🔮 予測する")

    if submitted:
        店舗 = 店舗マップ[店舗選択]
        台 = 台マップ[台選択]

        総回転数 = safe_int(総回転数)
        現在G = safe_int(現在G)
        前回当選G = safe_int(前回当選G)
        平均当選G = safe_int(平均当選G)
        差枚 = safe_int(差枚)
        連チャン = safe_int(連チャン)
        駆け抜け = safe_int(駆け抜け)
        当たり回数 = safe_int(当たり回数)

        input_data = [[店舗, 台, 総回転数, 現在G, 前回当選G,
                       平均当選G, 差枚, 連チャン, 駆け抜け, 当たり回数]]

        pred_g = model_g.predict(input_data)[0]
        pred_r = model_r.predict(input_data)[0]

        st.success(f"🎯 次の当たりまでの予想G数: {pred_g:.0f}G")
        st.success(f"🔥 次の連チャン予想: {pred_r:.1f}連")

        # 保存
        log_data = pd.DataFrame([{
            "ID": str(uuid.uuid4()),
            "日時": datetime.now().strftime("%Y-%m-%d %H:%M"),
            "店舗": 店舗選択,
            "台の種類": 台選択,
            "総回転数": 総回転数,
            "現在G": 現在G,
            "前回当選G": 前回当選G,
            "平均当選G": 平均当選G,
            "差枚": 差枚,
            "3連以上の連チャン数": 連チャン,
            "駆け抜け": 駆け抜け,
            "当たり回数": 当たり回数,
            "予測_当たりG": round(pred_g),
            "予測_連チャン数": round(pred_r, 1),
            "実際_当たりG": "",
            "実際_連チャン数": ""
        }])

        if os.path.exists(LOG_FILE):
            log_data.to_csv(LOG_FILE, mode="a", index=False, header=False)
        else:
            log_data.to_csv(LOG_FILE, index=False)

with tab2:
    st.subheader("📝 実際の当たり結果を追記")

    if os.path.exists(LOG_FILE):
        df = pd.read_csv(LOG_FILE)
        df_missing = df[df['実際_当たりG'] == ""]

        if df_missing.empty:
            st.info("✅ 追記待ちのデータはありません")
        else:
            選択ID = st.selectbox("対象の台を選択", df_missing['ID'])
            対象データ = df_missing[df_missing['ID'] == 選択ID].iloc[0]
            st.write(f"店舗: {対象データ['店舗']} / 台: {対象データ['台の種類']} / 入力日時: {対象データ['日時']}")

            実際G = st.number_input("実際の当たりG数", min_value=0)
            実際連 = st.number_input("実際の連チャン数", min_value=0)

            if st.button("✅ 結果を追記する"):
                df.loc[df['ID'] == 選択ID, '実際_当たりG'] = 実際G
                df.loc[df['ID'] == 選択ID, '実際_連チャン数'] = 実際連
                df.to_csv(LOG_FILE, index=False)
                st.success("追記完了！")
    else:
        st.warning("⚠ まだ入力データがありません。まずは予測からスタートしましょう！")
