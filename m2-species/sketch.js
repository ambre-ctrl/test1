/**
 * M2 物種 3D 運動學模型：羽狀流體輪傘獸 / 三維步進水母 (Pneumatoumbrella calcigrada)
 * 專案：後未來動物園 (Post-Future Zoo)
 * 創作者：李蕙希 (ambre-ctrl)
 * 
 * 核心機制：
 * 水力推進「羽狀流體輪傘」（Pneumatic Umbellate Propulsion）
 * 1. 水中模式：前後兩組半透明羽狀輪傘「交替開合脈衝」，藉肌肉擠壓水囊高速噴流前進。
 * 2. 岩壁模式：羽傘邊緣吸盤與微孔貼附石灰岩，藉傘緣局部蠕動波如「肉質花朵」步進爬行。
 * 3. 捕食模式：前後雙傘化為液壓雙向抓握夾具，向中心猛烈扣合包覆並捏碎獵物。
 * 視覺美學：漆黑暗河中如同一朵呼吸張合的「紫色琉璃花」，兼具柔美與機械獵奇感。
 */

let creature;
let cavernParticles = [];
let jetParticles = [];
let crushSparks = [];
let viewMode = 'solid'; // 'solid' (紫色琉璃半透明面) 或 'wireframe' (幾何神經骨架)
let activeMode = 'swim'; // 'swim' (暗河水力脈衝), 'creep' (岩壁肉質步進), 'crush' (雙傘捕食抓握)

function setup() {
  createCanvas(windowWidth, windowHeight, WEBGL);
  smooth();
  
  // 建立「羽狀流體輪傘獸」實例
  creature = new UmbellateMedusa();

  // 初始化深層溶洞碳酸鈣微晶 (CaCO3) 與水下微光浮游粒
  for (let i = 0; i < 75; i++) {
    cavernParticles.push({
      pos: createVector(random(-700, 700), random(-500, 500), random(-600, 600)),
      rot: createVector(random(TWO_PI), random(TWO_PI), random(TWO_PI)),
      rotSpeed: createVector(random(-0.015, 0.015), random(-0.015, 0.015), random(-0.015, 0.015)),
      size: random(3, 9),
      floatSpeed: random(0.1, 0.35),
      lum: random(100, 255)
    });
  }
}

function draw() {
  // 深沉溶洞黑水背景
  background(6, 9, 17);

  // 3D 視角軌道控制（滑鼠拖曳旋轉、滾輪縮放）
  orbitControl(1.5, 1.5, 0.1);

  // 預設立體 3/4 視角（讓前後雙羽傘與細長中軸脊椎立體展現）
  rotateX(0.28);
  rotateY(-0.72);

  // 3D 光照系統：冷青環境底光 + 紫晶亮色主光 + 正面微光
  ambientLight(90, 75, 125);
  directionalLight(235, 160, 255, 0.6, 0.8, -0.7); // 紫晶高光主光
  directionalLight(56, 189, 248, -0.7, -0.6, 0.6); // 逆光青藍冷邊緣
  pointLight(244, 114, 182, 0, -200, 200);        // 核心生物光暈

  // 1. 繪製石灰岩壁背景（當在攀爬模式或切換視角時提供空間感）
  if (activeMode === 'creep') {
    drawCavernWallBackdrop();
  }

  // 2. 繪製浮游方解石微晶與水質懸浮物
  drawCavernParticles();

  // 3. 更新並繪製生物水力推進水流微粒與粉碎火花
  updateAndDrawJetParticles();
  updateAndDrawCrushSparks();

  // 4. 更新並繪製輪傘生物
  creature.update();
  creature.draw(viewMode);

  // 5. 更新網頁 HUD 儀表數據
  updateHudDisplay();
}

function windowResized() {
  resizeCanvas(windowWidth, windowHeight);
}

// -------------------------------------------------------------
// 鍵盤與滑鼠互動控制
// -------------------------------------------------------------

