CC = gcc  # Compiler

TARGET = conn2khr.so  # Target file
SRCS = conn2khr.c  # Source files
CFLAGS = -I./librcb4/inc -shared -fPIC  # Compiler flags
LDFLAGS = -L./librcb4/lib -lrcb4  # Linker flags

# Default target
all: $(TARGET)

$(TARGET): $(SRCS)
	$(CC) $(CFLAGS) $(SRCS) $(LDFLAGS) -o $(TARGET)

# Remove target file
clean:
	rm -f $(TARGET)

.PHONY: all clean
