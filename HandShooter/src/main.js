// src/main.js

// ==== DOM Elements ====
const startScreen = document.getElementById('start-screen');
const gameContainer = document.getElementById('game-container');
const nicknameInput = document.getElementById('nickname-input');
const startButton = document.getElementById('start-button');
const nicknameDisplay = document.getElementById('nickname-display');

const videoElement = document.getElementById('webcam');
const canvasElement = document.getElementById('output_canvas');
const canvasCtx = canvasElement.getContext('2d');

const scoreDisplay = document.getElementById('score-display');
const ammoDisplay = document.getElementById('ammo-display');
const reloadWarning = document.getElementById('reload-warning');

// ==== State Variables ====
let score = 0;
let ammo = 10;
const MAX_AMMO = 10;
let playerName = "";

let previousGesture = 'NONE';
let flashFrames = 0;
let hitPoint = {x: 0, y: 0};

let fruits = [];
const FRUIT_TYPES = ['🍎', '🍏', '🍊', '🍇', '🍉', '🍌', '🍓', '🍒'];

// 캔버스 사이즈 (왜곡 방지를 위한 고정)
canvasElement.width = 800;
canvasElement.height = 600;

// ==== 이벤트 리스너 ====
nicknameInput.addEventListener('keypress', (e) => {
    if (e.key === 'Enter') startButton.click();
});

startButton.addEventListener('click', () => {
    const val = nicknameInput.value.trim();
    if (!val) {
        alert("닉네임을 입력해주세요!");
        nicknameInput.focus();
        return;
    }
    
    // 시작 처리
    playerName = val;
    nicknameDisplay.innerText = playerName;
    
    startScreen.classList.add('hidden');
    gameContainer.classList.remove('hidden');
    
    startGame();
});

// ==== 게임 로직 함수 ====
function spawnFruit() {
    const size = 150 + Math.random() * 60; // 과일을 엄청나게 키움 (최대 210px)
    const x = canvasElement.width * 0.1 + Math.random() * canvasElement.width * 0.8;
    fruits.push({
        id: Date.now() + Math.random(),
        x: x,
        y: -100,
        emoji: FRUIT_TYPES[Math.floor(Math.random() * FRUIT_TYPES.length)],
        size: size,
        speed: 3 + Math.random() * 4,
        rotation: Math.random() * Math.PI * 2,
        rotSpeed: (Math.random() - 0.5) * 0.1
    });
}

// ==== MediaPipe Hands 설정 ====
const hands = new Hands({locateFile: (file) => {
    return `https://cdn.jsdelivr.net/npm/@mediapipe/hands/${file}`;
}});

hands.setOptions({
    maxNumHands: 1,
    modelComplexity: 1,
    minDetectionConfidence: 0.6,
    minTrackingConfidence: 0.6
});

let latestResults = null;
hands.onResults((results) => {
    latestResults = results;
});

const camera = new Camera(videoElement, {
    onFrame: async () => {
        await hands.send({image: videoElement});
    },
    width: 640,
    height: 480
});

// 3차원 거리 연산식 (원근감 및 깊이 Z축 포함)
function getDistance3D(lm1, lm2) {
    return Math.hypot(lm1.x - lm2.x, lm1.y - lm2.y, (lm1.z || 0) - (lm2.z || 0));
}

let debugGesture = '인식 대기 중';

