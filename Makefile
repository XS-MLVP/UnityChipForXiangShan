.PHONY: dut rtl

export PYTHONPATH := $(shell pwd):$(shell picker --show_xcom_lib_location_python):$(PYTHONPATH)
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

test_all: dut
	@python3 run.py --config $(CFG) $(KV) -- $(REPORT) -vs ut_*/ $(args)

test: dut
	python3 run.py --config $(CFG) $(KV) -- $(REPORT) -vs $(target) $(args) -n auto

test_trigger: dut
	make test  CFG="./configs/frontend_trigger.yaml" target="./ut_frontend/ifu/frontend_trigger/"
	


test_predecode: dut
	make test target="./ut_frontend/ifu/predecode/"

dut: rtl
	@python3 run.py --config $(CFG) --build $(DUTS) $(args)

rtl:
	@python3 run.py --config $(CFG)  --download-rtl $(args)

doc:
	cd documents && hugo server --bind 0.0.0.0
