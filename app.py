import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(
    page_title="Traffic Dodge",
    page_icon="🚗",
    layout="centered"
)

st.title("🚗 Traffic Dodge")
st.caption("← → 방향키로 자동차를 움직여 장애물을 피하세요!")

# =========================================================
# 게임
# =========================================================

game_html = r"""
<!DOCTYPE html>
<html>
<head>

<meta charset="UTF-8">

<style>

* {
    box-sizing: border-box;
}

body {
    margin: 0;
    padding: 0;

    background: #111827;

    font-family: Arial, sans-serif;

    overflow: hidden;
}

#gameWrapper {
    width: 100%;
    display: flex;
    justify-content: center;
}

#game {
    position: relative;

    width: 400px;
    height: 650px;

    background:
        linear-gradient(
            to right,
            #333 0%,
            #333 20%,
            #555 20%,
            #555 80%,
            #333 80%,
            #333 100%
        );

    border: 5px solid white;
    border-radius: 15px;

    overflow: hidden;

    box-shadow:
        0 0 30px rgba(0,0,0,0.5);
}

/* 도로 중앙선 */

.line {
    position: absolute;

    width: 8px;
    height: 70px;

    background: white;

    left: 50%;

    transform: translateX(-50%);

    opacity: 0.7;
}

/* 플레이어 */

#player {
    position: absolute;

    width: 50px;
    height: 90px;

    bottom: 30px;
    left: 175px;

    background: #2196f3;

    border-radius: 12px;

    border: 3px solid white;

    box-shadow:
        0 0 10px rgba(33,150,243,0.8);

    z-index: 10;
}

/* 자동차 앞 유리 */

#player::before {
    content: "";

    position: absolute;

    width: 32px;
    height: 25px;

    left: 6px;
    top: 8px;

    background: #9ee7ff;

    border-radius: 6px;
}

/* 자동차 불빛 */

#player::after {
    content: "";

    position: absolute;

    width: 32px;
    height: 10px;

    left: 6px;
    bottom: 8px;

    background: #ff3333;

    border-radius: 5px;
}

/* 장애물 */

.enemy {
    position: absolute;

    width: 50px;
    height: 90px;

    background: #ef4444;

    border-radius: 12px;

    border: 3px solid white;

    z-index: 5;
}

.enemy::before {
    content: "";

    position: absolute;

    width: 32px;
    height: 25px;

    left: 6px;
    top: 8px;

    background: #222;

    border-radius: 6px;
}

.enemy::after {
    content: "";

    position: absolute;

    width: 32px;
    height: 10px;

    left: 6px;
    bottom: 8px;

    background: #ffff55;

    border-radius: 5px;
}

/* UI */

#score {
    position: absolute;

    top: 15px;
    left: 15px;

    color: white;

    font-size: 22px;
    font-weight: bold;

    z-index: 100;
}

#lives {
    position: absolute;

    top: 45px;
    left: 15px;

    color: white;

    font-size: 18px;

    z-index: 100;
}

#speed {
    position: absolute;

    top: 70px;
    left: 15px;

    color: #ddd;

    font-size: 15px;

    z-index: 100;
}

/* 시작 화면 */

#startScreen,
#gameOverScreen {
    position: absolute;

    inset: 0;

    background: rgba(0,0,0,0.8);

    display: flex;

    flex-direction: column;

    justify-content: center;

    align-items: center;

    color: white;

    z-index: 200;
}

#gameOverScreen {
    display: none;
}

h1 {
    font-size: 38px;
    margin-bottom: 10px;
}

button {
    padding: 15px 35px;

    border: none;

    border-radius: 10px;

    background: #22c55e;

    color: white;

    font-size: 20px;

    font-weight: bold;

    cursor: pointer;
}

button:hover {
    background: #16a34a;
}

</style>

</head>

<body>

<div id="gameWrapper">

<div id="game">

    <div id="score">
        점수: 0
    </div>

    <div id="lives">
        ❤️❤️❤️
    </div>

    <div id="speed">
        속도: 1
    </div>

    <!-- 도로 중앙선 -->

    <div class="line" style="top: 0px;"></div>
    <div class="line" style="top: 140px;"></div>
    <div class="line" style="top: 280px;"></div>
    <div class="line" style="top: 420px;"></div>
    <div class="line" style="top: 560px;"></div>

    <!-- 플레이어 -->

    <div id="player"></div>


    <!-- 시작 -->

    <div id="startScreen">

        <h1>🚗 Traffic Dodge</h1>

        <p>
            ← → 방향키로 자동차를 움직이세요
        </p>

        <p>
            장애물에 부딪히면 목숨을 잃습니다.
        </p>

        <button onclick="startGame()">
            게임 시작
        </button>

    </div>


    <!-- 게임 오버 -->

    <div id="gameOverScreen">

        <h1>💥 GAME OVER</h1>

        <p id="finalScore">
            점수: 0
        </p>

        <button onclick="restartGame()">
            다시 하기
        </button>

    </div>

</div>

</div>


<script>

// =======================================================
// 기본 변수
// =======================================================

const game =
    document.getElementById("game");

const player =
    document.getElementById("player");

const scoreText =
    document.getElementById("score");

const livesText =
    document.getElementById("lives");

const speedText =
    document.getElementById("speed");

const startScreen =
    document.getElementById("startScreen");

const gameOverScreen =
    document.getElementById("gameOverScreen");

const finalScore =
    document.getElementById("finalScore");


let playerX = 175;

let enemies = [];

let score = 0;

let lives = 3;

let speed = 3;

let gameRunning = false;

let keys = {};

let spawnTimer = 0;

let lastTime = 0;


// =======================================================
// 키보드
// =======================================================

document.addEventListener(
    "keydown",
    function(event) {

        keys[event.key] = true;

        if (
            event.key === "ArrowLeft" ||
            event.key === "ArrowRight"
        ) {

            event.preventDefault();

        }

    }
);


document.addEventListener(
    "keyup",
    function(event) {

        keys[event.key] = false;

    }
);


// =======================================================
// 게임 시작
// =======================================================

function startGame() {

    startScreen.style.display = "none";

    gameOverScreen.style.display = "none";

    playerX = 175;

    score = 0;

    lives = 3;

    speed = 3;

    enemies = [];

    spawnTimer = 0;

    player.style.left =
        playerX + "px";

    updateUI();

    gameRunning = true;

    lastTime = performance.now();

    requestAnimationFrame(gameLoop);

}


// =======================================================
// 다시 시작
// =======================================================

function restartGame() {

    // 기존 장애물 삭제

    enemies.forEach(
        enemy => enemy.element.remove()
    );

    enemies = [];

    startGame();

}


// =======================================================
// 장애물 생성
// =======================================================

function createEnemy() {

    const enemy =
        document.createElement("div");

    enemy.className = "enemy";


    // 차선 선택

    const lanes = [
        80,
        145,
        210,
        275
    ];

    const lane =
        lanes[
            Math.floor(
                Math.random() * lanes.length
            )
        ];


    enemy.style.left =
        lane + "px";

    enemy.style.top =
        "-100px";


    game.appendChild(enemy);


    enemies.push({

        element: enemy,

        x: lane,

        y: -100,

        speed:
            speed +
            Math.random() * 2

    });

}


// =======================================================
// 충돌 검사
// =======================================================

function collision(a, b) {

    const rectA =
        a.getBoundingClientRect();

    const rectB =
        b.getBoundingClientRect();


    return !(
        rectA.right < rectB.left ||
        rectA.left > rectB.right ||
        rectA.bottom < rectB.top ||
        rectA.top > rectB.bottom
    );

}


// =======================================================
// 목숨 감소
// =======================================================

function loseLife() {

    lives--;

    updateUI();


    if (lives <= 0) {

        endGame();

    }

}


// =======================================================
// UI
// =======================================================

function updateUI() {

    scoreText.innerText =
        "점수: " + score;

    livesText.innerText =
        "❤️".repeat(lives);

    speedText.innerText =
        "속도: " +
        Math.floor(speed);

}


// =======================================================
// 게임 종료
// =======================================================

function endGame() {

    gameRunning = false;

    finalScore.innerText =
        "점수: " + score;

    gameOverScreen.style.display =
        "flex";

}


// =======================================================
// 게임 루프
// =======================================================

function gameLoop(currentTime) {

    if (!gameRunning) {
        return;
    }


    const delta =
        currentTime - lastTime;

    lastTime = currentTime;


    // ===================================================
    // 플레이어 이동
    // ===================================================

    if (keys["ArrowLeft"]) {

        playerX -= 7;

    }

    if (keys["ArrowRight"]) {

        playerX += 7;

    }


    // 도로 밖으로 못 나가게

    if (playerX < 80) {

        playerX = 80;

    }

    if (playerX > 270) {

        playerX = 270;

    }


    player.style.left =
        playerX + "px";


    // ===================================================
    // 장애물 생성
    // ===================================================

    spawnTimer += delta;


    const spawnInterval =
        Math.max(
            400,
            1000 - score * 3
        );


    if (spawnTimer > spawnInterval) {

        createEnemy();

        spawnTimer = 0;

    }


    // ===================================================
    // 장애물 이동
    // ===================================================

    for (
        let i = enemies.length - 1;
        i >= 0;
        i--
    ) {

        const enemy =
            enemies[i];


        enemy.y +=
            enemy.speed;


        enemy.element.style.top =
            enemy.y + "px";


        // =================================================
        // 충돌
        // =================================================

        if (
            collision(
                player,
                enemy.element
            )
        ) {

            enemy.element.remove();

            enemies.splice(i, 1);

            loseLife();

            continue;

        }


        // =================================================
        // 화면 아래로 지나감
        // =================================================

        if (enemy.y > 700) {

            enemy.element.remove();

            enemies.splice(i, 1);

            score++;

            // 점수가 올라갈수록 속도 증가

            speed =
                3 +
                Math.floor(score / 10) * 0.5;

            updateUI();

        }

    }


    // ===================================================
    // 다음 프레임
    // ===================================================

    requestAnimationFrame(gameLoop);

}


// =======================================================
// 자동 포커스
// =======================================================

window.onload = function() {

    document.body.focus();

};

</script>

</body>
</html>
"""

components.html(
    game_html,
    height=700,
    scrolling=False
)
