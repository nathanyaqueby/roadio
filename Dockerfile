FROM python:3.10.11-slim-buster
WORKDIR streamlit

COPY requirements.txt .
COPY $PWD /streamlit
RUN pip install -r requirements.txt
CMD ["streamlit", "run", "🏠_Home.py"]