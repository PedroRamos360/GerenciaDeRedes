CC = gcc
CFLAGS = 
LIBS = -lnetsnmp

TARGET = main
SOURCE = main.c

all: $(TARGET)

$(TARGET): $(SOURCE)
	$(CC) $(CFLAGS) -o $@ $^ $(LIBS)

clean:
	rm -f $(TARGET)
