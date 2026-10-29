---
name: facebook-public-post-archive
description: Use when a user shares a Facebook post, photo, video, Reel, group post, or share URL and asks to extract, verify, archive, or summarize publicly accessible content without Facebook credentials.
version: 1.0.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [facebook, social-media, archive, browser, verification]
    related_skills: [hermes-agent]
---

# Facebook 公開貼文擷取與歸檔

## Overview

此技能用於從 Facebook 的公開貼文、相片、影片、Reel、社團貼文與 `share` 短連結擷取可公開取得的內容。Facebook 經常以登入遮罩或空殼 HTML 呈現內容；這不等於完全沒有可讀資訊。優先使用瀏覽器的「渲染後頁面」與公開 metadata 取得證據，並清楚區隔可見內容、社群自述與第一方可驗證事實。

## When to Use

- 使用者傳來 `facebook.com/share/...`、`facebook.com/.../posts/...`、`photo.php`、Reel、影片或社團貼文 URL。
- 使用者要求摘要、查核、保存圖片、建立知識庫條目或擷取提示詞。
- 一般 HTTP 抓取只得到登入牆、空白頁或 Open Graph 摘要。

不要用於：要求登入私人帳號、繞過權限、讀取私人社團／非公開內容，或索取、保存 Facebook 密碼、Cookie、access token。

## Required Capabilities

最佳效果需要：

- `browser`：開啟 URL，讀取瀏覽器渲染後的 DOM、連結與圖片。
- `web` 或 `terminal`：核對公開外連、HTTP headers 與素材 MIME。
- `vision`：當資訊位於可公開取得的圖卡、截圖或縮圖時，只轉錄清楚可讀的字。
- `file`：保存來源證據與經驗證的素材。

若沒有 `browser`，只能取得公開 metadata 或搜尋摘要，必須明確說明內容可能不完整。

## Workflow

### 1. 保留原始 URL，先解析 share 連結

1. 原樣記錄使用者提供的 URL。
2. 用 `browser_navigate` 開啟，而不是只用 HTTP request。
3. 從網址列、頁面連結、canonical / `og:url`、可見頁面資訊找出固定 URL，例如：
   - `https://www.facebook.com/photo.php?fbid=...`
   - `https://www.facebook.com/groups/<id>/posts/<id>/`
   - `https://www.facebook.com/<user>/posts/<id>/`
4. 保存原始 share URL、瀏覽器最終 URL、canonical URL（若可取得）。

### 2. 讀取渲染後內容，而非只看登入畫面

登入提示可能覆蓋內容，但公開貼文的下列資料仍可能已在 DOM 中：

- 作者、貼文日期／時間（若可見）
- 正文、留言中明確可見的文字
- 頁面標題、Open Graph description
- 圖片的 `src`、alt、尺寸與外連
- 貼文中引用的公開網站或文件

可透過瀏覽器 console 檢視：

```javascript
({
  url: location.href,
  title: document.title,
  text: document.body.innerText.slice(0, 20000),
  canonical: document.querySelector('link[rel="canonical"]')?.href,
  ogUrl: document.querySelector('meta[property="og:url"]')?.content,
  ogDescription: document.querySelector('meta[property="og:description"]')?.content,
  images: [...document.images].map(i => ({src: i.currentSrc || i.src, alt: i.alt, w: i.naturalWidth, h: i.naturalHeight}))
})
```

只採用實際可見或可公開讀取的文字。若全文被折疊、截斷或無法取得，標註「僅取得可見片段」，不可補寫。

### 3. 下載並驗證公開素材

僅下載瀏覽器已公開載入的圖片 URL；不要下載未知的執行檔或要求登入的檔案。

對準備保存的素材記錄：

```bash
file <image>
shasum -a 256 <image>
```

同時保存來源 URL、檔名、MIME、像素尺寸（可取得時）、bytes 與 SHA-256。使用本地副本作為歸檔圖片，避免依賴有期限或帶追蹤參數的 Facebook CDN 熱連結。

### 4. 查核貼文中的事實主張

- Facebook 作者的產品能力、模型、效果、發布日、下載或定價說法，均視為「社群自述」。
- 涉及產品規格、發布、可用性、安全性、下載連結時，另以官方公告、官方文件或官方產品頁查核。
- 找不到第一方來源時，寫明「尚未找到可公開核對的官方資料」，不要把貼文主張寫成事實。
- 非官方安裝檔、APK、DMG、ZIP、腳本：不下載、不執行、不轉貼；只記錄安全界線並建議等待官方來源與可核對的簽章／雜湊。

### 5. 輸出格式與證據邊界

摘要至少含：

1. 貼文重點（限可見文字與圖像）
2. 原始 URL 與解析後 canonical URL
3. 可公開驗證的外部來源
4. 已驗證事實與未驗證社群主張的區分
5. 圖片／影片取得限制與是否已保存本地副本

若歸檔到知識庫，來源 JSON 應包含擷取時間、URL 三種型態、作者（若可見）、可見正文、公開素材 metadata、查核來源與限制。

## Common Pitfalls

1. **把 HTTP 200 當成讀到內容。** Facebook 可能回傳登入殼層；應確認正文 marker 是否存在。
2. **登入遮罩就放棄。** 先檢查 `document.body.innerText`、metadata、圖片及可見外連。
3. **把 Open Graph 摘要當作完整貼文。** OG description 常被截斷，只能作輔助證據。
4. **臆測圖片內的字。** 只有清楚可辨識的文字才能轉錄；模糊內容應標示無法確認。
5. **把社群主張當產品事實。** 發布、支援模型、安全性與下載來源均須第一方核對。
6. **把 Cookie 或登入狀態傳到其他主機。** 技能檔不包含任何 session、token、帳密、環境變數或個人記憶。

## Verification Checklist

- [ ] 已保存原始 URL、最終 URL 與 canonical URL（可取得時）
- [ ] 已檢查渲染後 DOM，不只依賴 HTTP／搜尋摘要
- [ ] 可見貼文文字和未取得內容已清楚區隔
- [ ] 圖像文字僅轉錄可清楚辨識的部分
- [ ] 重要事實已用第一方來源核對，或標註未核對
- [ ] 保存素材已驗證 MIME 與 SHA-256（若有保存）
- [ ] 未要求、未保存、未傳遞 Facebook 登入資訊
