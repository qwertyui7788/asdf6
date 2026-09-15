import streamlit as st
import random
import time

# --------------------------------------------------
# 기본 설정
# --------------------------------------------------

st.set_page_config(
    page_title="Typing Master",
    page_icon="⌨️",
    layout="centered"
)

# --------------------------------------------------
# 문장 데이터
# --------------------------------------------------

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

# --------------------------------------------------
# 세션 상태 초기화
# --------------------------------------------------

if "game_started" not in st.session_state:
    st.session_state.game_started = False

if "game_finished" not in st.session_state:
    st.session_state.game_finished = False

if "start_time" not in st.session_state:
    st.session_state.start_time = None

if "target_text" not in st.session_state:
    st.session_state.target_text = ""

if "typed_text" not in st.session_state:
    st.session_state.typed_text = ""

if "score" not in st.session_state:
    st.session_state.score = 0

if "best_score" not in st.session_state:
    st.session_state.best_score = 0

if "combo" not in st.session_state:
    st.session_state.combo = 0

if "max_combo" not in st.session_state:
    st.session_state.max_combo = 0

if "correct_chars" not in st.session_state:
    st.session_state.correct_chars = 0

if "total_chars" not in st.session_state:
    st.session_state.total_chars = 0

# --------------------------------------------------
# 함수
# --------------------------------------------------

def start_game(difficulty):
    """게임 시작"""

    st.session_state.game_started = True
    st.session_state.game_finished = False

    st.session_state.target_text = random.choice(
        TEXTS[difficulty]
    )

    st.session_state.typed_text = ""
    st.session_state.score = 0
    st.session_state.combo = 0
    st.session_state.max_combo = 0
    st.session_state.correct_chars = 0
    st.session_state.total_chars = 0

    st.session_state.start_time = time.time()


def finish_game():
    """게임 종료"""

    st.session_state.game_finished = True
    st.session_state.game_started = False

    if st.session_state.score > st.session_state.best_score:
        st.session_state.best_score = st.session_state.score


def calculate_accuracy():
    """정확도 계산"""

    total = st.session_state.total_chars

    if total == 0:
        return 100.0

    return (
        st.session_state.correct_chars / total
    ) * 100


def calculate_wpm():
    """WPM 계산"""

    if st.session_state.start_time is None:
        return 0

    elapsed = max(
        time.time() - st.session_state.start_time,
        1
    )

    # 영어 타이핑 기준:
    # 5 characters = 1 word
    words = st.session_state.correct_chars / 5

    minutes = elapsed / 60

    return round(words / minutes)


def check_typing(user_text, target_text):
    """
    현재 입력을 기준으로
    정확한 글자 수와 콤보 계산
    """

    correct = 0

    for i in range(
        min(len(user_text), len(target_text))
    ):
        if user_text[i] == target_text[i]:
            correct += 1

    st.session_state.correct_chars = correct
    st.session_state.total_chars = len(user_text)

    # 콤보 계산
    if (
        len(user_text) > 0
        and user_text == target_text[:len(user_text)]
    ):
        st.session_state.combo = len(user_text)
    else:
        st.session_state.combo = 0

    st.session_state.max_combo = max(
        st.session_state.max_combo,
        st.session_state.combo
    )

    # 점수 계산
    accuracy = calculate_accuracy()

    st.session_state.score = int(
        correct * 10
        + st.session_state.combo * 2
        + accuracy
    )

# --------------------------------------------------
# 제목
# --------------------------------------------------

st.title("⌨️ Typing Master")

st.write(
    "주어진 문장을 최대한 빠르고 정확하게 입력하세요!"
)

# --------------------------------------------------
# 사이드바
# --------------------------------------------------

with st.sidebar:

    st.header("⚙️ 게임 설정")

    difficulty = st.selectbox(
        "난이도",
        ["쉬움", "보통", "어려움"]
    )

    game_time = st.slider(
        "게임 시간",
        min_value=10,
        max_value=60,
        value=30,
        step=5
    )

    st.divider()

    st.subheader("🏆 기록")

    st.metric(
        "최고 점수",
        st.session_state.best_score
    )

