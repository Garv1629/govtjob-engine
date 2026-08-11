import subprocess

cwd = r"e:\govtjob-engine-main\govtjob-engine-main"

with open(r"e:\govtjob-engine-main\govtjob-engine-main\git_history.txt", "w", encoding="utf-8") as out:
    out.write("=== GIT LOG ===\n")
    try:
        log = subprocess.check_output(["git", "log", "-n", "10", "--oneline", "--stat"], cwd=cwd, text=True)
        out.write(log)
    except Exception as e:
        out.write(str(e))
    
    out.write("\n=== GIT SHOW HEAD ===\n")
    try:
        show = subprocess.check_output(["git", "show", "HEAD", "--stat"], cwd=cwd, text=True)
        out.write(show)
    except Exception as e:
        out.write(str(e))

    out.write("\n=== GIT SHOW 3cc2238 ===\n")
    try:
        show_old = subprocess.check_output(["git", "show", "3cc2238bca3e2698b7c151411a984322e2435c8c", "--stat"], cwd=cwd, text=True)
        out.write(show_old)
    except Exception as e:
        out.write(str(e))
