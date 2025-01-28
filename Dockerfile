FROM python:3.10-slim

WORKDIR /loanApprovalPrediction
#
#RUN apt-get update && apt-get install -y \
#    build-essential \
#    libatlas-base-dev \
#    liblapack-dev \
#    gfortran \
#    libpng-dev \
#    libfreetype6-dev \
#    && rm -rf /var/lib/apt/lists/*
#
#RUN pip install --no-cache-dir --upgrade pip

COPY . /loanApprovalPrediction

RUN pip install --no-cache-dir -r requirements.txt

#COPY . /loanApprovalPrediction/

EXPOSE 8080

CMD ["python", "server.py"]