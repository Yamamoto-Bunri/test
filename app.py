import streamlit as st
import pandas as pd
import os
import requests

# --- 設定 ---
# Googleフォームの送信先URL（後ほど作成しましょう）
FORM_URL = "https://docs.google.com/forms/d/e/XXXXX/formResponse"

st.set_page_config(page_title="英単語フラッシュカード", page_icon="📝")

# ユーザー入力
with st.sidebar:
    name = st.text_input("フルネームを入力")
    files = [f for f in os.listdir() if f.endswith('.csv')]
    unit = st.selectbox("Unit選択", files)
    shuffle = st.checkbox("シャッフルする")

if not name or not unit:
    st.info("名前を入力し、Unitを選択してください。")
    st.stop()

# データ読み込み
if 'df' not in st.session_state or st.session_state.get('last_unit') != unit:
    df = pd.read_csv(unit)
    if shuffle:
        df = df.sample(frac=1).reset_index(drop=True)
    st.session_state.df = df
    st.session_state.last_unit = unit
    st.session_state.idx = 0
    st.session_state.mastered = [False] * len(df)

# カード表示
df = st.session_state.df
idx = st.session_state.idx
row = df.iloc[idx]

st.progress((idx + 1) / len(df))
st.write(f"Word {idx + 1} / {len(df)}")

# カードデザイン
st.markdown(f"""
<div style="background-color: #e3f2fd; padding: 50px; border-radius: 20px; text-align: center; border: 3px solid #1e88e5;">
    <h1 style="color: #0d47a1; font-size: 60px;">{row['base_form']}</h1>
    <p style="color: #555;">({row['pos_in_context']})</p>
</div>
""", unsafe_allow_html=True)

if st.button("意味を表示"):
    st.info(f"**意味:** {row['meaning']}\n\n**その他:** {row['others']}\n\n**派生語:** {row['derivatives']}")
    if st.button("Mastered! ✅"):
        st.session_state.mastered[idx] = True
        st.success("マスターしました！")

# 移動ボタン
c1, c2 = st.columns(2)
with c1:
    if st.button("⬅️ PREV") and idx > 0:
        st.session_state.idx -= 1
        st.rerun()
with c2:
    if st.button("NEXT ➡️"):
        if idx < len(df) - 1:
            st.session_state.idx += 1
            st.rerun()
        else:
            # 終了処理
            m_count = sum(st.session_state.mastered)
            pct = int((m_count / len(df)) * 100)
            st.balloons()
            st.success(f"終了！達成率: {pct}% ({m_count}/{len(df)})")
            
            # 記録送信（Googleフォームへの自動送信）
            # ここにフォーム送信のコードを書く
            st.write("成績を記録しました。お疲れ様でした！")