import difflib

with open(r"e:\govtjob-engine-main\govtjob-engine-main\preview.html", "r", encoding="utf-8") as f:
    preview = f.readlines()

with open(r"e:\govtjob-engine-main\govtjob-engine-main\index.html", "r", encoding="utf-8") as f:
    index = f.readlines()

diff = list(difflib.unified_diff(preview, index, fromfile="preview.html", tofile="index.html", n=2))
with open(r"e:\govtjob-engine-main\govtjob-engine-main\diff_output.txt", "w", encoding="utf-8") as out:
    out.writelines(diff)

print("Done diffing")
