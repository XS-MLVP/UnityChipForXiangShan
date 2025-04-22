.PHONY: dut rtl check_dut

export PYTHONPATH := $(shell pwd):$(shell picker --show_xcom_lib_location_python):$(PYTHONPATH)
export ENABLE_XINFO := 0
export CFG := ""
export DUTS := "*"
export REPORT := "--toffee-report"

comma:= ,
empty:=    
space:= $(empty) $(empty)

PROCESSED_DUTS := $(subst $(comma),$(space),$(strip $(DUTS)))

TIMESTAMP := $(shell date +'%Y-%m-%d %H:%M:%S,%3N')
CURDIR := $(abspath .)

INFO_PREFIX := [$(TIMESTAMP),$(CURDIR)/Makefile,INFO]
WARN_PREFIX := [$(TIMESTAMP),$(CURDIR)/Makefile,Warning]

all: rtl dut test_all

update_python_deps:
	pip3 uninstall -y -r requirements.txt
	pip3 install -r requirements.txt

clean:
	rm -rf out/*

clean_dut:
	cd dut && ls | grep -v __init__.py | xargs rm -rf

clean_rtl:
	cd rtl && ls | grep -v README.md | xargs rm -rf

test_all: check_all_dut
	@python3 run.py --config $(CFG) $(KV) -- $(REPORT) -vs ut_*/ $(args)

check_all_dut:
	@python3 run.py --config $(CFG) --build $(DUTS) $(args)

test: check_dut
	@python3 run.py --config $(CFG) $(KV) -- $(REPORT) -vs $(target) $(args)

check_dut: generate_dirmap
	@if [ -n "$(target)" ]; then \
		for t in $(target); do \
			CLEANED_TARGET=$$(echo "$$t" | sed 's/\/$$//'); \
			grep ".* --> .* --> $$CLEANED_TARGET$$" .dirmap.autogen | while read -r MATCHED_LINE; do \
				DUT_NAME=$$(echo "$$MATCHED_LINE" | awk -F' --> ' '{print $$1}'); \
				DUT_DIR=dut/$$(echo "$$MATCHED_LINE" | awk -F' --> ' '{print $$2}'); \
				if [ ! -d "$$DUT_DIR" ]; then \
					echo "$(INFO_PREFIX) Building missing DUT for target $$t: $$DUT_NAME"; \
					$(MAKE) dut DUTS="$$DUT_NAME" NO_GEN_DIRMAP=1; \
				fi; \
			done; \
		done; \
	fi

dut: rtl $(if $(NO_GEN_DIRMAP),,generate_dirmap)
	@if [ "$(PROCESSED_DUTS)" = "*" ]; then \
		$(MAKE) clean_dut; \
	else \
		for d in $(PROCESSED_DUTS); do \
			dir=$$(awk -F' --> ' -v dut="$$d" '$$1 == dut {print $$2; exit}' .dirmap.autogen); \
			if [ -z "$$dir" ]; then \
				echo "$(WARN_PREFIX) No mapping found for DUT: $$d in .dirmap.autogen, skipping deletion" >&2; \
				continue; \
			fi; \
			echo "$(INFO_PREFIX) Cleaning dut/$$dir"; \
			rm -rf "dut/$$dir"; \
		done; \
	fi
	@python3 run.py --config $(CFG) --build $(DUTS) $(args)

generate_dirmap:
	@python3 -c "from comm.functions import generate_dirmap; generate_dirmap()"

rtl:
	@python3 run.py --config $(CFG)  --download-rtl $(args)

doc:
	cd documents && hugo server --bind 0.0.0.0
