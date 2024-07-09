import {InputHandler} from "./InputHandler.js";
import {Bird} from "./Objects/Bird.js";
import {Pipe} from "./Objects/Pipe.js";
import {Scorebox} from "./Objects/Scorebox.js";
import {getAIAction} from "./AI_Handler.js";

const canvas = document.getElementById("gameCanvas");
const fpsElement = document.getElementById("fps");
const context = canvas.getContext("2d");
const playAgainButton = document.getElementById("playAgainBtn");
const gameOverWrapper = document.getElementById("gameOverWrapper");
const scoreLabel = document.getElementById("scoreLabel");

let inputHandler;

let bird;
let scoreBox;
let pipes = [];

let oldTimeStamp = 0;
let lastSpawn = 0;
let gameOver = false;

// Pipe settings
const pipeGap = 190;
const pipeSpeed = 200;
const pipeSpawnInterval = 2000;

// for FPS calculation
let deltaTime;
let fps;

function start() {
    // init objects
    bird = new Bird(canvas, context);
    scoreBox = new Scorebox(context);
    spawnPipe();
    inputHandler = new InputHandler(bird);

    // start game loop
    window.requestAnimationFrame(gameLoop);
}

let lastFlapTime = 0;
async function gameLoop(timestamp) {
    deltaTime = (timestamp - oldTimeStamp) / 1000;

    // Move forward in time with a maximum amount || Limit for very large deltaTime values.
    deltaTime = Math.min(deltaTime, 0.1);
    oldTimeStamp = timestamp;

    fps = Math.round(1 / deltaTime);
    fpsElement.innerHTML = "FPS: " + fps;

    const time = timestamp / 1000;
    const interval = time % 1 >= 0.99 && time % 1 <= 1;
    if (interval && time - lastFlapTime > 0.05) {
        lastFlapTime = time;
        const state = {
            birdRightX: bird.rightHitboxX,
            birdLeftX: bird.leftHitboxX,
            birdBottomY: bird.bottomHitboxY,
            birdTopY: bird.topRightHitboxY,

            nextPipeRightX: pipes[0].headRightX,
            nextPipeLeftX: pipes[0].headLeftX,
            nextPipeBottomY: pipes[0].headBottomY,
            nextPipeTopY: pipes[0].headTopY,

            score: scoreBox.score
        };

        // async request to get AI action
        asyncronousRequest(state);
    }

    update(timestamp, deltaTime);
    draw();

    if (!gameOver) {
        requestAnimationFrame(gameLoop);
    } else {
        console.log("Game has ended");
        scoreLabel.innerText = "Score: " + scoreBox.score;
        gameOverWrapper.hidden = false;
    }
}

function asyncronousRequest(state) {
    console.log("Requesting...");
    getAIAction(state).then(action => {
        console.log("Action received:", action)
        if (action === 1) {
            bird.flap();
        }
    }).catch(error => {
        console.error('Error fetching AI action:', error);
    });
}

function update(timestamp, deltaTime) {
    bird.update(deltaTime);

    if (timestamp - lastSpawn > pipeSpawnInterval) {
        spawnPipe();
        lastSpawn = timestamp;
    }

    pipes.forEach(pipe => pipe.update(deltaTime));
    pipes = pipes.filter(pipe => pipe.headLeftX >= 0 || isNaN(pipe.headLeftX));

        checkCollisions();
}

function spawnPipe() {
    const canvasHeight = canvas.height;

    const upperPipeLength = Math.random() * (canvasHeight / 2);
    const lowerPipeLength = canvasHeight - upperPipeLength - pipeGap;

    pipes.push(new Pipe(canvas, true, pipeSpeed, upperPipeLength));
    pipes.push(new Pipe(canvas, false, pipeSpeed, lowerPipeLength, upperPipeLength + pipeGap));
}

function draw() {
    context.clearRect(0, 0, canvas.width, canvas.height);

    bird.render(context);
    pipes.forEach(pipe => pipe.render(context));
    scoreBox.render(context);
}

let maxVelocity = 0;
let minVelocity = 0;
let timeSinceLastPipe = 0;
function checkCollisions() {
    for (let i = 0; i < pipes.length; i++) {
        const pipe = pipes[i];

        // pipe body
        const collisionWithBody =
            bird.leftHitboxX >= pipe.bodyRightX
            && bird.rightHitboxX <= pipe.bodyLeftX
            && bird.bottomHitboxY >= pipe.bodyBottomY
            && bird.topRightHitboxY <= pipe.bodyTopY;

        // pipe head
        const collisionWithHead =
            bird.leftHitboxX >= pipe.headRightX
            && bird.rightHitboxX <= pipe.headLeftX
            && bird.topRightHitboxY >= pipe.headBottomY
            && bird.bottomHitboxY <= pipe.headTopY;

        if (collisionWithBody || collisionWithHead) {
            gameOver = true;
            break;
        }

        let velocity = bird.velocity;

        if (velocity > maxVelocity) {
            maxVelocity = velocity;
        } else if (velocity < minVelocity) {
            minVelocity = velocity;
        }

        //check if bird passed two pipes vertically and more than 0.5 second has passed before this can happen again
        if (timeSinceLastPipe > 0.5 && bird.x > pipe.x && !pipe.passedByBird && !pipe.isUpsideDown && !pipe.isOffScreen()) {
            pipe.passedByBird = true;
            timeSinceLastPipe = 0;
            scoreBox.incrementScore();
        }
    }
    timeSinceLastPipe += deltaTime;
}

function init() {
    window.devicePixelRatio = 1;
    let heightSize = window.innerHeight * 0.7;
    let widthSize = window.innerWidth * 0.7;

    canvas.style.height = heightSize + "px";
    canvas.style.width = widthSize + "px";

    let scale = window.devicePixelRatio;
    canvas.height = Math.floor(heightSize * scale);
    canvas.width = Math.floor(widthSize * scale);
    context.scale(scale, scale);
}

playAgainButton.addEventListener("click", () => {
    location.reload();
});

document.addEventListener("DOMContentLoaded", () => {
    init();
    start();
});
