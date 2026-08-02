import os
base = r"C:\Users\Admin\Desktop\Projetos\bruno-vinicius-interiores\src\scripts"
for fname in ["content_blog.py","content_blog_es.py","content_blog_it.py","content_blog_fr.py","content_blog_pt.py"]:
    path = os.path.join(base, fname)
    with open(path, encoding="utf-8") as f:
        text = f.read()
    before = text.count(" , ")
    text = text.replace(" , ", ", ")
    after = text.count(" , ")
    if before:
        print(f"{fname}: fixed {before} of \" , \"")
    with open(path, "w", encoding="utf-8") as f:
        f.write(text)
print("Done")