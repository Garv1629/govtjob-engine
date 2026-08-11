import subprocess

cwd = r"e:\govtjob-engine-main\govtjob-engine-main"

print("--- GIT LOG ---")
out = subprocess.check_output(["git", "log", "-n", "5", "--stat"], cwd=cwd, text=True)
print(out)

print("--- RECENT COMMIT DIFF STAT ---")
out_diff = subprocess.check_output(["git", "diff", "HEAD~1", "HEAD", "--stat"], cwd=cwd, text=True)
print(out_diff)
