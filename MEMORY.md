# 後未來動物園：物種研究與長期記憶 (MEMORY.md)

*最後更新時間：2026-09-24*

---

## 1. 創作者與工作流設定
- **創作者角色**：李蕙希 (ambre-ctrl) — 科技藝術大一學生（修習「物件導向程式設計」，江振維老師課程）。
- **協作模式**：技術輔助與思維鷹架。創作者主導世界觀與物種設定；AI 負責技術實現、提供研究材料、引導式提問與白話原理解釋。
- **語言**：繁體中文（台灣）。
- **術語規範**：使用生命詞彙（物種、基因、行為、演化、變異、族群），不使用抽象程式結構名詞。

---

## 2. 專案資訊與里程碑進度 (Post-Future Zoo)
- **專案目錄**：`/Users/cheng-kuanglee/post-future-zoo`
- **遠端倉庫**：[ambre-ctrl/test1](https://github.com/ambre-ctrl/test1)
- **當前里程碑**：**M1 世界（10/1 報告站，已完成產出）**
- **里程碑全覽**：
  - [x] 專案環境初始化（已導入課程官方範本結構）
  - [x] **M0 裝備 (9/24)**：第一次試跑（呼吸圓）、讓 AI 出錯實驗截圖 [x]、README.md 反思與 AI 揭露欄 [x]、推送至 GitHub [x]
  - [x] **M1 世界 (10/1，報告站)**：世界觀全新確立（聚合物吞噬浩劫與 400 年後的礦化新生命圈）、5 篇頂級科學文獻佐證、產出完整 8 頁 [m1-簡報.pdf](file:///Users/cheng-kuanglee/post-future-zoo/m1-world/m1-簡報.pdf)、高清圖檔 [slides_images/](file:///Users/cheng-kuanglee/post-future-zoo/m1-world/slides_images/) 與 [canva_text_template.md](file:///Users/cheng-kuanglee/post-future-zoo/m1-world/canva_text_template.md)
  - [ ] **M2 物種 (10/15，報告站)**：物種設定書、會動的雛形＋m2-簡報.pdf
  - [ ] **M3 個體 (11/12，報告站)**：有天性的個體＋m3-簡報.pdf
  - [ ] **M4 族群 (12/3)**：一群牠（群集、演化與競爭）
  - [ ] **M5 棲地 (12/17)**：棲地與觀眾互動（Perlin noise、ml5.js）
  - [ ] **M6 開園 (12/24，報告站)**：展出版本、首席研究員導覽演練＋m6-簡報.pdf

---

## 3. 物種發想與世界觀檔案（400 年深層溶洞避難生態圈）
- **物種命名**：**幽境石灰洞螈 (*Proteus calcis*)**（衍生自斯洛維尼亞盲眼洞螈 *Proteus anguinus*）
- **核心定案句**：「在人類消失後 400 年的世界，城市地鐵與地下室因水泥剝落與鋼筋鏽蝕崩毀為劇毒水墓；然而天然深層石灰岩溶洞不受人造材料退化影響，以碳酸鈣 (CaCO₃) 天然中和酸雨與酸化水質，成為超低代謝盲眼生物的避難聖所。」
- **時間尺度**：人類消失後 400 年。
- **三大演化特化機制**：
  1. **天然地質避險與化學中和**：生存在深層天然石灰岩／花崗岩水系，避開人造工程結構塌陷；依賴碳酸鈣（$\text{CaCO}_3$）天然化學緩衝層穩定中和地表酸雨與氯化氫酸氣，微氣候維持在 pH 7.8。
  2. **極致超低代謝模型**：終生生活在無光深水，新陳代謝率僅為地表脊椎動物的 1/10，心率僅 15~20 bpm，不依賴陽光食物鏈，具備極端抗老化與飢餓耐受力（文獻佐證：Voituron et al., 2011）。
  3. **非視覺感官陣列**：視覺器官完全退化為皮下淡痕；吻部邊緣密佈微電感受器（Ampullary organs），軀幹兩側具備靈敏側線水壓感知，頸部外露 3 對羽狀鮮紅外鰓（Branchiae）進行極低氧交換。
- **權威文獻**：Voituron, Y., et al. (2011). Extreme longevity in the olm *Proteus anguinus*: a new model for ageing research. *Biology Letters*.

---

## 4. 當前行動與進度 (TODO)
- [x] 完成 M1 世界觀研究報告、8 頁簡報圖檔、PDF 與 Canva 文字模板。
- [x] 完成 M2 測試生物 3D 動態模型程式碼（[m2-species/sketch.js](file:///Users/cheng-kuanglee/post-future-zoo/m2-species/sketch.js) 與 [m2-species/index.html](file:///Users/cheng-kuanglee/post-future-zoo/m2-species/index.html)）：
  - 採用 p5.js WEBGL 渲染引擎與物件導向階層矩陣（Hierarchical Kinematics Chain）。
  - 15 節俐落簡約低多邊形（Low-poly）幾何方塊構成蠑螈軀幹與垂直尾鰭刃。
  - 3D 空間脊椎正弦行進波（Serpentine Sine Wave）傳遞，包含水平偏航 (Yaw) 與微幅俯仰 (Pitch) 游動。
  - 幾何珊瑚紅外鰓呼吸張合、超低代謝幾何心臟搏動、微型幾何四肢。
  - 支援滑鼠 360° 拖曳旋轉 3D 視角（`orbitControl`）、空白鍵切換幾何實體與線框骨架模式。
- [ ] 創作者填寫 M2 物種設定書五欄（外觀、習性、演化、環境關係等）至 [m2-species/README.md](file:///Users/cheng-kuanglee/post-future-zoo/m2-species/README.md)。
- [ ] 錄製／截圖生物動態畫面備查。
- [ ] 製作 M2 上台簡報 [m2-簡報.pdf](file:///Users/cheng-kuanglee/post-future-zoo/m2-species/m2-簡報.pdf)（10/15 報告站準備）。
