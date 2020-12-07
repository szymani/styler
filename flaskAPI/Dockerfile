FROM ubuntu:xenial

ENV PATH="/root/miniconda3/bin:${PATH}"
ARG PATH="/root/miniconda3/bin:${PATH}"

ENV DEBIAN_FRONTEND=noninteractive
RUN apt-get update && apt-get install -y --no-install-recommends \
         wget \
	     axel \
         imagemagick \
         libopencv-dev \
         libpython-dev \
         python-opencv \
         build-essential \
         cmake \
         git \
         curl \
         ca-certificates \
         libjpeg-dev \
         libpng-dev \
         axel \
         zip \
         unzip

RUN wget \
    https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh \
    && mkdir /root/.conda \
    && bash Miniconda3-latest-Linux-x86_64.sh -b \
    && rm -f Miniconda3-latest-Linux-x86_64.sh 

RUN conda install python=3.6
RUN conda install pytorch==1.2.0 torchvision==0.4.0
RUN conda install -y -c anaconda pip 
RUN conda install -y -c menpo opencv3
RUN conda install -y -c conda-forge uwsgi

# Set the working directory to /application
WORKDIR /application
# Copy the current directory contents into the container at /app 
ADD . /application
RUN pip install -r requirements.txt
# Weird but needed to work
RUN pip uninstall -y pillow
RUN pip install pillow

# run the command to start uWSGI
CMD ["uwsgi", "app.ini"]