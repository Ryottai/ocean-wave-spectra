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
        ### Ocean Wave Spectra
        This application shows ocean wave spectra and simulates waves made from each spectrum.
        """
    })

########################################

########################################
# Utility Code
omega = np.linspace(0,4,10000)
time = np.linspace(0,100,10000)
########################################

title = '<h1 style="padding:0;margin:0;color:#04ADE2;">Ocean Wave Spectra</h1>'
st.components.v1.html("<center>" + title + "</center>",height=50,)
st.markdown("---")

spectrum_list = ['None', 'Pierson-Moskowitz', 'ISSC', 'ITTC', 'JONSWAP (by wind information)', 'JONSWAP (by wave information)', 'Bretschneider-Mitsuyasu', 'Ochi-Hubble']

st.sidebar.markdown("## Menu")
st.sidebar.selectbox('select page:',['Main Page'])

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
if spectrum == 'Pierson-Moskowitz':
    st.header('Pierson-Moskowitz Spectrum')

    st.subheader('Formula')
    st.latex(r'''S(\omega)=\alpha\frac{g^2}{\omega^5}\exp\biggl\{-\beta\biggl(\frac{g}{\omega U}\biggr)^4\biggr\}''')
    st.latex(r'''\alpha=8.10\times10^{-3}, \quad \beta=0.74''')

    st.subheader('Plot')
    data = {
        'ω': omega,
        'PM': PM(omega),
    }
    wave = data
    df = pd.DataFrame(data)
    df = df.set_index('ω', drop=True)
    st.line_chart(df)
    PM_fig, max_S  = plot_function(PM)
    #st.plotly_chart(PM_fig)
    st.write(max_S)

    st.subheader('Wave')
    st.button('Remake wave')
    #st.dataframe(df)
    #st.write(random.uniform(0, 1))
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
    st.sidebar.markdown("## Parameters")
    Hv = st.sidebar.slider('Visually Observed Significant Wave Height', 0.1, 15., 7.5, 0.1)
    Tv = st.sidebar.slider('Visually Observed Wave Period', 0.1, 15., 7.5, 0.1)
    st.subheader('Formula')
    st.latex(r'''S(\omega)=\frac{0.11}{2\pi} H_v^2T_v^2 \biggl(T_v\frac{\omega}{2\pi} \biggr)^{-5} \exp\biggl\{ 0.44 \biggl( \frac{T_v \omega}{2\pi} \biggr)^{-4} \biggr\}''')

    st.subheader('Plot')
    
    data = {
        'ω': omega,
        'ISSC': ISSC(omega,Hv,Tv),
    }
    wave = data
    df = pd.DataFrame(data)
    df = df.set_index('ω', drop=True)
    st.line_chart(df)
    ISSC_fig, max_S = plot_function(ISSC, Hv=Hv, Tv=Tv)
    #st.plotly_chart(ISSC_fig)
    st.write(max_S)

    st.subheader('Wave')
    st.button('Remake wave')
    xmin = 0.01
    height_list = []
    omega_list = []
    for _ in range(10):
        if xmin <= 3.5:
            domega = random.uniform(0,0.5)
            height2 = integral(ISSC, xmin, xmin+domega, h=0.0001, Hv=Hv, Tv=Tv)
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

## ITTC
if spectrum == 'ITTC':
    st.header('ITTC Spectrum')
    st.sidebar.markdown("## Parameters")
    Hs = st.sidebar.slider('Significant Wave Height', 0.1, 15., 7.5, 0.1)

    st.subheader('Formula')
    st.latex(r'''S(\omega)=8.10\times10^{-3} g^2 \omega^{-5} \exp \biggl( \frac{-3.11}{H_s^2 \omega^4} \biggr)''')
    
    st.subheader('Plot')
    data = {
        'ω': omega,
        'ISSC': ITTC(omega,Hs),
    }
    wave = data # copy
    df = pd.DataFrame(data)
    df = df.set_index('ω', drop=True)
    st.line_chart(df)
    ITTC_fig, max_S = plot_function(ITTC, Hs=Hs)
    #st.plotly_chart(ITTC_fig)
    st.write(max_S)

    st.subheader('Wave')
    st.button('Remake wave')
    xmin = 0.01
    height_list = []
    omega_list = []
    for _ in range(10):
        if xmin <= 3.5:
            domega = random.uniform(0,0.5)
            height2 = integral(ITTC, xmin, xmin+domega, h=0.0001, Hs=Hs)
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

if spectrum == 'JONSWAP (by wind information)':
    st.header('JONSWAP Spectrum (by wind information)')
    st.sidebar.markdown("## Parameters")
    U = st.sidebar.slider('Wind Speed', 0.1, 50., 10., 0.1)
    X = st.sidebar.slider('Fetch', 0.1, 1000000., 100000., 0.1)
    
    st.subheader('Formula')
    st.latex(r'''S(\omega)=''')

    st.subheader('Plot')
    data = {
        'ω': omega,
        'JONSWAP(wind)': JONSWAP_wind(omega,U, X),
    }
    wave = data # copy
    df = pd.DataFrame(data)
    df = df.set_index('ω', drop=True)
    st.line_chart(df)
    JONSWAP_wind_fig, max_S = plot_function(JONSWAP_wind, U=U, X=X)
    #st.plotly_chart(JONSWAP_wind_fig)
    st.write(max_S)

    st.subheader('Wave')
    st.button('Remake wave')
    xmin = 0.01
    height_list = []
    omega_list = []
    for _ in range(10):
        if xmin <= 3.5:
            domega = random.uniform(0,0.5)
            height2 = integral(JONSWAP_wind, xmin, xmin+domega, h=0.0001, U=U, X=X)
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

if spectrum == 'JONSWAP (by wave information)':
    st.header('JONSWAP Spectrum (by wave information)')
    st.sidebar.markdown("## Parameters")
    Hs = st.sidebar.slider('Significant Wave Height', 0.1, 15., 7.5, 0.1)
    Ts = st.sidebar.slider('Significant Wave Period', 0.1, 15., 7.5, 0.1)

    st.subheader('Formula')
    st.latex(r'''S(\omega)=''')

    st.subheader('Plot')
    data = {
        'ω': omega,
        'JONSWAP(wave)': JONSWAP_wave(omega, Hs, Ts),
    }
    wave = data # copy
    df = pd.DataFrame(data)
    df = df.set_index('ω', drop=True)
    st.line_chart(df)
    JONSWAP_wave_fig, max_S = plot_function(JONSWAP_wave, Hs=Hs, Ts=Ts)
    #st.plotly_chart(JONSWAP_wave_fig)
    st.write(max_S)

    st.subheader('Wave')
    st.button('Remake wave')
    xmin = 0.01
    height_list = []
    omega_list = []
    for _ in range(10):
        if xmin <= 3.5:
            domega = random.uniform(0,0.5)
            height2 = integral(JONSWAP_wave, xmin, xmin+domega, h=0.0001, Hs=Hs, Ts=Ts)
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

if spectrum == 'Bretschneider-Mitsuyasu':
    st.header('Bretschneider-Mitsuyasu Spectrum')
    st.sidebar.markdown("## Parameters")
    Hs = st.sidebar.slider('Significant Wave Height', 0.1, 15., 7.5, 0.1)
    Ts = st.sidebar.slider('Significant Wave Period', 0.1, 15., 7.5, 0.1)

    st.subheader('Formula')
    st.latex(r'''S(\omega)=''')

    st.subheader('Plot')
    data = {
        'ω': omega,
        'Bretschneider-Mitsuyasu': Bretschneider_Mitsuyasu(omega, Hs, Ts),
    }
    wave = data # copy
    df = pd.DataFrame(data)
    df = df.set_index('ω', drop=True)
    st.line_chart(df)
    Bretschneider_Mitsuyasu_fig, max_S = plot_function(Bretschneider_Mitsuyasu, Hs=Hs, Ts=Ts)
    #st.plotly_chart(Bretschneider_Mitsuyasu_fig)
    st.write(max_S)

    st.subheader('Wave')
    st.button('Remake wave')
    xmin = 0.01
    height_list = []
    omega_list = []
    for _ in range(10):
        if xmin <= 3.5:
            domega = random.uniform(0,0.5)
            height2 = integral(Bretschneider_Mitsuyasu, xmin, xmin+domega, h=0.0001, Hs=Hs, Ts=Ts)
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

if spectrum == 'Ochi-Hubble':
    st.header('Ochi-Hubble Spectrum')
    st.subheader('*under construction')