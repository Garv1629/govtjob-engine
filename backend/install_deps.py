import os
import sys
import subprocess

# Auto-add DLL search paths for Windows Python installations
if sys.platform == "win32":
    py_base = os.path.dirname(sys.executable)
    dll_paths = [
        os.path.join(py_base, "DLLs"),
        os.path.join(os.path.dirname(py_base), "DLLs"),
        r"C:\Users\GARV\AppData\Local\Programs\Python\Python314\DLLs"
    ]
    for p in dll_paths:
        if os.path.exists(p):
            try:
                os.add_dll_directory(p)
            except Exception:
                pass
            os.environ["PATH"] = p + os.pathsep + os.environ.get("PATH", "")

print(f"Python Executable: {sys.executable}")
print(f"Python Version: {sys.version}")

def run(cmd):
    print(f"Executing: {cmd}")
    res = subprocess.run(cmd, shell=True)
    return res.returncode

# Upgrade pip
run(f'"{sys.executable}" -m pip install --upgrade pip setuptools wheel')

print("Installing all backend packages in single pass...")
cmd = f'"{sys.executable}" -m pip install --prefer-binary fastapi uvicorn pydantic pydantic-settings sqlalchemy alembic apscheduler openai python-telegram-bot httpx python-multipart passlib cryptography'
run(cmd)

# Verify Uvicorn installation
try:
    import uvicorn
    print("✓ VERIFIED: Uvicorn imported successfully!")
except ImportError as e:
    print(f"Retrying uvicorn installation... ({e})")
    run(f'"{sys.executable}" -m pip install uvicorn')

# Graceful Playwright check
try:
    import playwright
    print("Playwright available! Downloading Chromium binaries...")
    run(f'"{sys.executable}" -m playwright install chromium')
except ImportError:
    print("Notice: Playwright C-extensions not compatible with Python 3.14 pre-release yet. Engine will operate in HTTP fallback mode.")

print("Dependency installation completed.")
