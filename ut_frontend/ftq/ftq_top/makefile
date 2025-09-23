CUR := $(abspath $(CURDIR))
ROOT := $(shell cd $(CURDIR)/../../.. && pwd)

TEST_DIR ?= test
CASE ?= 
TEST_FILE ?= 
S ?= 1
REPORT ?= 1
PYTEST_OPTS ?=

FLAGS :=
ifneq ($(S),1)
FLAGS += -s
endif
ifneq ($(REPORT),0)
FLAGS += --toffee-report
endif

.PHONY: run run-single clean help

run:
ifdef TEST_FILE
	cd "$(CUR)" && PYTHONPATH="$(ROOT)" pytest $(FLAGS) $(PYTEST_OPTS) "$(ROOT)/$(TEST_FILE)"
else ifdef CASE
	cd "$(CUR)" && PYTHONPATH="$(ROOT)" pytest $(FLAGS) $(PYTEST_OPTS) "$(CUR)/$(TEST_DIR)/test_ftq_top$(CASE).py"
else
	cd "$(CUR)" && PYTHONPATH="$(ROOT)" pytest $(FLAGS) $(PYTEST_OPTS) "$(CUR)/$(TEST_DIR)"
endif

run-single:
	cd "$(CUR)" && PYTHONPATH="$(ROOT)" pytest $(FLAGS) $(PYTEST_OPTS) "$(CUR)/$(TEST_DIR)/test_ftq_top$(CASE).py"
clean:
	rm -rf "$(CUR)/reports"

help:
	@echo "用法："
	@echo "  make run                    # 默认执行 test/ 目录下的所有测试"
	@echo "  make run CASE=3             # 执行 test_ftq_top3.py"
	@echo "  make run S=1                # 关闭 -s（显示输出）"
	@echo ""
