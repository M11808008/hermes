#!/usr/bin/env python3
from pathlib import Path
from datetime import date, timedelta
import json, re, html, shutil
BASE = Path('/Users/luarn/.hermes/user-notes/knowledge-base')
SITE = Path('/Users/luarn/.hermes/user-notes/knowledge-base-site')
DEPLOY = Path('/Users/luarn/.hermes/deploy/hermes')
PUBLIC_BASE = 'https://m11808008.github.io/hermes/knowledge-base/'
CSS = ':root{--bg:#090b10;--panel:#121722;--text:#eef2ff;--muted:#98a2b3;--line:#2a3345;--gold:#d8b46a;--blue:#7dd3fc}*{box-sizing:border-box}body{margin:0;font-family:-apple-system,BlinkMacSystemFont,"Noto Sans TC","Segoe UI",sans-serif;background:radial-gradient(circle at top left,#1e293b 0,#090b10 38%,#05060a 100%);color:var(--text)}a{color:var(--blue);text-decoration:none}a:hover{text-decoration:underline}.wrap{max-width:1180px;margin:0 auto;padding:28px}.hero{padding:34px;border:1px solid var(--line);border-radius:28px;background:linear-gradient(135deg,rgba(216,180,106,.16),rgba(125,211,252,.08)),rgba(18,23,34,.86);box-shadow:0 24px 80px rgba(0,0,0,.35)}.hero-inner{display:grid;grid-template-columns:minmax(0,1fr) 148px;gap:26px;align-items:center}.radar-mark{width:148px;height:148px;border-radius:34px;object-fit:cover;object-position:center 58%;filter:drop-shadow(0 22px 34px rgba(0,0,0,.42))}.eyebrow{color:var(--gold);letter-spacing:.16em;text-transform:uppercase;font-size:12px}.hero h1{font-size:44px;line-height:1.05;margin:12px 0}.hero p{color:#cbd5e1;font-size:18px;max-width:780px}.toolbar{display:grid;grid-template-columns:1fr auto;gap:14px;margin:24px 0}.search{width:100%;padding:14px 16px;border-radius:16px;border:1px solid var(--line);background:#0f1420;color:var(--text);font-size:16px}.pill,.tag,.tag-button{display:inline-flex;align-items:center;gap:6px;border:1px solid var(--line);background:#111827;border-radius:999px;padding:7px 11px;color:#dbeafe;font-size:13px;margin:4px}.tag-button{cursor:pointer;font:inherit}.tag-button:hover,.tag-button.active{border-color:var(--gold);color:#fde68a;background:#1b2434}.tag-count{font-size:11px;color:#94a3b8;background:#0b1020;border-radius:999px;padding:1px 6px}.topic-panel{margin:18px 0 26px;padding:16px;border:1px solid var(--line);border-radius:22px;background:rgba(18,23,34,.62)}.topic-head{display:flex;justify-content:space-between;gap:12px;align-items:flex-start}.topic-head p{margin:4px 0 0;color:var(--muted);line-height:1.6}.topic-featured{margin-top:10px}.topic-all{margin-top:10px;border-top:1px solid var(--line);padding-top:10px}.topic-all>summary,.topic-group>summary{cursor:pointer;color:#fde68a;list-style:none}.topic-all>summary::-webkit-details-marker,.topic-group>summary::-webkit-details-marker{display:none}.topic-all>summary:before,.topic-group>summary:before{content:"＋";display:inline-block;margin-right:8px;color:var(--gold)}.topic-all[open]>summary:before,.topic-group[open]>summary:before{content:"－"}.topic-groups{display:grid;grid-template-columns:repeat(auto-fit,minmax(230px,1fr));gap:10px;margin-top:10px}.topic-group{border:1px solid rgba(148,163,184,.22);border-radius:16px;padding:10px;background:rgba(15,20,32,.62)}.topic-group summary{display:flex;justify-content:space-between;gap:10px}.topic-group summary span{color:var(--muted);font-size:12px}.topic-group-body{margin-top:8px}.clear-filter{cursor:pointer;color:#fde68a}.grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(280px,1fr));gap:16px}.card{border:1px solid var(--line);border-radius:22px;padding:18px;background:rgba(18,23,34,.88);transition:.2s}.card:hover{transform:translateY(-2px);border-color:rgba(216,180,106,.55)}.meta{color:var(--muted);font-size:13px}.card h2{font-size:20px;margin:10px 0}.card p{color:#cbd5e1;line-height:1.65}.layout{display:grid;grid-template-columns:minmax(0,1fr) 280px;gap:22px}.article{border:1px solid var(--line);border-radius:24px;background:rgba(18,23,34,.9);padding:30px}.article h1{font-size:34px}.article h2{margin-top:32px;color:#fde68a}.article p,.article li{line-height:1.85;color:#d6deed}.article img{max-width:100%;height:auto;border-radius:18px;border:1px solid var(--line);box-shadow:0 18px 50px rgba(0,0,0,.32);background:#05060a}.article figure{margin:22px 0}.article figcaption{color:var(--muted);font-size:13px;margin-top:8px}.side{position:sticky;top:20px;align-self:start;border:1px solid var(--line);border-radius:22px;background:rgba(18,23,34,.8);padding:18px}.section-title{margin:28px 0 14px;color:#fde68a}.footer{color:var(--muted);margin:34px 0 10px;text-align:center}@media(max-width:820px){.wrap{padding:18px}.hero{padding:22px}.hero-inner{grid-template-columns:1fr;gap:14px}.radar-mark{width:76px;height:76px;border-radius:18px;justify-self:start;order:-1}.hero h1{font-size:32px}.hero p{font-size:16px}.toolbar{grid-template-columns:1fr}.layout{grid-template-columns:1fr}.side{position:static}}@media(max-width:480px){.radar-mark{width:64px;height:64px;border-radius:16px}.hero{padding:20px}}'

