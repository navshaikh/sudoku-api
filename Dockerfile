FROM python:2.7-slim

RUN apt-get update -y 
RUN apt-get install -y git

RUN git clone https://github.com/navshaikh/sudoku.git app/sudoku
# Remove extraneous stuff
RUN rm -rf app/sudoku/data

WORKDIR app
COPY app.py requirements.txt /app/

RUN pip install -r requirements.txt

CMD flask run -h 0.0.0.0

