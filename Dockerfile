FROM nvidia/cuda:10.2-cudnn7-devel-ubuntu16.04
ENV ANACONDA /opt/anaconda3
ENV CUDA_PATH /usr/local/cuda
ENV PATH ${ANACONDA}/bin:${CUDA_PATH}/bin:$PATH
ENV LD_LIBRARY_PATH ${ANACONDA}/lib:${CUDA_PATH}/bin64:$LD_LIBRARY_PATH
ENV C_INCLUDE_PATH ${CUDA_PATH}/include
ENV DEBIAN_FRONTEND=noninteractive
RUN apt-get update && apt-get install -y --no-install-recommends \
         wget \
	 axel \
         imagemagick \
         libopencv-dev \
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
RUN wget https://repo.continuum.io/archive/Anaconda3-2020.02-Linux-x86_64.sh -P /tmp
RUN bash /tmp/Anaconda3-2020.02-Linux-x86_64.sh -b -p $ANACONDA
RUN rm /tmp/Anaconda3-2020.02-Linux-x86_64.sh -rf
RUN conda install pytorch==1.2.0 torchvision==0.4.0 cudatoolkit=10.0 -c pytorch
Run conda install python=3.6
RUN conda install -y -c anaconda pip 
RUN conda install -y -c menpo opencv3
WORKDIR home/code
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt
RUN rm requirements.txt
RUN pip uninstall -y pillow
RUN pip install pillow
