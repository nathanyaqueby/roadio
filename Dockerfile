FROM python:3.10.11-slim-buster
WORKDIR streamlit

COPY requirements.txt .

RUN pip install -r requirements.txt
CMD ["streamlit", "run", "🏠_Home.py"]