# --------------------------------------------------
# 게임 시작 전
# --------------------------------------------------

if not st.session_state.game_started:

    st.info(
        f"난이도: **{difficulty}** | "
        f"제한시간: **{game_time}초**"
    )

    if st.button(
        "🎮 게임 시작",
        type="primary",
        use_container_width=True
    ):
        start_game(difficulty)
        st.rerun()

# --------------------------------------------------
# 게임 진행
# --------------------------------------------------

if st.session_state.game_started:

    elapsed = time.time() - st.session_state.start_time
    remaining = max(
        0,
        game_time - int(elapsed)
    )

    # 시간 종료
    if remaining <= 0:
        finish_game()
        st.rerun()

    # 상단 정보
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric(
            "⏱️ 남은 시간",
            f"{remaining}초"
        )

    with col2:
        st.metric(
            "🎯 점수",
            st.session_state.score
        )

    with col3:
        st.metric(
            "🔥 콤보",
            st.session_state.combo
        )

    with col4:
        st.metric(
            "⚡ WPM",
            calculate_wpm()
        )

    st.divider()

    # 출제 문장
    st.subheader("⌨️ 다음 문장을 입력하세요")

    st.code(
        st.session_state.target_text,
        language=None
    )

    # 입력창
    typed = st.text_input(
        "입력",
        value=st.session_state.typed_text,
        key="typing_input",
        label_visibility="collapsed",
        placeholder="위 문장을 그대로 입력하세요..."
    )

    # 입력 처리
    if typed != st.session_state.typed_text:

        st.session_state.typed_text = typed

        check_typing(
            typed,
            st.session_state.target_text
        )

        # 문장을 정확하게 완성
        if typed == st.session_state.target_text:

            st.session_state.score += 100

            st.session_state.target_text = random.choice(
                TEXTS[difficulty]
            )

            st.session_state.typed_text = ""

            # Streamlit 입력창 초기화를 위해 rerun
            st.rerun()

    # 정확도
    accuracy = calculate_accuracy()

    st.progress(
        min(accuracy / 100, 1.0)
    )

    st.caption(
        f"정확도: **{accuracy:.1f}%**"
    )

    # 현재 입력 상태
    if typed:

        if st.session_state.target_text.startswith(
            typed
        ):
            st.success("✅ 지금까지 정확합니다!")

        else:
            st.error(
                "❌ 오타가 있습니다. 다시 확인하세요."
            )

    # 종료 버튼
    if st.button(
        "🛑 게임 종료",
        use_container_width=True
    ):
        finish_game()
        st.rerun()

    # 자동 새로고침
    time.sleep(1)
    st.rerun()

# --------------------------------------------------
# 게임 종료 화면
# --------------------------------------------------

if st.session_state.game_finished:

    st.balloons()

    st.header("🎉 게임 종료!")

    accuracy = calculate_accuracy()

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric(
            "🏆 점수",
            st.session_state.score
        )

    with col2:
        st.metric(
            "⚡ WPM",
            calculate_wpm()
        )

    with col3:
        st.metric(
            "🎯 정확도",
            f"{accuracy:.1f}%"
        )

    st.divider()

    st.subheader("📊 결과")

    st.write(
        f"🔥 최고 콤보: **{st.session_state.max_combo}**"
    )

    st.write(
        f"⌨️ 정확하게 입력한 글자: "
        f"**{st.session_state.correct_chars}자**"
    )

    st.write(
        f"🏆 현재 최고 점수: "
        f"**{st.session_state.best_score}점**"
    )

    if st.session_state.score >= 1000:
        st.success("👑 타이핑 마스터!")

    elif st.session_state.score >= 500:
        st.success("🔥 엄청 빠르네요!")

    elif st.session_state.score >= 200:
        st.info("👍 좋은 기록입니다!")

    else:
        st.warning("💪 조금 더 연습해보세요!")

    st.divider()

    if st.button(
        "🔄 다시 플레이",
        type="primary",
        use_container_width=True
    ):
        start_game(difficulty)
        st.rerun()
