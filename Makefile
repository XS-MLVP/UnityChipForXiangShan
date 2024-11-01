.PHONY: dut rtl

export PYTHONPATH := $(shell pwd):$(shell picker --show_xcom_lib_location_python):$(PYTHONPATH)
export ENABLE_XINFO := 0
export CFG := ""

RLT_DOWNLOAD_FROM="https://raw.githubusercontent.com/XS-MLVP/UnityChipXiangShanRTLs/refs/heads/main/README.md"
RLT_DOWNLOAD_URL_BASE="https://github.com/XS-MLVP/UnityChipXiangShanRTLs/releases/download/"

all: dut_all test_all

clean:
	rm -rf out/*

clean_dut:
	cd dut && ls | grep -v __init__.py | xargs rm -rf

test_all:
	python3 run.py --config $(CFG) $(KV) -- --toffee-report --report-dir=out -vs ut_*/ $(args)

test:
	python3 run.py --config $(CFG) $(KV) -- --toffee-report --report-dir=out -vs $(target) $(args)

dut:
	$(MAKE) -C scripts -f Makefile.build_ut_$(target) args=$(args)

dut_all:
	@for file in $(wildcard scripts/Makefile.build_ut_*); do \
        echo "Processing $$file"; \
        $(MAKE) -C scripts -f $$(basename $$file) args=$(args); \
    done

rtl:
	python3 run.py --config $(CFG)  --download-rtl

doc:
	cd documents && hugo server
