FROM python:3.8

RUN apt-get update
RUN apt-get install -y texlive-full python-pydot python-pydot-ng graphviz
RUN python3.8 -m pip install --index-url https://test.pypi.org/simple/ --no-deps fibonacci-ast-gen -U
RUN python3.8 -m pip install matplotlib

WORKDIR /workspace

COPY . /workspace
COPY /hw_1/src/astgen/fibo.py /workspace/fibo.py
RUN python3.8 /workspace/latex.py
RUN pdflatex /workspace/artifacts/file.tex