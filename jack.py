import streamlit as st
import random

# --- データの保存場所（セッションステート）の設定 ---
if "game_started" not in st.session_state:
    st.session_state.game_started = False
    st.session_state.player_cards = []
    st.session_state.dealer_cards = []
    st.session_state.score = 0

# --- 関数定義：カードの数値を計算 ---
def calculate_total(cards):
    total = sum([min(10, c) if c > 1 else 11 for c in cards])
    # エースの調整（21を超えたら11を1に読み替える）
    num_aces = cards.count(1)
    while total > 21 and num_aces > 0:
        total -= 10
        num_aces -= 1
    return total

# --- 画面表示 ---
st.title("🃏 ブラックジャック Online")
st.write(f"現在の賞金: {st.session_state.score} 円")

# スタートボタン
if not st.session_state.game_started:
    if st.button("ゲームスタート"):
        st.session_state.player_cards = [random.randint(1, 13), random.randint(1, 13)]
        st.session_state.dealer_cards = [random.randint(1, 13), random.randint(1, 13)]
        st.session_state.game_started = True
        st.rerun()

# ゲーム進行中
if st.session_state.game_started:
    p_total = calculate_total(st.session_state.player_cards)
    
    # ディーラーの表示（最初は1枚隠す）
    st.subheader("ディーラーのカード")
    d_cols = st.columns(5)
    d_cols[0].image(f"image/{st.session_state.dealer_cards[0]}.png", width=100)
    d_cols[1].image("image/トランプ_裏.png", width=100) # 2枚目は裏

    # プレイヤーの表示
    st.subheader(f"あなたのカード (合計: {p_total})")
    p_cols = st.columns(5)
    for i, card in enumerate(st.session_state.player_cards):
        p_cols[i].image(f"image/{card}.png", width=100)

    # 操作ボタン
    if p_total <= 21:
        col_h, col_s = st.columns(2)
        if col_h.button("ヒット"):
            st.session_state.player_cards.append(random.randint(1, 13))
            st.rerun()
        
        if col_s.button("スタンド"):
            # ディーラーが17以上になるまで引く
            while calculate_total(st.session_state.dealer_cards) < 17:
                st.session_state.dealer_cards.append(random.randint(1, 13))
            
            # 判定ロジック（ここを完成させると遊べます！）
            d_total = calculate_total(st.session_state.dealer_cards)
            st.write(f"ディーラー合計: {d_total}")
            # ...判定後に st.session_state.game_started = False に戻す
    else:
        st.error("バースト！あなたの負けです。")
        if st.button("もう一回"):
            st.session_state.game_started = False
            st.rerun()
