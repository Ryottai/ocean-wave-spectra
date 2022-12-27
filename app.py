import streamlit as st
import numpy as np
import plotly.graph_objects as go
#import time
#from PIL import Image

from utility import derivative, PM, ISSC, ITTC, JONSWAP_wind, JONSWAP_wave, Bretschneider_Mitsuyasu, plot_function, plot_function_derivative

########################################
# Settings
#image = Image.open('スライム.jpg')
st.set_page_config(
    page_title="Ocean Wave Spectra", 
    #page_icon=image, 
    layout="centered", 
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
omega = np.linspace(0,20,4000)
########################################

title_top = '<h1 style="color:#008b8b">Ocean Wave Spectra</h1>'
st.write(title_top, unsafe_allow_html=True)

spectrum_list = ['None', 'P-M (Pierson-Moskowitz)', 'ISSC', 'ITTC', 'JONSWAP (by wind)', 'JONSWAP (by wave)', 'Bretschneider-Mitsuyasu', 'Ochi-Hubble']

st.sidebar.markdown("## Select")
spectrum = st.sidebar.radio('Choose a spectrum', spectrum_list)

# None
if spectrum == 'None':
    st.header('')
    st.subheader('**This app is still incomplete.**')
    st.write('If we look out to sea, we notice that waves on the sea surface are not simple sinusoids. The surface appears to be composed of random waves of various lengths and periods. How can we describe this surface? The simple answer is, Not very easily. We can however, with some simplifications, come close to describing the surface. The simplifications lead to the concept of the spectrum of ocean waves. The spectrum gives the distribution of wave energy among different wave frequencies of wave-lengths on the sea surface.')
    st.caption('by wikiwaves')
    st.multiselect('Comparison', spectrum_list)

## PM
if spectrum == 'P-M (Pierson-Moskowitz)':
    st.header('Pierson-Moskowitz Spectrum')

    st.subheader('Formula')
    st.latex(r'''S(\omega)=\alpha\frac{g^2}{\omega^5}\exp\Bigl\{-\beta\Bigl(\frac{g}{\omega U}\Bigr)^4\Bigr\}''')
    st.latex(r'''\alpha=8.10\times10^{-3}, \beta=0.74''')

    st.subheader('Plot')
    PM_fig  = plot_function(PM)
    st.plotly_chart(PM_fig)

## ISSC
if spectrum == 'ISSC':
    st.header('ISSC Spectrum')

    st.subheader('Formula')

    st.subheader('Plot')
    st.sidebar.markdown("## Settings")
    Hv = st.sidebar.slider('Visually Observed Significant Wave Height', 0.1, 15., 7.5, 0.1)
    Tv = st.sidebar.slider('Visually Observed Wave Period', 0.1, 15., 7.5, 0.1)
    ISSC_fig = plot_function(ISSC, Hv=Hv, Tv=Tv)
    st.plotly_chart(ISSC_fig)

## ITTC
if spectrum == 'ITTC':
    st.header('ITTC Spectrum')

    st.subheader('Plot')
    st.sidebar.markdown("## Settings")
    Hs = st.sidebar.slider('Significant Wave Height', 0.1, 15., 7.5, 0.1)
    ITTC_fig = plot_function(ITTC, Hs=Hs)
    st.plotly_chart(ITTC_fig)

if spectrum == 'JONSWAP (by wind)':
    st.header('JONSWAP Spectrum (by wind)')

    st.subheader('Formula')

    st.subheader('Plot')
    st.sidebar.markdown("## Settings")
    U = st.sidebar.slider('Wind Speed', 0.1, 50., 25., 0.1)
    X = st.sidebar.slider('Fetch', 0.1, 1000000., 500000., 0.1)
    JONSWAP_wind_fig = plot_function(JONSWAP_wind, U=U, X=X)
    st.plotly_chart(JONSWAP_wind_fig)

if spectrum == 'JONSWAP Spectrum (by wave)':
    st.header('JONSWAP (by wave)')

    st.subheader('Formula')

    st.subheader('Plot')
    st.sidebar.markdown("## Settings")
    Hs = st.sidebar.slider('Significant Wave Height', 0.1, 15., 7.5, 0.1)
    Ts = st.sidebar.slider('Significant Wave Period', 0.1, 15., 7.5, 0.1)
    JONSWAP_wave_fig = plot_function(JONSWAP_wave, Hs=Hs, Ts=Ts)
    st.plotly_chart(JONSWAP_wave_fig)

if spectrum == 'Bretschneider-Mitsuyasu':
    st.header('Bretschneider-Mitsuyasu Spectrum')

    st.subheader('Formula')

    st.subheader('Plot')
    st.sidebar.markdown("## Settings")
    Hs = st.sidebar.slider('Significant Wave Height', 0.1, 15., 7.5, 0.1)
    Ts = st.sidebar.slider('Significant Wave Period', 0.1, 15., 7.5, 0.1)
    Bretschneider_Mitsuyasu_fig = plot_function(Bretschneider_Mitsuyasu, Hs=Hs, Ts=Ts)
    st.plotly_chart(Bretschneider_Mitsuyasu_fig)