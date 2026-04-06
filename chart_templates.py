#!/usr/bin/env python3
"""
chart_templates.py - 종목분석 리포트 차트 생성 모듈
report-generator가 이 파일을 import하여 데이터를 넘기면 SVG 문자열을 반환한다.

사용법:
  from chart_templates import radar_chart, bar_chart, line_chart, risk_heatmap, price_range_bar, donut_chart, etf_performance_chart
  svg = radar_chart([("Moat", 8), ("수익성", 7), ...])
"""
import math

C = {"bg":"#1A2733","border":"#2D3A45","text":"#E8EAED","sub":"#9AA0A6","buy":"#26A69A","sell":"#EF5350","blue":"#42A5F5","warn":"#FFA726","grid":"#21262d"}
SECTOR_COLORS = ["#42A5F5","#26A69A","#FFA726","#EF5350","#AB47BC","#66BB6A","#FF7043","#5C6BC0","#FFCA28","#78909C","#EC407A","#8D6E63"]

def radar_chart(scores, size=280):
    cx, cy, r = size//2, size//2+10, size//2-40
    n = len(scores)
    if n == 0: return ""
    def polar(i, val, mx=10):
        a = (2*math.pi*i/n) - math.pi/2
        return cx+r*(val/mx)*math.cos(a), cy+r*(val/mx)*math.sin(a)
    outer = " ".join("{:.1f},{:.1f}".format(*polar(i,10)) for i in range(n))
    inner = " ".join("{:.1f},{:.1f}".format(*polar(i,s)) for i,(_,s) in enumerate(scores))
    axes = ""
    guides = ""
    for v in [5,10]:
        pts = " ".join("{:.1f},{:.1f}".format(*polar(i,v)) for i in range(n))
        guides += '<polygon points="{}" fill="none" stroke="{}" stroke-width="0.5" stroke-dasharray="3,3"/>'.format(pts, C["grid"])
    for i,(label,s) in enumerate(scores):
        ox,oy = polar(i,10)
        lx,ly = polar(i,12.5)
        axes += '<line x1="{}" y1="{}" x2="{:.1f}" y2="{:.1f}" stroke="{}" stroke-width="0.5"/>'.format(cx,cy,ox,oy,C["grid"])
        anc = "end" if lx < cx-10 else ("start" if lx > cx+10 else "middle")
        axes += '<text x="{:.1f}" y="{:.1f}" fill="{}" font-size="11" text-anchor="{}" dominant-baseline="middle">{}</text>'.format(lx,ly,C["sub"],anc,label)
        sx,sy = polar(i,s)
        axes += '<circle cx="{:.1f}" cy="{:.1f}" r="3" fill="{}"/>'.format(sx,sy,C["buy"])
    return '<svg viewBox="0 0 {} {}" xmlns="http://www.w3.org/2000/svg" style="width:100%;max-width:{}px;">{}<polygon points="{}" fill="none" stroke="{}" stroke-width="1"/><polygon points="{}" fill="rgba(38,166,154,0.25)" stroke="{}" stroke-width="2"/>{}</svg>'.format(size,size+20,size,guides,outer,C["border"],inner,C["buy"],axes)

