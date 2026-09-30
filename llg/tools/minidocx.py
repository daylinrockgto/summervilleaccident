# -*- coding: utf-8 -*-
"""Minimal .docx builder. Produces a small file that Google Drive converts to a
native Doc WITH tel: hyperlinks preserved. The HTML import path strips them."""
import re, zipfile, io, base64, html as _html

CT = ('<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
 '<Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types">'
 '<Default Extension="rels" ContentType="application/vnd.openxmlformats-package.relationships+xml"/>'
 '<Default Extension="xml" ContentType="application/xml"/>'
 '<Override PartName="/word/document.xml" ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.document.main+xml"/>'
 '<Override PartName="/word/styles.xml" ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.styles+xml"/>'
 '<Override PartName="/word/numbering.xml" ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.numbering+xml"/>'
 '</Types>')
RELS = ('<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
 '<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">'
 '<Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/officeDocument" Target="word/document.xml"/>'
 '</Relationships>')

def _styles():
    s = ['<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
         '<w:styles xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main">'
         '<w:style w:type="paragraph" w:default="1" w:styleId="Normal"><w:name w:val="Normal"/></w:style>']
    sizes = {1:36, 2:28, 3:24, 4:22, 5:20}
    for i in range(1,6):
        s.append(f'<w:style w:type="paragraph" w:styleId="Heading{i}"><w:name w:val="heading {i}"/>'
                 f'<w:basedOn w:val="Normal"/><w:pPr><w:outlineLvl w:val="{i-1}"/></w:pPr>'
                 f'<w:rPr><w:b/><w:sz w:val="{sizes[i]}"/></w:rPr></w:style>')
    s.append('<w:style w:type="character" w:styleId="Hyperlink"><w:name w:val="Hyperlink"/>'
             '<w:rPr><w:color w:val="0563C1"/><w:u w:val="single"/></w:rPr></w:style>')
    s.append('</w:styles>')
    return ''.join(s)

NUMBERING = ('<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
 '<w:numbering xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main">'
 '<w:abstractNum w:abstractNumId="0"><w:multiLevelType w:val="hybridMultilevel"/>'
 '<w:lvl w:ilvl="0"><w:start w:val="1"/><w:numFmt w:val="bullet"/><w:lvlText w:val="\u2022"/><w:lvlJc w:val="left"/>'
 '<w:pPr><w:ind w:left="720" w:hanging="360"/></w:pPr></w:lvl></w:abstractNum>'
 '<w:num w:numId="1"><w:abstractNumId w:val="0"/></w:num></w:numbering>')

def _esc(t):
    return (t.replace('&','&amp;').replace('<','&lt;').replace('>','&gt;'))

def build(page_html, out_path=None):
    """page_html: the blog HTML (h1-h5, p, a, strong, em). Returns (bytes, b64)."""
    rels = []
    def relid(url):
        for i,(u,_) in enumerate(rels,1):
            if u == url: return f"rH{i}"
        rels.append((url,None)); return f"rH{len(rels)}"

    body = []
    for tag, inner in re.findall(r'<(h[1-5]|p|li)>(.*?)</\1>', page_html, re.S):
        inner = inner.strip()
        if not inner: continue
        runs = []
        for tok in re.split(r'(<a href="[^"]+">.*?</a>|<strong>.*?</strong>|<em>.*?</em>)', inner, flags=re.S):
            if not tok: continue
            a  = re.match(r'<a href="([^"]+)">(.*?)</a>', tok, re.S)
            st = re.match(r'<strong>(.*?)</strong>', tok, re.S)
            em = re.match(r'<em>(.*?)</em>', tok, re.S)
            if a:
                txt = _esc(_html.unescape(re.sub(r'<[^>]+>','',a.group(2))))
                rid = relid(a.group(1))
                runs.append(f'<w:hyperlink r:id="{rid}"><w:r><w:rPr><w:rStyle w:val="Hyperlink"/></w:rPr>'
                            f'<w:t xml:space="preserve">{txt}</w:t></w:r></w:hyperlink>')
            elif st:
                txt = _esc(_html.unescape(re.sub(r'<[^>]+>','',st.group(1))))
                runs.append(f'<w:r><w:rPr><w:b/></w:rPr><w:t xml:space="preserve">{txt}</w:t></w:r>')
            elif em:
                txt = _esc(_html.unescape(re.sub(r'<[^>]+>','',em.group(1))))
                runs.append(f'<w:r><w:rPr><w:i/></w:rPr><w:t xml:space="preserve">{txt}</w:t></w:r>')
            else:
                txt = _esc(_html.unescape(re.sub(r'<[^>]+>','',tok)))
                if txt: runs.append(f'<w:r><w:t xml:space="preserve">{txt}</w:t></w:r>')
        if tag == 'li':
            ppr = '<w:pPr><w:numPr><w:ilvl w:val="0"/><w:numId w:val="1"/></w:numPr></w:pPr>'
        elif tag.startswith('h'):
            ppr = f'<w:pPr><w:pStyle w:val="Heading{tag[1]}"/></w:pPr>'
        else:
            ppr = ''
        body.append(f'<w:p>{ppr}{"".join(runs)}</w:p>')

    doc = ('<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
           '<w:document xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main" '
           'xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships"><w:body>'
           + ''.join(body) + '</w:body></w:document>')
    drels = ['<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
             '<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">'
             '<Relationship Id="rIdS" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/styles" Target="styles.xml"/>'
             '<Relationship Id="rIdN" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/numbering" Target="numbering.xml"/>']
    for i,(u,_) in enumerate(rels,1):
        drels.append(f'<Relationship Id="rH{i}" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/hyperlink" '
                     f'Target="{_esc(u)}" TargetMode="External"/>')
    drels.append('</Relationships>')

    buf = io.BytesIO()
    with zipfile.ZipFile(buf,'w',zipfile.ZIP_DEFLATED,compresslevel=9) as z:
        z.writestr('[Content_Types].xml', CT)
        z.writestr('_rels/.rels', RELS)
        z.writestr('word/styles.xml', _styles())
        z.writestr('word/numbering.xml', NUMBERING)
        z.writestr('word/document.xml', doc)
        z.writestr('word/_rels/document.xml.rels', ''.join(drels))
    data = buf.getvalue()
    if out_path: open(out_path,'wb').write(data)
    return data, base64.b64encode(data).decode(), [u for u,_ in rels]
