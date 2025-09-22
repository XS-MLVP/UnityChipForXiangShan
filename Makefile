.PHONY: dut rtl

export PYTHONPATH := $(shell pwd):$(shell picker --show_xcom_lib_location_python | tail -n 1):$(PYTHONPATH)
export ENABLE_XINFO := 0
export CFG := ""
export DUTS := "*"
export REPORT := "--toffee-report"

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

test_all:
	@python3 run.py --config $(CFG) $(KV) -- $(REPORT) -vs ut_*/ $(args)

test_all_fast:
	@python3 run.py --config $(CFG) --no-waveform --no-code-cov $(KV) -- -vs ut_*/ $(args)

test_without_waveform:
	@python3 run.py --config $(CFG) --no-waveform $(KV) -- $(REPORT) -vs $(target) $(args)

test:
	@python3 run.py --config $(CFG) $(KV) -- $(REPORT) -vs $(args) $(target)

dut:
	@python3 run.py --config $(CFG) --build $(DUTS) $(args)

rtl:
	@python3 run.py --config $(CFG) --download-rtl $(args)

doc:
	cd documents && hugo server --bind 0.0.0.0
