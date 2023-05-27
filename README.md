# Roadio
Developed during the Hackaburg 2023 for Vitesco's challenge and the sustainable mobility track.

![devpost thumbnail - hackaburg (1)](https://github.com/nathanyaqueby/roadio/assets/73829218/79210727-699d-4480-b675-a8d60bbaecfe)

Instead of switching between multiple navigation apps for different purposes, we offer a convenient one-stop solution to access all types of navigation services to save time and effort. Introducing: **_Roadio_**, an all-encompassing mobility platform developed for [Vitesco](https://www.vitesco-technologies.com/en-us)'s Work Smarter & Sustainable challenge.

## ❓ What it does
- Our app offers seamless transitions between driving directions, walking routes, public transit information, cycling paths, and more.
- Users can access real-time traffic updates, estimated time of arrival, alternative routes, and public transportation schedules to choose the best path based on their preferences.
- Roadio provides **personalized features** tailored to individual preferences where users can save personalized addresses, collect sustainability points, and rank up the leaderboard.
- Users can **carpool** using a fellow co-worker's vehicle on their way to the office or offer a ride and earn sustainability points.

## 💻 How we built it
- Technologies: `Docker`, `Streamlit`, `React`, `Figma`, and of course, `StackOverflow`
- Datasets: `Vitesco`'s sample dataset, `OpenStreetMap`'s API, and `World CO2 emissions` dataset
- Languages: `Python`, `JavaScript`, `HTML/CSS`

https://github.com/nathanyaqueby/roadio/assets/73829218/23d3e7da-e14f-4926-9125-5b742beddf28

## Setup Instructions

```bash 
# create environment
python -m venv venv

# activate environment
source venv/bin/activate

# install dependencies
pip install -r requirements.txt
```

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

## 🤗 Meet our team!
- Tayfun Bönsch (Germany)
- Marvin Lederer (Germany)
- Sohangkumar Patel (India)
- Hari Kesavan (India)
- Nathanya Queby (Indonesia)