function keyPressed() {
  if (key === '1') {
    setMovementMode('swim');
  } else if (key === '2') {
    setMovementMode('creep');
  } else if (key === '3' || key === 'c' || key === 'C') {
    setMovementMode('crush');
  } else if (key === ' ' || keyCode === 32) {
    // 空白鍵切換：紫色琉璃實體面 ↔ 幾何神經骨架線框
    viewMode = viewMode === 'solid' ? 'wireframe' : 'solid';
  } else if (key === 'b' || key === 'B') {
    // 按 B 激發突發水力超壓衝刺
    creature.triggerBurst();
  }
}

function mousePressed() {
  if (mouseButton === LEFT && !keyIsDown(SHIFT)) {
    if (activeMode === 'crush') {
      creature.triggerCrushSnap();
    } else if (activeMode === 'swim') {
      creature.triggerBurst();
    } else if (activeMode === 'creep') {
      creature.triggerWallRippleBurst();
    }
  }
}

function setMovementMode(mode) {
  activeMode = mode;
  creature.setMode(mode);

  // 同步連動 HUD 按鈕高亮狀態
  let btnSwim = document.getElementById('btn-swim');
  let btnCreep = document.getElementById('btn-creep');
  let btnCrush = document.getElementById('btn-crush');
  if (btnSwim && btnCreep && btnCrush) {
    btnSwim.classList.remove('active');
    btnCreep.classList.remove('active');
    btnCrush.classList.remove('active');
    let activeBtn = document.getElementById('btn-' + mode);
    if (activeBtn) activeBtn.classList.add('active');
  }
}

// -------------------------------------------------------------
// 核心生物類別：羽狀流體輪傘獸 (UmbellateMedusa)
// -------------------------------------------------------------

class UmbellateMedusa {
  constructor() {
    this.mode = 'swim'; // 'swim', 'creep', 'crush'

    // 細長中軸脊椎（8 節流線型流體關節）
    this.spineSegments = 8;
    this.spineDist = 28;
    this.spineAngles = new Array(this.spineSegments).fill(0);
    this.spinePitch = new Array(this.spineSegments).fill(0);

    // 前後兩大「羽狀流體輪傘」
    // 前傘 (Anterior Umbel): 10 根羽狀骨架射線，偏向感測與轉向導引
    this.frontUmbel = new FeatherUmbel({
      isFront: true,
      ribCount: 10,
      radius: 88,
      bellHeight: 52,
      baseColor: color(168, 85, 247), // 紫羅蘭晶琉璃
      glowColor: color(56, 189, 248)  // 青藍微電光
    });

    // 後傘 (Posterior Umbel): 12 根羽狀骨架射線，主動力強勁水力推進水囊
    this.backUmbel = new FeatherUmbel({
      isFront: false,
      ribCount: 12,
      radius: 112,
      bellHeight: 66,
      baseColor: color(192, 38, 211), // 洋紫琉璃
      glowColor: color(244, 63, 94)   // 珊瑚紅發光環
    });

    // 生理數值
    this.hydraulicPressure = 120; // 水囊水壓 (kPa)
    this.wallAdhesion = 0;        // 岩壁吸附力 (0 ~ 100%)
    this.pulsePhase = 0;          // 脈衝開合相位
    this.creepPhase = 0;          // 岩壁步進相位
    this.crushT = 0;              // 捕食抓握插值 (0: 放鬆, 1: 緊握粉碎)
    this.swimSpeed = 2.4;         // 當前游速
    this.preyFracture = 0;        // 獵物碎裂度
  }

  setMode(newMode) {
    this.mode = newMode;
    if (newMode === 'crush') {
      this.triggerCrushSnap();
    }
  }

  triggerBurst() {
    this.swimSpeed = 6.2;
    this.hydraulicPressure = 295;
    this.spawnWaterJets(20, true, 'back');
  }

  triggerCrushSnap() {
    this.crushT = 1.0;
    this.hydraulicPressure = 380;
    this.preyFracture = 1.0;
    this.spawnCrushSparks(24);
  }

  triggerWallRippleBurst() {
    this.creepPhase += 1.8;
    this.hydraulicPressure = 195;
  }