function checkGestures(landmarks) {
    // 1) 손가락 펴짐 유무: 3차원 상에서 손끝(Tip)이 손목(0)에서 두 번째 마디(PIP)보다 더 먼가?
    // 이 방식을 사용하면 손가락이 위를 향하든 화면 앞(카메라)을 찌르든 완벽하게 '펴진 상태'를 인식합니다.
    const isIndexExtended = getDistance3D(landmarks[8], landmarks[0]) > getDistance3D(landmarks[6], landmarks[0]);
    const isMiddleExtended = getDistance3D(landmarks[12], landmarks[0]) > getDistance3D(landmarks[10], landmarks[0]);
    const isRingExtended = getDistance3D(landmarks[16], landmarks[0]) > getDistance3D(landmarks[14], landmarks[0]);
    const isPinkyExtended = getDistance3D(landmarks[20], landmarks[0]) > getDistance3D(landmarks[18], landmarks[0]);
    
    // 2) 카메라 방향(Forward)을 정통으로 가리키고 있는지 확인 (Z축 깊이 비교)
    // MediaPipe에서 z좌표가 작을(음수일)수록 카메라 렌즈와 물리적으로 가깝습니다. 
    // 검지 손끝(8)이 마디(5)보다 확실히 카메라 쪽으로 튀어나와 있는가?
    const isPointingForward = landmarks[8].z < landmarks[5].z - 0.015;

    // 3) 엄지 상태: 엄지가 펴져 있는지 여부 (검지 밑둥 5번과의 3차원 거리)
    const thumbDistToIndexBase = getDistance3D(landmarks[4], landmarks[5]);
    const isThumbUp = thumbDistToIndexBase > 0.1; // 0.1 이상 멀어지면 펴진 상태

    // 4) 검지와 중지가 딱 붙어있는가?
    const indexMiddleDist = getDistance3D(landmarks[8], landmarks[12]);
    const isIndexMiddleTogether = indexMiddleDist < 0.15; 

    let currentGesture = 'NONE';

    // 주먹 모양 (4개 손가락 모두 확실하게 접힘)
    if (!isIndexExtended && !isMiddleExtended && !isRingExtended && !isPinkyExtended) {
        currentGesture = 'RELOAD'; 
    } 
    // 총 모양 (검/중 펴고 나머진 접혔으며, 검지/중지가 같이 붙어있음)
    else if (isIndexExtended && isMiddleExtended && !isRingExtended && !isPinkyExtended && isIndexMiddleTogether) {
        // 총구가 정확히 '카메라 방향(화면 앞)'을 단단하게 가리킬 때만 '조준 및 발사' 모드로 진입 인정!
        if (isPointingForward) {
            if (isThumbUp) {
                currentGesture = 'GUN_SHAPE'; // 엄지 세움 = 조준
            } else {
                currentGesture = 'SHOOT'; // 엄지 접음 = 발사
            }
        }
    }

    debugGesture = currentGesture; // 디버그 UI 출력용 갱신

    if (currentGesture === 'RELOAD') {
        if (previousGesture !== 'RELOAD') {
            ammo = MAX_AMMO;
            updateUI();
        }
    } else if (currentGesture === 'SHOOT' && previousGesture !== 'SHOOT') { 
        if (ammo > 0) {
            // 발사 동작!
            ammo--;
            updateUI();
            
            // 조준점 위치로 피격 판정
            let canvasX = landmarks[8].x * canvasElement.width;
            let canvasY = landmarks[8].y * canvasElement.height;
            
            fireShot(canvasX, canvasY);
        }
    }
    
    previousGesture = currentGesture;
}

function fireShot(x, y) {
    hitPoint = {x, y};
    flashFrames = 10;
    const HIT_RADIUS = 110; 
    let hitIndex = -1;
    
    for (let i = fruits.length - 1; i >= 0; i--) {
        const f = fruits[i];
        const dist = Math.hypot(f.x - x, f.y - y);
        if (dist < HIT_RADIUS) {
            hitIndex = i;
            break;
        }
    }

    if (hitIndex !== -1) {
        createHitParticles(fruits[hitIndex].x, fruits[hitIndex].y);
        fruits.splice(hitIndex, 1);
        score += 100;
        updateUI();
    }
}

let particles = [];
function createHitParticles(x, y) {
    for(let i=0; i<12; i++){
        particles.push({
            x: x, y: y,
            vx: (Math.random()-0.5)*20,
            vy: (Math.random()-0.5)*20,
            life: 25
        });
    }
}

function updateUI() {
    scoreDisplay.innerText = `Score: ${score}`;
    ammoDisplay.innerText = `Ammo: ${ammo} / ${MAX_AMMO}`;
    
    if (ammo <= 0) {
        reloadWarning.classList.remove('hidden');
    } else {
        reloadWarning.classList.add('hidden');
    }
}

