# 變數設定
PYTHON = python3
HUGO = hugo
SCRIPT = scripts/typst_watch.py

.PHONY: all server build clean

# 預設動作：顯示指令
all:
	@echo "Available commands:"
	@echo "  make server  - Start local preview (Hugo + Typst Watcher)"
	@echo "  make build   - Build static site for deployment"
	@echo "  make clean   - Remove generated files"

# 本地開發模式
server:
	@echo "🚀 Starting development environment..."
	@# 使用 & 在背景執行 Python watcher，並捕捉 PID 以便之後關閉
	@trap 'kill %1' SIGINT; \
	$(PYTHON) $(SCRIPT) --watch & \
	$(HUGO) server -D

# 生產環境建置
build:
	@echo "🔨 Building site..."
	@$(PYTHON) $(SCRIPT)
	@$(HUGO) -D --minify

# 清理暫存檔 (選擇性)
clean:
	@rm -rf public resources
	@rm -rf static/images/typst
	@echo "🧹 Cleaned."