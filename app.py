import streamlit as st
import random
import time

# =========================================================
# 페이지 설정
# =========================================================

st.set_page_config(
    page_title="⌨️ Typing Master",
    page_icon="⌨️",
    layout="centered"
)

# =========================================================
# 문장
# =========================================================

TEXTS = {
    "쉬움": [
        "hello world",
        "python is fun",
        "have a nice day",
        "i like coding",
        "streamlit is easy",
        "let us play a game",
        "practice makes perfect",
        "welcome to typing game",
        "coding is interesting",
        "keep going"
    ],

    "보통": [
        "Python is a powerful programming language.",
        "Streamlit makes it easy to build web applications.",
        "Practice typing every day to become faster.",
        "GitHub is useful for sharing and managing code.",
        "Programming requires patience and problem solving.",
        "The quick brown fox jumps over the lazy dog.",
        "A good programmer never stops learning.",
        "Small improvements can create big results."
    ],

    "어려움": [
        "Artificial intelligence is changing the way we interact with computers.",
        "Software developers need creativity, logic, patience, and problem solving skills.",
        "Building a successful application requires testing, debugging, and continuous improvement.",
        "GitHub provides powerful tools for version control and collaborative software development.",
        "Learning programming may seem difficult at first, but consistent practice makes it easier.",
        "Streamlit allows Python developers to quickly create interactive data applications."
    ]
}


# =========================================================
# 세션 상태
# =========================================================

if "started" not in st.session_state:
    st.session_state.started = False

if "finished" not in st.session_state:
    st.session_state.finished = False

if "target" not in st.session_state:
    st.session_state.target = ""

if "difficulty" not in st.session_state:
    st.session_state.difficulty = "쉬움"

if "game_time" not in st.session_state:
    st.session_state.game_time = 30

if "start_time" not in st.session_state:
    st.session_state.start_time = 0

if "score" not in st.session_state:
    st.session_state.score = 0

if "best_score" not in st.session_state:
    st.session_state.best_score = 0

if "correct_chars" not in st.session_state:
    st.session_state.correct_chars = 0

if "total_chars" not in st.session_state:
    st.session_state.total_chars = 0

if "sentences" not in st.session_state:
    st.session_state.sentences = 0

if "combo" not in st.session_state:
    st.session_state.combo = 0

if "max_combo" not in st.session_state:
    st.session_state.max_combo = 0

if "input_version" not in st.session_state:
    st.session_state.input_version = 0


# =========================================================
# 게임 시작
# =========================================================

def start_game(difficulty, game_time):

    st.session_state.started = True
    st.session_state.finished = False

    st.session_state.difficulty = difficulty
    st.session_state.game_time = game_time

    st.session_state.target = random.choice(
        TEXTS[difficulty]
    )

    st.session_state.start_time = time.time()

    st.session_state.score = 0
    st.session_state.correct_chars = 0
    st.session_state.total_chars = 0

    st.session_state.sentences = 0

    st.session_state.combo = 0
    st.session_state.max_combo = 0

    st.session_state.input_version += 1


# =========================================================
# 게임 종료
# =========================================================

def finish_game():

    st.session_state.started = False
    st.session_state.finished = True

    if st.session_state.score > st.session_state.best_score:
        st.session_state.best_score = st.session_state.score


# =========================================================
# 정확도
# =========================================================

def accuracy():

    if st.session_state.total_chars == 0:
        return 100.0

    return (
        st.session_state.correct_chars
        / st.session_state.total_chars
    ) * 100


# =========================================================
# WPM
# =========================================================

def wpm():

    if st.session_state.start_time == 0:
        return 0

    elapsed = max(
        time.time() - st.session_state.start_time,
        1
    )

    minutes = elapsed / 60

    words = st.session_state.correct_chars / 5

    return round(words / minutes)


# =========================================================
# 타이틀
# =========================================================

st.title("⌨️ Typing Master")

st.caption(
    "문장을 빠르고 정확하게 입력하세요!"
)


# =========================================================
# 시작 화면
# =========================================================

if not st.session_state.started:

    st.subheader("🎮 게임 설정")

    difficulty = st.selectbox(
        "난이도",
        ["쉬움", "보통", "어려움"]
    )

    game_time = st.slider(
        "게임 시간",
        10,
        60,
        30,
        5
    )

    st.write(
        f"현재 최고 점수: "
        f"**{st.session_state.best_score}점**"
    )

    if st.button(
        "🎮 게임 시작",
        type="primary",
        use_container_width=True
    ):

        start_game(
            difficulty,
            game_time
        )

        st.rerun()


# =========================================================
# 게임
# =========================================================