  update() {
    if (this.mode === 'swim') {
      this.updateSwimKinematics();
    } else if (this.mode === 'creep') {
      this.updateCreepKinematics();
    } else if (this.mode === 'crush') {
      this.updateCrushKinematics();
    }

    this.frontUmbel.update();
    this.backUmbel.update();

    if (this.preyFracture > 0) {
      this.preyFracture = lerp(this.preyFracture, 0, 0.03);
    }
  }

  // --- 動態 1：暗河水力脈衝游動（交替脈衝開合）---
  updateSwimKinematics() {
    this.pulsePhase += 0.062 * (this.swimSpeed / 2.0);
    this.wallAdhesion = lerp(this.wallAdhesion, 0, 0.05);
    this.swimSpeed = lerp(this.swimSpeed, 2.2, 0.025);
    this.hydraulicPressure = lerp(this.hydraulicPressure, 125, 0.03);
    this.crushT = lerp(this.crushT, 0, 0.08);

    // 交替開合核心機制：
    // 前傘相位 = pulsePhase；後傘相位 = pulsePhase + PI (反相交替開合)
    let frontPulse = sin(this.pulsePhase);
    let backPulse = sin(this.pulsePhase + PI);

    // 當前傘劇烈收縮（排擠水囊噴流）時
    if (frontPulse > 0.82 && frameCount % 3 === 0) {
      this.spawnWaterJets(3, false, 'front');
    }
    // 當後傘劇烈收縮時
    if (backPulse > 0.82 && frameCount % 2 === 0) {
      this.spawnWaterJets(6, false, 'back');
    }

    this.frontUmbel.setPulse(frontPulse, 0);
    this.backUmbel.setPulse(backPulse, 0);

    // 細長中軸脊椎的正弦行進微波
    for (let i = 0; i < this.spineSegments; i++) {
      this.spineAngles[i] = sin(this.pulsePhase * 1.4 - i * 0.45) * 0.12;
      this.spinePitch[i] = cos(this.pulsePhase * 0.8 - i * 0.3) * 0.06;
    }
  }

  // --- 動態 2：岩壁肉質步進（邊緣蠕動波 + 微型吸盤爬行）---
  updateCreepKinematics() {
    this.creepPhase += 0.048;
    this.wallAdhesion = lerp(this.wallAdhesion, 97.2 + sin(this.creepPhase * 2) * 2.2, 0.05);
    this.swimSpeed = lerp(this.swimSpeed, 0.42, 0.04);
    this.hydraulicPressure = lerp(this.hydraulicPressure, 160, 0.03);
    this.crushT = lerp(this.crushT, 0, 0.08);

    // 傘面平鋪於岩壁，邊緣呈現局部行進蠕動波（花朵多足步進）
    this.frontUmbel.setCreep(this.creepPhase, 0.65);
    this.backUmbel.setCreep(this.creepPhase + 1.25, 0.8);

    // 脊椎因攀爬而在石灰岩縫隙間緩慢側弓
    for (let i = 0; i < this.spineSegments; i++) {
      this.spineAngles[i] = sin(this.creepPhase * 0.75 + i * 0.6) * 0.2;
      this.spinePitch[i] = sin(this.creepPhase * 0.5 + i * 0.4) * 0.09;
    }
  }

  // --- 動態 3：雙傘捕食抓握粉碎（高壓扣合夾具）---
  updateCrushKinematics() {
    this.crushT = lerp(this.crushT, 0.35, 0.025); // 扣合捏碎後保持微張咬合
    this.hydraulicPressure = lerp(this.hydraulicPressure, 310, 0.02);
    this.wallAdhesion = lerp(this.wallAdhesion, 88.5, 0.03);
    this.swimSpeed = lerp(this.swimSpeed, 0.08, 0.05);

    // 雙傘同時向內弧形包覆，如同液壓夾爪向中心閉合
    this.frontUmbel.setCrush(this.crushT, true);
    this.backUmbel.setCrush(this.crushT, false);

    // 脊椎因抓握收縮而向中央隆起屈曲
    for (let i = 0; i < this.spineSegments; i++) {
      let arch = sin(map(i, 0, this.spineSegments - 1, 0, PI));
      this.spinePitch[i] = -arch * 0.28 * this.crushT;
      this.spineAngles[i] = sin(frameCount * 0.28) * 0.05 * this.crushT;
    }
  }

