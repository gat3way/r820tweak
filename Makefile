CC = gcc
CFLAGS = -fPIC -Wall -O2 -g -Iinclude -I/usr/include/libusb-1.0 -I/usr/include/libusb-1.1
LDFLAGS = -shared -lusb -lpthread
RM = rm -f
TARGET_LIB = build/librtlsdr.so
SRCS = src/librtlsdr.c  src/rtlsdr_rpc.c  src/rtlsdr_rpc_msg.c  src/tuner_e4k.c  src/tuner_fc0012.c  src/tuner_fc0013.c  src/tuner_fc2580.c  src/tuner_r82xx.c src/convenience/convenience.c
OBJS = $(SRCS:.c=.o)

.PHONY: all


all: ${TARGET_LIB}

$(TARGET_LIB): $(OBJS)
	$(CC) ${LDFLAGS} -o $@ $^

$(SRCS:.c=.d):%.d:%.c
	$(CC) $(CFLAGS) -MM $< >$@


include $(SRCS:.c=.d)

.PHONY: clean

clean:
	-${RM} ${TARGET_LIB} ${OBJS}

install:
	mkdir -p /usr/local/bin 2>/dev/null
	mkdir -p /usr/local/share/r820tweak 2>/dev/null
	cp build/librtlsdr.so /usr/local/share/r820tweak
	cp python/r820tweak.py /usr/local/bin/r820tweak
	chmod ugo+x /usr/local/bin/r820tweak