#!/usr/bin/env python3
"""src.html -> index.html: iešuj visus assets/*.jpg kā base64, lai fails būtu pašpietiekams."""
import base64, re, pathlib
root = pathlib.Path(__file__).parent
src = (root / "src.html").read_text(encoding="utf-8")
def inline(m):
    data = base64.b64encode((root / m.group(1)).read_bytes()).decode()
    return "data:image/jpeg;base64," + data
out = re.sub(r"(assets/[\w\-]+\.jpg)", inline, src)
(root / "index.html").write_text(out, encoding="utf-8")
print(f"index.html: {len(out)/1e6:.2f} MB")
