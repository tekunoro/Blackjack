import streamlit as st
import random

# ページ全体のデザイン設定
st.set_page_config(page_title="VIPブラックジャック・ルーム", layout="centered")

# --- 高級カジノ風デザイン（CSS） ---
st.markdown("""
    <style>
    /* 深みのあるフェルトテーブルの質感をグラデーションで再現 */
    .stApp {
        background: radial-gradient(circle, #2e5d48 0%, #1a3026 100%);
    }
    
    /* 文字に高級感のある影を適用 */
    h1, h2, h3, p, span, div {
        color: #fdfdfd !important;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.5);
    }

    /* 獲得賞金表示のスタイル */
    [data-testid="stMetricValue"] {
        background: rgba(0,0,0,0.3);
        padding: 10px;
        border-radius: 10px;
        border: 1px solid #d4af37;
        color: #d4af37 !important;
    }

    /* ボタンのデザイン（ゴールド基調） */
    .stButton>button {
        width: 100%;
        background: linear-gradient(145deg, #b8860b, #8b4513);
        color: #ffffff !important;
        border: 2px solid #d4af37;
        border-radius: 5px;
        font-weight: bold;
        box-shadow: 0 4px 15px rgba(0,0,0,0.3);
    }
    .stButton>button:hover {
        color: #ffeb3b !important;
        border: 2px solid #ffffff;
    }
    
    /* カードに影をつけて立体感を出す */
    [data-testid="stImage"] {
        filter: drop-shadow(5px 5px 10px rgba(0,0,0,0.5));
    }
    </style>
    """, unsafe_allow_html=True)

# --- ゲームシステム ---
if "money" not in st.session_state: st.session_state.money = 0
if "status" not in st.session_state: st.session_state.status = "waiting"
if "p_hand" not in st.session_state: st.session_state.p_hand = []
if "d_hand" not in st.session_state: st.session_state.d_hand = []

def draw(): return random.randint(1, 13)

def score(hand):
    val = sum([min(10, c) if c > 1 else 11 for c in hand])
    aces = hand.count(1)
    while val > 21 and aces > 0: val -= 10; aces -= 1
    return val

# --- メイン画面 ---
st.title("⚜️ VIP ブラックジャック・ルーム")
st.metric("現在の獲得賞金", f"{st.session_state.money} 円")

if st.session_state.status == "waiting":
    st.write("### テーブルへようこそ。勝負を始めますか？")
    if st.button("チップを賭けてスタート"):
        st.session_state.p_hand = [draw(), draw()]
        st.session_state.d_hand = [draw(), draw()]
        st.session_state.status = "playing"
        st.rerun()

elif st.session_state.status == "playing":
    # ディーラー側
    st.write("#### ディーラーの手札")
    d_cols = st.columns(6)
    d_cols[0].image(f"image/{st.session_state.d_hand[0]}.png", width=100)
    d_cols[1].image("image/トランプ_裏.png", width=100)

    # プレイヤー側
    ps = score(st.session_state.p_hand)
    st.write(f"#### あなたの手札 (合計: {ps})")
    p_cols = st.columns(6)
    for i, c in enumerate(st.session_state.p_hand):
        p_cols[i].image(f"image/{c}.png", width=100)

    # 操作ボタン
    st.write("---")
    c1, c2, _ = st.columns([1,1,2])
    if c1.button("ヒット（もう1枚）"):
        st.session_state.p_hand.append(draw())
        if score(st.session_state.p_hand) > 21:
            st.session_state.status = "result"; st.session_state.money -= 10
        st.rerun()
    if c2.button("スタンド（勝負）"):
        st.session_state.status = "result"
        while score(st.session_state.d_hand) < 17:
            st.session_state.d_hand.append(draw())
        ds, ps = score(st.session_state.d_hand), score(st.session_state.p_hand)
        if ds > 21 or ps > ds: st.session_state.money += 10
        elif ps < ds: st.session_state.money -= 10
        st.rerun()

elif st.session_state.status == "result":
    ds, ps = score(st.session_state.d_hand), score(st.session_state.p_hand)
    
    st.write(f"#### ディーラーの最終結果: {ds}")
    dc = st.columns(6)
    for i, c in enumerate(st.session_state.d_hand): dc[i].image(f"image/{c}.png", width=100)

    st.write(f"#### あなたの最終結果: {ps}")
    pc = st.columns(6)
    for i, c in enumerate(st.session_state.p_hand): pc[i].image(f"image/{c}.png", width=100)

    st.write("---")
    if ps > 21: st.error("💥 バースト！あなたの負けです（-10円）")
    elif ds > 21 or ps > ds: st.success("🏆 おめでとうございます！あなたの勝ちです（+10円）")
    elif ps < ds: st.error("💀 ディーラーの勝ちです（-10円）")
    else: st.warning("⚖️ 引き分け（プッシュ）です")

    if st.button("次のゲームへ"):
        st.session_state.status = "waiting"
        st.rerun()
