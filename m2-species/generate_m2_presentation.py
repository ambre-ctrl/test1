import os
import subprocess

OUTPUT_DIR = "/Users/cheng-kuanglee/post-future-zoo/m2-species"
CHROME_PATH = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"

SLIDES_HTML = os.path.join(OUTPUT_DIR, "m2-slides.html")
PDF_PATH = os.path.join(OUTPUT_DIR, "m2-簡報.pdf")

html_content = """<!DOCTYPE html>
<html lang="zh-TW">
<head>
<meta charset="UTF-8">
<title>M2 物種簡報：羽狀流體輪傘獸｜後未來動物園</title>
<style>
  @import url('https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@500;700&family=Noto+Sans+TC:wght@400;500;700;900&display=swap');

  @page {
    size: 1920px 1080px;
    margin: 0;
  }

  * {
    box-sizing: border-box;
    margin: 0;
    padding: 0;
  }

  body {
    background-color: #060911;
    color: #f1f5f9;
    font-family: -apple-system, BlinkMacSystemFont, "Space Grotesk", "Noto Sans TC", "PingFang TC", sans-serif;
    -webkit-font-smoothing: antialiased;
  }

  .slide {
    width: 1920px;
    height: 1080px;
    position: relative;
    padding: 60px 85px;
    background: radial-gradient(circle at 85% 15%, rgba(168, 85, 247, 0.14) 0%, transparent 45%),
                radial-gradient(circle at 10% 85%, rgba(56, 189, 248, 0.09) 0%, transparent 45%),
                #060911;
    overflow: hidden;
    page-break-after: always;
    display: flex;
    flex-direction: column;
  }

  .grid-bg {
    position: absolute;
    inset: 0;
    background-image: linear-gradient(rgba(255, 255, 255, 0.02) 1px, transparent 1px),
                      linear-gradient(90deg, rgba(255, 255, 255, 0.02) 1px, transparent 1px);
    background-size: 50px 50px;
    pointer-events: none;
  }

  .header {
    display: flex;
    justify-content: space-between;
    align-items: flex-end;
    margin-bottom: 32px;
    position: relative;
    z-index: 2;
    border-bottom: 1px solid rgba(168, 85, 247, 0.3);
    padding-bottom: 16px;
  }

  .tag {
    font-size: 13.5px;
    letter-spacing: 2.5px;
    text-transform: uppercase;
    color: #e879f9;
    font-weight: 700;
    display: flex;
    align-items: center;
    gap: 8px;
  }

  .tag::before {
    content: "";
    display: inline-block;
    width: 8px;
    height: 8px;
    background: #e879f9;
    border-radius: 50%;
    box-shadow: 0 0 10px #e879f9;
  }

  .title {
    font-size: 40px;
    font-weight: 900;
    color: #ffffff;
    letter-spacing: -0.5px;
    margin-top: 5px;
  }

  .slide-num {
    font-family: 'Space Grotesk', monospace;
    font-size: 24px;
    color: #64748b;
    font-weight: 700;
  }

  .content-area {
    flex: 1;
    position: relative;
    z-index: 2;
    display: flex;
    gap: 40px;
  }

  .card {
    background: rgba(15, 23, 42, 0.72);
    border: 1px solid rgba(255, 255, 255, 0.08);
    border-radius: 14px;
    padding: 20px 24px;
    backdrop-filter: blur(14px);
  }

  .card-highlight {
    border-color: rgba(168, 85, 247, 0.45);
    background: linear-gradient(135deg, rgba(168, 85, 247, 0.14), rgba(15, 23, 42, 0.8));
    box-shadow: 0 10px 30px rgba(0, 0, 0, 0.4);
  }

  .card h3 {
    font-size: 20px;
    color: #e879f9;
    margin-bottom: 8px;
    display: flex;
    align-items: center;
    gap: 8px;
  }

  .card p, .card li {
    font-size: 16px;
    color: #cbd5e1;
    line-height: 1.65;
  }

  .badge {
    display: inline-block;
    padding: 3px 8px;
    border-radius: 4px;
    font-size: 12px;
    font-weight: 700;
    margin-right: 6px;
  }
  .badge-purple { background: rgba(168, 85, 247, 0.25); color: #d8b4fe; border: 1px solid rgba(168, 85, 247, 0.5); }
  .badge-cyan { background: rgba(56, 189, 248, 0.2); color: #38bdf8; border: 1px solid rgba(56, 189, 248, 0.4); }
  .badge-pink { background: rgba(244, 63, 94, 0.2); color: #fb7185; border: 1px solid rgba(244, 63, 94, 0.4); }

  .preview-container {
    width: 100%;
    height: 100%;
    border-radius: 16px;
    overflow: hidden;
    border: 1px solid rgba(168, 85, 247, 0.35);
    box-shadow: 0 16px 40px rgba(0, 0, 0, 0.8);
    background: #0a0f1d;
  }
  .preview-container img {
    width: 100%;
    height: 100%;
    object-fit: cover;
  }

  /* 封面特殊樣式 */
  .cover-slide {
    justify-content: center;
    align-items: center;
    text-align: center;
    padding: 80px 100px;
  }
  .cover-badge {
    display: inline-block;
    padding: 8px 24px;
    background: rgba(168, 85, 247, 0.18);
    border: 1px solid rgba(168, 85, 247, 0.45);
    color: #e879f9;
    font-size: 15px;
    letter-spacing: 3px;
    border-radius: 50px;
    margin-bottom: 24px;
    text-transform: uppercase;
    font-weight: 700;
  }
  .cover-title {
    font-size: 72px;
    font-weight: 900;
    line-height: 1.15;
    margin-bottom: 20px;
    background: linear-gradient(135deg, #ffffff 30%, #e879f9 75%, #38bdf8 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
  }
  .cover-sub {
    font-size: 24px;
    color: #94a3b8;
    max-width: 1100px;
    line-height: 1.6;
    margin-bottom: 40px;
  }
  .cover-world-box {
    background: rgba(15, 23, 42, 0.7);
    border: 1px solid rgba(56, 189, 248, 0.3);
    padding: 16px 30px;
    border-radius: 12px;
    max-width: 1050px;
    margin-bottom: 45px;
    font-size: 17px;
    color: #38bdf8;
    text-align: left;
  }
  .cover-meta {
    display: flex;
    gap: 50px;
    font-size: 16px;
    color: #cbd5e1;
  }
  .cover-meta div {
    display: flex;
    flex-direction: column;
    gap: 4px;
  }
  .cover-meta span.label {
    font-size: 12px;
    color: #64748b;
    text-transform: uppercase;
    letter-spacing: 1px;
  }
  .cover-meta span.val {
    font-weight: 600;
    color: #f1f5f9;
  }
</style>
</head>
<body>

  <!-- ========================================== -->
  <!-- SLIDE 1: 封面與世界一句話回顧 -->
  <!-- ========================================== -->
  <div class="slide cover-slide">
    <div class="grid-bg"></div>
    <div class="cover-badge">Post-Future Zoo · M2 Species Milestone · 3-Min Presentation</div>
    <div class="cover-title">
      羽狀流體輪傘獸<br>
      <span style="font-size: 44px; font-weight: 600; color: #c084fc;">Pneumatoumbrella calcigrada</span>
    </div>
    <div class="cover-sub">
      水力推進「羽狀流體輪傘」—— 像倒貼在岩壁上的「三維步進水母」<br>
      暗河中的紫色琉璃花 · 吸盤多足肉質步進 · 雙傘液壓抓握粉碎
    </div>

    <!-- 世界一句話定案 -->
    <div class="cover-world-box">
      <strong>【M1 世界一句話定案】</strong><br>
      人類消失 400 年後的城市廢墟深層溶洞，人造聚合物水解浩劫與混凝土碳化淋溶，形成 pH 7.8 恆溫高飽和碳酸鈣 (CaCO₃) 暗河與鐘乳石岩壁。
    </div>

    <div class="cover-meta">
      <div><span class="label">Course</span><span class="val">科技藝術：物件導向程式設計</span></div>
      <div><span class="label">Presenter</span><span class="val">李蕙希 (ambre-ctrl)</span></div>
      <div><span class="label">Date</span><span class="val">2026.10.15 報告站</span></div>
      <div><span class="label">Format</span><span class="val">3 分鐘物種簡報 + 現場動態檢核</span></div>
    </div>
  </div>

  <!-- ========================================== -->
  <!-- SLIDE 2: 物種設定書五欄（每欄一句話＋根據） -->
  <!-- ========================================== -->
  <div class="slide">
    <div class="grid-bg"></div>
    <div class="header">
      <div>
        <div class="tag">Species Specification · 5 Columns</div>
        <div class="title">物種設定書五欄：生理適應與生存根據</div>
      </div>
      <div class="slide-num">02 / 05</div>
    </div>
    <div class="content-area">
      <div style="flex: 1.4; display: flex; flex-direction: column; gap: 14px;">
        
        <!-- 1. 型態 -->
        <div class="card" style="padding: 14px 20px;">
          <div style="display: flex; justify-content: space-between; align-items: baseline;">
            <strong style="color: #e879f9; font-size: 18px;"><span class="badge badge-purple">1. 型態</span>前後雙羽傘與細長流體脊椎</strong>
            <span style="font-size: 13px; color: #94a3b8;">體長 45 cm · 紫水晶半透膜</span>
          </div>
          <p style="font-size: 15px; margin-top: 4px;">由一條流體脊椎串聯前後兩組半透明羽狀輪傘，邊緣佈滿微型吸盤與微孔噴嘴。<br>
          <em style="color: #64748b; font-size: 13.5px;">【根據】揚棄硬質關節以免疫 CaCO₃ 沉積卡死磨損，改採高韌性流體薄膜（Costello et al., 2021）。</em></p>
        </div>

        <!-- 2. 代謝 -->
        <div class="card" style="padding: 14px 20px;">
          <div style="display: flex; justify-content: space-between; align-items: baseline;">
            <strong style="color: #38bdf8; font-size: 18px;"><span class="badge badge-cyan">2. 代謝</span>微塑膠聚酯濾食與化學晶光自養</strong>
            <span style="font-size: 13px; color: #94a3b8;">心率 18 bpm · 低溫休眠</span>
          </div>
          <p style="font-size: 15px; margin-top: 4px;">濾食暗河聚合物水解微粒與甲殼類，紫晶外膜吸收方解石微光維持超低代謝自養。<br>
          <em style="color: #64748b; font-size: 13.5px;">【根據與查證來源】Voituron et al. (2011, Biology Letters) 洞穴蠑螈極端低耗能與抗老化模型。</em></p>
        </div>

        <!-- 3. 繁衍 -->
        <div class="card" style="padding: 14px 20px;">
          <div style="display: flex; justify-content: space-between; align-items: baseline;">
            <strong style="color: #f43f5e; font-size: 18px;"><span class="badge badge-pink">3. 繁衍</span>橫裂生殖與石灰岩壁休眠水螅體</strong>
            <span style="font-size: 13px; color: #94a3b8;">世代交替 · 枯水囊胚</span>
          </div>
          <p style="font-size: 15px; margin-top: 4px;">在鐘乳石縫隙固著分泌鈣化硬囊休眠，水流脈衝週期橫裂釋放微型自由水母體。<br>
          <em style="color: #64748b; font-size: 13.5px;">【根據】刺胞動物水母體與固著水螅體之極端乾旱休眠交替機制（Boero et al., 2008）。</em></p>
        </div>

        <!-- 4. 行為 -->
        <div class="card" style="padding: 14px 20px;">
          <div style="display: flex; justify-content: space-between; align-items: baseline;">
            <strong style="color: #34d399; font-size: 18px;"><span class="badge" style="background: rgba(52, 211, 153, 0.2); color: #34d399; border: 1px solid rgba(52,211,153,0.4);">4. 行為</span>天性趨暗伏擊、雙傘抓握夾持</strong>
            <span style="font-size: 13px; color: #94a3b8;">微電感應 · 液壓夾爪</span>
          </div>
          <p style="font-size: 15px; margin-top: 4px;">貼壁靜止避光，感應水震時反折雙傘化為夾具粉碎獵物；懼怕強酸水流擾動。<br>
          <em style="color: #64748b; font-size: 13.5px;">【根據】走觸性獵食與周向分散控制（Kano et al., 2017, Bioinspiration & Biomimetics）。</em></p>
        </div>

        <!-- 5. 威脅 -->
        <div class="card" style="padding: 14px 20px;">
          <div style="display: flex; justify-content: space-between; align-items: baseline;">
            <strong style="color: #fbbf24; font-size: 18px;"><span class="badge" style="background: rgba(251, 191, 36, 0.2); color: #fbbf24; border: 1px solid rgba(251,191,36,0.4);">5. 威脅</span>強酸水流脫鈣與溶洞地下水枯竭</strong>
            <span style="font-size: 13px; color: #94a3b8;">pH 突降 &lt; 6.5 · 膜脆化</span>
          </div>
          <p style="font-size: 15px; margin-top: 4px;">地表酸雨滲漏會溶解岩壁附著點並腐蝕琉璃膜，溶洞坍塌將直接粉碎其水囊。<br>
          <em style="color: #64748b; font-size: 13.5px;">【根據】喀斯特高鈣水體酸化緩衝失衡對洞穴特化生物群的致死性打擊。</em></p>
        </div>

      </div>

      <!-- 右側：核心生存問答卡 -->
      <div style="flex: 1; display: flex; flex-direction: column; justify-content: space-between;">
        <div class="card card-highlight" style="padding: 28px;">
          <h3 style="font-size: 22px; color: #38bdf8;">【核心檢核問答】<br>牠憑什麼在你的世界活下來？</h3>
          <p style="font-size: 18px; line-height: 1.8; margin-top: 14px; color: #ffffff;">
            <strong>「牠以無關節軸承的純水力羽傘，徹底免疫了高鈣暗河的碳酸鈣結垢磨損；並以微吸盤周向蠕動在垂直鐘乳石上立體攀爬，在湍急暗流中零損耗存活與伏擊。」</strong>
          </p>
        </div>
        <div class="preview-container" style="max-height: 380px;">
          <img src="m2-species-wireframe.png" alt="Geometric Wireframe Model">
        </div>
      </div>
    </div>
  </div>

  <!-- ========================================== -->
  <!-- SLIDE 3: 牠是怎麼動的？三種生命動態與獵奇美學 -->
  <!-- ========================================== -->
  <div class="slide">
    <div class="grid-bg"></div>
    <div class="header">
      <div>
        <div class="tag">Kinematics & Biological Aesthetics</div>
        <div class="title">牠是怎麼動的？三態運動機制與獵奇美學</div>
      </div>
      <div class="slide-num">03 / 05</div>
    </div>
    <div class="content-area">
      
      <!-- 動態 1 -->
      <div style="flex: 1; display: flex; flex-direction: column; gap: 16px;">
        <div class="preview-container" style="height: 310px;">
          <img src="m2-species-preview.png" alt="Aquatic Jet Propulsion">
        </div>
        <div class="card card-highlight" style="flex: 1;">
          <div style="display: flex; align-items: center; gap: 8px; margin-bottom: 6px;">
            <span class="badge badge-cyan">動態 1</span>
            <strong style="color: #38bdf8; font-size: 18px;">暗河水力高速脈衝</strong>
          </div>
          <p style="font-size: 15px;">
            前後兩組羽傘<strong>交替反相開合（Alternating Phase）</strong>：前傘擠壓噴流時後傘充水蓄壓，反之亦然。消除了傳統水母的停頓減速，形成持續推力穿梭。
          </p>
          <p style="font-size: 13.5px; color: #e879f9; margin-top: 8px;">
            <em>視覺：暗河中呼吸綻放的「紫色琉璃花」。</em>
          </p>
        </div>
      </div>

      <!-- 動態 2 -->
      <div style="flex: 1; display: flex; flex-direction: column; gap: 16px;">
        <div class="preview-container" style="height: 310px;">
          <img src="m2-species-creep.png" alt="Wall Creeping Stepping">
        </div>
        <div class="card card-highlight" style="flex: 1;">
          <div style="display: flex; align-items: center; gap: 8px; margin-bottom: 6px;">
            <span class="badge badge-purple">動態 2</span>
            <strong style="color: #c084fc; font-size: 18px;">岩壁肉質花朵步進</strong>
          </div>
          <p style="font-size: 15px;">
            雙傘平展貼在石灰岩壁，邊緣微吸盤咬合，沿周向傳遞<strong>局部蠕動行進波</strong>，微足輪流吸附、拱起前推。
          </p>
          <p style="font-size: 13.5px; color: #e879f9; margin-top: 8px;">
            <em>視覺：倒貼在懸崖上爬行的「肉質琉璃花朵」。</em>
          </p>
        </div>
      </div>

      <!-- 動態 3 -->
      <div style="flex: 1; display: flex; flex-direction: column; gap: 16px;">
        <div class="preview-container" style="height: 310px;">
          <img src="m2-species-crush.png" alt="Predatory Crush">
        </div>
        <div class="card card-highlight" style="flex: 1;">
          <div style="display: flex; align-items: center; gap: 8px; margin-bottom: 6px;">
            <span class="badge badge-pink">動態 3</span>
            <strong style="color: #fb7185; font-size: 18px;">雙傘液壓抓握粉碎</strong>
          </div>
          <p style="font-size: 15px;">
            伏擊獵物時前後雙傘反折對向包覆，化為<strong>液壓雙向夾具</strong>。水囊肌肉爆發 380 kPa 高壓捏碎獵物外殼。
          </p>
          <p style="font-size: 13.5px; color: #e879f9; margin-top: 8px;">
            <em>視覺：機械生物收攏包覆的獵奇瞬間。</em>
          </p>
        </div>
      </div>

    </div>
  </div>

  <!-- ========================================== -->
  <!-- SLIDE 4: 現場 DEMO 與設定書逐項對照 -->
  <!-- ========================================== -->
  <div class="slide">
    <div class="grid-bg"></div>
    <div class="header">
      <div>
        <div class="tag">Live Prototype & Alignment Check</div>
        <div class="title">現場跑雛形：程式動態與設定書對照</div>
      </div>
      <div class="slide-num">04 / 05</div>
    </div>
    <div class="content-area">
      <div style="flex: 1.1; display: flex; flex-direction: column; justify-content: space-between;">
        
        <div class="card card-highlight" style="padding: 22px;">
          <h3 style="font-size: 20px; color: #38bdf8;">【現場動態導覽按鍵】</h3>
          <p style="font-size: 15.5px; line-height: 1.8;">
            ▸ 按 <strong style="color: #38bdf8;">[1]</strong>：切換<strong>水力交替脈衝游動</strong>（展示氣泡噴流）<br>
            ▸ 按 <strong style="color: #c084fc;">[2]</strong>：切換<strong>岩壁肉質步進</strong>（展示傘緣蠕動波）<br>
            ▸ 按 <strong style="color: #fb7185;">[3] / [C]</strong>：觸發<strong>雙傘對向抓握粉碎</strong>（展示 380 kPa 捏碎電弧）<br>
            ▸ 按 <strong style="color: #ffffff;">[SPACE]</strong>：切換<strong>紫色琉璃膜 ↔ 幾何骨架線框</strong><br>
            ▸ 滑鼠左鍵拖曳 360° 旋轉 · 滾輪縮放觀察吸盤微孔
          </p>
        </div>

        <div class="card" style="padding: 22px;">
          <h3 style="font-size: 20px; color: #e879f9;">【雛形與設定書對照檢核】</h3>
          <ul style="list-style: none; font-size: 15.5px; line-height: 1.8;">
            <li>✓ <strong>型態對應</strong>：10 根前傘骨 + 12 根後傘骨 + 8 節脊椎，對應非對稱雙輪傘。</li>
            <li>✓ <strong>代謝對應</strong>：HUD 即時顯示水壓 (kPa)、吸附率 (%) 與游速，反映低耗能生理。</li>
            <li>✓ <strong>行為對應</strong>：水中噴射高速巡航與岩壁步進對應其水陸雙棲伏擊習性。</li>
          </ul>
        </div>

      </div>

      <div style="flex: 1.3; display: flex; gap: 20px;">
        <div class="preview-container" style="flex: 1;">
          <img src="m2-species-preview.png" alt="Demo Solid View">
        </div>
        <div class="preview-container" style="flex: 1;">
          <img src="m2-species-wireframe.png" alt="Demo Wireframe View">
        </div>
      </div>
    </div>
  </div>

  <!-- ========================================== -->
  <!-- SLIDE 5: 卡關、解法與下一站天性 (M3 展望) -->
  <!-- ========================================== -->
  <div class="slide">
    <div class="grid-bg"></div>
    <div class="header">
      <div>
        <div class="tag">Reflections & Milestone 3 Vision</div>
        <div class="title">卡關與解法 · 下一站讓牠長出什麼天性？</div>
      </div>
      <div class="slide-num">05 / 05</div>
    </div>
    <div class="content-area">
      
      <!-- 左側：卡關與解法 -->
      <div style="flex: 1.1; display: flex; flex-direction: column; justify-content: space-between;">
        
        <div class="card card-highlight" style="padding: 24px;">
          <h3 style="font-size: 21px; color: #fb7185;">【卡在哪裡？】</h3>
          <p style="font-size: 16px; line-height: 1.75; margin-top: 8px;">
            一開始做單傘水母原型時，推進後擴張吸水會產生<strong>極嚴重的失速與停頓感</strong>，像垂死掙扎而非具生命力的深河獵食者；且岩壁攀爬時如果讓所有吸盤同時開合，視覺僵硬如同機械齒輪，缺乏花朵肉質蠕動的獵奇感。
          </p>
        </div>

        <div class="card" style="padding: 24px; border-color: rgba(56, 189, 248, 0.4);">
          <h3 style="font-size: 21px; color: #38bdf8;">【怎麼解的？】</h3>
          <p style="font-size: 16px; line-height: 1.75; margin-top: 8px;">
            ▸ <strong>前後雙傘反相相位差</strong>：賦予前傘與後傘 $\\pi$ 相位差（<code>sin(phase)</code> 與 <code>sin(phase + PI)</code>），前推後吸、後推前吸，推力無縫銜接。<br>
            ▸ <strong>周向正弦波疊加</strong>：將傘骨旋轉角結合時間相位（<code>sin(creepPhase * 2.8 + theta * 3)</code>），實現邊緣肉質花瓣多足步進。
          </p>
        </div>

      </div>

      <!-- 右側：M3 展望與總結 -->
      <div style="flex: 1.1; display: flex; flex-direction: column; justify-content: space-between;">
        
        <div class="card card-highlight" style="padding: 24px; border-color: rgba(168, 85, 247, 0.5);">
          <h3 style="font-size: 21px; color: #e879f9;">【下一站 M3：讓牠長出什麼天性？】</h3>
          <p style="font-size: 16px; line-height: 1.8; margin-top: 8px;">
            從「會動的原型」進展為<strong>「活著的個體 (Living Individual)」</strong>：<br>
            ▸ <strong>走觸性與自主避障 (Steering)</strong>：遇到鐘乳石岩壁時自主轉向，尋找石縫棲息。<br>
            ▸ <strong>趨暗避險性格 (Braitenberg / Personality)</strong>：畏懼強光與強酸突波，受驚擾時心囊水壓瞬間飆高、噴射加速逃竄。<br>
            ▸ <strong>觸手微電通信</strong>：邊緣感測鬚在黑暗中散發脈動式微光通信。
          </p>
        </div>

        <div class="card" style="padding: 20px; background: rgba(10, 15, 29, 0.9);">
          <div style="display: flex; justify-content: space-between; align-items: center;">
            <div>
              <strong style="color: #ffffff; font-size: 17px;">報告站完成確認</strong><br>
              <span style="font-size: 13.5px; color: #94a3b8;">m2-species/ 檔案已齊備，準備 15:30 登台 3 分鐘簡報</span>
            </div>
            <span class="badge badge-purple" style="font-size: 14px; padding: 6px 14px;">M2 Check Ready</span>
          </div>
        </div>

      </div>

    </div>
  </div>

</body>
</html>
"""

with open(SLIDES_HTML, "w", encoding="utf-8") as f:
    f.write(html_content)

print(f"HTML presentation written to {SLIDES_HTML}")

# 透過 Chrome Headless 輸出 16:9 PDF
cmd = [
    CHROME_PATH,
    "--headless",
    "--disable-gpu",
    "--print-to-pdf=" + PDF_PATH,
    "--no-pdf-header-footer",
    "--print-to-pdf-no-header",
    SLIDES_HTML
]

subprocess.run(cmd, check=True)
print(f"Successfully generated teacher-spec M2 presentation PDF: {PDF_PATH}")