  spawnWaterJets(count, isBurst, source = 'back') {
    let zOrigin = source === 'front' ? 45 : -135;
    for (let i = 0; i < count; i++) {
      let spreadX = random(-24, 24);
      let spreadY = random(-24, 24);
      let velZ = isBurst ? random(7, 16) : random(3.5, 9);
      jetParticles.push(new JetParticle(spreadX, spreadY, zOrigin, velZ));
    }
  }

  spawnCrushSparks(count) {
    for (let i = 0; i < count; i++) {
      crushSparks.push(new CrushSpark(0, 0, -12));
    }
  }

  draw(mode) {
    push();
    translate(75, 10, 0);
    scale(1.28);

    if (this.mode === 'swim') {
      let floatBob = sin(this.pulsePhase * 0.8) * 8;
      translate(0, floatBob, 0);
      rotateX(sin(this.pulsePhase * 0.5) * 0.06);
    } else if (this.mode === 'creep') {
      translate(0, 0, -80);
      rotateX(0.22);
    } else if (this.mode === 'crush') {
      translate(0, 0, -40);
    }

    // 1. 繪製前部羽傘（Anterior Feather-Umbel）
    push();
    translate(0, 0, 75);
    if (this.mode === 'crush') {
      rotateX(0.42 * this.crushT);
    }
    this.frontUmbel.draw(mode);
    pop();

    // 2. 繪製細長中軸脊椎（Slender Central Spine Chain）
    this.drawSpine(mode);

    // 3. 繪製後部羽傘（Posterior Feather-Umbel）
    push();
    translate(0, 0, -100);
    if (this.mode === 'crush') {
      rotateY(lerp(PI, 0.15, this.crushT));
      rotateX(-0.42 * this.crushT);
    } else {
      rotateY(PI);
    }
    this.backUmbel.draw(mode);
    pop();

    // 4. 若在捕食模式，繪製被雙傘包覆捏碎的發光生物獵物
    if (this.mode === 'crush') {
      this.drawTrappedPrey(mode);
    }

    pop();
  }

  // 繪製細長中軸脊椎
  drawSpine(mode) {
    push();
    translate(0, 0, 60);

    for (let i = 0; i < this.spineSegments; i++) {
      rotateY(this.spineAngles[i]);
      rotateX(this.spinePitch[i]);

      push();
      if (mode === 'wireframe') {
        noFill();
        stroke(168, 85, 247, 180);
        strokeWeight(1.2);
        box(14, 12, this.spineDist * 0.9);
      } else {
        // 外層半透明紫色琉璃骨鞘
        fill(147, 51, 234, 160);
        stroke(216, 180, 254, 180);
        strokeWeight(0.9);
        box(14, 11, this.spineDist * 0.88);

        // 內部紫紅微光水力管道
        fill(236, 72, 153, 230);
        noStroke();
        box(5, 5, this.spineDist * 0.95);
      }
      pop();

      translate(0, 0, -this.spineDist);
    }
    pop();
  }

  // 繪製中央被捏碎的獵物節點
  drawTrappedPrey(mode) {
    push();
    translate(0, 0, -12);
    let crushP = 1.0 - this.crushT * 0.65;
    scale(crushP, crushP, crushP * 0.7);

    if (mode === 'wireframe') {
      stroke(244, 63, 94);
      strokeWeight(1.5);
      noFill();
      box(16);
    } else {
      fill(244, 63, 94, 220);
      stroke(255, 200, 210);
      strokeWeight(1.0);
      box(15, 12, 18);

      fill(56, 189, 248, 180);
      noStroke();
      sphere(8 * (1 + sin(frameCount * 0.5) * 0.2));
    }
    pop();
  }
}

