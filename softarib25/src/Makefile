PREFIX = /usr/local
MAJOR = 0
MINOR = 2
REVISION = 5
VER = $(MAJOR).$(MINOR).$(REVISION)

DEST_HEADER = $(PREFIX)/include/arib25

CC     = gcc
CXX    = g++
CPPFLAGS = -Wall -D_LARGEFILE_SOURCE -D_FILE_OFFSET_BITS=64 -I /usr/local/include/
CFLAGS = -O2 -g -fPIC
CXXFLAGS = -O2 -g -fPIC

LIBS = -lm -lecmdecoder
LDFLAGS ?= -L /usr/local/lib/

# All build outputs go here so they can be ignored by git
BUILD_DIR ?= build

OBJS  = $(addprefix $(BUILD_DIR)/,arib_std_b25.o b_cas_card.o multi2.o ts_section_parser.o)
TD_OBJ = $(BUILD_DIR)/td.o
HEADERS = arib_std_b25.h b_cas_card.h portable.h
TARGET_APP = $(BUILD_DIR)/b25
LIB_NAME = libarib25.so
TARGET_LIB = $(BUILD_DIR)/$(LIB_NAME)
TARGETS = $(TARGET_APP) $(TARGET_LIB)
SONAME = $(LIB_NAME).$(MAJOR)

all: $(TARGETS)

clean:
	rm -rf $(BUILD_DIR)

$(BUILD_DIR):
	mkdir -p $@

$(BUILD_DIR)/%.o: %.c | $(BUILD_DIR)
	$(CC) $(CPPFLAGS) $(CFLAGS) -MMD -MP -c -o $@ $<

$(BUILD_DIR)/%.o: %.cpp | $(BUILD_DIR)
	$(CXX) $(CPPFLAGS) $(CXXFLAGS) -MMD -MP -c -o $@ $<

$(TARGET_APP): $(OBJS) $(TD_OBJ)
	$(CXX) $(LDFLAGS) -o $@ $(OBJS) $(TD_OBJ) $(LIBS)

$(TARGET_LIB): $(OBJS)
	$(CXX) $(LDFLAGS) -shared -o $@ $(OBJS) $(LIBS) -Wl,-soname,$(SONAME)

install: $(TARGETS) install-headers
	install -m755 $(TARGET_APP) $(PREFIX)/bin
	install -m755 $(TARGET_LIB) $(PREFIX)/lib/$(LIB_NAME).$(VER)
	ln -sf $(PREFIX)/lib/$(LIB_NAME).$(VER) $(PREFIX)/lib/$(LIB_NAME).$(MAJOR)
	ln -sf $(PREFIX)/lib/$(LIB_NAME).$(MAJOR) $(PREFIX)/lib/$(LIB_NAME)
	ldconfig

install-headers:
	mkdir -p $(DEST_HEADER)
	install -m644 $(HEADERS) $(DEST_HEADER)

-include $(OBJS:.o=.d) $(TD_OBJ:.o=.d)
