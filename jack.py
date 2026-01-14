import streamlit as st
import random

# ページ全体のデザイン設定
st.set_page_config(page_title="VIP Blackjack Room", layout="centered")

# --- 高級カジノ風デザイン（最新CSS） ---
st.markdown("""
    <style>
    /* 深みのあるフェルトテーブルの質感をグラデーションで再現 */
    .stApp {
        background: radial-gradient(circle, #2e5d48 0%, #1a3026 100%);
    }
    
    /* 文字に高級感のあるゴールドとホワイトの影を適用 */
    h1, h2, h3, p, span, div {
        color: #fdfdfd !important;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.5);
        font-family: 'Georgia', serif;
    }

    /* メトリック（賞金表示）をカード状にデザイン */
    [data-testid="stMetricValue"] {
        background: rgba(0,0,0,0.3);
        padding: 10px;
        border-radius: 10px;
        border: 1px solid #d4af37; /* ゴールドの縁取り */
        color: #d4af37 !important;
    }

    /* ボタンを光沢のある高級仕様に */
    .stButton>button {
        background: linear-gradient(145deg, #b8860b, #8b4513);
        color: gold !important;
        border: 2px solid #d4af37;
        border-radius: 5px;
        font-weight: bold;
        box-shadow: 0 4px 15px rgba(0,0,0,0.3);
        transition: all 0.3s;
    }
    .stButton>button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(212,175,55,0.4);
        border: 2px solid #fff;
    }
    
    /* カードの背景に影をつけて浮かび上がらせる */
    [data-testid="stImage"] {
        filter: drop-shadow(5px 5px 10px rgba(0,0,0,0.5));
        border-radius: 5px;
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
st.title("⚜️ VIP BLACKJACK ROOM")
st.metric("TOTAL BANK", f"{st.session_state.money} JPY")

if st.session_state.status == "waiting":
    st.write("### テーブルへようこそ。勝負を始めますか？")
    if st.button("PLACE BET & START"):
        st.session_state.p_hand = [draw(), draw()]
        st.session_state.d_hand = [draw(), draw()]
        st.session_state.status = "playing"
        st.rerun()

elif st.session_state.status == "playing":
    # ディーラー側
    st.write("#### DEALER'S HAND")
    d_cols = st.columns(6)
    d_cols[0].image(f"image/{st.session_state.d_hand[0]}.png", width=100)
    d_cols[1].image("image/トランプ_裏.png", width=100)

    # プレイヤー側
    ps = score(st.session_state.p_hand)
    st.write(f"#### YOUR HAND (Score: {ps})")
    p_cols = st.columns(6)
    for i, c in enumerate(st.session_state.p_hand):
        p_cols[i].image(f"image/{c}.png", width=100)

    # アクション
    st.write("---")
    c1, c2, _ = st.columns([1,1,2])
    if c1.button("HIT"):
        st.session_state.p_hand.append(draw())
        if score(st.session_state.p_hand) > 21:
            st.session_state.status = "result"; st.session_state.money -= 10
        st.rerun()
    if c2.button("STAND"):
        st.session_state.status = "result"
        while score(st.session_state.d_hand) < 17:
            st.session_state.d_hand.append(draw())
        ds, ps = score(st.session_state.d_hand), score(st.session_state.p_hand)
        if ds > 21 or ps > ds: st.session_state.money += 10
        elif ps < ds: st.session_state.money -= 10
        st.rerun()

elif st.session_state.status == "result":
    ds, ps = score(st.session_state.d_hand), score(st.session_state.p_hand)
    
    st.write(f"#### DEALER (Final: {ds})")
    dc = st.columns(6)
    for i, c in enumerate(st.session_state.d_hand): dc[i].image(f"image/{c}.png", width=100)

    st.write(f"#### YOU (Final: {ps})")
    pc = st.columns(6)
    for i, c in enumerate(st.session_state.p_hand): pc[i].image(f"image/{c}.png", width=100)

    st.write("---")
    if ps > 21: st.error("💥 BUST! You Lost 10 JPY")
    elif ds > 21 or ps > ds: st.success("🏆 WIN! You Gained 10 JPY")
    elif ps < ds: st.error("💀 DEALER WINS! You Lost 10 JPY")
    else: st.warning("⚖️ PUSH (Draw)")

    if st.button("PLAY NEXT HAND"):
        st.session_state.status = "waiting"
        st.rerun()
