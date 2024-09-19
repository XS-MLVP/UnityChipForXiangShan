.PHONY: test_all

all: test_all

init:
	echo "init this repo"

clean:
	rm -rf out/*

test_all:
	PYTHONPATH=. pytest --mlvp-report --report-dir=out -vs ut_*/ $(ARGS)

test_bpu:
	PYTHONPATH=. pytest --mlvp-report --report-dir=out -vs ut_frontend/ut_bpu $(ARGS)

dut_bpu:
	echo "build_bpu"

dut_icache:
	echo "build_icache"

dut_all: dut_bpu dut_icache
	echo "build all dut complete"
