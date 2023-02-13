import streamlit as st
import numpy as np
import pandas as pd
import plotly.graph_objects as go
import random
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
#import time
#from PIL import Image

from utility import derivative, PM, ISSC, ITTC, JONSWAP_wind, JONSWAP_wave, Bretschneider_Mitsuyasu, plot_function, plot_function_derivative, integral

########################################
# Settings
st.set_page_config(
    page_title="Ocean Wave Spectra", 
    #page_icon=image, 
    layout="wide", 
    initial_sidebar_state="auto", 
    menu_items={
        #'Get Help': 'https://discuss.streamlit.io/',
        #'Report a bug': "https://github.com/Ryottai/ocean_wave_spectra",
        'About': """
        # Ocean Wave Spectra
        This app shows ocean wave spectra.
        """
    })

########################################

########################################
# Utility Code
omega = np.linspace(0,4,10000)
time = np.linspace(0,100,10000)
########################################

title_top = '<h1 style="color:#008b8b">Ocean Wave Spectra</h1>'
st.write(title_top, unsafe_allow_html=True)
st.markdown("---")

spectrum_list = ['None', 'P-M (Pierson-Moskowitz)', 'ISSC', 'ITTC', 'JONSWAP (by wind)', 'JONSWAP (by wave)', 'Bretschneider-Mitsuyasu', 'Ochi-Hubble']

st.sidebar.markdown("## Main Menu")
st.sidebar.selectbox('select page:',['Top Page'])

st.sidebar.markdown("---")

st.sidebar.markdown("## Select")
spectrum = st.sidebar.radio('Choose a spectrum:', spectrum_list)

# None
if spectrum == 'None':
    st.header('Introduction')
    st.info('**This app is still incomplete.**')
    #st.write('If we look out to sea, we notice that waves on the sea surface are not simple sinusoids. The surface appears to be composed of random waves of various lengths and periods. How can we describe this surface? The simple answer is, Not very easily. We can however, with some simplifications, come close to describing the surface. The simplifications lead to the concept of the spectrum of ocean waves. The spectrum gives the distribution of wave energy among different wave frequencies of wave-lengths on the sea surface.')
    #st.caption('by wikiwaves')
    #st.multiselect('Comparison', spectrum_list)

## PM
if spectrum == 'P-M (Pierson-Moskowitz)':
    st.header('Pierson-Moskowitz Spectrum')

    st.subheader('Formula')
    st.latex(r'''S(\omega)=\alpha\frac{g^2}{\omega^5}\exp\Bigl\{-\beta\Bigl(\frac{g}{\omega U}\Bigr)^4\Bigr\}''')
    st.latex(r'''\alpha=8.10\times10^{-3}, \beta=0.74''')

    st.subheader('Plot')
    data = {
        'ω': omega,
        'PM': PM(omega),
    }
    df = pd.DataFrame(data)
    df = df.set_index('ω', drop=True)
    st.line_chart(df)
    PM_fig, max_S  = plot_function(PM)
    #st.plotly_chart(PM_fig)
    st.write(max_S)
    #st.dataframe(df)
    #st.write(random.uniform(0, 1))
    wave = {
        'ω': omega,
        'PM': PM(omega),
    }
    xmin = 0.01
    height_list = []
    omega_list = []
    for _ in range(10):
        if xmin <= 3.5:
            domega = random.uniform(0,0.5)
            height2 = integral(PM, xmin, xmin+domega, h=0.0001)
            height = np.sqrt(height2)
            omega = xmin+domega/2
            #T = 2*np.pi/omega
            xmin += domega
            height_list.append(height)
            omega_list.append(omega)
        else:
            pass
    #st.write(height_list)
    #st.write(omega_list)
    wave = {'t': time}
    for i in range(len(height_list)):
        wave['wave{}'.format(i)] = height_list[i] * np.sin(omega_list[i]*time)
    df_wave = pd.DataFrame(wave)
    df_wave = df_wave.set_index('t', drop=True)
    #st.dataframe(df_wave)
    st.write('elemental wave')
    st.line_chart(df_wave, height=300)
    st.write('synthetic wave')
    df_wave['wave'] = df_wave.sum(axis=1)
    st.line_chart(df_wave['wave'], height=300)


## ISSC
if spectrum == 'ISSC':
    st.header('ISSC Spectrum')

    st.subheader('Formula')

    st.subheader('Plot')
    st.sidebar.markdown("## Settings")
    Hv = st.sidebar.slider('Visually Observed Significant Wave Height', 0.1, 15., 7.5, 0.1)
    Tv = st.sidebar.slider('Visually Observed Wave Period', 0.1, 15., 7.5, 0.1)
    ISSC_fig, max_S = plot_function(ISSC, Hv=Hv, Tv=Tv)
    st.plotly_chart(ISSC_fig)
    st.write(max_S)

## ITTC
if spectrum == 'ITTC':
    st.header('ITTC Spectrum')

    st.subheader('Plot')
    st.sidebar.markdown("## Settings")
    Hs = st.sidebar.slider('Significant Wave Height', 0.1, 15., 7.5, 0.1)
    ITTC_fig, max_S = plot_function(ITTC, Hs=Hs)
    st.plotly_chart(ITTC_fig)
    st.write(max_S)

if spectrum == 'JONSWAP (by wind)':
    st.header('JONSWAP Spectrum (by wind)')

    st.subheader('Formula')

    st.subheader('Plot')
    st.sidebar.markdown("## Settings")
    U = st.sidebar.slider('Wind Speed', 0.1, 50., 10., 0.1)
    X = st.sidebar.slider('Fetch', 0.1, 1000000., 100000., 0.1)
    JONSWAP_wind_fig, max_S = plot_function(JONSWAP_wind, U=U, X=X)
    st.plotly_chart(JONSWAP_wind_fig)
    st.write(max_S)

if spectrum == 'JONSWAP (by wave)':
    st.header('JONSWAP Spectrum (by wave)')

    st.subheader('Formula')

    st.subheader('Plot')
    st.sidebar.markdown("## Settings")
    Hs = st.sidebar.slider('Significant Wave Height', 0.1, 15., 7.5, 0.1)
    Ts = st.sidebar.slider('Significant Wave Period', 0.1, 15., 7.5, 0.1)
    JONSWAP_wave_fig, max_S = plot_function(JONSWAP_wave, Hs=Hs, Ts=Ts)
    st.plotly_chart(JONSWAP_wave_fig)
    st.write(max_S)

if spectrum == 'Bretschneider-Mitsuyasu':
    st.header('Bretschneider-Mitsuyasu Spectrum')

    st.subheader('Formula')

    st.subheader('Plot')
    st.sidebar.markdown("## Settings")
    Hs = st.sidebar.slider('Significant Wave Height', 0.1, 15., 7.5, 0.1)
    Ts = st.sidebar.slider('Significant Wave Period', 0.1, 15., 7.5, 0.1)
    Bretschneider_Mitsuyasu_fig, max_S = plot_function(Bretschneider_Mitsuyasu, Hs=Hs, Ts=Ts)
    st.plotly_chart(Bretschneider_Mitsuyasu_fig)
    st.write(max_S)