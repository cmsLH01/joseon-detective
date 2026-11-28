import base64, json, os
S = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(S)
old = open(os.path.join(S,'case1_base.html'),encoding='utf-8').read()
def between(a, b, src=old):
    i = src.index(a); j = src.index(b, i)
    return src[i:j]
css = between('<style>\n', '</style>')[len('<style>\n'):]
icon = between('  const ICON = {', '  const tm =')
c1 = between('  const E = {', '  const PAIR = {};') + between('  const PLACES = [', '  const isClue')

def load(folder, keys):
    out = {}
    for k in keys:
        p = os.path.join(ROOT, 'images', folder, k + '.jpg')
        if os.path.exists(p):
            out[k] = 'data:image/jpeg;base64,' + base64.b64encode(open(p,'rb').read()).decode()
    return out
imgs = {
  'c1': load('case1', ['anbang','sarang','yard','kitchen','gate','haeng','kim','dolsoe','kkeut','park']),
  'c2': load('case2', ['yakbang','brew','room','store','yunroom','garden','hdo','yun','bok','choi']),
  'c3': load('case3', ['hunroom','hall','library','dorm','backwall','shop','lee','pak','jung','manbok']),
  'c4': load('case4', ['front','vault','yard','gamble','kwakroom','office','ma','kwak','wol','han','owner']),
}
t = open(os.path.join(S,'template2.html'),encoding='utf-8').read()
t = t.replace('/*CSS*/', css).replace('/*ICON*/', icon).replace('/*C1DATA*/', c1)
t = t.replace('/*CASE2*/', open(os.path.join(S,'case2.js'),encoding='utf-8').read())
t = t.replace('/*CASE3*/', open(os.path.join(S,'case3.js'),encoding='utf-8').read())
t = t.replace('/*CASE4*/', open(os.path.join(S,'case4.js'),encoding='utf-8').read())
# 글자 크기: 모든 font-size를 약 12% 키운다
import re
t = re.sub(r'font-size:\s*(\d+(?:\.\d+)?)px', lambda m: 'font-size:%dpx' % round(float(m.group(1))*1.12), t)
t = t.replace('/*IMAGES*/', 'window.IMG = ' + json.dumps(imgs) + ';')
# GitHub Pages용: 아티팩트가 자동으로 넣어 주는 문서 뼈대와 모바일 설정을 직접 붙인다
cut = t.index('<div class="wrap">')
page = ('<!doctype html>\n<html lang="ko">\n<head>\n<meta charset="utf-8">\n'
        '<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">\n'
        + t[:cut] +
        '<style>:root{padding-top:env(safe-area-inset-top,0px);padding-bottom:env(safe-area-inset-bottom,0px)}'
        'body{margin:0}img{max-width:100%}[hidden]{display:none!important}</style>\n'
        '</head>\n<body>\n' + t[cut:] + '\n</body>\n</html>\n')
open(os.path.join(ROOT,'index.html'),'w',encoding='utf-8').write(page)
print(len(t)//1024, 'KB', {k: len(v) for k, v in imgs.items()})
