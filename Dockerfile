# Build Stage
FROM --platform=linux/amd64 python:3.11-slim as builder

USER root

# Install binutils (includes objdump)
RUN apt-get update && apt-get install -y binutils

WORKDIR /usr/src/app

COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy only necessary source files
COPY . .

# Use PyInstaller to create a standalone executable
RUN pyinstaller --onedir src/main.py

# Final Stage
FROM --platform=linux/amd64 python:3.11-slim as production

USER root

# Install dependencies
RUN apt-get update && \
    apt-get install -y \
    wget \
    gnupg \
    unzip \
    libglib2.0-0 \
    libnss3 \
    libgconf-2-4 \
    libfontconfig1

WORKDIR /usr/src/app

COPY --from=builder /usr/src/app/dist ./dist
COPY --from=builder /usr/src/app/build ./build

# Ensure execute permissions
RUN chmod +x ./dist/main/main

# Command to run your application
CMD ["./dist/main/main"]