// -------------------------------------------------------------
// 羽狀流體輪傘類別 (FeatherUmbel)
// 包含水囊核心、羽狀骨架射線、琉璃薄膜、微型噴孔與邊緣吸盤
// -------------------------------------------------------------

class FeatherUmbel {
  constructor(cfg) {
    this.isFront = cfg.isFront;
    this.ribCount = cfg.ribCount;
    this.radius = cfg.radius;
    this.bellHeight = cfg.bellHeight;
    this.baseColor = cfg.baseColor;
    this.glowColor = cfg.glowColor;

    this.openFactor = 0.5;
    this.creepPhase = 0;
    this.creepStrength = 0;
    this.isCrushing = false;
    this.crushT = 0;
    this.sacPulse = 1.0;
  }

  setPulse(val, crushVal) {
    this.openFactor = map(val, -1, 1, 0.95, 0.28);
    this.sacPulse = map(val, -1, 1, 0.8, 1.35);
    this.creepStrength = 0;
    this.isCrushing = false;
  }

  setCreep(phase, strength) {
    this.openFactor = 0.88;
    this.creepPhase = phase;
    this.creepStrength = strength;
    this.isCrushing = false;
  }

  setCrush(t, isFront) {
    this.crushT = t;
    this.isCrushing = true;
    this.openFactor = map(t, 0, 1, 0.82, 0.16);
    this.sacPulse = 1.0 + t * 0.5;
  }

  update() {}

  draw(mode) {
    push();

    // 1. 中央水囊肌肉腔體
    this.drawHydraulicSac(mode);

    // 2. 傘骨羽狀射線陣列
    let ribTipCoords = [];
    for (let r = 0; r < this.ribCount; r++) {
      let theta = (TWO_PI / this.ribCount) * r;
      let coords = this.drawRib(r, theta, mode);
      ribTipCoords.push(coords);
    }

    // 3. 羽傘相鄰骨架間的「紫色琉璃半透明膜」
    this.drawMembranes(ribTipCoords, mode);

    pop();
  }

  drawHydraulicSac(mode) {
    push();
    let sH = this.bellHeight * 0.55 * this.sacPulse;
    let sR = (this.radius * 0.32) * (2 - this.sacPulse * 0.8);

    if (mode === 'wireframe') {
      stroke(this.glowColor);
      strokeWeight(1.2);
      noFill();
      cylinder(sR, sH, 8, 1);
    } else {
      fill(red(this.baseColor), green(this.baseColor), blue(this.baseColor), 180);
      stroke(230, 200, 255, 180);
      strokeWeight(0.9);
      cylinder(sR, sH, 12, 1);

      push();
      fill(red(this.glowColor), green(this.glowColor), blue(this.glowColor), 220);
      noStroke();
      sphere(sR * 0.45);
      pop();
    }
    pop();
  }

  drawRib(idx, theta, mode) {
    push();
    rotateZ(theta);

    let flareAngle = map(this.openFactor, 0.2, 1.0, 0.35, 1.45);

    if (this.creepStrength > 0) {
      let wave = sin(this.creepPhase * 2.8 + theta * 3);
      flareAngle += wave * 0.38 * this.creepStrength;
    }

    let tipCurl = 0;
    if (this.isCrushing) {
      flareAngle = lerp(flareAngle, 0.18, this.crushT);
      tipCurl = this.crushT * 1.1;
    }

    let ribLen1 = this.radius * 0.48;
    let ribLen2 = this.radius * 0.55;

    // 第一段傘骨
    rotateY(flareAngle);
    if (mode === 'wireframe') {
      stroke(this.glowColor);
      strokeWeight(1.5);
      noFill();
    } else {
      fill(red(this.baseColor) + 20, green(this.baseColor) + 20, blue(this.baseColor) + 40, 220);
      stroke(230, 210, 255, 180);
      strokeWeight(1.0);
    }

    push();
    translate(0, 0, ribLen1 * 0.5);
    box(3.8, 3.8, ribLen1);
    pop();

    this.drawPinnules(ribLen1, mode);

    translate(0, 0, ribLen1);

    // 第二段傘骨
    rotateY(0.25 - tipCurl);
    push();
    translate(0, 0, ribLen2 * 0.5);
    box(3.0, 2.4, ribLen2);
    pop();

    translate(0, 0, ribLen2);
    this.drawNozzleAndSuction(mode);

    let totalAngle = flareAngle + 0.25 - tipCurl;
    let localZ = ribLen1 * cos(flareAngle) + ribLen2 * cos(totalAngle);
    let localDist = ribLen1 * sin(flareAngle) + ribLen2 * sin(totalAngle);
    let endX = cos(theta) * localDist;
    let endY = sin(theta) * localDist;

    pop();

    return { x: endX, y: endY, z: localZ };
  }

