PREFIX ?= /usr/local
BUILD_DIR := build
BCASID_INFO ?= /etc/bcasid.inf
PCSC_CFLAGS ?= $(shell pkg-config --cflags libpcsclite 2>/dev/null)
PCSC_LIBS ?= $(shell pkg-config --libs libpcsclite 2>/dev/null || printf '%s' '-lpcsclite')

BCASID := bcasid/bcasid
ECMDECODER := $(BUILD_DIR)/libecmdecoder.so
ARIB25_DIR := softarib25/src
ARIB25_APP := $(ARIB25_DIR)/b25
ARIB25_LIB := $(ARIB25_DIR)/libarib25.so

BCASID_SOURCES := bcasid/bcasid.c bcasid/b_cas_card.c
ECMDECODER_SOURCES := \
	libecmdecoder/Crypto.cpp \
	libecmdecoder/Decoder-ECM.cpp \
	libecmdecoder/Keys.cpp \
	libecmdecoder/Keyset.cpp

.PHONY: all bcasid-inf install clean softarib25

all: $(BCASID) $(ECMDECODER) $(ARIB25_APP) $(ARIB25_LIB)

$(BCASID): $(BCASID_SOURCES) bcasid/b_cas_card.h bcasid/portable.h
	$(CC) $(CPPFLAGS) $(PCSC_CFLAGS) $(CFLAGS) -o $@ $(BCASID_SOURCES) $(PCSC_LIBS)

$(ECMDECODER): $(ECMDECODER_SOURCES) $(wildcard libecmdecoder/*.h)
	mkdir -p $(BUILD_DIR)
	$(CXX) $(CPPFLAGS) $(CXXFLAGS) -shared -fPIC -Wl,-soname,libecmdecoder.so -o $@ $(ECMDECODER_SOURCES)

softarib25: $(ECMDECODER)
	$(MAKE) -C $(ARIB25_DIR) \
		CPPFLAGS="-I$(abspath .) -Wall -D_LARGEFILE_SOURCE -D_FILE_OFFSET_BITS=64 -I/usr/local/include" \
		LDFLAGS="-L$(abspath $(BUILD_DIR))"

$(ARIB25_APP) $(ARIB25_LIB): softarib25

bcasid-inf: $(BCASID)
	./$(BCASID) > $(BCASID_INFO)

install: all
	mkdir -p $(PREFIX)/bin $(PREFIX)/lib
	install -m755 $(ECMDECODER) $(PREFIX)/lib/libecmdecoder.so
	$(MAKE) -C $(ARIB25_DIR) install PREFIX=$(PREFIX)

clean:
	rm -f $(BCASID) $(ECMDECODER)
	$(MAKE) -C $(ARIB25_DIR) clean
