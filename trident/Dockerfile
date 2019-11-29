FROM ubuntu:18.04 as builder

# Install Deps
RUN apt update
RUN apt install -y git cmake gcc build-essential zlib1g zlib1g-dev

# Install trident
WORKDIR /app
RUN git clone --depth 1 https://github.com/WDPS-Team/trident

RUN mkdir build
WORKDIR /app/trident/build
RUN cmake .. -DSERVER=1
RUN make

FROM ubuntu:18.04 as runtime
RUN apt install -y zlib1g

COPY --from=builder /app /app

WORKDIR /app/trident/build
CMD $KB_BIN server -i $KB_PATH --port $KB_PORT