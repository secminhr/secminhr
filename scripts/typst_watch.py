import os
import re
import hashlib
import subprocess
import glob
import time
import sys

# --- 設定區 ---
PROJECT_ROOT = os.getcwd()
CONTENT_DIR = os.path.join(PROJECT_ROOT, "content")
OUTPUT_DIR = os.path.join(PROJECT_ROOT, "static", "images", "typst")

# 正規表達式：抓取 ```typst ... ``` 區塊
PATTERN = re.compile(r"```typst\n(.*?)```", re.DOTALL)

def ensure_dir():
    os.makedirs(OUTPUT_DIR, exist_ok=True)

def compile_typst(code, code_hash):
    output_path = os.path.join(OUTPUT_DIR, f"{code_hash}.svg")
    
    # 如果檔案已存在且 hash 沒變，就不重新編譯 (Cache 機制)
    if os.path.exists(output_path):
        return False

    print(f"   🎨 Compiling Typst block: {code_hash[:8]}...")
    
    # 包裝程式碼：預設開啟 auto page size
    wrapped_code = code
    if "#set page" not in code:
        wrapped_code = f"#set page(width: auto, height: auto, margin: 5pt)\n{code}"
    
    temp_typ = os.path.join(OUTPUT_DIR, f"temp_{code_hash}.typ")
    
    try:
        with open(temp_typ, "w", encoding="utf-8") as f:
            f.write(wrapped_code)
        
        # 呼叫 typst CLI
        subprocess.run(
            ["typst", "compile", "--root", PROJECT_ROOT, temp_typ, output_path],
            check=True, 
            capture_output=True
        )
        return True
    except subprocess.CalledProcessError as e:
        print(f"   ❌ Error compiling {code_hash[:8]}:")
        print(e.stderr.decode())
        return False
    finally:
        if os.path.exists(temp_typ):
            os.remove(temp_typ)

def scan_and_compile():
    ensure_dir()
    md_files = glob.glob(os.path.join(CONTENT_DIR, "**/*.md"), recursive=True)
    count = 0
    
    for md_file in md_files:
        try:
            with open(md_file, "r", encoding="utf-8") as f:
                content = f.read()
            
            matches = PATTERN.findall(content)
            for code in matches:
                # 🔥 關鍵修正：在計算 Hash 前先 strip() 去除頭尾空白
                normalized_code = code.strip()
                code_hash = hashlib.md5(normalized_code.encode("utf-8")).hexdigest()
                if compile_typst(code, code_hash):
                    count += 1
        except Exception as e:
            print(f"Error reading {md_file}: {e}")

    if count > 0:
        print(f"✅ Compiled {count} new Typst images.")

def watch_mode():
    print("👀 Watching for changes in .md files (Press Ctrl+C to stop)...")
    last_mtimes = {}
    
    try:
        # 初次執行
        scan_and_compile()
        
        while True:
            has_change = False
            md_files = glob.glob(os.path.join(CONTENT_DIR, "**/*.md"), recursive=True)
            
            for md_file in md_files:
                try:
                    mtime = os.stat(md_file).st_mtime
                    if md_file not in last_mtimes:
                        last_mtimes[md_file] = mtime
                        # 新檔案不一定需要觸發，等到下次存檔
                    elif mtime > last_mtimes[md_file]:
                        print(f"📝 Detected change in: {os.path.basename(md_file)}")
                        last_mtimes[md_file] = mtime
                        has_change = True
                except FileNotFoundError:
                    pass # 檔案可能被刪除了
            
            if has_change:
                scan_and_compile()
            
            time.sleep(1) # 每秒檢查一次
            
    except KeyboardInterrupt:
        print("\n🛑 Stopping Typst watcher.")

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "--watch":
        watch_mode()
    else:
        scan_and_compile()