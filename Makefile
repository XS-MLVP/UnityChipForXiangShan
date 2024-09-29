.PHONY: dut rtl

export PYTHONPATH := $(shell pwd):$(shell picker --show_xcom_lib_location_python):$(PYTHONPATH)

RLT_DOWNLOAD_FROM="https://raw.githubusercontent.com/XS-MLVP/UnityChipXiangShanRTLs/refs/heads/main/README.md"
RLT_DOWNLOAD_URL_BASE="https://github.com/XS-MLVP/UnityChipXiangShanRTLs/releases/download/"

all: rtl dut_all test_all

init:
	echo "init this repo"

clean:
	rm -rf out/*

clean_dut:
	cd dut && ls | grep -v __init__.py | xargs rm -rf

test_all:
	pytest --mlvp-report --report-dir=out -vs ut_*/ $(args)

test:
	pytest --mlvp-report --report-dir=out -vs $(target) $(args)

dut:
	$(MAKE) -C scripts -f Makefile.build_ut_$(target) args=$(args)

dut_all:
	@for file in $(wildcard scripts/Makefile.build_ut_*); do \
        echo "Processing $$file"; \
        $(MAKE) -C scripts -f $$(basename $$file) args=$(args); \
    done

rtl:
	@RLT_DOWNLOAD_URL="";\
	if [ -L rtl/rtl ] && [ -e rtl/rtl ]; then \
		echo "RTL already exists. Please delete the rtl directories manually."; \
	else \
		if [ "$(target)" ]; then \
			RLT_DOWNLOAD_URL="$(RLT_DOWNLOAD_URL_BASE)$(target)"; \
		else \
			echo "Search latest RTL from: $(RLT_DOWNLOAD_FROM)"; \
			RLT_DOWNLOAD_URL=`curl $(RLT_DOWNLOAD_FROM)|grep -m 1 openxiangshan-kmh-|grep -oP '(?<=\().*?(?=\))'`; \
	    fi;\
		RTL_ZIP=$$(basename $$RLT_DOWNLOAD_URL);\
		RTL_DIR=$${RTL_ZIP%.tar.gz};\
		if [ -f rtl/$$RTL_ZIP ]; then \
			echo "RTL tarball exists, ignore download"; \
		else \
			echo "Download: $$RLT_DOWNLOAD_URL"; \
			wget -P rtl/ $$RLT_DOWNLOAD_URL; \
		fi;\
		if [ -d rtl/$$RTL_DIR ]; then \
            echo "RTL directory already exists, ignore extract"; \
        else \
            echo "Extracting $$RTL_ZIP to rtl/$$RTL_DIR"; \
            mkdir -p rtl/$$RTL_DIR; \
            tar -xzf rtl/$$RTL_ZIP -C rtl/$$RTL_DIR --strip-components=1; \
        fi;\
		ln -s $$RTL_DIR rtl/rtl;\
	fi;\
