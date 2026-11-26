# Threads｜AstrBot：LINE 串接、授權、費用與安全界線

查核時間：2026-11-26（台灣時間）；[原帖](https://www.threads.com/@aiposthub/post/DgMuu0dAdfz)／[分享連結](https://www.threads.com/share/BAYLrYbxOV)。

## 原帖與全部可見作者續文

@aiposthub 宣稱 AstrBot 讓 LINE 變私人 AI 助理，GitHub 約 4.75 萬星，並稱其為 OpenClaw 替代方案。[第一則續文](https://www.threads.com/@aiposthub/post/DgMuvWfAcYA)列 LINE、Telegram、Discord、Slack、飛書、GPT／Claude／Gemini／DeepSeek、Ollama、MCP、Agent、RAG、後台及插件；稱 AGPL-3.0。另稱可用於個人助理、客服、社群管理與自動化。[第二則續文](https://www.threads.com/@aiposthub/post/DgMuv4ZgVrf)要求留言 Bot 以索取完整介紹、GitHub 與部署教學。上述為當時可見的兩則作者續文；登入牆或未載入回覆不排除更多內容，未留言或領取教學。

原帖可見一張連往 [AI郵報文章](https://www.aiposthub.com/astrbot-47k-stars-multi-platform-im-ai-agent-framework-guide-20261126/)的 1200×600 預覽封面，不是實際操作截圖；可見兩則續文無獨立附圖。封面來源與再散布授權未確認，不轉載；原頁可查看。文章 11 月 26 日稱 47,520 星；查核 GitHub API 為 47,527 星，數字會變動。

## 官方固定版本核對

以下依 GitHub 預設分支快照 [57415b79e03d1d8585417d7fd9f8da5a5b4586fe](https://github.com/AstrBotDevs/AstrBot/tree/57415b79e03d1d8585417d7fd9f8da5a5b4586fe)（2026-11-26 09:02 UTC），不是保證穩定版；GitHub latest release 當時顯示 v4.30.0-beta.1，勿將預設分支等同最新穩定版。[README](https://github.com/AstrBotDevs/AstrBot/blob/57415b79e03d1d8585417d7fd9f8da5a5b4586fe/README.md)列 LINE、Telegram、Discord、Slack、飛書均為官方維護，並列 OpenAI 相容、Anthropic、Gemini、DeepSeek、Ollama 等模型服務及 MCP、Agent、知識庫、WebUI 和插件。可串接不代表帳號、金鑰、費用、功能或安全性自動就緒。

「OpenClaw 替代方案」是原帖／文章的定位及比較，不是相容性、功能優劣或可直接取代的證明。兩者均面向助理與通訊整合，但架構、平台、擴充、安全及操作依版本不同；需依實際工作流評估，未做對照實測。參考 [OpenClaw 官方專案](https://github.com/openclaw/openclaw)。

## LINE 官方支援與配置

[AstrBot 固定版本 LINE 文件](https://github.com/AstrBotDevs/AstrBot/blob/57415b79e03d1d8585417d7fd9f8da5a5b4586fe/docs/zh/platform/line.md)標示 v4.17.0，支援文字、圖片、語音、影片、文件收發；貼圖可收不可發，支援主動推送。其適配器只用統一 Webhook。建立 LINE Official Account 與 Messaging API channel（不是 LINE Login），取得 Channel Secret 和 Channel Access Token，在後台建立並啟用 LINE 適配器，保存後複製 Webhook URL 至 LINE Developers Console，Verify 並開啟 Use webhook，再加好友測試。群組要先邀入帳號。Webhook 必須能以公開 HTTPS 到達，宜只公開必要路徑，後台走私有網路／認證；憑證不得公開。[固定版本程式碼](https://github.com/AstrBotDevs/AstrBot/blob/57415b79e03d1d8585417d7fd9f8da5a5b4586fe/astrbot/core/platform/sources/line/line_adapter.py)檢查 LINE 簽章。這是文件核查，不是部署或實測。

## 授權例外與費用

主專案 [LICENSE](https://github.com/AstrBotDevs/AstrBot/blob/57415b79e03d1d8585417d7fd9f8da5a5b4586fe/LICENSE) 是 AGPL v3，檔尾專案通知寫 v3 或更新版；修改版供使用者透過網路互動時，第 13 條要求向互動者提供對應原始碼。分發也有其他義務；並非單純「只要商用就必須公開全部公司程式」。第 13 條也允許與 GPLv3 作品組合，各部分仍受各自條款約束；系統函式庫和一般工具有對應原始碼排除條件。獨立部分、插件、修改與組合的界線需按事實判定。另 [dashboard/LICENSE](https://github.com/AstrBotDevs/AstrBot/blob/57415b79e03d1d8585417d7fd9f8da5a5b4586fe/dashboard/LICENSE) 是 CodedThemes MIT 許可，應保留版權與許可聲明；不代表整個專案都變 MIT。專案另列 [EULA](https://github.com/AstrBotDevs/AstrBot/blob/57415b79e03d1d8585417d7fd9f8da5a5b4586fe/EULA.md) 使用限制、隱私及插件免責，部分文字可能與 AGPL 權利或使用者期待存在張力，其法律效力不在此判定；商用請審閱完整條款並諮詢律師。本摘要非法律意見。

軟體開源不等於整體免費：模型 API、本機硬體電力、主機、公網與第三方插件均可能收費。[LINE 官方計費](https://developers.line.biz/en/docs/messaging-api/pricing/)依地區及方案有所不同，Reply API 不計入訊息方案配額，push 等發送可能計入；每次回覆多個氣泡與計費單位不同，不可直接等同氣泡數。[台灣官方費用頁](https://tw.linebiz.com/service/account-solutions/line-official-account/)稱 2026-11-01 起調整方案、列 Reply API 不計訊息費，部分加購條件與稅另計；價格表為圖片，未可靠核讀具體現價，請以官方帳號後台與公告為準，不套用日本範例。API 模型呼叫費仍可能發生。

## 安全與限制

第三方插件可能執行程式並接觸資料，外部訊息也可能含提示詞注入；採最小權限、人工核准高風險動作、審核插件、隔離敏感資料、限制預算並備份。自架和本機模型不代表訊息完全不出設備：LINE、模型供應商、外掛及日誌各有資料流。未安裝 AstrBot、未更動現有服務或帳號，也未實際測試連線與功能。
