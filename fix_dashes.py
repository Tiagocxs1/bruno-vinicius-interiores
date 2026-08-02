# -*- coding: utf-8 -*-
"""Fix excessive em-dashes in content files. Context-aware replacements."""
import os, re

BASE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "src", "scripts")

def fix_file(fname):
    path = os.path.join(BASE, fname)
    with open(path, encoding="utf-8") as f:
        text = f.read()

    before = text.count("\u2014")

    lines = text.split("\n")
    new_lines = []
    for line in lines:
        if "\u2014" not in line:
            new_lines.append(line)
            continue

        # For blog body paragraphs: replace em-dash appositives "X — Y" with ": Y" where Y is a list/definition
        # Pattern "X — Y — Z" (double em-dash) is always AI-sounding, reduce to 1
        if '{"t": "p"' in line or '{"t": "li"' in line:
            # Count em-dashes
            count = line.count("\u2014")
            if count >= 2:
                # Replace first em-dash with colon, second with semicolon or comma
                parts = line.split("\u2014")
                if len(parts) >= 3:
                    # First em-dash is usually the main break, keep style
                    # Second is overdone: join with comma
                    result = parts[0] + "\u2014" + parts[1] + ", " + parts[2]
                    for extra in parts[3:]:
                        result += ", " + extra
                    line = result

        # In h2 titles with em-dash (rare but "Os neutros voltaram — e não são bege")
        # Keep one; these are stylistically valid for editorial Portuguese/Spanish
        if '{"t": "h2"' in line:
            count = line.count("\u2014")
            if count >= 2:
                parts = line.split("\u2014")
                line = parts[0] + "\u2014" + parts[1] + ", " + parts[2]

        # In list items (Ambient — / 60% —) replace with colon for consistency
        if ('"' in line and line.strip().startswith('"')) or line.strip().startswith("'"):
            # These are simple string definitions
            for pct in ["60%", "30%", "10%", "60 %", "30 %", "10 %",
                         "Ambient", "Ambiance", "Ambiental",
                         "Task", "Travail", "Tarefa", "Luce da compito",
                         "Accent", "Destaque", "Luce ambientale",
                         "Luce d"]:
                prefix = pct + " "
                if prefix in line or (pct in line):
                    line = line.replace(" " + pct + " \u2014 ", " " + pct + ": ")
                    line = line.replace('"' + pct + " \u2014 ", '"' + pct + ": ")
                    break

        # In UL blocks: replace em-dash with colon
        for pct in ["60%", "30%", "10%", "60 %", "30 %", "10 %",
                     "Ambient", "Ambiance", "Ambiental",
                     "Task", "Travail", "Tarefa", "Luce da compito",
                     "Accent", "Destaque",
                     "Luce ambientale", "Luce d"]:
            if ' "' + pct in line and "\u2014" in line:
                line = line.replace(" " + pct + "\u2014 ", " " + pct + ": ")
                break

        new_lines.append(line)

    result = "\n".join(new_lines)
    after = result.count("\u2014")
    if before != after:
        print(f"  {fname}: {before} -> {after} (removed {before-after})")

    with open(path, "w", encoding="utf-8") as f:
        f.write(result)

    return before, after


total_before = 0
total_after = 0
FILES = [
    "content_site.py", "content_blog.py",
    "content_blog_es.py", "content_blog_it.py",
    "content_blog_fr.py", "content_blog_pt.py",
]

for f in FILES:
    b, a = fix_file(f)
    total_before += b
    total_after += a

print(f"")
print(f"TOTAL: {total_before} -> {total_after} ({total_before-total_after} removed)")