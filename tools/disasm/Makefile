BUILD_DIR := build
SRC_FILES := $(wildcard *.cc)
OBJ_FILES := $(SRC_FILES:%.cc=$(BUILD_DIR)/%.o)
LIBRARY := $(BUILD_DIR)/libdisasm.so

CXX := g++
CXXFLAGS := -fPIC -shared -Wall
LDFLAGS := -shared

.PHONY: all clean

all: $(LIBRARY)

$(BUILD_DIR):
	mkdir -p $(BUILD_DIR)

$(LIBRARY): $(OBJ_FILES)
	$(CXX) $(LDFLAGS) -o $@ $^

$(BUILD_DIR)/%.o: %.cc | $(BUILD_DIR)
	$(CXX) $(CXXFLAGS) -c $^ -o $@

clean:
	rm -rf $(BUILD_DIR)
