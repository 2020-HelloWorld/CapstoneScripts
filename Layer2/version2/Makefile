CC = gcc
LIBS = -lpcap -ljson-c

SRC = Flows.c
TARGET = packet_capture

all: $(TARGET)

$(TARGET): $(SRC)
	$(CC) $(SRC) -o $(TARGET) $(LIBS)

clean:
	rm -f $(TARGET)

.PHONY: all clean

