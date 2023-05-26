import streamlit as st
import streamlit_authenticator as stauth
import pandas as pd
from awesome_table import AwesomeTable
from awesome_table.columns import (Column, ColumnDType)

st.set_page_config(layout="wide",
                initial_sidebar_state="expanded",
                page_title="Roadio",
                page_icon="🚗",
                menu_items={
                    'Get Help': 'https://www.github.com/nathanyaqueby/roadio/',
                    'Report a bug': "https://www.github.com/nathanyaqueby/roadio/issues",
                    'About': "https://www.github.com/nathanyaqueby/roadio/"
                })

st.title("Leaderboard")
st.markdown("See how much sustainable travel you've done and how you compare to others!")

sample_data = {
  "id": 1,
  "name": "Liesa McMinn",
  "avatar": "https://robohash.org/solutareprehenderitmolestias.png?size=50x50&set=set1",
  "job_title": "Cost Accountant",
  "_url": {
    "social_media": "https://typepad.com/quam.xml",
    "document": "http://dummyimage.com/180x100.png/ff4444/ffffff"
  }
}, {
  "id": 2,
  "name": "Augusta Yansons",
  "avatar": "https://robohash.org/sedsintiusto.png?size=50x50&set=set1",
  "job_title": "Sales Representative",
  "_url": {
    "social_media": "https://miitbeian.gov.cn/dapibus/dolor/vel/est/donec/odio.js",
    "document": "http://dummyimage.com/160x100.png/dddddd/000000"
  }
}, {
  "id": 3,
  "name": "Errick Lingner",
  "avatar": "https://robohash.org/molestiasipsumnesciunt.png?size=50x50&set=set1",
  "job_title": "Structural Analysis Engineer",
  "_url": {
    "social_media": "http://istockphoto.com/lectus/in/quam/fringilla/rhoncus.json",
    "document": "http://dummyimage.com/176x100.png/5fa2dd/ffffff"
  }
}, {
  "id": 4,
  "name": "Suki Roderham",
  "avatar": "https://robohash.org/veniamprovidentqui.png?size=50x50&set=set1",
  "job_title": "Computer Systems Analyst II",
  "_url": {
    "social_media": "http://fastcompany.com/morbi/ut/odio.json",
    "document": "http://dummyimage.com/125x100.png/dddddd/000000"
  }
}, {
  "id": 5,
  "name": "Tarrah Gatehouse",
  "avatar": "https://robohash.org/praesentiumtemporemaxime.png?size=50x50&set=set1",
  "job_title": "Teacher",
  "_url": {
    "social_media": "http://admin.ch/est/et/tempus/semper/est.json",
    "document": "http://dummyimage.com/194x100.png/ff4444/ffffff"
  }
}, {
  "id": 6,
  "name": "Roland Goane",
  "avatar": "https://robohash.org/laudantiumofficiaincidunt.png?size=50x50&set=set1",
  "job_title": "Quality Control Specialist",
  "_url": {
    "social_media": "http://list-manage.com/non/velit/nec/nisi/vulputate.json",
    "document": "http://dummyimage.com/158x100.png/5fa2dd/ffffff"
  }
}, {
  "id": 7,
  "name": "Trude Greenham",
  "avatar": "https://robohash.org/nequeetfugiat.png?size=50x50&set=set1",
  "job_title": "Nuclear Power Engineer",
  "_url": {
    "social_media": "https://biglobe.ne.jp/turpis/adipiscing/lorem/vitae/mattis/nibh/ligula.aspx",
    "document": "http://dummyimage.com/215x100.png/dddddd/000000"
  }
}

AwesomeTable(pd.json_normalize(sample_data), columns=[
    Column(name='id', label='ID'),
    Column(name='name', label='Name'),
    Column(name='job_title', label='Job Title'),
    Column(name='avatar', label='Avatar', dtype=ColumnDType.IMAGE),
    Column(name='_url.social_media', label='Social Media', dtype=ColumnDType.ICONBUTTON, icon='fa-solid fa-share-nodes'), ## From FontAwesome v6.0.0
    Column(name='_url.document', label='Document', dtype=ColumnDType.DOWNLOAD),
], show_search=True, show_order=True)