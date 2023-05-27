# roadio
Developed during the Hackaburg 2023 for Vitesco's challenge and the mobility &amp; sustainability track.


## Setup Instructions

```bash 
# create environment
python -m venv venv
# activate environment
source venv/bin/activate
# install dependencies
pip install -r requirements.txt
´´´

## Run Instructions

```bash
# activate environment
source venv/bin/activate
# run app
streamlit run 🏠_Home.py
```

## Run in Docker

```bash
# build docker image
docker build -t roadio .
# run docker image
docker run -p 8501:8501 roadio
```

