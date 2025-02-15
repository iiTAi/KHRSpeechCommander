CC = gcc  # Compiler

INCLUDES = -I./librcb4/inc  # Include path
LIBS = -L./librcb4/lib  # Library path

TARGET = conn2khr.so  # Target file
SRCS = conn2khr.c  # Source files
CFLAGS = -shared -fPIC  # Compiler flags

# Default target
all: $(TARGET)

$(TARGET): $(SRCS)
	$(CC) $(INCLUDES) $(LIBS) $(CFLAGS) $(SRCS) -o $(TARGET)

# Remove target file
clean:
	rm -f $(TARGET)

.PHONY: all clean