def parse(text):
    meta, body = {}, text
    if text.startswith('---'):
        parts = text.split('---', 2)
        raw, body = parts[1], parts[2].lstrip('\n')
        cur = None
        for line in raw.splitlines():
            if re.match(r'^[A-Za-z0-9-]+:', line):
                k,v = line.split(':',1); cur=k.strip(); v=v.strip().strip('"')
                meta[cur] = v if v else []
            elif line.strip().startswith('-') and cur:
                if not isinstance(meta.get(cur), list): meta[cur]=[meta[cur]] if meta.get(cur) else []
                meta[cur].append(line.strip()[1:].strip())
    return meta, body

def linkify(text):
    """Render explicit Markdown links and conservative bare URL autolinks.

    Bare CJK text is ambiguous without a delimiter; use Markdown link syntax
    or percent encoding for URLs containing CJK characters.
    """
    def anchor(url, label):
        return '<a href="'+html.escape(url, quote=True)+'" target="_blank" rel="noopener">'+html.escape(label)+'</a>'

    def url_end(start, markdown=False):
        depth = 0
        i = start
        while i < len(text):
            c = text[i]
            if c.isspace() or c in '<>"\'`' or (not markdown and (ord(c) > 127 or c in '[]')):
                break
            if c == '(':
                depth += 1
            elif c == ')':
                if not depth: break
                depth -= 1
            i += 1
        return i

    result = []
    i = 0
    while i < len(text):
        m = re.search(r'\[([^\]\n]+)\]\((https?://)|https?://', text[i:])
        if not m:
            result.append(html.escape(text[i:])); break
        start = i + m.start()
        result.append(html.escape(text[i:start]))
        if m.group(1) is not None:
            url_start = i + m.end() - len(m.group(2))
            end = url_end(url_start, markdown=True)
            if end < len(text) and text[end] == ')':
                result.append(anchor(text[url_start:end], m.group(1)))
                i = end + 1
                continue
        else:
            end = url_end(start)
            while end > start and text[end-1] in '.,;:!?': end -= 1
            if end > start + len(m.group(0)):
                result.append(anchor(text[start:end], text[start:end]))
                i = end
                continue
        result.append(html.escape(text[start:start+1])); i = start+1
    return ''.join(result)
def render_image_line(raw):
    m = re.match(r'^!\[([^\]]*)\]\(([^\s)]+)(?:\s+"([^"]*)")?\)\s*$', raw.strip())
    if not m:
        return None
    alt, src, title = m.group(1), m.group(2), m.group(3) or m.group(1)
    safe_src = html.escape(src, quote=True)
    safe_alt = html.escape(alt, quote=True)
    caption = '<figcaption>'+html.escape(title)+'</figcaption>' if title else ''
    return '<figure><img src="'+safe_src+'" alt="'+safe_alt+'" loading="lazy" referrerpolicy="no-referrer">'+caption+'</figure>'
