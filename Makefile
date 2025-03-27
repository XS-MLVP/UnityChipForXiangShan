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

check_dut:
	@if [ -n "$(target)" ]; then \
		for t in $(target); do \
			CLEANED_TARGET=$$(echo "$$t" | sed 's/\/$$//'); \
			MATCHED_LINE=$$(grep ".* --> .* --> $$CLEANED_TARGET" dir_map.f | head -1); \
			if [ -n "$$MATCHED_LINE" ]; then \
				DUT_NAME=$$(echo "$$MATCHED_LINE" | awk -F' --> ' '{print $$1}'); \
				DUT_DIR=dut/$$(echo "$$MATCHED_LINE" | awk -F' --> ' '{print $$2}'); \
				if [ ! -d "$$DUT_DIR" ]; then \
					echo "Building missing DUT for target $$t: $$DUT_NAME"; \
					$(MAKE) dut DUTS="$$DUT_NAME"; \
				fi; \
			else \
				echo "No mapping found for target: $$t in dir_map.f, skipping check" >&2; \
			fi; \
		done; \
	fi

dut: rtl
	@if [ "$(PROCESSED_DUTS)" = "*" ]; then \
		$(MAKE) clean_dut; \
	else \
		for d in $(PROCESSED_DUTS); do \
			dir=$$(awk -F' --> ' -v dut="$$d" '$$1 == dut {print $$2; exit}' dir_map.f); \
			if [ -z "$$dir" ]; then \
				echo "No mapping found for DUT: $$d in dir_map.f, skipping deletion" >&2; \
				continue; \
			fi; \
			echo "Cleaning dut/$$dir"; \
			rm -rf "dut/$$dir"; \
		done; \
	fi
	@python3 run.py --config $(CFG) --build $(DUTS) $(args)

rtl:
	@python3 run.py --config $(CFG)  --download-rtl $(args)

doc:
	cd documents && hugo server --bind 0.0.0.0
