import streamlit as st
import random

# ページの設定
st.set_page_config(page_title="本格ブラックジャック", layout="centered")

# カスタムCSSで背景をカジノ風の緑に
st.markdown("""
    <style>
    .stApp {
        background-color: #2f4f4f;
    }
    h1, h2, h3, p {
        color: white !important;
    }
    </style>
    """, unsafe_allow_html=True)

st.title("🃏 本格ブラックジャック")

# --- データ管理（セッションステート） ---
if "money" not in st.session_state:
    st.session_state.money = 0  # 獲得賞金
if "game_status" not in st.session_state:
    st.session_state.game_status = "waiting"  # waiting, playing, result
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
        if card > 10:
            score += 10
        elif card == 1:
            aces += 1
            score += 11
        else:
            score += card
    while score > 21 and aces > 0:
        score -= 10
        aces -= 1
    return score

# --- メインロジック ---
st.sidebar.metric("現在の獲得賞金", f"{st.session_state.money} 円")

if st.session_state.game_status == "waiting":
    if st.button("ゲームスタート", key="start"):
        st.session_state.player_hand = [draw_card(), draw_card()]
        st.session_state.dealer_hand = [draw_card(), draw_card()]
        st.session_state.game_status = "playing"
        st.rerun()

elif st.session_state.game_status == "playing":
    p_score = get_score(st.session_state.player_hand)

    # ディーラーの表示
    st.subheader("ディーラーのカード")
    cols = st.columns(5)
    cols[0].image(f"image/{st.session_state.dealer_hand[0]}.png", width=100)
    cols[1].image("image/トランプ_裏.png", width=100)

    # プレイヤーの表示
    st.subheader(f"あなたのカード (合計: {p_score})")
    cols = st.columns(5)
    for i, card in enumerate(st.session_state.player_hand):
        cols[i].image(f"image/{card}.png", width=100)

    # 操作ボタン
    col1, col2 = st.columns(2)
    if col1.button("ヒット"):
        st.session_state.player_hand.append(draw_card())
        if get_score(st.session_state.player_hand) > 21:
            st.session_state.game_status = "result"
            st.session_state.money -= 10
        st.rerun()

    if col2.button("スタンド"):
        st.session_state.game_status = "result"
        # ディーラーが17以上になるまで引く
        while get_score(st.session_state.dealer_hand) < 17:
            st.session_state.dealer_hand.append(draw_card())
        
        # 勝敗判定と賞金の計算
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

    # 全カード公開表示
    st.subheader(f"ディーラーの合計: {d_score}")
    cols = st.columns(5)
    for i, card in enumerate(st.session_state.dealer_hand):
        cols[i].image(f"image/{card}.png", width=100)

    st.subheader(f"あなたの合計: {p_score}")
    cols = st.columns(5)
    for i, card in enumerate(st.session_state.player_hand):
        cols[i].image(f"image/{card}.png", width=100)

    # 結果メッセージ
    if p_score > 21:
        st.error("バーストしました！あなたの負けです（-10円）")
    elif d_score > 21:
        st.success("ディーラーがバースト！あなたの勝ちです（+10円）")
    elif p_score > d_score:
        st.success("おめでとうございます！あなたの勝ちです（+10円）")
    elif p_score < d_score:
        st.error("残念！ディーラーの勝ちです（-10円）")
    else:
        st.warning("引き分けです")

    if st.button("もう一度プレイする"):
        st.session_state.game_status = "waiting"
        st.rerun()