def strip_duplicate_title_heading(md, title):
    """Remove the article body's first H1 when it duplicates frontmatter title.

    Article pages already render frontmatter `title` as the page H1. Most
    archived markdown files also start with `# <same title>`, which otherwise
    creates two identical headings in the generated HTML.
    """
    lines = md.splitlines()
    while lines and not lines[0].strip():
        lines.pop(0)
    if lines and lines[0].startswith('# '):
        heading = lines[0][2:].strip()
        if heading == (title or '').strip():
            lines = lines[1:]
            while lines and not lines[0].strip():
                lines.pop(0)
    return '\n'.join(lines)

def mdhtml(md):
    out=[]; ul=False
    for raw in md.splitlines():
        raw=raw.rstrip()
        image_html = render_image_line(raw)
        if image_html:
            if ul: out.append('</ul>'); ul=False
            out.append(image_html)
            continue
        if not raw:
            if ul: out.append('</ul>'); ul=False
            continue
        if raw.startswith('# '):
            if ul: out.append('</ul>'); ul=False
            out.append('<h1>'+html.escape(raw[2:])+'</h1>')
        elif raw.startswith('## '):
            if ul: out.append('</ul>'); ul=False
            out.append('<h2>'+html.escape(raw[3:])+'</h2>')
        elif re.match(r'^[-*] ', raw) or re.match(r'^\d+\. ', raw):
            if not ul: out.append('<ul>'); ul=True
            item=re.sub(r'^\d+\. ','',raw[2:] if raw[:2] in ['- ','* '] else raw)
            out.append('<li>'+linkify(item)+'</li>')
        else:
            if ul: out.append('</ul>'); ul=False
            out.append('<p>'+linkify(raw)+'</p>')
    if ul: out.append('</ul>')
    return '\n'.join(out)

def collect():
    items=[]
    for p in sorted((BASE/'articles').glob('**/*.md')):
        meta, body = parse(p.read_text(encoding='utf-8'))
        if str(meta.get('public','true')).lower() == 'false': continue
        raw_topics = meta.get('topics') or meta.get('tags') or []
        topics = raw_topics if isinstance(raw_topics, list) else [raw_topics]
        uses = meta.get('use', []) if isinstance(meta.get('use', []), list) else [meta.get('use')]
        links=[]
        for k in ['original-url','canonical-url']:
            if meta.get(k): links.append(meta[k])
        extra=meta.get('links', [])
        links += extra if isinstance(extra, list) else ([extra] if extra else [])
        m=re.search(r'# 一句話摘要\s+(.+?)(?:\n#|\Z)', body, re.S)
        excerpt=re.sub(r'\s+',' ',m.group(1)).strip() if m else re.sub(r'\s+',' ',body)[:160]
        items.append({'title':meta.get('title',p.stem),'date':meta.get('date','1970-01-01'),'source':meta.get('source',''),'author':meta.get('author',''),'type':meta.get('type','article'),'topics':[t for t in topics if t],'use':[u for u in uses if u],'importance':meta.get('importance','medium'),'status':meta.get('status','archived'),'links':links,'excerpt':excerpt,'slug':p.stem,'html':'articles/'+p.stem+'.html','markdown':str(p.relative_to(BASE)),'body':body})
    return sorted(items, key=lambda x:x['date'], reverse=True)

def page(title, content, rel=''):
    return '<!doctype html><html lang="zh-Hant"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1"><title>'+html.escape(title)+'</title><link rel="stylesheet" href="'+rel+'assets/style.css"></head><body><div class="wrap">'+content+'<div class="footer">Luarn-Pin Knowledge Base · Generated by Hermes Agent</div></div></body></html>'