def bar_chart(years, revenue, op_income, unit="조원", estimates_from=None):
    w,h = 400,200
    n = len(years)
    if n == 0: return ""
    max_val = max(max(revenue),max(op_income))*1.2
    bar_w = min(28,(w-80)//(n*2)-4)
    ml,mb = 50,30
    bars = '<defs><pattern id="est" patternUnits="userSpaceOnUse" width="6" height="6"><path d="M0,6 L6,0" stroke="{}" stroke-width="1" opacity="0.4"/></pattern></defs>'.format(C["sub"])
    for i,yr in enumerate(years):
        xc = ml+(w-ml-20)*(i+0.5)/n
        rh = (revenue[i]/max_val)*(h-mb-20)
        ry = h-mb-rh
        rx = xc-bar_w-1
        fr = "url(#est)" if estimates_from and i>=estimates_from else C["blue"]
        bars += '<rect x="{:.0f}" y="{:.0f}" width="{}" height="{:.0f}" fill="{}" stroke="{}" stroke-width="0.5" rx="2"/>'.format(rx,ry,bar_w,rh,fr,C["blue"])
        oh = (op_income[i]/max_val)*(h-mb-20)
        oy = h-mb-oh
        ox = xc+1
        fo = "url(#est)" if estimates_from and i>=estimates_from else C["buy"]
        bars += '<rect x="{:.0f}" y="{:.0f}" width="{}" height="{:.0f}" fill="{}" stroke="{}" stroke-width="0.5" rx="2"/>'.format(ox,oy,bar_w,oh,fo,C["buy"])
        bars += '<text x="{:.0f}" y="{}" fill="{}" font-size="11" text-anchor="middle">{}</text>'.format(xc,h-8,C["sub"],yr)
    for v in [0,max_val*0.5,max_val]:
        y = h-mb-(v/max_val)*(h-mb-20)
        bars += '<line x1="{}" y1="{:.0f}" x2="{}" y2="{:.0f}" stroke="{}" stroke-width="0.5"/>'.format(ml-5,y,w-10,y,C["grid"])
        bars += '<text x="{}" y="{:.0f}" fill="{}" font-size="10" text-anchor="end" dominant-baseline="middle">{:.0f}</text>'.format(ml-8,y,C["sub"],v)
    legend = '<rect x="{}" y="5" width="10" height="10" fill="{}" rx="2"/><text x="{}" y="14" fill="{}" font-size="10">매출({})</text>'.format(ml,C["blue"],ml+14,C["sub"],unit)
    legend += '<rect x="{}" y="5" width="10" height="10" fill="{}" rx="2"/><text x="{}" y="14" fill="{}" font-size="10">영업이익({})</text>'.format(ml+80,C["buy"],ml+94,C["sub"],unit)
    return '<svg viewBox="0 0 {} {}" xmlns="http://www.w3.org/2000/svg" style="width:100%;max-width:{}px;">{}{}</svg>'.format(w,h+10,w,legend,bars)

def line_chart(years, series, labels=None, colors=None):
    if not series or not series[0]: return ""
    w,h = 380,180
    n = len(years)
    colors = colors or [C["blue"],C["buy"],C["warn"],C["sell"]]
    labels = labels or ["Series {}".format(i+1) for i in range(len(series))]
    all_v = [v for s in series for v in s if v is not None]
    if not all_v: return ""
    min_v,max_v = min(all_v)*0.8, max(all_v)*1.2
    if max_v==min_v: max_v=min_v+1
    ml,mb = 45,30
    def xy(i,v):
        x = ml+(w-ml-20)*i/max(n-1,1)
        y = h-mb-((v-min_v)/(max_v-min_v))*(h-mb-20)
        return x,y
    lines = ""
    for si,s in enumerate(series):
        col = colors[si%len(colors)]
        pts = []
        for i,v in enumerate(s):
            if v is not None:
                x,y = xy(i,v)
                pts.append("{:.1f},{:.1f}".format(x,y))
                lines += '<circle cx="{:.1f}" cy="{:.1f}" r="3" fill="{}"/>'.format(x,y,col)
        if pts:
            lines += '<polyline points="{}" fill="none" stroke="{}" stroke-width="2"/>'.format(" ".join(pts),col)
    for i,yr in enumerate(years):
        x,_ = xy(i,min_v)
        lines += '<text x="{:.1f}" y="{}" fill="{}" font-size="10" text-anchor="middle">{}</text>'.format(x,h-8,C["sub"],yr)
    legend = ""
    for si,lb in enumerate(labels):
        lx = ml+si*90
        col = colors[si%len(colors)]
        legend += '<line x1="{}" y1="8" x2="{}" y2="8" stroke="{}" stroke-width="2"/>'.format(lx,lx+15,col)
        legend += '<text x="{}" y="12" fill="{}" font-size="10">{}</text>'.format(lx+19,C["sub"],lb)
    return '<svg viewBox="0 0 {} {}" xmlns="http://www.w3.org/2000/svg" style="width:100%;max-width:{}px;">{}{}</svg>'.format(w,h+10,w,legend,lines)

def risk_heatmap(risks):
    w,h = 320,280
    gc = {("저","저"):"rgba(63,185,80,0.15)",("저","중"):"rgba(63,185,80,0.1)",("저","고"):"rgba(210,153,34,0.15)",("중","저"):"rgba(63,185,80,0.1)",("중","중"):"rgba(210,153,34,0.15)",("중","고"):"rgba(248,81,73,0.15)",("고","저"):"rgba(210,153,34,0.15)",("고","중"):"rgba(248,81,73,0.15)",("고","고"):"rgba(248,81,73,0.25)"}
    lm = {"저":0,"중":1,"고":2}
    cw,ch = 80,70
    ox,oy = 60,30
    cells = ""
    for li in range(3):
        for ii in range(3):
            lk,ik = ["저","중","고"][li],["저","중","고"][ii]
            x,y = ox+li*cw, oy+(2-ii)*ch
            cells += '<rect x="{}" y="{}" width="{}" height="{}" fill="{}" stroke="{}" stroke-width="0.5"/>'.format(x,y,cw,ch,gc[(lk,ik)],C["grid"])
    placed = {}
    for name,lk,imp in risks:
        li,ii = lm.get(lk,1),lm.get(imp,1)
        key = (li,ii)
        off = placed.get(key,0)
        placed[key] = off+1
        x,y = ox+li*cw+cw//2, oy+(2-ii)*ch+20+off*18
        dc = C["sell"] if (lk=="고" or imp=="고") else (C["warn"] if (lk=="중" or imp=="중") else C["buy"])
        cells += '<circle cx="{}" cy="{}" r="5" fill="{}"/>'.format(x,y,dc)
        cells += '<text x="{}" y="{}" fill="{}" font-size="10">{}</text>'.format(x+9,y+4,C["text"],name)
    for i,lb in enumerate(["저","중","고"]):
        cells += '<text x="{}" y="{}" fill="{}" font-size="11" text-anchor="middle">{}</text>'.format(ox+i*cw+cw//2,oy+3*ch+18,C["sub"],lb)
        cells += '<text x="{}" y="{}" fill="{}" font-size="11" text-anchor="end" dominant-baseline="middle">{}</text>'.format(ox-10,oy+(2-i)*ch+ch//2,C["sub"],lb)
    cells += '<text x="{}" y="{}" fill="{}" font-size="12" text-anchor="middle">발생가능성 →</text>'.format(ox+cw*1.5,oy+3*ch+32,C["sub"])
    return '<svg viewBox="0 0 {} {}" xmlns="http://www.w3.org/2000/svg" style="width:100%;max-width:{}px;">{}</svg>'.format(w,h,w,cells)

def price_range_bar(low52, high52, current, stop_loss=None, target=None, currency="₩"):
    w,h = 380,80
    mg = 30
    bw,by,bh = w-mg*2, 30, 16
    rng = high52-low52
    if rng <= 0: return ""
    def xp(v): return mg+bw*(v-low52)/rng
    p = []
    p.append('<rect x="{}" y="{}" width="{}" height="{}" fill="{}" rx="8"/>'.format(mg,by,bw,bh,C["grid"]))
    if stop_loss and target:
        sx,tx = xp(max(stop_loss,low52)),xp(min(target,high52))
        p.append('<rect x="{:.0f}" y="{}" width="{:.0f}" height="{}" fill="rgba(66,165,245,0.15)" rx="8"/>'.format(sx,by,max(tx-sx,0),bh))
    if stop_loss:
        sx = xp(stop_loss)
        p.append('<line x1="{:.0f}" y1="{}" x2="{:.0f}" y2="{}" stroke="{}" stroke-width="2"/>'.format(sx,by-4,sx,by+bh+4,C["sell"]))
        p.append('<text x="{:.0f}" y="{}" fill="{}" font-size="10" text-anchor="middle">{}{:,.0f}</text>'.format(sx,by-8,C["sell"],currency,stop_loss))
    cx = xp(current)
    p.append('<line x1="{:.0f}" y1="{}" x2="{:.0f}" y2="{}" stroke="{}" stroke-width="3"/>'.format(cx,by-6,cx,by+bh+6,C["text"]))
    p.append('<text x="{:.0f}" y="{}" fill="{}" font-size="11" font-weight="600" text-anchor="middle">{}{:,.0f}</text>'.format(cx,by+bh+20,C["text"],currency,current))
    if target:
        tx = xp(target)
        p.append('<line x1="{:.0f}" y1="{}" x2="{:.0f}" y2="{}" stroke="{}" stroke-width="2"/>'.format(tx,by-4,tx,by+bh+4,C["buy"]))
        p.append('<text x="{:.0f}" y="{}" fill="{}" font-size="10" text-anchor="middle">{}{:,.0f}</text>'.format(tx,by-8,C["buy"],currency,target))
    p.append('<text x="{}" y="{}" fill="{}" font-size="9">52주 저: {}{:,.0f}</text>'.format(mg,h,C["sub"],currency,low52))
    p.append('<text x="{}" y="{}" fill="{}" font-size="9" text-anchor="end">52주 고: {}{:,.0f}</text>'.format(w-mg,h,C["sub"],currency,high52))
    return '<svg viewBox="0 0 {} {}" xmlns="http://www.w3.org/2000/svg" style="width:100%;max-width:{}px;">{}</svg>'.format(w,h+5,w,"".join(p))

def donut_chart(sectors, size=260):
    cx,cy = size//2,size//2
    ro,ri = size//2-30,size//2-55
    total = sum(p for _,p in sectors)
    if total <= 0: return ""
    parts,angle = [],-90
    for i,(name,pct) in enumerate(sectors):
        sweep = 360*pct/total
        a1,a2 = math.radians(angle),math.radians(angle+sweep)
        x1o,y1o = cx+ro*math.cos(a1),cy+ro*math.sin(a1)
        x2o,y2o = cx+ro*math.cos(a2),cy+ro*math.sin(a2)
        x1i,y1i = cx+ri*math.cos(a2),cy+ri*math.sin(a2)
        x2i,y2i = cx+ri*math.cos(a1),cy+ri*math.sin(a1)
        lg = 1 if sweep>180 else 0
        col = SECTOR_COLORS[i%len(SECTOR_COLORS)]
        d = "M{:.1f},{:.1f} A{},{} 0 {},1 {:.1f},{:.1f} L{:.1f},{:.1f} A{},{} 0 {},0 {:.1f},{:.1f} Z".format(x1o,y1o,ro,ro,lg,x2o,y2o,x1i,y1i,ri,ri,lg,x2i,y2i)
        parts.append('<path d="{}" fill="{}" stroke="{}" stroke-width="1"/>'.format(d,col,C["bg"]))
        angle += sweep
    legend = ""
    for i,(name,pct) in enumerate(sectors[:8]):
        ly = 20+i*18
        col = SECTOR_COLORS[i%len(SECTOR_COLORS)]
        legend += '<rect x="{}" y="{}" width="10" height="10" fill="{}" rx="2"/>'.format(size+10,ly,col)
        legend += '<text x="{}" y="{}" fill="{}" font-size="11">{} {:.1f}%</text>'.format(size+24,ly+9,C["sub"],name,pct)
    return '<svg viewBox="0 0 {} {}" xmlns="http://www.w3.org/2000/svg" style="width:100%;max-width:{}px;">{}{}</svg>'.format(size+130,max(size,len(sectors)*18+40),size+130,"".join(parts),legend)

def etf_performance_chart(periods, etf_returns, index_returns, etf_name="ETF", index_name="Index"):
    w,h = 380,200
    n = len(periods)
    if n == 0: return ""
    all_v = etf_returns+index_returns
    max_v = max(abs(v) for v in all_v)*1.3
    bar_w = min(24,(w-80)//(n*2)-4)
    ml,mb = 45,30
    bars = ""
    for i,period in enumerate(periods):
        xc = ml+(w-ml-20)*(i+0.5)/n
        for j,(vals,col) in enumerate([(etf_returns,C["blue"]),(index_returns,C["buy"])]):
            v = vals[i]
            bh = abs(v)/max_v*(h-mb-30)
            bx = xc+(j*2-1)*(bar_w//2+1)
            by_pos = h-mb-bh if v>=0 else h-mb
            bars += '<rect x="{:.0f}" y="{:.0f}" width="{}" height="{:.0f}" fill="{}" rx="2" opacity="0.85"/>'.format(bx,by_pos,bar_w,bh,col)
            bars += '<text x="{:.0f}" y="{:.0f}" fill="{}" font-size="9" text-anchor="middle">{:.1f}%</text>'.format(bx+bar_w//2,by_pos-4,col,v)
        bars += '<text x="{:.0f}" y="{}" fill="{}" font-size="11" text-anchor="middle">{}</text>'.format(xc,h-8,C["sub"],period)
    legend = '<rect x="{}" y="5" width="10" height="10" fill="{}" rx="2"/><text x="{}" y="14" fill="{}" font-size="10">{}</text>'.format(ml,C["blue"],ml+14,C["sub"],etf_name)
    legend += '<rect x="{}" y="5" width="10" height="10" fill="{}" rx="2"/><text x="{}" y="14" fill="{}" font-size="10">{}</text>'.format(ml+100,C["buy"],ml+114,C["sub"],index_name)
    return '<svg viewBox="0 0 {} {}" xmlns="http://www.w3.org/2000/svg" style="width:100%;max-width:{}px;">{}{}</svg>'.format(w,h+10,w,legend,bars)

if __name__ == "__main__":
    print("=== 차트 템플릿 테스트 ===")
    tests = [
        ("radar", radar_chart([("Moat",8),("수익성",7),("성장성",6),("재무",9),("밸류",5),("모멘텀",4),("배당",3),("리스크",7),("산업",8),("경영",6)])),
        ("bar", bar_chart(["21","22","23","24","25E"],[100,120,110,130,150],[20,25,22,28,35])),
        ("line", line_chart(["21","22","23"],[[15,18,12],[10,11,9]],["ROE","OPM"])),
        ("risk", risk_heatmap([("HBM수율","중","고"),("환율","고","중"),("규제","저","저")])),
        ("price", price_range_bar(50000,90000,72000,66000,86000)),
        ("donut", donut_chart([("기술",35),("금융",20),("헬스케어",15),("에너지",10),("기타",20)])),
        ("etf", etf_performance_chart(["1M","3M","1Y"],[2.1,5.3,15.1],[2.0,5.1,14.8])),
    ]
    for name, svg in tests:
        print("  {} : {} bytes — {}".format(name, len(svg), "OK" if "<svg" in svg else "FAIL"))
    print("=== 완료 ===")
