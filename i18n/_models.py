"""Render the DEX table from one checked data snapshot, in all four locales."""
from html import escape as e
from pathlib import Path
import json
import re

ROOT = Path(__file__).resolve().parent.parent
LABELS = {
 'zh': ('复制', '已复制', 'MT 地址', 'API 调用 ID', '在 FOMO 查看', '模型与 MT 对照（{n} 个）', '资料日期：{date} · DEX {n} 个 · 分类沿用 Marketplace。'),
 'en': ('Copy', 'Copied', 'MT address', 'API model ID', 'View on FOMO', 'Models and MTs ({n} tokens)', 'Data as of {date} · {n} DEX · Marketplace categories.'),
 'ja': ('コピー', 'コピー済み', 'MT アドレス', 'API モデル ID', 'FOMO で表示', 'モデルと MT の対応（{n} 件）', '確認日：{date} · DEX {n} 件 · Marketplace の分類。'),
 'ko': ('복사', '복사됨', 'MT 주소', 'API 모델 ID', 'FOMO에서 보기', '모델 및 MT 목록 ({n}개)', '확인일: {date} · DEX {n}개 · Marketplace 분류.'),
}

def render_models(html, lang):
    data = json.loads((ROOT/'data/season-3-models.json').read_text())
    models = [m for m in data['models'] if m['category'] == 'DEX']
    copy, done, address, api, view, title, snapshot = LABELS[lang]
    title = title.format(n=len(models))
    def button(value, kind, label):
        return f'<div class="model-id-cell"><button class="copy-id" type="button" data-copy-kind="{kind}" aria-label="{e(label)}: {e(value)}" disabled><i data-lucide="copy" class="copy-icon" aria-hidden="true"></i><i data-lucide="check" class="copied-icon" aria-hidden="true"></i><code>{e(value)}</code><span class="copied-label" aria-hidden="true">{done}</span></button></div>'
    rows = []
    for m in models:
        symbol, chain, model = e(m['symbol']), e(m['chainName']), e(m['modelId'])
        family = next(k for k in ('gemini','deepseek','kimi') if m['modelId'].lower().startswith(k))
        name = f'<p class="mt-project-name">{e(m["name"])}</p>' if m['name'] and m['name'] != m['symbol'] else ''
        rows.append(f'<tr role="row"><td role="cell"><div class="mt-heading"><strong>{symbol}</strong><span class="mt-chain"><img src="/assets/tokens/{e(m["chainKey"])}.svg" alt="" width="14" height="14">{chain}</span></div>{name}' + button(m['address'],'address',f'{copy} {m["symbol"]} {address} ({m["chainName"]})') + f'</td><td role="cell"><span class="mapping-mobile-label" aria-hidden="true">{api}</span><p class="mt-base-model"><img src="/assets/tokens/{family}.svg" alt="" width="18" height="18"><span>Model ID: {model}</span></p>' + button(m['apiPlatformId'],'model',f'{copy} {api}') + f'</td><td role="cell"><a class="model-project-link" href="{e(m["projectUrl"])}" target="_blank" rel="noopener" aria-label="{view} · {symbol} ({chain})"><img src="/assets/tokens/fomo.svg" alt="" width="16" height="16"><span>FOMO</span><i data-lucide="arrow-up-right" aria-hidden="true"></i></a></td></tr>')
    html = re.sub(r'(<tbody role="rowgroup">)[\s\S]*?(</tbody>)',lambda m:m[1]+'\n'+'\n'.join(rows)+'\n'+m[2],html,count=1)
    html = re.sub(r'(<details class="model-ids"[^>]*><summary>)[^<]*',lambda m:m[1]+title,html,count=1)
    html = re.sub(r'(<caption class="sr-only">)[^<]*',lambda m:m[1]+title+' · DEX',html,count=1)
    html = re.sub(r'(<h3 class="mapping-group-title">DEX <span>)\(\d+\)',lambda m:m[1]+f'({len(models)})',html,count=1)
    html = re.sub(r'(<p class="mapping-snapshot">)[^<]*',lambda m:m[1]+snapshot.format(date=data['checkedOn'],n=len(models)),html,count=1)
    return html