function gameLoop() {
    canvasCtx.save();
    canvasCtx.clearRect(0, 0, canvasElement.width, canvasElement.height);

    if (latestResults && latestResults.image) {
        canvasCtx.drawImage(latestResults.image, 0, 0, canvasElement.width, canvasElement.height);

        if (latestResults.multiHandLandmarks && latestResults.multiHandLandmarks.length > 0) {
            const landmarks = latestResults.multiHandLandmarks[0];
            
            checkGestures(landmarks);

            const indexX = landmarks[8].x * canvasElement.width;
            const indexY = landmarks[8].y * canvasElement.height;
            
            // 강렬하고 눈에 확 띄는 FPS 스타일 크로스헤어
            const aimSize = 25; 
            const crossColor = ammo > 0 ? '#FF0000' : '#888'; 
            const crossColorAlpha = ammo > 0 ? 'rgba(255, 0, 0, 0.85)' : 'rgba(136, 136, 136, 0.85)';
            
            canvasCtx.beginPath();
            canvasCtx.arc(indexX, indexY, 6, 0, Math.PI*2);
            canvasCtx.fillStyle = crossColor;
            canvasCtx.fill();

            canvasCtx.beginPath();
            canvasCtx.arc(indexX, indexY, aimSize, 0, Math.PI*2);
            canvasCtx.strokeStyle = crossColorAlpha;
            canvasCtx.lineWidth = 5;
            canvasCtx.setLineDash([10, 10]); 
            canvasCtx.stroke();
            canvasCtx.setLineDash([]); 
            
            canvasCtx.beginPath();
            canvasCtx.moveTo(indexX, indexY - aimSize - 4); canvasCtx.lineTo(indexX, indexY - aimSize - 20);
            canvasCtx.moveTo(indexX, indexY + aimSize + 4); canvasCtx.lineTo(indexX, indexY + aimSize + 20);
            canvasCtx.moveTo(indexX - aimSize - 4, indexY); canvasCtx.lineTo(indexX - aimSize - 20, indexY);
            canvasCtx.moveTo(indexX + aimSize + 4, indexY); canvasCtx.lineTo(indexX + aimSize + 20, indexY);
            canvasCtx.strokeStyle = crossColor;
            canvasCtx.lineWidth = 7; 
            canvasCtx.stroke();
        }
    }

    canvasCtx.textAlign = 'center';
    canvasCtx.textBaseline = 'middle';
    fruits.forEach(f => {
        f.y += f.speed;
        f.rotation += f.rotSpeed;
        
        canvasCtx.save();
        canvasCtx.translate(f.x, f.y);
        canvasCtx.rotate(f.rotation);
        canvasCtx.font = `${f.size}px Arial`;
        canvasCtx.fillText(f.emoji, 0, 0);
        canvasCtx.restore();
    });

    fruits = fruits.filter(f => f.y < canvasElement.height + 150);

    // 하단에 제스처 상태를 알려주는 디버거 UI 추가
    canvasCtx.save();
    // 캔버스 자체의 거울 모드(CSS scaleX:-1)를 상쇄하여 글자가 똑바로 보이게 뒤집음
    canvasCtx.translate(canvasElement.width, 0);
    canvasCtx.scale(-1, 1);

    canvasCtx.fillStyle = 'rgba(0, 0, 0, 0.6)';
    canvasCtx.fillRect(0, canvasElement.height - 40, canvasElement.width, 40);
    canvasCtx.fillStyle = '#fff';
    canvasCtx.font = '24px Jua';
    canvasCtx.textAlign = 'center';
    canvasCtx.textBaseline = 'middle';
    
    let gestureKor = (debugGesture === 'GUN_SHAPE') ? '조준 중' : 
                     (debugGesture === 'SHOOT') ? '발사!' : 
                     (debugGesture === 'RELOAD') ? '장전 모션' : '인식 불가';
                     
    canvasCtx.fillText(`현재 인식 상태: ${gestureKor} (${debugGesture})`, canvasElement.width / 2, canvasElement.height - 20);
    canvasCtx.restore();

    for(let i=particles.length-1; i>=0; i--){
        let p = particles[i];
        p.x += p.vx;
        p.y += p.vy;
        p.life--;
        canvasCtx.fillStyle = `rgba(255, 200, 50, ${p.life/25})`;
        canvasCtx.beginPath();
        canvasCtx.arc(p.x, p.y, p.life/2 + 2, 0, Math.PI*2);
        canvasCtx.fill();
        if(p.life <= 0) particles.splice(i, 1);
    }

    if (flashFrames > 0) {
        flashFrames--;
        canvasCtx.beginPath();
        canvasCtx.arc(hitPoint.x, hitPoint.y, 50 + flashFrames*3, 0, Math.PI * 2);
        canvasCtx.fillStyle = `rgba(255, 255, 0, ${flashFrames / 10})`;
        canvasCtx.fill();
        
        canvasCtx.beginPath();
        canvasCtx.arc(hitPoint.x, hitPoint.y, 25 + flashFrames*2, 0, Math.PI * 2);
        canvasCtx.fillStyle = `rgba(255, 255, 255, ${flashFrames / 10})`;
        canvasCtx.fill();
    }

    canvasCtx.restore();
    requestAnimationFrame(gameLoop);
}

// ==== 최초 시작 함수 ====
function startGame() {
    camera.start();
    setInterval(spawnFruit, 800);
    requestAnimationFrame(gameLoop);
}