def weekly(items, today=None):
    today = today or date.today(); start=today-timedelta(days=6)
    week=[i for i in items if start.isoformat() <= i['date'] <= today.isoformat()] or items[:8]
    topics={}
    for i in week:
        for t in i['topics']: topics[t]=topics.get(t,0)+1
    top=sorted(topics.items(), key=lambda x:x[1], reverse=True)[:8]
    slug=today.isoformat()+'-weekly-digest'
    md=['---','title: '+today.isoformat()+' 週報與知識回顧','date: '+today.isoformat(),'type: weekly-digest','public: true','---','','# 本週知識回顧','','期間：'+start.isoformat()+' 至 '+today.isoformat(),'','# 主題焦點']
    md += ['- '+t+'：'+str(c)+' 篇' for t,c in top]
    md += ['','# 本週重要資料'] + ['- '+i['title']+'：'+i['excerpt']+'（'+PUBLIC_BASE+i['html']+'）' for i in week] + ['','# 知識庫首頁','',PUBLIC_BASE]
    (BASE/'weekly-digests'/ (slug+'.md')).write_text('\n'.join(md)+'\n', encoding='utf-8')
    cards=''.join(['<div class="card"><div class="meta">'+html.escape(i['date'])+' · '+html.escape(i['type'])+'</div><h2><a href="../'+i['html']+'">'+html.escape(i['title'])+'</a></h2><p>'+html.escape(i['excerpt'])+'</p></div>' for i in week])
    tags=''.join(['<span class="tag">'+html.escape(t)+' · '+str(c)+'</span>' for t,c in top])
    content='<div class="hero"><div class="eyebrow">Weekly Digest</div><h1>'+today.isoformat()+' 週報與知識回顧</h1><p>自動整理本週收藏與學習重點，保留原文連結，方便跨裝置查閱。</p><p><a class="pill" href="../index.html">返回知識庫首頁</a></p></div><h2 class="section-title">主題焦點</h2>'+tags+'<h2 class="section-title">本週重要資料</h2><div class="grid">'+cards+'</div>'
    return slug, page(today.isoformat()+' 週報與知識回顧', content, '../')

