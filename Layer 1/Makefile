CC = gcc
LIBS = -lpcap -ljson-c

SRC = TTL_Deviation.c
TARGET = packet_capture

all: $(TARGET)

$(TARGET): $(SRC)
	$(CC) $(SRC) -o $(TARGET) $(LIBS)

clean:
	rm -f $(TARGET)

.PHONY: all clean