  drawPinnules(len, mode) {
    if (mode === 'wireframe') return;

    let numPinn = 3;
    for (let p = 1; p <= numPinn; p++) {
      let pz = (len / (numPinn + 1)) * p;
      let pLen = 14 * (1 - p * 0.2);

      for (let side of [-1, 1]) {
        push();
        translate(0, 0, pz);
        rotateX(side * 0.7);
        fill(216, 180, 254, 180);
        stroke(168, 85, 247, 120);
        strokeWeight(0.7);
        translate(0, side * pLen * 0.5, 0);
        box(1.8, pLen, 1.8);
        pop();
      }
    }
  }

  drawNozzleAndSuction(mode) {
    push();
    if (mode === 'wireframe') {
      stroke(56, 189, 248);
      strokeWeight(1.8);
      noFill();
      sphere(3.2);
    } else {
      fill(56, 189, 248, 230);
      stroke(186, 230, 253, 220);
      strokeWeight(0.9);
      torus(3.4, 1.3, 6, 8);

      fill(15, 23, 42);
      noStroke();
      sphere(1.6);
    }
    pop();
  }

  drawMembranes(tipCoords, mode) {
    if (mode === 'wireframe') {
      stroke(168, 85, 247, 110);
      strokeWeight(1.0);
      noFill();
      beginShape();
      for (let pt of tipCoords) {
        vertex(pt.x, pt.y, pt.z);
      }
      endShape(CLOSE);
      return;
    }

    noStroke();
    for (let i = 0; i < tipCoords.length; i++) {
      let p1 = tipCoords[i];
      let p2 = tipCoords[(i + 1) % tipCoords.length];

      // 漸層琉璃紫膜
      fill(red(this.baseColor), green(this.baseColor), blue(this.baseColor), 115);
      beginShape(TRIANGLES);
      vertex(0, 0, 0);
      vertex(p1.x, p1.y, p1.z);
      vertex(p2.x, p2.y, p2.z);
      endShape();

      // 外緣發光弧線
      stroke(244, 114, 182, 190);
      strokeWeight(1.2);
      line(p1.x, p1.y, p1.z, p2.x, p2.y, p2.z);
      noStroke();
    }
  }
}

// -------------------------------------------------------------
// 水力推進噴流微粒系統 (Jet Bubble Particle)
// -------------------------------------------------------------

class JetParticle {
  constructor(x, y, z, vZ) {
    this.pos = createVector(x, y, z);
    this.vel = createVector(random(-0.8, 0.8), random(-0.8, 0.8), -vZ);
    this.size = random(3, 7.5);
    this.life = 255;
    this.decay = random(6, 12);
  }

  update() {
    this.pos.add(this.vel);
    this.vel.mult(0.94);
    this.life -= this.decay;
  }

  draw() {
    push();
    translate(this.pos.x, this.pos.y, this.pos.z);
    noStroke();
    fill(147, 197, 253, map(this.life, 0, 255, 0, 200));
    sphere(this.size * (this.life / 255));
    pop();
  }
}

function updateAndDrawJetParticles() {
  for (let i = jetParticles.length - 1; i >= 0; i--) {
    let p = jetParticles[i];
    p.update();
    p.draw();
    if (p.life <= 0) {
      jetParticles.splice(i, 1);
    }
  }
}