def build():
    items=collect();
    for sub in ['assets','articles','weekly','data','topics']: (SITE/sub).mkdir(parents=True, exist_ok=True)
    (SITE/'assets/style.css').write_text(CSS, encoding='utf-8')
    assets_src = BASE/'assets'
    assets_dst = SITE/'assets'
    if assets_src.exists():
        # Private originals are retained locally but must never enter the generated
        # site (which is subsequently copied to the public GitHub Pages checkout).
        for src in assets_src.rglob('*'):
            if src.is_file() and 'private-documents' not in src.relative_to(assets_src).parts:
                dst = assets_dst/src.relative_to(assets_src)
                dst.parent.mkdir(parents=True, exist_ok=True)
                shutil.copy2(src, dst)
    public=[{k:v for k,v in i.items() if k!='body'} for i in items]
    (BASE/'metadata/index.json').write_text(json.dumps(public, ensure_ascii=False, indent=2), encoding='utf-8')
    (SITE/'data/index.json').write_text(json.dumps(public, ensure_ascii=False, indent=2), encoding='utf-8')
    topic_counts={}
    for i in items:
        for t in i['topics']:
            topic_counts[t]=topic_counts.get(t,0)+1
    alltopics=sorted(topic_counts)
    top_topics=sorted(topic_counts.items(), key=lambda x:(-x[1], x[0].lower()))[:12]
    group_defs=[
        ('開發與程式', ['codex','code','coding','github','repo','framework','plugin','python','developer']),
        ('AI Agent / 自動化', ['agent','automation','workflow','mcp','browser','computer','api','tool','agentic']),
        ('模型與平台', ['gpt','chatgpt','claude','gemini','copilot','openai','anthropic','google','qwen','llm','model']),
        ('教育與課程', ['education','course','university','student','learning','教學','課程']),
        ('多媒體與內容', ['image','meme','instagram','facebook','line','youtube','content','tagging','cloudinary']),
        ('商業與生產力', ['office','excel','powerpoint','productivity','business','lead','sales','報價']),
        ('美食', ['美食','food','restaurant','餐廳','料理','市場','小吃','火鍋','咖啡','甜點','牛肉麵','涼麵'])]
    grouped={name:[] for name,_ in group_defs}; grouped['其他主題']=[]
    for t in alltopics:
        low=t.lower(); placed=False
        for name,keys in group_defs:
            if any(k in low for k in keys):
                grouped[name].append(t); placed=True; break
        if not placed: grouped['其他主題'].append(t)
    def topic_button(t, cls='tag-button'):
        return '<button class="'+cls+'" data-tag="'+html.escape(t.lower())+'" type="button">'+html.escape(t)+'<span class="tag-count">'+str(topic_counts.get(t,0))+'</span></button>'
    featured=''.join([topic_button(t) for t,c in top_topics])
    groups=''.join(['<details class="topic-group"><summary>'+html.escape(name)+'<span>'+str(len(ts))+' 個</span></summary><div class="topic-group-body">'+''.join([topic_button(t) for t in ts])+'</div></details>' for name,ts in grouped.items() if ts])
    cards=''.join(['<article class="card" data-topics="'+html.escape('|||'.join([t.lower() for t in i['topics']]))+'" data-q="'+html.escape((i['title']+' '+' '.join(i['topics'])+' '+i['excerpt']).lower())+'"><div class="meta">'+html.escape(i['date'])+' · '+html.escape(i['source'])+' · '+html.escape(i['importance'])+'</div><h2><a href="'+i['html']+'">'+html.escape(i['title'])+'</a></h2><p>'+html.escape(i['excerpt'])+'</p><div>'+''.join([topic_button(t, 'tag-button mini') for t in i['topics'][:4]])+'</div></article>' for i in items])
    topicpanel='<section class="topic-panel"><div class="topic-head"><div><h2 class="section-title">主題探索</h2><p>先顯示最常用標籤；需要完整清單時再展開分類，避免首頁被標籤淹沒。</p></div><button class="tag-button clear-filter" data-tag="" type="button">全部</button></div><div class="topic-featured">'+featured+'</div><details class="topic-all"><summary>展開全部主題分類</summary><div class="topic-groups">'+groups+'</div></details></section>'
    idx='<section class="hero"><div class="hero-inner"><div><div class="eyebrow">Luarn-Pin Knowledge Base</div><h1>AI 學習雷達</h1><p>自動歸檔你在 LINE / Telegram 分享的新聞、技術文章與靈感，保留原始鏈結，並產生可跨裝置查詢的 HTML 知識庫。</p><p><a class="pill" href="weekly/">週報</a><a class="pill" href="data/index.json">JSON Index</a></p></div><img class="radar-mark" src="assets/ai-learning-radar-logo.jpg" alt="愛馬仕小小斌頭像 logo" loading="eager"></div></section><div class="toolbar"><input id="search" class="search" placeholder="搜尋標題、主題、摘要，或點選精選/分類主題…"><span class="pill" id="result-count">共 '+str(len(items))+' 筆</span></div>'+topicpanel+'<h2 class="section-title">最新歸檔</h2><div class="grid" id="cards">'+cards+'</div><script>const s=document.getElementById("search"),count=document.getElementById("result-count");const buttons=[...document.querySelectorAll(".tag-button[data-tag]")];function applyFilter(tag){if(tag!==undefined)s.value=tag;const q=s.value.toLowerCase().trim();let n=0;document.querySelectorAll(".card").forEach(c=>{const topics=(c.dataset.topics||"").split("|||");const ok=!q||c.dataset.q.includes(q)||topics.includes(q);c.style.display=ok?"block":"none";if(ok)n++});buttons.forEach(b=>b.classList.toggle("active",q&&b.dataset.tag===q));count.textContent=q?`篩選：${q} · ${n} 筆`:`共 ${document.querySelectorAll(".card").length} 筆`;}s.addEventListener("input",()=>applyFilter());buttons.forEach(b=>b.addEventListener("click",()=>applyFilter(b.dataset.tag)));const initial=new URLSearchParams(location.search).get("tag");if(initial)applyFilter(initial.toLowerCase());</script>'
    (SITE/'index.html').write_text(page('Luarn-Pin Knowledge Base', idx), encoding='utf-8')
    for i in items:
        links=''.join(['<p><a href="'+html.escape(u)+'" target="_blank" rel="noopener">'+html.escape(u)+'</a></p>' for u in i['links']])
        side='<aside class="side"><p><a href="../index.html">← 回首頁</a></p><div class="meta">'+html.escape(i['date'])+' · '+html.escape(i['source'])+' · '+html.escape(i['type'])+'</div><h3>標籤</h3>'+''.join(['<span class="tag">'+html.escape(t)+'</span>' for t in i['topics']])+'<h3>原始連結</h3>'+links+'</aside>'
        body_html = mdhtml(strip_duplicate_title_heading(i['body'], i['title']))
        content='<div class="layout"><article class="article"><h1>'+html.escape(i['title'])+'</h1>'+body_html+'</article>'+side+'</div>'
        (SITE/i['html']).write_text(page(i['title'], content, '../'), encoding='utf-8')
    slug, wh = weekly(items)
    (SITE/'weekly'/(slug+'.html')).write_text(wh, encoding='utf-8')
    (SITE/'weekly/index.html').write_text('<!doctype html><meta charset="utf-8"><meta http-equiv="refresh" content="0; url='+slug+'.html"><a href="'+slug+'.html">latest weekly digest</a>', encoding='utf-8')
    if DEPLOY.exists():
        target=DEPLOY/'knowledge-base'
        if target.exists(): shutil.rmtree(target)
        shutil.copytree(SITE, target)
    print(json.dumps({'success':True,'articles':len(items),'weekly':slug,'site':str(SITE),'url':PUBLIC_BASE}, ensure_ascii=False, indent=2))
if __name__ == '__main__': build()
