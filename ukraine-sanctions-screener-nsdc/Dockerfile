FROM apify/actor-python:3.12
WORKDIR /usr/src/app
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt
COPY data ./data
COPY src ./src
CMD ["python", "-m", "src"]
