import streamlit as st
import random

# ページの設定：タイトルとレイアウト
st.set_page_config(page_title="本格ブラックジャック", layout="centered")

# --- デザイン調整（CSS） ---
# どんな背景モードでも文字が見えるようにし、テーブルを緑色に固定します
st.markdown("""
    <style>
    /* アプリ全体の背景をカジノグリーンに */
    .stApp {
        background-color: #1e3d2f;
    }
    /* すべての文字を白に固定し、縁取りをつけて読みやすくする */
    h1, h2, h3, p, span, div {
        color: #ffffff !important;
        text-shadow: 1px 1px 2px #000000;
    }
    /* ボタンのスタイル調整 */
    .stButton>button {
        width: 100%;
        border-radius: 10px;
        height: 3em;
        background-color: #2e5d48;
        color: white !important;
        border: 1px solid #ffffff;
    }
    .stButton>button:hover {
        background-color: #3e7d61;
        border: 1px solid #ffeb3b;
    }
    </style>
    """, unsafe_allow_html=True)

st.title("🃏 本格ブラックジャック")

# --- データ管理（セッションステート） ---
if "money" not in st.session_state:
    st.session_state.money = 0
if "game_status" not in st.session_state:
    st.session_state.game_status = "waiting"
if "player_hand" not in st.session_state:
    st.session_state.player_hand = []
if "dealer_hand" not in st.session_state:
    st.session_state.dealer_hand = []

# --- 便利関数 ---
def draw_card():
    return random.randint(1, 13)

def get_score(hand):
    score = 0
    aces = 0
    for card in hand:
        if card > 10: score += 10
        elif card == 1:
            aces += 1
            score += 11
        else: score += card
    while score > 21 and aces > 0:
        score -= 10
        aces -= 1
    return score

# --- 画面構成 ---
# 現在の賞金を最上部に表示
st.subheader(f"💰 獲得賞金合計: {st.session_state.money} 円")
st.write("---")

if st.session_state.game_status == "waiting":
    col_start, _ = st.columns([1, 2])
    if col_start.button("ゲームスタート"):
        st.session_state.player_hand = [draw_card(), draw_card()]
        st.session_state.dealer_hand = [draw_card(), draw_card()]
        st.session_state.game_status = "playing"
        st.rerun()

elif st.session_state.game_status == "playing":
    p_score = get_score(st.session_state.player_hand)

    # ディーラー
    st.write("### ディーラーのカード")
    d_cols = st.columns(6)
    d_cols[0].image(f"image/{st.session_state.dealer_hand[0]}.png", width=90)
    d_cols[1].image("image/トランプ_裏.png", width=90)

    # プレイヤー
    st.write(f"### あなたのカード (合計: {p_score})")
    p_cols = st.columns(6)
    for i, card in enumerate(st.session_state.player_hand):
        p_cols[i].image(f"image/{card}.png", width=90)

    # 操作ボタン
    st.write("")
    col_h, col_s, _ = st.columns([1, 1, 2])
    if col_h.button("ヒット"):
        st.session_state.player_hand.append(draw_card())
        if get_score(st.session_state.player_hand) > 21:
            st.session_state.game_status = "result"
            st.session_state.money -= 10
        st.rerun()

    if col_s.button("スタンド"):
        st.session_state.game_status = "result"
        while get_score(st.session_state.dealer_hand) < 17:
            st.session_state.dealer_hand.append(draw_card())
        
        p_final = get_score(st.session_state.player_hand)
        d_final = get_score(st.session_state.dealer_hand)
        
        if d_final > 21 or p_final > d_final:
            st.session_state.money += 10
        elif p_final < d_final:
            st.session_state.money -= 10
        st.rerun()

elif st.session_state.game_status == "result":
    p_score = get_score(st.session_state.player_hand)
    d_score = get_score(st.session_state.dealer_hand)

    # ディーラー全公開
    st.write(f"### ディーラーの合計: {d_score}")
    d_cols = st.columns(6)
    for i, card in enumerate(st.session_state.dealer_hand):
        d_cols[i].image(f"image/{card}.png", width=90)

    # プレイヤー
    st.write(f"### あなたの合計: {p_score}")
    p_cols = st.columns(6)
    for i, card in enumerate(st.session_state.player_hand):
        p_cols[i].image(f"image/{card}.png", width=90)

    # 結果判定
    st.write("---")
    if p_score > 21:
        st.error("❌ バースト！負けです（-10円）")
    elif d_score > 21:
        st.success("✨ ディーラーがバースト！勝ちです（+10円）")
    elif p_score > d_score:
        st.success("✨ あなたの勝ちです！（+10円）")
    elif p_score < d_score:
        st.error("❌ ディーラーの勝ちです（-10円）")
    else:
        st.info("🤝 引き分けです（±0円）")

    if st.button("もう一度プレイする"):
        st.session_state.game_status = "waiting"
        st.rerun()