if st.session_state.started:

    # -----------------------------------------------------
    # 시간 계산
    # -----------------------------------------------------

    elapsed = (
        time.time()
        - st.session_state.start_time
    )

    remaining = max(
        0,
        st.session_state.game_time
        - int(elapsed)
    )

    # -----------------------------------------------------
    # 시간 종료
    # -----------------------------------------------------

    if remaining <= 0:

        finish_game()

        st.rerun()

    # -----------------------------------------------------
    # 정보
    # -----------------------------------------------------

    c1, c2, c3, c4 = st.columns(4)

    with c1:
        st.metric(
            "⏱️ 남은 시간",
            f"{remaining}초"
        )

    with c2:
        st.metric(
            "🎯 점수",
            st.session_state.score
        )

    with c3:
        st.metric(
            "🔥 콤보",
            st.session_state.combo
        )

    with c4:
        st.metric(
            "⚡ WPM",
            wpm()
        )

    st.divider()

    # -----------------------------------------------------
    # 문제
    # -----------------------------------------------------

    st.subheader("⌨️ 다음 문장")

    st.markdown(
        f"""
        <div style="
            background:#1f2937;
            color:white;
            padding:25px;
            border-radius:15px;
            font-size:24px;
            font-weight:bold;
            text-align:center;
            margin-bottom:20px;
        ">
            {st.session_state.target}
        </div>
        """,
        unsafe_allow_html=True
    )

    # -----------------------------------------------------
    # 입력창
    #
    # key가 바뀌면 입력창이 새로 만들어짐
    # -----------------------------------------------------

    input_key = (
        f"typing_{st.session_state.input_version}"
    )

    typed = st.text_input(
        "문장 입력",
        key=input_key,
        label_visibility="collapsed",
        placeholder="여기에 입력하세요...",
        autocomplete="off"
    )

    # -----------------------------------------------------
    # 입력 처리
    # -----------------------------------------------------

    if typed:

        target = st.session_state.target

        # 정확하게 입력한 글자 계산
        correct = 0

        for i in range(
            min(len(typed), len(target))
        ):

            if typed[i] == target[i]:
                correct += 1

        st.session_state.correct_chars += correct
        st.session_state.total_chars += len(typed)

        # -------------------------------------------------
        # 정확한 입력 중
        # -------------------------------------------------

        if target.startswith(typed):

            st.success(
                "✅ 정확합니다!"
            )

        # -------------------------------------------------
        # 오타
        # -------------------------------------------------

        else:

            st.error(
                "❌ 오타가 있습니다!"
            )

            st.session_state.combo = 0

        # -------------------------------------------------
        # 정답
        # -------------------------------------------------

        if typed == target:

            # 점수
            st.session_state.score += (
                len(target) * 10
            )

            # 보너스
            st.session_state.score += 100

            # 콤보
            st.session_state.combo += 1

            st.session_state.max_combo = max(
                st.session_state.max_combo,
                st.session_state.combo
            )

            # 완료 문장
            st.session_state.sentences += 1

            # -------------------------------------------------
            # ⭐ 핵심
            #
            # 기존 문장을 새로운 문장으로 교체
            # -------------------------------------------------

            st.session_state.target = random.choice(
                TEXTS[
                    st.session_state.difficulty
                ]
            )

            # -------------------------------------------------
            # ⭐ 핵심
            #
            # 입력창을 완전히 새로 생성
            # -------------------------------------------------

            st.session_state.input_version += 1

            # -------------------------------------------------
            # 화면 즉시 갱신
            # -------------------------------------------------

            st.rerun()

    # -----------------------------------------------------
    # 정확도
    # -----------------------------------------------------

    current_accuracy = accuracy()

    st.progress(
        min(
            current_accuracy / 100,
            1.0
        )
    )

    st.caption(
        f"🎯 정확도: "
        f"**{current_accuracy:.1f}%**"
    )

    st.caption(
        f"📝 완료한 문장: "
        f"**{st.session_state.sentences}개**"
    )

    # -----------------------------------------------------
    # 종료 버튼
    # -----------------------------------------------------

    if st.button(
        "🛑 게임 종료",
        use_container_width=True
    ):

        finish_game()

        st.rerun()

    # -----------------------------------------------------
    # 타이머 갱신
    # -----------------------------------------------------

    time.sleep(1)

    st.rerun()


# =========================================================
# 결과 화면
# =========================================================

if st.session_state.finished:

    st.balloons()

    st.header("🎉 게임 종료!")

    current_accuracy = accuracy()

    c1, c2, c3 = st.columns(3)

    with c1:

        st.metric(
            "🏆 점수",
            st.session_state.score
        )

    with c2:

        st.metric(
            "⚡ WPM",
            wpm()
        )

    with c3:

        st.metric(
            "🎯 정확도",
            f"{current_accuracy:.1f}%"
        )

    st.divider()

    st.write(
        f"📝 완료한 문장: "
        f"**{st.session_state.sentences}개**"
    )

    st.write(
        f"🔥 최고 콤보: "
        f"**{st.session_state.max_combo}**"
    )

    st.write(
        f"🏆 최고 점수: "
        f"**{st.session_state.best_score}점**"
    )

    # -----------------------------------------------------
    # 등급
    # -----------------------------------------------------

    if st.session_state.score >= 1000:

        st.success(
            "👑 타이핑 마스터!"
        )

    elif st.session_state.score >= 500:

        st.success(
            "🔥 엄청난 기록입니다!"
        )

    elif st.session_state.score >= 200:

        st.info(
            "👍 좋은 기록입니다!"
        )

    else:

        st.warning(
            "💪 조금 더 연습해보세요!"
        )

    st.divider()

    # -----------------------------------------------------
    # 다시 시작
    # -----------------------------------------------------

    if st.button(
        "🔄 다시 플레이",
        type="primary",
        use_container_width=True
    ):

        start_game(
            st.session_state.difficulty,
            st.session_state.game_time
        )

        st.rerun()
