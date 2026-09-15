import streamlit as st
import streamlit.components.v1 as components
import random
import json
import time

# =========================================================
# 기본 설정
# =========================================================

st.set_page_config(
    page_title="Typing Master",
    page_icon="⌨️",
    layout="centered"
)

# =========================================================
# 문장 데이터
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

if "game_started" not in st.session_state:
    st.session_state.game_started = False

if "game_finished" not in st.session_state:
    st.session_state.game_finished = False

if "difficulty" not in st.session_state:
    st.session_state.difficulty = "쉬움"

if "game_time" not in st.session_state:
    st.session_state.game_time = 30

if "target_text" not in st.session_state:
    st.session_state.target_text = ""

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

if "completed_sentences" not in st.session_state:
    st.session_state.completed_sentences = 0

if "combo" not in st.session_state:
    st.session_state.combo = 0

if "max_combo" not in st.session_state:
    st.session_state.max_combo = 0

if "last_result" not in st.session_state:
    st.session_state.last_result = ""

if "game_id" not in st.session_state:
    st.session_state.game_id = 0


# =========================================================
# 게임 시작
# =========================================================

def start_game(difficulty, game_time):

    st.session_state.game_started = True
    st.session_state.game_finished = False

    st.session_state.difficulty = difficulty
    st.session_state.game_time = game_time

    st.session_state.target_text = random.choice(
        TEXTS[difficulty]
    )

    st.session_state.start_time = time.time()

    st.session_state.score = 0
    st.session_state.correct_chars = 0
    st.session_state.total_chars = 0

    st.session_state.completed_sentences = 0

    st.session_state.combo = 0
    st.session_state.max_combo = 0

    st.session_state.last_result = ""

    st.session_state.game_id += 1


# =========================================================
# 게임 종료
# =========================================================

def finish_game():

    st.session_state.game_started = False
    st.session_state.game_finished = True

    if st.session_state.score > st.session_state.best_score:
        st.session_state.best_score = st.session_state.score


# =========================================================
# 정확도
# =========================================================

def get_accuracy():

    if st.session_state.total_chars == 0:
        return 100.0

    return (
        st.session_state.correct_chars
        / st.session_state.total_chars
    ) * 100


# =========================================================
# WPM
# =========================================================

def get_wpm():

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
# 제목
# =========================================================

st.title("⌨️ Typing Master")

st.caption(
    "마우스를 사용하지 않고 키보드만으로 플레이하세요!"
)


# =========================================================
# 게임 설정
# =========================================================

