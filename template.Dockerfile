# build: docker build -t <image_name> .
# create container (without volume): docker run -it --rm <image_name>
# create container (with volume): docker run -it --rm -v $(pwd):/vol <image_name>

FROM <insert_base_image_here>

ENV DEBIAN_FRONTEND=noninteractive

RUN mkdir -p /ctf
WORKDIR /ctf

# COPY flag.txt .
# COPY <challenge_binary> .
# RUN chmod +x <challenge_binary>

RUN apt-get update -y
RUN apt-get upgrade -y

RUN apt-get install -y strace gdb gdb-multiarch gcc gdbserver \
  libc6-dbg gcc-multilib g++-multilib curl wget make python3 \
  python3-pip vim binutils ruby ruby-dev netcat tmux \
  file less man jq lsof tree iproute2 iputils-ping iptables dnsutils \
  traceroute nmap socat p7zip-full git

# python/pwntools
RUN python3 -m pip install --upgrade pip
RUN python3 -m pip install --upgrade pwntools keystone-engine unicorn capstone ropper

# ruby/one_gadget
RUN gem install one_gadget

# Install pwndbg
RUN git clone https://github.com/pwndbg/pwndbg && cd pwndbg && ./setup.sh

# GDB
RUN echo "set confirm off" >> ~/.gdbinit
RUN echo "set pagination off" >> ~/.gdbinit