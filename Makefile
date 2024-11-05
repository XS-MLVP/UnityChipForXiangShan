.PHONY: dut rtl

export PYTHONPATH := $(shell pwd):$(shell picker --show_xcom_lib_location_python):$(PYTHONPATH)
export ENABLE_XINFO := 0
export CFG := ""
export DUTS := "*"

all: dut test_all

clean:
	rm -rf out/*

clean_dut:
	cd dut && ls | grep -v __init__.py | xargs rm -rf

test_all:
	@python3 run.py --config $(CFG) $(KV) -- --toffee-report -vs ut_*/ $(args)

test:
	@python3 run.py --config $(CFG) $(KV) -- --toffee-report -vs $(target) $(args)

dut:
	@python3 run.py --config $(CFG) --build $(DUTS) $(args)

rtl:
	@python3 run.py --config $(CFG)  --download-rtl

doc:
	cd documents && hugo server
