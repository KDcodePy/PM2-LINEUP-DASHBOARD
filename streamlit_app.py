import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import altair as alt
import json
import requests
from streamlit_lottie import st_lottie

# Page config

st.set_page_config(
    page_title='PM2 Rotation Dashboard',
    layout='wide',
    initial_sidebar_state='expanded'
)

alt.themes.enable('dark')
# CSS styling
st.markdown("""
<style>

[data-testid="block-container"] {
    padding-left: 2rem;
    padding-right: 2rem;
    padding-top: 1rem;
    padding-bottom: 0rem;
    margin-bottom: -7rem;
}

[data-testid="stVerticalBlock"] {
    padding-left: 0rem;
    padding-right: 0rem;
}

[data-testid="stMetric"] {
    background-color: #393939;
    text-align: center;
    padding: 15px 0;
}

[data-testid="stMetricLabel"] {
  display: flex;
  justify-content: center;
  align-items: center;
}

[data-testid="stMetricDeltaIcon-Up"] {
    position: relative;
    left: 38%;
    -webkit-transform: translateX(-50%);
    -ms-transform: translateX(-50%);
    transform: translateX(-50%);
}

[data-testid="stMetricDeltaIcon-Down"] {
    position: relative;
    left: 38%;
    -webkit-transform: translateX(-50%);
    -ms-transform: translateX(-50%);
    transform: translateX(-50%);
}

</style>
""", unsafe_allow_html=True)

# Load json file
def load_lottiefile(filepath: str):
    with open(filepath,'r') as f:
        return json.load(f)
    
# Load lottieurl
def load_lottieurl(url:str):
    r= requests.get(url)
    if r.status_code != 200:
        return None
    return r.json()

df = pd.read_csv(r'C:\Users\kdelfino\Documents\GitHub\PM2_Lineup_Dashboard\PM2-LINEUP-DASHBOARD\data\out.cvs')

st.title('***Welcome!***')


# Sub header
# st.subheader('**PM2 Station Rotation Dashboard**')

# Sidebar
with st.sidebar:
    st.title('🏂 PM2 Rotation Dashboard')
    # Logo 

    lottie_cybertruck = load_lottiefile(r'C:\Users\kdelfino\Documents\GitHub\PM2_Lineup_Dashboard\PM2-LINEUP-DASHBOARD\animation\cybertruck.json')

    st_lottie(lottie_cybertruck,
            speed=1,
            reverse=False,
            loop=True,
            #   renderer='svg',
            height=300,
            width=300)
    

#######################
# Dashboard Main Panel
col = st.columns((.5, 20, 2), gap='medium')

lottie_tesla = load_lottiefile(r'C:\Users\kdelfino\Documents\GitHub\PM2_Lineup_Dashboard\PM2-LINEUP-DASHBOARD\animation\tesla.json')
st_lottie(lottie_tesla,
            speed=1,
            reverse=False,
            loop=True,
            height=200,
            width=750,
            )
    

def random_bytes(n):
    "Return n random bytes"
    with open('/dev/urandom', 'rb') as file:
        return file.read(n)
with col[1]:
    
    aka  =st.selectbox('Select a Name', df['AKA'].unique())
    # Get name
    

    data_per_aka = df[(df['AKA']==aka)&(df['Station']!='Callout')]
    # Creating dataset
    Station = data_per_aka['Station'].unique()
    
    data = data_per_aka['Station'].value_counts()
    
    
    # # Creating explode data
    # explode = (0.1,0.2,0.0,0.0,0.2,0.1,0.1,0.2,0.1)
    explode = tuple(0.15 for i in range(len(Station)))
    
    # Creating color parameters
    colors = ("moccasin", "peru", "darkgray",
              "darkkhaki", "darkturquoise", "plum",
              'darkorange','khaki','skyblue',
              'coral','tomato','salmon','pink')
    
    # Wedge properties
    wp = {'linewidth': 1, 'edgecolor': "green"}
    
    # Creating autocpt arguments
    
    
    def func(pct, allvalues):
        absolute = int(pct / 100.*np.sum(allvalues))
        return "{:.1f}%\n({:d})".format(pct, absolute)
    
    
    # Creating plot
    fig, ax = plt.subplots(figsize=(25, 20))
    wedges, texts, autotexts = ax.pie(data,
                                    autopct=lambda pct: func(pct, data),
                                    explode=explode,
                                    labels=Station,
                                    shadow=True,
                                    colors=colors,
                                    startangle=75,
                                    wedgeprops={'edgecolor': 'black'},
                                    
                                    textprops=dict(color="k",
                                                   fontsize= 25,
                                                    fontstyle='oblique' ))
    
    
    # Adding legend
    ax.legend(wedges, Station,
            title="Stations",
            loc="upper right",
            bbox_to_anchor=(1, 0, 0.5, 1),
            fontsize='xx-large',
            title_fontsize = 'xx-large')
    
    plt.setp(autotexts, size=20, weight="bold")
    ax.set_title(f"{aka}'s Top Station Rotation",
                 loc= 'center',
                 fontdict={
                     'fontsize': 40,
                     'fontstyle': 'italic'
                 })
    fig.set_facecolor('bisque')
    
    
    # show plot
    st.pyplot(plt.gcf())


