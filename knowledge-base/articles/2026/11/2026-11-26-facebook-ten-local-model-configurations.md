# Facebook｜十種本機模型配置：量化、作者測速與授權查核

查核：2026-11-27。來源為 [陳盟升公開社團貼文](https://www.facebook.com/groups/1270451518569482/permalink/1478963534384945/)；[分享連結](https://www.facebook.com/share/p/1CV2cJq16d/)。公開社團不等於著作權授權；本文摘要並連回原文。原圖是十列規格圖，署名陳盟升 Darks；已私下保存，未確認再散布授權，故不公開轉載。

## 先釐清：十列不是十個獨立基礎模型

原圖十列有 Inkling、Qwen 27B、Occamy、Nemotron Bolt 各一列；Qwen Flash 四種量化；Hy4 Flash 兩種量化，共六個模型家族、十種配置。原帖另列十個倉庫，其中 Hy4 拒答修正檔不是獨立模型；一個 4bit 倉庫當時無法公開核讀。量化格式、衍生版和基礎模型不能混為一談。

下表數字全是貼文作者或原圖的自述，非官方效能保證；未重跑。作者稱使用兩台 128GB 的 GB10 與 MacBook M5 Max，AI Agent 長上下文幾萬至十幾萬字；並未逐項公開引擎版本、批次、精確 token 長度、KV cache、取樣及測速方法。讀入與生成分別是 prefill 和 decode，均以 token/s 計；不同工作負載不可直接比較。記憶體包含執行額外負擔，不能拿量化權重大小直接推算能否放進顯存。

## 原圖十列：作者自述，不是獨立驗證

- Inkling 2 Mini SQ-20：約 22GB，GB10 生成 17–35、讀入 770–1300；作者另稱 SQ-10 約 10.5GB。引擎加速 2–3 倍是作者聽說，未證實。
- Qwen3.8 27B Heretic NVFP4：約 21GB，生成 25–43、讀入約 2000；文中稱聊天約 25、寫程式約 43。各數值條件未完整披露。
- Occamy 1.0 35B Q6_K：約 29GB，GB10 生成 55–64、讀入約 1650；並非一般 24GB 顯卡必然能完整載入。
- Nemotron Bolt 74B 社群 24GB 版：約 29GB，GB10 生成 57–75、讀入 600–1000。24GB 是版本名稱，不是含上下文的峰值保證；作者稱測試 22 題有 16 題照做，題目及方法未公開。
- Qwen3.8 Flash Next Swift 1.5 IQ3_S：約 58GB，GB10 生成 48–55、讀入約 2000。
- 同系列 4bit MLX：約 72GB，Mac 生成 106–132、讀入 1700–2100；原帖列出的倉庫 API 回 401，無法驗證公開性、授權或具體實作。
- 同系列 UD-IQ4_XS：約 78GB，原圖生成 43–50、讀入約 2200；原文稱 GB10 峰值 78GB。
- 同系列 oQ5e MLX：約 94–110GB，原圖生成 52–78、讀入約 1660；原文稱 128GB Mac。精度較高不保證每項任務品質更好。
- Hy4-Flash SQ-64：約 59GB；原圖生成 35–74、讀入 750–830，原文區分 GB10 35–42／約 750，Mac 62–74／約 800。
- Hy4-Flash SQ-96／128：約 100–112GB，原圖生成 28–41、讀入約 890；原文稱 Mac SQ-96 生成約 41。SQ-128 四題程式全過與拒答題結果均為作者小樣本自述，非安全或能力認證。

## 來源與授權：2026-11-27 Hugging Face API 模型卡 metadata

以下是倉庫自行標示，非法律結論；需同時檢查衍生權重、基礎模型、使用限制及再散布條件。尤其 Qwen Flash 原始模型標 Qwen Community 1.0，與部分衍生卡標 Apache-2.0 不一致，不能僅憑衍生標籤認定授權；Swift 另標專屬條款。限制可能變更，使用前應讀原文。

1. [SC117 Inkling Strata](https://huggingface.co/SC117/Inkling-2-Mini-abliterated-Strata)：Apache-2.0；base 是 [thinkingmachines Inkling 2 Mini](https://huggingface.co/thinkingmachines/Inkling-2-Mini)，官方卡亦標 Apache-2.0。
2. [SC117 Occamy GGUF](https://huggingface.co/SC117/occamy-1.0-abliterated-FIT-GGUF)：Apache-2.0；base [Accio-Lab Occamy 1.0](https://huggingface.co/Accio-Lab/occamy-1.0) 卡標 Apache-2.0，並列 Qwen3.6-35B-A3B 為基礎。
3. [BoldingBuilds Nemotron Bolt GGUF](https://huggingface.co/BoldingBuilds/NVIDIA-Nemotron-3.5-Bolt-74B-A9B-Abliterated-24GB-GGUF)：OpenMDW 1.1，非 Apache；[NVIDIA 原模型](https://huggingface.co/nvidia/NVIDIA-Nemotron-3.5-Bolt-74B-A9B-BF16)亦標相同授權。原模型標 image-text-to-text；特定衍生版是否完整保留影片管線未實測。
4. [SC117 Swift Q3 GGUF](https://huggingface.co/SC117/Swift-1.5-Qwen3.8-Flash-Next-GSQ-RCO-abliterated-GGUF)：模型卡標 Swift Open License 1.0，基礎是 ukisai 的 Swift 衍生模型。
5. [SC117 Qwen Flash UD GGUF](https://huggingface.co/SC117/Qwen3.8-Flash-Next-abliterated-UD-GGUF)：卡標 Apache-2.0；[Qwen 原始 Flash](https://huggingface.co/Qwen/Qwen3.8-Flash-Next)卡標 Qwen Community 1.0，存在上述衝突。
6. [ARC4NUM Flash 4bit MLX](https://huggingface.co/ARC4NUM/Qwen3.8-Flash-Next-Uncensored-MLX-Serve-4bit)：API 返回 401；不存在、私人或限制存取均可能，無法判定，授權未核實。
7. [mlx-community Flash oQ5e](https://huggingface.co/mlx-community/Qwen3.8-Flash-Next-Uncensored-oQ5e-mtp)：卡標 Qwen Community 1.0；為第三方量化。
8. [SmokeyPete Qwen 27B Heretic NVFP4](https://huggingface.co/SmokeyPete/Qwen3.8-27B-Heretic-NVFP4-DGX-Spark)：卡標 Apache-2.0，[Qwen 27B 原卡](https://huggingface.co/Qwen/Qwen3.8-27B)亦標 Apache-2.0。NVFP4／DGX Spark 為特定格式及目標環境，非所有後端可直接執行。
9. [strata-engine Hy4 Flash](https://huggingface.co/strata-engine/Hy4-Flash-Strata)：卡標 Tencent HY License；base [tencent Hy4-flash](https://huggingface.co/tencent/Hy4-flash)亦標 Tencent HY License。不能推定商用條件與 Apache 相同。
10. [alesha-pro Hy4 Flash GGUF](https://huggingface.co/alesha-pro/Hy4-flash-Uncensored-GGUF)：卡標 Tencent HY License；原帖稱其為拒答修正來源，具體修正檔相容性、授權及操作方式未核驗，不等同已驗證安全。

## 判讀與風險

作者推薦 Qwen Flash 是個人經驗；「無審查」是社群稱呼，不保證政治中立、事實正確、無偏見或一定不拒答。作者提及 Strata 官方 12GB RTX 5070 加 64GB 記憶體達 53 token/s，以及 Hy4 官方 64GB 記憶體加 8GB 顯卡可跑；本次未獨立核對該兩組官方完整測試條件，僅屬轉述，不能當保證。作者聽說 48GB 加 SSD 可跑但未實測，同樣未證實。GB10 統一記憶體、Mac 統一記憶體與獨立 GPU VRAM 不能直接等同。實際需考慮上下文/KV cache、推論引擎版本、系統餘量及多模態元件。不要盲目執行社群程式或修正檔；先查來源、授權、雜湊，隔離執行並對 Agent 採最小權限。

本次只讀取模型卡 metadata，未下載權重、未安裝、未執行或測速。相關舊文：[Inkling 2 Mini](https://m11808008.github.io/hermes/knowledge-base/articles/2026-11-23-threads-inkling-2-mini.html)。
