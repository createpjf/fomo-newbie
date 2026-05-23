# -*- coding: utf-8 -*-
"""S2 EN/KO/JA link fixes + EN/KO JS/CSS leak fixes."""

S2_LINKS = {
    "en": {
        "guide": "/en",
        "s1": "/season-1/en",
        "s2": "/season-2/en",
    },
    "ko": {
        "guide": "/ko",
        "s1": "/season-1/ko",
        "s2": "/season-2/ko",
    },
    "ja": {
        "guide": "/ja",
        "s1": "/season-1/ja",
        "s2": "/season-2/ja",
    },
}


S2_EN_EXTRA = [
    ("content:'达标线'", "content:'Min target'"),
    ("content:'展开'", "content:'Expand'"),
    ("content:'收起'", "content:'Collapse'"),
    ("/* CJK 排版：正文减少行尾孤字（渐进增强） */", "/* CJK typography (progressive enhancement) */"),
    ("<!-- ============ 04 · FRAMEWORK RECAP (沿用 S1) ============ -->", "<!-- ============ 04 · FRAMEWORK RECAP (from S1) ============ -->"),
    ("if(lbl) lbl.textContent = '已复制';", "if(lbl) lbl.textContent = 'Copied';"),
    ("if(v<=0) return '未持有';", "if(v<=0) return 'None';"),
    ("if(v<=25) return '少量持有';", "if(v<=25) return 'Small';"),
    ("if(v<=50) return '中等持有';", "if(v<=50) return 'Medium';"),
    ("if(v<=75) return '较多持有';", "if(v<=75) return 'Large';"),
    ("return '大量持有';", "return 'Whale';"),
    (
        "'基础份额 '+(base*100).toFixed(1)+'%（'+myV+'÷'+poolV+'）× 质押'+(stakeOn?'×1.5':'×1')+' × gmFLOCK×'+gmM.toFixed(2)+' ≈ '+pct.toFixed(1)+'%';",
        "'Base share '+(base*100).toFixed(1)+'% ('+myV+'÷'+poolV+') × stake'+(stakeOn?'×1.5':'×1')+' × gmFLOCK×'+gmM.toFixed(2)+' ≈ '+pct.toFixed(1)+'%';",
    ),
    (
        "document.getElementById('avPhaseLabel').textContent=(t<0.2?'早期':t<0.7?'进行中':'后期')+' · 约 '+Math.round(t*100)+'%';",
        "document.getElementById('avPhaseLabel').textContent=(t<0.2?'Early':t<0.7?'Mid':'Late')+' · ~'+Math.round(t*100)+'%';",
    ),
    (
        "document.getElementById('avGapText').innerHTML='当前阶段：质押比不质押大约多 <b style=\"color:#fff\">'+Math.round(gap*100)+'%</b> 得分（α≈'+alpha.toFixed(2)+'，仅作理解用）。';",
        "document.getElementById('avGapText').innerHTML='At this phase, staking scores ~<b style=\"color:#fff\">'+Math.round(gap*100)+'%</b> higher than not staking (α≈'+alpha.toFixed(2)+', illustrative).';",
    ),
]

S2_KO_EXTRA = [
    ("content:'达标线'", "content:'최소 목표'"),
    ("content:'展开'", "content:'펼치기'"),
    ("content:'收起'", "content:'접기'"),
    ("/* CJK 排版：正文减少行尾孤字（渐进增强） */", "/* CJK typography (progressive enhancement) */"),
    ("<!-- ============ 04 · FRAMEWORK RECAP (沿用 S1) ============ -->", "<!-- ============ 04 · FRAMEWORK RECAP (from S1) ============ -->"),
    ("if(lbl) lbl.textContent = '已复制';", "if(lbl) lbl.textContent = '복사됨';"),
    ("if(v<=0) return '未持有';", "if(v<=0) return '미보유';"),
    ("if(v<=25) return '少量持有';", "if(v<=25) return '소량';"),
    ("if(v<=50) return '中等持有';", "if(v<=50) return '중간';"),
    ("if(v<=75) return '较多持有';", "if(v<=75) return '다량';"),
    ("return '大量持有';", "return '대량';"),
    (
        "'基础份额 '+(base*100).toFixed(1)+'%（'+myV+'÷'+poolV+'）× 质押'+(stakeOn?'×1.5':'×1')+' × gmFLOCK×'+gmM.toFixed(2)+' ≈ '+pct.toFixed(1)+'%';",
        "'기본 비중 '+(base*100).toFixed(1)+'% ('+myV+'÷'+poolV+') × 스테이킹'+(stakeOn?'×1.5':'×1')+' × gmFLOCK×'+gmM.toFixed(2)+' ≈ '+pct.toFixed(1)+'%';",
    ),
    (
        "document.getElementById('avPhaseLabel').textContent=(t<0.2?'早期':t<0.7?'进行中':'后期')+' · 约 '+Math.round(t*100)+'%';",
        "document.getElementById('avPhaseLabel').textContent=(t<0.2?'초기':t<0.7?'진행 중':'후기')+' · 약 '+Math.round(t*100)+'%';",
    ),
    (
        "document.getElementById('avGapText').innerHTML='当前阶段：质押比不质押大约多 <b style=\"color:#fff\">'+Math.round(gap*100)+'%</b> 得分（α≈'+alpha.toFixed(2)+'，仅作理解用）。';",
        "document.getElementById('avGapText').innerHTML='현재 단계: 스테이킹이 미스테이킹보다 약 <b style=\"color:#fff\">'+Math.round(gap*100)+'%</b> 높은 점수 (α≈'+alpha.toFixed(2)+', 이해용).';",
    ),
]

S2_JA_EXTRA = [
    ("if(lbl) lbl.textContent = '已复制';", "if(lbl) lbl.textContent = 'コピー済み';"),
]