// -------------------------------------------------------------
// 捕食粉碎噴發微粒火花 (Crush Spark Particle)
// -------------------------------------------------------------

class CrushSpark {
  constructor(x, y, z) {
    this.pos = createVector(x + random(-5, 5), y + random(-5, 5), z + random(-5, 5));
    this.vel = p5.Vector.random3D().mult(random(3, 8));
    this.size = random(2, 5);
    this.life = 255;
    this.decay = random(10, 20);
  }

  update() {
    this.pos.add(this.vel);
    this.vel.mult(0.92);
    this.life -= this.decay;
  }

  draw() {
    push();
    translate(this.pos.x, this.pos.y, this.pos.z);
    noStroke();
    fill(244, 63, 94, this.life);
    box(this.size * (this.life / 255));
    pop();
  }
}

function updateAndDrawCrushSparks() {
  for (let i = crushSparks.length - 1; i >= 0; i--) {
    let s = crushSparks[i];
    s.update();
    s.draw();
    if (s.life <= 0) {
      crushSparks.splice(i, 1);
    }
  }
}

// -------------------------------------------------------------
// 溶洞環境背景與方解石晶體
// -------------------------------------------------------------

function drawCavernParticles() {
  push();
  noStroke();
  for (let p of cavernParticles) {
    p.pos.y += p.floatSpeed;
    if (p.pos.y > 500) p.pos.y = -500;

    p.rot.x += p.rotSpeed.x;
    p.rot.y += p.rotSpeed.y;

    push();
    translate(p.pos.x, p.pos.y, p.pos.z);
    rotateX(p.rot.x);
    rotateY(p.rot.y);
    fill(216, 180, 254, map(p.lum, 0, 255, 30, 95));
    box(p.size);
    pop();
  }
  pop();
}

// 攀爬模式下的石灰岩石壁格網背景
function drawCavernWallBackdrop() {
  push();
  translate(0, 0, -180);
  stroke(30, 41, 59, 120);
  strokeWeight(1.0);
  noFill();

  let gridSize = 800;
  let step = 60;
  for (let x = -gridSize; x <= gridSize; x += step) {
    line(x, -gridSize, 0, x, gridSize, 0);
  }
  for (let y = -gridSize; y <= gridSize; y += step) {
    line(-gridSize, y, 0, gridSize, y, 0);
  }
  pop();
}

// -------------------------------------------------------------
// HUD 即時儀表介面數據連動
// -------------------------------------------------------------

function updateHudDisplay() {
  const pressureElem = document.getElementById('hud-pressure');
  const speedElem = document.getElementById('hud-speed');
  const adhesionElem = document.getElementById('hud-adhesion');
  const modeElem = document.getElementById('hud-active-mode');
  const renderElem = document.getElementById('hud-render-mode');

  if (pressureElem) pressureElem.innerText = round(creature.hydraulicPressure) + ' kPa';
  if (speedElem) speedElem.innerText = (creature.swimSpeed * 1.8).toFixed(1) + ' cm/s';
  if (adhesionElem) adhesionElem.innerText = creature.wallAdhesion.toFixed(1) + ' %';
  
  if (modeElem) {
    if (activeMode === 'swim') {
      modeElem.innerText = '水力脈衝高速推進 (Aquatic Jet)';
      modeElem.style.color = '#38bdf8';
    } else if (activeMode === 'creep') {
      modeElem.innerText = '岩壁肉質花朵步進 (Wall Creeping)';
      modeElem.style.color = '#a855f7';
    } else if (activeMode === 'crush') {
      modeElem.innerText = '雙傘液壓抓握粉碎 (Predatory Crush)';
      modeElem.style.color = '#f43f5e';
    }
  }

  if (renderElem) {
    renderElem.innerText = viewMode === 'solid' ? '紫色琉璃半透明膜 (Amethyst Glass)' : '幾何神經骨架 (Kinetic Wireframe)';
    renderElem.style.color = viewMode === 'solid' ? '#e879f9' : '#38bdf8';
  }
}
