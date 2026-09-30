import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(
    page_title="벽돌 깨기",
    page_icon="🧱",
    layout="centered"
)

game_html = r"""
<!DOCTYPE html>

<html lang="ko">

<head>

<meta charset="UTF-8">

<meta name="viewport"
      content="width=device-width, initial-scale=1.0">

<style>

* {
    box-sizing: border-box;
}

html, body {
    margin: 0;
    padding: 0;
    background: #080b16;
    font-family: Arial, sans-serif;
}

body {
    color: white;
}

.game {
    width: 100%;
    max-width: 820px;
    margin: 0 auto;
    text-align: center;
}

.title {
    font-size: 32px;
    font-weight: bold;
    margin: 10px 0 15px;
}

.info {
    display: flex;
    justify-content: center;
    gap: 10px;
    margin-bottom: 12px;
    flex-wrap: wrap;
}

.info-box {
    background: #171d31;
    border: 1px solid #30384f;
    border-radius: 10px;
    padding: 8px 18px;
    min-width: 100px;
}

.info-label {
    font-size: 13px;
    color: #aab3ca;
}

.info-value {
    font-size: 21px;
    font-weight: bold;
    color: #ffd166;
    margin-top: 3px;
}

.canvas-box {
    position: relative;
    width: 100%;
    background: #02040a;
    border: 2px solid #39435e;
    border-radius: 12px;
    overflow: hidden;
}

canvas {
    display: block;
    width: 100%;
    height: auto;
    background: #050816;
}

.start-screen {
    position: absolute;
    left: 50%;
    top: 50%;
    transform: translate(-50%, -50%);

    width: 80%;
    max-width: 500px;

    padding: 25px;

    background: rgba(0, 0, 0, 0.88);

    border: 1px solid #46506b;
    border-radius: 18px;
}

.start-screen h2 {
    margin: 0 0 10px;
    font-size: 30px;
}

.start-screen p {
    color: #c8cedd;
    line-height: 1.6;
}

button {
    border: 0;
    border-radius: 10px;
    padding: 12px 22px;

    background: #2563eb;
    color: white;

    font-size: 16px;
    font-weight: bold;

    cursor: pointer;
}

button:hover {
    background: #1d4ed8;
}

.controls {
    display: flex;
    justify-content: center;
    align-items: center;
    gap: 10px;
    margin-top: 15px;
}

.control-button {
    width: 90px;
    height: 50px;
    font-size: 20px;
    background: #29344e;
}

.control-button:hover {
    background: #3b4969;
}

.pause-button {
    width: 130px;
    font-size: 14px;
}

.help {
    color: #8993ad;
    font-size: 13px;
    margin-top: 12px;
}

</style>

</head>

<body>

<div class="game">

    <div class="title">
        🧱 벽돌 깨기
    </div>

    <div class="info">

        <div class="info-box">
            <div class="info-label">점수</div>
            <div
                class="info-value"
                id="score"
            >0</div>
        </div>

        <div class="info-box">
            <div class="info-label">목숨</div>
            <div
                class="info-value"
                id="lives"
            >3</div>
        </div>

        <div class="info-box">
            <div class="info-label">레벨</div>
            <div
                class="info-value"
                id="level"
            >1</div>
        </div>

        <div class="info-box">
            <div class="info-label">최고점수</div>
            <div
                class="info-value"
                id="highScore"
            >0</div>
        </div>

    </div>


    <div class="canvas-box">

        <canvas
            id="gameCanvas"
            width="800"
            height="600"
        ></canvas>


        <div
            class="start-screen"
            id="startScreen"
        >

            <h2>🧱 벽돌 깨기</h2>

            <p>
                패들을 움직여 공을 튕기고
                모든 벽돌을 깨세요!
            </p>

            <button
                id="startButton"
            >
                게임 시작
            </button>

        </div>

    </div>


    <div class="controls">

        <button
            class="control-button"
            id="leftButton"
        >
            ◀
        </button>

        <button
            class="pause-button"
            id="pauseButton"
        >
            일시정지
        </button>

        <button
            class="control-button"
            id="rightButton"
        >
            ▶
        </button>

    </div>


    <div class="help">
        ← → 또는 A / D 키로 이동 · Space로 일시정지
    </div>

</div>


<script>

"use strict";


// ========================================
// DOM
// ========================================

const canvas =
    document.getElementById("gameCanvas");

const ctx =
    canvas.getContext("2d");

const scoreElement =
    document.getElementById("score");

const livesElement =
    document.getElementById("lives");

const levelElement =
    document.getElementById("level");

const highScoreElement =
    document.getElementById("highScore");

const startScreen =
    document.getElementById("startScreen");

const startButton =
    document.getElementById("startButton");

const pauseButton =
    document.getElementById("pauseButton");

const leftButton =
    document.getElementById("leftButton");

const rightButton =
    document.getElementById("rightButton");


// ========================================
// 게임 변수
// ========================================

let score = 0;

let lives = 3;

let level = 1;

let running = false;

let paused = false;

let animationId = null;


// ========================================
// 최고 점수
// ========================================

let highScore = 0;

try {

    highScore =
        Number(
            localStorage.getItem(
                "brick_breaker_high_score"
            )
        ) || 0;

} catch (error) {

    highScore = 0;
}

highScoreElement.textContent =
    highScore;


// ========================================
// 공
// ========================================

const ball = {

    x: 400,

    y: 500,

    radius: 9,

    dx: 4,

    dy: -4
};


// ========================================
// 패들
// ========================================

const paddle = {

    width: 120,

    height: 15,

    x: 340,

    y: 555,

    speed: 8,

    dx: 0
};


// ========================================
// 벽돌
// ========================================

const brickConfig = {

    rows: 5,

    columns: 10,

    width: 70,

    height: 25,

    gap: 7,

    top: 60,

    left: 20
};

let bricks = [];


// ========================================
// 벽돌 생성
// ========================================

function createBricks() {

    bricks = [];

    for (
        let row = 0;
        row < brickConfig.rows;
        row++
    ) {

        const currentRow = [];

        for (
            let column = 0;
            column < brickConfig.columns;
            column++
        ) {

            currentRow.push({

                x:
                    brickConfig.left +
                    column *
                    (
                        brickConfig.width +
                        brickConfig.gap
                    ),

                y:
                    brickConfig.top +
                    row *
                    (
                        brickConfig.height +
                        brickConfig.gap
                    ),

                width:
                    brickConfig.width,

                height:
                    brickConfig.height,

                alive: true
            });
        }

        bricks.push(currentRow);
    }
}


// ========================================
// 공 초기화
// ========================================

function resetBall() {

    ball.x = canvas.width / 2;

    ball.y = 500;

    const speed =
        4.5 +
        (level - 1) * 0.4;

    ball.dx =
        Math.random() < 0.5
        ? -speed
        : speed;

    ball.dy = -speed;
}


// ========================================
// 패들 초기화
// ========================================

function resetPaddle() {

    paddle.x =
        canvas.width / 2 -
        paddle.width / 2;

    paddle.dx = 0;
}


// ========================================
// 배경
// ========================================

function drawBackground() {

    const gradient =
        ctx.createLinearGradient(
            0,
            0,
            0,
            canvas.height
        );

    gradient.addColorStop(
        0,
        "#050816"
    );

    gradient.addColorStop(
        1,
        "#111a35"
    );

    ctx.fillStyle = gradient;

    ctx.fillRect(
        0,
        0,
        canvas.width,
        canvas.height
    );

    // 별

    ctx.fillStyle =
        "rgba(255,255,255,0.25)";

    for (
        let i = 0;
        i < 50;
        i++
    ) {

        const x =
            (i * 137) %
            canvas.width;

        const y =
            (i * 83) %
            500;

        ctx.fillRect(
            x,
            y,
            2,
            2
        );
    }
}


// ========================================
// 공 그리기
// ========================================

function drawBall() {

    ctx.beginPath();

    ctx.arc(
        ball.x,
        ball.y,
        ball.radius,
        0,
        Math.PI * 2
    );

    ctx.fillStyle =
        "#ffffff";

    ctx.shadowBlur = 15;

    ctx.shadowColor =
        "#00e5ff";

    ctx.fill();

    ctx.shadowBlur = 0;

    ctx.closePath();
}


// ========================================
// 패들 그리기
// ========================================

function drawPaddle() {

    const gradient =
        ctx.createLinearGradient(
            0,
            paddle.y,
            0,
            paddle.y +
            paddle.height
        );

    gradient.addColorStop(
        0,
        "#ffffff"
    );

    gradient.addColorStop(
        0.4,
        "#00e5ff"
    );

    gradient.addColorStop(
        1,
        "#2563eb"
    );

    ctx.fillStyle =
        gradient;

    ctx.beginPath();

    ctx.roundRect(
        paddle.x,
        paddle.y,
        paddle.width,
        paddle.height,
        7
    );

    ctx.fill();

    ctx.closePath();
}


// ========================================
// 벽돌 그리기
// ========================================

function drawBricks() {

    const colors = [

        "#ff595e",

        "#ff924c",

        "#ffca3a",

        "#8ac926",

        "#1982c4",

        "#6a4c93"

    ];

    for (
        let row = 0;
        row < bricks.length;
        row++
    ) {

        for (
            let column = 0;
            column < bricks[row].length;
            column++
        ) {

            const b =
                bricks[row][column];

            if (!b.alive) {
                continue;
            }

            ctx.fillStyle =
                colors[
                    row %
                    colors.length
                ];

            ctx.beginPath();

            ctx.roundRect(
                b.x,
                b.y,
                b.width,
                b.height,
                5
            );

            ctx.fill();

            ctx.fillStyle =
                "rgba(255,255,255,0.25)";

            ctx.fillRect(
                b.x + 4,
                b.y + 3,
                b.width - 8,
                4
            );

            ctx.closePath();
        }
    }
}


// ========================================
// 전체 그리기
// ========================================

function draw() {

    drawBackground();

    drawBricks();

    drawBall();

    drawPaddle();
}


// ========================================
// 패들 이동
// ========================================

function movePaddle() {

    paddle.x += paddle.dx;

    if (paddle.x < 0) {

        paddle.x = 0;
    }

    if (
        paddle.x +
        paddle.width >
        canvas.width
    ) {

        paddle.x =
            canvas.width -
            paddle.width;
    }
}


// ========================================
// 공 이동
// ========================================

function moveBall() {

    ball.x += ball.dx;

    ball.y += ball.dy;


    // 왼쪽 벽

    if (
        ball.x -
        ball.radius <= 0
    ) {

        ball.x =
            ball.radius;

        ball.dx =
            Math.abs(ball.dx);
    }


    // 오른쪽 벽

    if (
        ball.x +
        ball.radius >=
        canvas.width
    ) {

        ball.x =
            canvas.width -
            ball.radius;

        ball.dx =
            -Math.abs(ball.dx);
    }


    // 위쪽 벽

    if (
        ball.y -
        ball.radius <= 0
    ) {

        ball.y =
            ball.radius;

        ball.dy =
            Math.abs(ball.dy);
    }


    // 패들 충돌

    if (

        ball.dy > 0 &&

        ball.y +
        ball.radius >=
        paddle.y &&

        ball.y -
        ball.radius <=
        paddle.y +
        paddle.height &&

        ball.x >=
        paddle.x &&

        ball.x <=
        paddle.x +
        paddle.width

    ) {

        const center =
            paddle.x +
            paddle.width / 2;

        const distance =
            (
                ball.x -
                center
            )
            /
            (
                paddle.width / 2
            );

        const speed =
            Math.sqrt(
                ball.dx * ball.dx +
                ball.dy * ball.dy
            );

        ball.dx =
            speed * distance;

        ball.dy =
            -Math.sqrt(
                Math.max(
                    1,
                    speed * speed -
                    ball.dx * ball.dx
                )
            );

        ball.y =
            paddle.y -
            ball.radius;
    }


    // 바닥

    if (
        ball.y -
        ball.radius >
        canvas.height
    ) {

        loseLife();
    }
}


// ========================================
// 벽돌 충돌
// ========================================

function checkBrickCollision() {

    for (
        let row = 0;
        row < bricks.length;
        row++
    ) {

        for (
            let column = 0;
            column < bricks[row].length;
            column++
        ) {

            const b =
                bricks[row][column];

            if (!b.alive) {
                continue;
            }

            const hit =

                ball.x +
                ball.radius >
                b.x &&

                ball.x -
                ball.radius <
                b.x +
                b.width &&

                ball.y +
                ball.radius >
                b.y &&

                ball.y -
                ball.radius <
                b.y +
                b.height;


            if (hit) {

                b.alive = false;

                ball.dy =
                    -ball.dy;

                score += 10;

                scoreElement.textContent =
                    score;

                updateHighScore();

                checkLevelComplete();

                return;
            }
        }
    }
}


// ========================================
// 최고점수
// ========================================

function updateHighScore() {

    if (
        score > highScore
    ) {

        highScore = score;

        highScoreElement.textContent =
            highScore;

        try {

            localStorage.setItem(
                "brick_breaker_high_score",
                highScore
            );

        } catch (error) {

            // 저장할 수 없는 환경에서도 게임은 계속 진행
        }
    }
}


// ========================================
// 레벨 클리어
// ========================================

function checkLevelComplete() {

    let remaining = 0;

    for (
        let row = 0;
        row < bricks.length;
        row++
    ) {

        for (
            let column = 0;
            column < bricks[row].length;
            column++
        ) {

            if (
                bricks[row][column].alive
            ) {

                remaining++;
            }
        }
    }


    if (remaining === 0) {

        level++;

        levelElement.textContent =
            level;

        if (
            brickConfig.rows < 8
        ) {

            brickConfig.rows++;
        }

        createBricks();

        resetBall();

        resetPaddle();
    }
}


// ========================================
// 목숨
// ========================================

function loseLife() {

    lives--;

    livesElement.textContent =
        lives;

    if (lives <= 0) {

        gameOver();

    } else {

        resetBall();

        resetPaddle();
    }
}


// ========================================
// 게임 시작
// ========================================

function startGame() {

    score = 0;

    lives = 3;

    level = 1;

    brickConfig.rows = 5;

    scoreElement.textContent =
        score;

    livesElement.textContent =
        lives;

    levelElement.textContent =
        level;

    resetBall();

    resetPaddle();

    createBricks();

    running = true;

    paused = false;

    pauseButton.textContent =
        "일시정지";

    startScreen.style.display =
        "none";

    if (animationId !== null) {

        cancelAnimationFrame(
            animationId
        );
    }

    gameLoop();
}


// ========================================
// 게임 오버
// ========================================

function gameOver() {

    running = false;

    paused = false;

    if (animationId !== null) {

        cancelAnimationFrame(
            animationId
        );
    }

    startScreen.style.display =
        "block";

    startScreen.innerHTML = `

        <h2>GAME OVER</h2>

        <p>
            최종 점수 :
            <strong>${score}</strong>
        </p>

        <p>
            도달 레벨 :
            <strong>${level}</strong>
        </p>

        <button id="restartButton">
            다시 시작
        </button>

    `;

    document
        .getElementById("restartButton")
        .addEventListener(
            "click",
            startGame
        );
}


// ========================================
// 일시정지
// ========================================

function togglePause() {

    if (!running) {
        return;
    }

    paused = !paused;

    pauseButton.textContent =
        paused
        ? "계속하기"
        : "일시정지";
}


// ========================================
// 게임 루프
// ========================================

function gameLoop() {

    if (!running) {
        return;
    }

    if (!paused) {

        movePaddle();

        moveBall();

        checkBrickCollision();
    }

    draw();

    animationId =
        requestAnimationFrame(
            gameLoop
        );
}


// ========================================
// 키보드
// ========================================

document.addEventListener(
    "keydown",
    function(event) {

        const key =
            event.key.toLowerCase();

        if (
            key === "arrowleft" ||
            key === "a"
        ) {

            paddle.dx =
                -paddle.speed;

            event.preventDefault();
        }

        if (
            key === "arrowright" ||
            key === "d"
        ) {

            paddle.dx =
                paddle.speed;

            event.preventDefault();
        }

        if (
            key === " "
        ) {

            togglePause();

            event.preventDefault();
        }
    }
);


document.addEventListener(
    "keyup",
    function(event) {

        const key =
            event.key.toLowerCase();

        if (

            key === "arrowleft" ||
            key === "arrowright" ||
            key === "a" ||
            key === "d"

        ) {

            paddle.dx = 0;
        }
    }
);


// ========================================
// 마우스로 패들 조작
// ========================================

canvas.addEventListener(
    "mousemove",
    function(event) {

        const rect =
            canvas.getBoundingClientRect();

        const scale =
            canvas.width /
            rect.width;

        const mouseX =
            (
                event.clientX -
                rect.left
            ) * scale;

        paddle.x =
            mouseX -
            paddle.width / 2;

        if (paddle.x < 0) {

            paddle.x = 0;
        }

        if (
            paddle.x +
            paddle.width >
            canvas.width
        ) {

            paddle.x =
                canvas.width -
                paddle.width;
        }
    }
);


// ========================================
// 모바일 버튼
// ========================================

function moveLeft() {

    paddle.dx =
        -paddle.speed;
}

function moveRight() {

    paddle.dx =
        paddle.speed;
}

function stopMove() {

    paddle.dx = 0;
}


leftButton.addEventListener(
    "mousedown",
    moveLeft
);

rightButton.addEventListener(
    "mousedown",
    moveRight
);

leftButton.addEventListener(
    "mouseup",
    stopMove
);

rightButton.addEventListener(
    "mouseup",
    stopMove
);

leftButton.addEventListener(
    "mouseleave",
    stopMove
);

rightButton.addEventListener(
    "mouseleave",
    stopMove
);


leftButton.addEventListener(
    "touchstart",
    function(event) {

        event.preventDefault();

        moveLeft();
    }
);

rightButton.addEventListener(
    "touchstart",
    function(event) {

        event.preventDefault();

        moveRight();
    }
);

leftButton.addEventListener(
    "touchend",
    function(event) {

        event.preventDefault();

        stopMove();
    }
);

rightButton.addEventListener(
    "touchend",
    function(event) {

        event.preventDefault();

        stopMove();
    }
);


// ========================================
// 버튼
// ========================================

startButton.addEventListener(
    "click",
    startGame
);

pauseButton.addEventListener(
    "click",
    togglePause
);


// ========================================
// 최초 화면
// ========================================

createBricks();

draw();

</script>

</body>

</html>
"""


components.html(
    game_html,
    height=800,
    scrolling=False
)