if not st.session_state.game_started:

    st.subheader("🎮 게임 설정")

    difficulty = st.selectbox(
        "난이도",
        ["쉬움", "보통", "어려움"],
        index=["쉬움", "보통", "어려움"].index(
            st.session_state.difficulty
        )
    )

    game_time = st.slider(
        "게임 시간",
        min_value=10,
        max_value=60,
        value=st.session_state.game_time,
        step=5
    )

    st.info(
        f"난이도: **{difficulty}** | "
        f"게임 시간: **{game_time}초**"
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

    st.divider()

    st.metric(
        "🏆 최고 점수",
        st.session_state.best_score
    )


# =========================================================
# 게임 화면
# =========================================================

if st.session_state.game_started:

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
    # 게임 정보
    # -----------------------------------------------------

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
            get_wpm()
        )

    st.divider()

    # -----------------------------------------------------
    # 문제 표시
    # -----------------------------------------------------

    st.subheader("⌨️ 다음 문장을 입력하세요")

    st.markdown(
        f"""
        <div style="
            background-color:#1e1e1e;
            color:#ffffff;
            padding:25px;
            border-radius:12px;
            font-size:24px;
            font-weight:bold;
            text-align:center;
            margin-bottom:20px;
            letter-spacing:1px;
        ">
            {st.session_state.target_text}
        </div>
        """,
        unsafe_allow_html=True
    )

    # -----------------------------------------------------
    # JavaScript 타이핑 게임
    # -----------------------------------------------------

    target = json.dumps(
        st.session_state.target_text
    )

    game_id = st.session_state.game_id

    html_code = f"""
    <!DOCTYPE html>

    <html>

    <head>

        <meta charset="UTF-8">

        <style>

            * {{
                box-sizing: border-box;
            }}

            body {{
                margin: 0;
                padding: 0;
                background: transparent;
                font-family: Arial, sans-serif;
            }}

            #typingInput {{
                width: 100%;
                height: 65px;

                border: 3px solid #4CAF50;
                border-radius: 12px;

                background: #111827;
                color: white;

                font-size: 22px;
                padding: 15px;

                outline: none;

                transition: 0.2s;
            }}

            #typingInput:focus {{
                border-color: #00ff88;

                box-shadow:
                    0 0 10px rgba(0,255,136,0.4);
            }}

            #typingInput.error {{
                border-color: #ff4444;

                box-shadow:
                    0 0 10px rgba(255,68,68,0.4);
            }}

            #status {{
                height: 30px;
                margin-top: 8px;

                font-size: 16px;
                font-weight: bold;
            }}

            .correct {{
                color: #00ff88;
            }}

            .wrong {{
                color: #ff5555;
            }}

        </style>

    </head>

    <body>

        <input
            id="typingInput"
            type="text"
            autocomplete="off"
            autocorrect="off"
            autocapitalize="off"
            spellcheck="false"
            placeholder="여기에 입력하세요..."
        >

        <div id="status"></div>


        <script>

            const target = {target};

            const input = document.getElementById(
                "typingInput"
            );

            const status = document.getElementById(
                "status"
            );


            // -----------------------------------------
            // 페이지가 열리면 자동 포커스
            // -----------------------------------------

            window.onload = function() {{

                input.focus();

            }};


            // -----------------------------------------
            // 마우스로 다른 곳을 클릭해도
            // 입력창을 다시 클릭할 필요가 없도록 함
            // -----------------------------------------

            document.addEventListener(
                "click",
                function() {{

                    if (
                        document.activeElement !== input
                    ) {{

                        input.focus();

                    }}

                }}
            );


            // -----------------------------------------
            // 키 입력
            // -----------------------------------------

            input.addEventListener(
                "input",
                function() {{

                    const value = input.value;


                    // -----------------------------------
                    // 아직 정확하게 입력 중
                    // -----------------------------------

                    if (
                        target.startsWith(value)
                    ) {{

                        input.classList.remove(
                            "error"
                        );

                        status.className =
                            "correct";

                        status.innerText =
                            "✓ 정확합니다";

                    }}

                    // -----------------------------------
                    // 오타
                    // -----------------------------------

                    else {{

                        input.classList.add(
                            "error"
                        );

                        status.className =
                            "wrong";

                        status.innerText =
                            "✕ 오타가 있습니다";

                    }}


                    // -----------------------------------
                    // 정답
                    // -----------------------------------

                    if (value === target) {{

                        status.className =
                            "correct";

                        status.innerText =
                            "🎉 정답!";

                        // Streamlit에 정답 전달
                        window.parent.postMessage(
                            {{
                                type: "typing_complete",
                                game_id: {game_id}
                            }},
                            "*"
                        );


                        // --------------------------------
                        // 입력창 즉시 비우기
                        // --------------------------------

                        input.value = "";

                        input.classList.remove(
                            "error"
                        );


                        // --------------------------------
                        // 다시 포커스
                        // --------------------------------

                        setTimeout(
                            function() {{

                                input.focus();

                            }},
                            50
                        );

                    }}

                }}
            );


            // -----------------------------------------
            // Enter 키 방지
            // -----------------------------------------

            input.addEventListener(
                "keydown",
                function(event) {{

                    if (event.key === "Enter") {{

                        event.preventDefault();

                    }}

                }}
            );

        </script>

    </body>

    </html>
    """

    components.html(
        html_code,
        height=115,
        scrolling=False
    )

    # -----------------------------------------------------
    # 진행 상황
    # -----------------------------------------------------

    accuracy = get_accuracy()

    st.progress(
        min(accuracy / 100, 1.0)
    )

    st.caption(
        f"🎯 정확도: **{accuracy:.1f}%**"
    )

    st.caption(
        f"📝 완료한 문장: "
        f"**{st.session_state.completed_sentences}개**"
    )

    # -----------------------------------------------------
    # 종료
    # -----------------------------------------------------

    if st.button(
        "🛑 게임 종료",
        use_container_width=True
    ):

        finish_game()

        st.rerun()

    # -----------------------------------------------------
    # 새로고침
    #
    # 타이머를 갱신하기 위한 부분
    # -----------------------------------------------------

    time.sleep(1)

    st.rerun()


# =========================================================
# 게임 종료 화면
# =========================================================

if st.session_state.game_finished:

    st.balloons()

    st.header("🎉 게임 종료!")

    accuracy = get_accuracy()
    wpm = get_wpm()

    col1, col2, col3 = st.columns(3)

    with col1:

        st.metric(
            "🏆 점수",
            st.session_state.score
        )

    with col2:

        st.metric(
            "⚡ WPM",
            wpm
        )

    with col3:

        st.metric(
            "🎯 정확도",
            f"{accuracy:.1f}%"
        )

    st.divider()

    st.subheader("📊 결과")

    st.write(
        f"🔥 최고 콤보: "
        f"**{st.session_state.max_combo}**"
    )

    st.write(
        f"📝 완료한 문장: "
        f"**{st.session_state.completed_sentences}개**"
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
            "🔥 엄청 빠르네요!"
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
    # 다시하기
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
