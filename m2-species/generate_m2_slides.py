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
<title>後未來動物園 M2 簡報：羽狀流體輪傘獸</title>
<style>
  @import url('https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@400;600;700&family=Noto+Sans+TC:wght@400;500;700;900&display=swap');

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
    padding: 70px 90px;
    background: radial-gradient(circle at 85% 15%, rgba(168, 85, 247, 0.12) 0%, transparent 45%),
                radial-gradient(circle at 10% 85%, rgba(56, 189, 248, 0.08) 0%, transparent 45%),
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
    background-size: 60px 60px;
    pointer-events: none;
  }

  .header {
    display: flex;
    justify-content: space-between;
    align-items: flex-end;
    margin-bottom: 40px;
    position: relative;
    z-index: 2;
    border-bottom: 1px solid rgba(168, 85, 247, 0.25);
    padding-bottom: 20px;
  }

  .tag {
    font-size: 14px;
    letter-spacing: 2.5px;
    text-transform: uppercase;
    color: #e879f9;
    font-weight: 700;
    display: flex;
    align-items: center;
    gap: 10px;
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
    font-size: 44px;
    font-weight: 900;
    color: #ffffff;
    letter-spacing: -0.5px;
    margin-top: 6px;
  }

  .slide-num {
    font-family: 'Space Grotesk', monospace;
    font-size: 26px;
    color: #64748b;
    font-weight: 600;
  }

  .content-area {
    flex: 1;
    position: relative;
    z-index: 2;
    display: flex;
    gap: 50px;
  }

  .left-col {
    flex: 1.1;
    display: flex;
    flex-direction: column;
    justify-content: space-between;
  }

  .right-col {
    flex: 1.3;
    display: flex;
    align-items: center;
    justify-content: center;
  }

  .preview-card {
    width: 100%;
    height: 100%;
    max-height: 750px;
    border-radius: 20px;
    overflow: hidden;
    border: 1px solid rgba(168, 85, 247, 0.35);
    box-shadow: 0 20px 50px rgba(0, 0, 0, 0.8), 0 0 30px rgba(168, 85, 247, 0.15);
    background: #0a0f1d;
    position: relative;
  }

  .preview-card img {
    width: 100%;
    height: 100%;
    object-fit: cover;
  }

  .card {
    background: rgba(15, 23, 42, 0.65);
    border: 1px solid rgba(255, 255, 255, 0.08);
    border-radius: 16px;
    padding: 24px 30px;
    backdrop-filter: blur(12px);
    margin-bottom: 20px;
  }

  .card-highlight {
    border-color: rgba(168, 85, 247, 0.4);
    background: linear-gradient(135deg, rgba(168, 85, 247, 0.12), rgba(15, 23, 42, 0.75));
  }

  .card h3 {
    font-size: 22px;
    color: #e879f9;
    margin-bottom: 10px;
    display: flex;
    align-items: center;
    gap: 10px;
  }

  .card p {
    font-size: 17px;
    color: #cbd5e1;
    line-height: 1.7;
  }

  .stat-badge {
    display: inline-flex;
    align-items: center;
    gap: 6px;
    background: rgba(56, 189, 248, 0.15);
    border: 1px solid rgba(56, 189, 248, 0.35);
    color: #38bdf8;
    padding: 4px 12px;
    border-radius: 6px;
    font-family: monospace;
    font-size: 15px;
    font-weight: bold;
    margin-right: 8px;
    margin-top: 8px;
  }

  .citation-bar {
    font-size: 13.5px;
    color: #64748b;
    border-top: 1px dashed rgba(255, 255, 255, 0.15);
    padding-top: 14px;
    margin-top: 10px;
  }

  /* 封面特殊樣式 */
  .cover-slide {
    justify-content: center;
    align-items: center;
    text-align: center;
    padding: 100px;
  }
  .cover-badge {
    display: inline-block;
    padding: 8px 22px;
    background: rgba(168, 85, 247, 0.18);
    border: 1px solid rgba(168, 85, 247, 0.45);
    color: #e879f9;
    font-size: 16px;
    letter-spacing: 3px;
    border-radius: 50px;
    margin-bottom: 30px;
    text-transform: uppercase;
    font-weight: 700;
  }
  .cover-title {
    font-size: 74px;
    font-weight: 900;
    line-height: 1.15;
    margin-bottom: 24px;
    background: linear-gradient(135deg, #ffffff 40%, #e879f9 80%, #38bdf8 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
  }
  .cover-sub {
    font-size: 26px;
    color: #94a3b8;
    max-width: 950px;
    line-height: 1.6;
    margin-bottom: 50px;
  }
  .cover-meta {
    display: flex;
    gap: 40px;
    font-size: 18px;
    color: #cbd5e1;
  }
  .cover-meta div {
    display: flex;
    flex-direction: column;
    gap: 4px;
  }
  .cover-meta span.label {
    font-size: 13px;
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

  <!-- SLIDE 1: 封面 -->
  <div class="slide cover-slide">
    <div class="grid-bg"></div>
    <div class="cover-badge">Post-Future Zoo · Milestone 2</div>
    <div class="cover-title">羽狀流體輪傘獸<br><span style="font-size: 46px; font-weight: 600; color: #a855f7;">Pneumatoumbrella calcigrada</span></div>
    <div class="cover-sub">
      水力推進「羽狀流體輪傘」—— 倒貼在岩壁上的「三維步進水母」<br>
      暗河中的紫色琉璃花・微孔吸盤多足步進・雙傘液壓抓握粉碎
    </div>
    <div class="cover-meta">
      <div><span class="label">Course</span><span class="val">科技藝術：物件導向程式設計</span></div>
      <div><span class="label">Creator</span><span class="val">李蕙希 (ambre-ctrl)</span></div>
      <div><span class="label">Date</span><span class="val">2026.10.15 報告站</span></div>
      <div><span class="label">Tech Stack</span><span class="val">p5.js (WEBGL) · OOP Kinematics</span></div>
    </div>
  </div>

  <!-- SLIDE 2: 演化背景與世界觀承接 -->
  <div class="slide">
    <div class="grid-bg"></div>
    <div class="header">
      <div>
        <div class="tag">Evolution & Environmental Pressure</div>
        <div class="title">世界觀承接：人類消失後 400 年高鈣暗河</div>
      </div>
      <div class="slide-num">02 / 07</div>
    </div>
    <div class="content-area">
      <div class="left-col">
        <div class="card card-highlight">
          <h3>溶洞水體碳酸鈣飽和危機</h3>
          <p>400 年前聚合物水解浩劫後，高鈣雨水長期淋溶城市混凝土瓦礫，地下暗河形成高飽和碳酸鈣 (CaCO3) 水系（pH 7.8 恆溫）。傳統鉸鏈式附肢極易被石灰微晶卡死結垢。</p>
        </div>
        <div class="card">
          <h3>演化適應：無關節軸承之純水力輪傘</h3>
          <p>輪傘獸揚棄容易鈣化損壞的硬質骨骼，特化出<strong>前後雙組半透明羽狀輪傘</strong>與細長流體脊椎。以肌肉擠壓水囊水流推進，並以生物黏液螯合石灰岩形成微型吸盤，實現抗鈣化、高推力的全新流體生命型態。</p>
        </div>
        <div class="citation-bar">
          理論佐證：Voituron et al. (2011) 洞穴超低代謝休眠模型；Kano et al. (2017) 軟體生物分散式步進機制。
        </div>
      </div>
      <div class="right-col">
        <div class="preview-card">
          <img src="m2-species-wireframe.png" alt="Geometric Wireframe">
        </div>
      </div>
    </div>
  </div>

  <!-- SLIDE 3: 解剖構造與形態 -->
  <div class="slide">
    <div class="grid-bg"></div>
    <div class="header">
      <div>
        <div class="tag">Anatomical Architecture</div>
        <div class="title">解剖構造：前後雙羽傘與細長中軸脊椎</div>
      </div>
      <div class="slide-num">03 / 07</div>
    </div>
    <div class="content-area">
      <div class="left-col">
        <div class="card card-highlight">
          <h3>非對稱雙輪傘構造 (Bipartite Feather-Umbels)</h3>
          <p>
            ▸ <strong>前傘 (Anterior)</strong>：10 根羽狀射線，主控環境水流感應與微電轉向導引。<br>
            ▸ <strong>後傘 (Posterior)</strong>：12 根羽狀射線，配備厚實肌肉水囊，為主要推力引擎。<br>
            ▸ <strong>紫水晶琉璃薄膜</strong>：相鄰羽骨間鋪展半透明高韌性生物膜，宛如琉璃花瓣。
          </p>
        </div>
        <div class="card">
          <h3>邊緣微構造與水力水囊</h3>
          <p>
            ▸ <strong>微型噴水孔</strong>：以肌肉急速排擠水囊，噴出高壓空泡水流。<br>
            ▸ <strong>微型吸盤陣列</strong>：環繞於羽骨尖端，牢牢固著光滑石灰岩鐘乳石。<br>
            ▸ <strong>細長中軸脊椎</strong>：8 節流線型骨鞘，內嵌發光水力管道與神經索。
          </p>
          <div style="margin-top: 10px;">
            <span class="stat-badge">水壓: 120-380 kPa</span>
            <span class="stat-badge">吸附率: 98%</span>
            <span class="stat-badge">心率: 18 bpm</span>
          </div>
        </div>
      </div>
      <div class="right-col">
        <div class="preview-card">
          <img src="m2-species-preview.png" alt="3D Creature Preview">
        </div>
      </div>
    </div>
  </div>

  <!-- SLIDE 4: 動態模式 1 - 水中高速推進 -->
  <div class="slide">
    <div class="grid-bg"></div>
    <div class="header">
      <div>
        <div class="tag">Locomotion Mode 1 · Water Jet</div>
        <div class="title">暗河水力脈衝：交替開合高速穿梭</div>
      </div>
      <div class="slide-num">04 / 07</div>
    </div>
    <div class="content-area">
      <div class="left-col">
        <div class="card card-highlight">
          <h3>反相交替開合 (Alternating Phase Jetting)</h3>
          <p>
            傳統水母在擴張吸水時會停頓失速；輪傘獸前後兩傘具有 $\\pi$ 相位差：<br>
            當前傘收縮排空噴水時，後傘順勢展開舒張吸水蓄壓；隨後後傘收縮推進，前傘張開蓄壓。
          </p>
        </div>
        <div class="card">
          <h3>連續推力與紫色琉璃花視覺</h3>
          <p>
            藉由交替脈衝，克服了單傘水母推進間歇減速的致命缺陷，巡航游速可達 4.3 cm/s，超壓噴流時可飆升至 10 cm/s 以上。<br>
            在漆黑暗河中游動時，宛如一朵不斷呼吸綻放與收攏的<strong>「紫色琉璃花」</strong>。
          </p>
        </div>
        <div class="citation-bar">
          參考文獻：Costello et al. (2021) Multi-jet propulsion in medusae (Nature Communications).
        </div>
      </div>
      <div class="right-col">
        <div class="preview-card">
          <img src="m2-species-preview.png" alt="Jet Propulsion Mode">
        </div>
      </div>
    </div>
  </div>

  <!-- SLIDE 5: 動態模式 2 - 岩壁肉質步進 -->
  <div class="slide">
    <div class="grid-bg"></div>
    <div class="header">
      <div>
        <div class="tag">Locomotion Mode 2 · Wall Creeping</div>
        <div class="title">岩壁肉質步進：倒貼岩壁的三維步進水母</div>
      </div>
      <div class="slide-num">05 / 07</div>
    </div>
    <div class="content-area">
      <div class="left-col">
        <div class="card card-highlight">
          <h3>傘緣周向行進蠕動波 (Peristaltic Locomotion)</h3>
          <p>
            當爬行光滑石灰岩壁時，雙傘平鋪貼附於岩石表面。<br>
            傘膜邊緣不再進行大張大合的收縮，而是產生沿圓周方向傳遞的<strong>局部蠕動行進波</strong>。
          </p>
        </div>
        <div class="card">
          <h3>微型吸盤輪流咬合</h3>
          <p>
            邊緣數十顆微型吸盤順著波浪依次「吸附 $\\rightarrow$ 拱起拉動 $\\rightarrow$ 脫離前移 $\\rightarrow$ 重新咬合」。<br>
            整隻生物像一朵<strong>「能在峭壁上多足爬行的肉質花朵」</strong>，在垂直甚至倒懸岩壁上游刃有餘。
          </p>
        </div>
        <div class="citation-bar">
          機制參考：Kano et al. (2017) Bioinspiration & Biomimetics 多足蠕動步態控制。
        </div>
      </div>
      <div class="right-col">
        <div class="preview-card">
          <img src="m2-species-creep.png" alt="Wall Creeping Mode">
        </div>
      </div>
    </div>
  </div>

  <!-- SLIDE 6: 動態模式 3 - 雙傘捕食抓握粉碎 -->
  <div class="slide">
    <div class="grid-bg"></div>
    <div class="header">
      <div>
        <div class="tag">Locomotion Mode 3 · Predation</div>
        <div class="title">雙傘捕食粉碎：液壓雙向夾具伏擊</div>
      </div>
      <div class="slide-num">06 / 07</div>
    </div>
    <div class="content-area">
      <div class="left-col">
        <div class="card card-highlight">
          <h3>對向包覆扣合 (Bipartite Hydraulic Gripper)</h3>
          <p>
            貼在岩壁伏擊獵物時，前後兩組羽傘反折相對，化為液壓雙向夾爪。<br>
            細長脊椎受肌肉牽引向中央拱起，兩組羽傘同時向內猛烈合攏。
          </p>
        </div>
        <div class="card">
          <h3>380 kPa 液壓拘束與粉碎</h3>
          <p>
            傘骨尖端羽棘急速內曲，微型吸盤強力固著獵物。<br>
            水囊腔體肌肉瞬間爆發，高達 380 kPa 的高壓直接包覆並捏碎暗河穴居甲殼類外殼，伴隨生物放電閃爍。
          </p>
        </div>
      </div>
      <div class="right-col">
        <div class="preview-card">
          <img src="m2-species-crush.png" alt="Predatory Crush Mode">
        </div>
      </div>
    </div>
  </div>

  <!-- SLIDE 7: 程式實現與 OOP 設計 -->
  <div class="slide">
    <div class="grid-bg"></div>
    <div class="header">
      <div>
        <div class="tag">Engineering & Reflection</div>
        <div class="title">OOP 物件導向架構與未來展望 (M3)</div>
      </div>
      <div class="slide-num">07 / 07</div>
    </div>
    <div class="content-area">
      <div class="left-col">
        <div class="card card-highlight">
          <h3>p5.js WEBGL 階層矩陣架構</h3>
          <p>
            ▸ <code>UmbellateMedusa</code>：中央協調狀態機（游動／步進／捕食）。<br>
            ▸ <code>FeatherUmbel</code>：前後傘實例化，包含水囊、傘骨射線與膜扇面。<br>
            ▸ <code>CentralSpine</code>：8 節關節鏈矩陣變換。<br>
            ▸ <code>JetParticles</code>：高壓空泡微粒系統。
          </p>
        </div>
        <div class="card">
          <h3>M3 下一步展望：群體行為與共生氣漩</h3>
          <p>
            在 M3 階段，規劃讓多隻步進水母在石灰岩壁群聚，產生<strong>水力協同氣漩</strong>與<strong>連鎖生物螢光通信</strong>，構建完整的地下暗河共生微生態圈。
          </p>
        </div>
      </div>
      <div class="right-col">
        <div class="preview-card">
          <img src="m2-species-wireframe.png" alt="Architecture & Wireframe">
        </div>
      </div>
    </div>
  </div>

</body>
</html>
"""

with open(SLIDES_HTML, "w", encoding="utf-8") as f:
    f.write(html_content)

print(f"HTML slides written to {SLIDES_HTML}")

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
print(f"Successfully generated presentation PDF: {PDF_PATH}")
