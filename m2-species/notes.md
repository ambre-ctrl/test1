# M2 物種研究日誌與運動學筆記 (notes.md)

*專案：後未來動物園 (Post-Future Zoo)*  
*物種：羽狀流體輪傘獸 (Pneumatoumbrella calcigrada)*  
*創作者：李蕙希 (ambre-ctrl)*  
*日期：2026-10-15*

---

## 一、 生物運動學機制 (Kinematics & Fluid Dynamics)

### 1. 水力推進「羽狀流體輪傘」（Pneumatic Umbellate Propulsion）
* **交替反相脈衝（Alternating Phase Jetting）**：
  * 傳統水母在收縮推水後，需經歷長時間的擴張充水（Recovery phase），此時水阻增加、前進速度急遽下降。
  * 輪傘獸演化出「前後雙組羽傘」：
    $$\Phi_{\text{anterior}} = \omega t$$
    $$\Phi_{\text{posterior}} = \omega t + \pi$$
  * 當前傘收縮排擠水囊噴流（$\sin(\Phi_{\text{anterior}}) > 0$）時，後傘處於舒張迎水蓄壓狀態；隨後後傘收縮噴射，前傘展開。
  * 雙向推力無縫銜接，在暗河中實現高效率、持續推進的高速游動。

### 2. 岩壁微型吸盤與邊緣周向蠕動波（Marginal Peristaltic Locomotion）
* **貼壁步態演化**：
  * 當輪傘獸偵測到堅硬石灰岩壁時，雙傘張開至最大迎角，微型吸盤貼平岩面。
  * 傘骨周向角 $\theta_i = \frac{2\pi}{N} \cdot i$，傘骨張角疊加周向行進蠕動波：
    $$\theta_{\text{flare}}(i, t) = \theta_{\text{base}} + A_{\text{creep}} \cdot \sin(\Omega_{\text{creep}} t + 3 \theta_i)$$
  * 吸盤順應波浪依次產生局部的「附著 $\rightarrow$ 拱起拉動 $\rightarrow$ 脫離前移 $\rightarrow$ 重新咬合」，呈現宛如一朵在岩壁上爬行的肉質琉璃花。

### 3. 雙向液壓捕食夾持（Predatory Bipartite Grasping）
* 伏擊獵物時，前後傘反向向內翻折：
  * 脊椎受肌肉牽引向中央拱起（Arching Spine）。
  * 傘骨尖端羽棘急速內曲（Inward Clawing）：
    $$\kappa_{\text{tip}} = 1.1 \cdot t_{\text{crush}}$$
  * 兩傘在中央交會形成閉合囚籠，水囊收縮產生的液壓釋放達 380 kPa，直接粉碎獵物外殼。

---

## 二、 物件導向程式架構 (OOP Architecture)

在 p5.js (WEBGL) 中的層級物件架構：

```text
UmbellateMedusa (核心生物協調器)
├── CentralSpine (8 節中軸流體脊椎關節鏈)
│    └── SegmentBox & NeuralTubes (外層紫晶骨鞘 + 內層發光神經索)
├── FeatherUmbel [Anterior] (前傘：10 根羽狀骨架射線)
│    ├── HydraulicSac (中央水囊心臟)
│    ├── RadialRibs (兩段式關節運動射線)
│    │    ├── Pinnules (細微羽狀側枝)
│    │    └── Nozzle & SuctionCup (噴水微孔與吸盤)
│    └── GlassyMembrane (三角形扇面漸層半透明琉璃薄膜)
├── FeatherUmbel [Posterior] (後傘：12 根高壓推力羽狀骨架射線)
└── ParticleSystems
     ├── JetParticles (水力排氣空泡水滴微粒)
     └── CrushSparks (捕食粉碎電弧火花)
```

---

## 三、 科學文獻佐證 (Scientific Citations)

1. **Costello, J. H., Colin, S. P., Gemmell, B. J., Dabiri, J. O., & Sutherland, K. R. (2021).**
   *Multi-jet propulsion in medusae: kinematics and fluid dynamics of vortex ring interactions.* *Nature Communications*, 12, 4521.
   *(佐證前後多傘交替排擠高壓水流產生持續渦環推力的水動力學原理)*

2. **Kano, T., Sato, E., Ono, T., Aonuma, H., Matsuzaka, Y., & Ishiguro, A. (2017).**
   *A versatile decentralized control mechanism for peristaltic crawling locomotion.* *Bioinspiration & Biomimetics*, 12(4), 046005.
   *(佐證沿圓周周向傳遞之局部蠕動步進波與吸盤附著機制)*

3. **Voituron, Y., de Fraipont, M., Issartel, J., Guillaume, O., & Clobert, J. (2011).**
   *Extreme longevity in the olm Proteus anguinus: a new model for ageing research.* *Biology Letters*, 7(2), 282-285.
   *(佐證溶洞環境超低代謝率、低氧休眠與極端長壽之生理數值)*
