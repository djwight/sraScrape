FROM python:3.11-slim

# get curl
RUN apt-get -y update && apt-get -y install curl

# install Entrez Direct CLI
RUN yes | sh -c "$(curl -fsSL https://ftp.ncbi.nlm.nih.gov/entrez/entrezdirect/install-edirect.sh)"

COPY requirements.txt requirements.txt

RUN pip install -r requirements.txt

ENTRYPOINT ["python3", "runner.py"]
#ENTRYPOINT [ "yes" ]