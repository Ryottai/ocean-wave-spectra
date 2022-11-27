import streamlit as st
import numpy as np
import plotly.graph_objects as go

from utility import derivative, PM, ISSC, ITTC, plot_function, plot_function_derivative

########################################
# Utility Code
omega = np.linspace(0,2,200)
#########################################

st.title('Ocean Wave Spectra')

spectrum = st.sidebar.selectbox('Choose a spectrum', ['None', 'P-M (Pierson-Moskowitz)', 'ISSC', 'ITTC', 'JONSWAP', 'Bretschneider', 'Ochi-Hubble'])

# None
if spectrum == 'None':
    st.subheader('**This app is still incomplete.**')
    st.write('If we look out to sea, we notice that waves on the sea surface are not simple sinusoids. The surface appears to be composed of random waves of various lengths and periods. How can we describe this surface? The simple answer is, Not very easily. We can however, with some simplifications, come close to describing the surface. The simplifications lead to the concept of the spectrum of ocean waves. The spectrum gives the distribution of wave energy among different wave frequencies of wave-lengths on the sea surface.')
    st.caption('by wikiwaves')

## PM
if spectrum == 'P-M (Pierson-Moskowitz)':
    st.header('P-M (Pierson-Moskowitz) Spectrum')

    st.subheader('Formula')
    st.latex(r'''S(\omega)=\alpha\frac{g^2}{\omega^5}\exp\Bigl\{-\beta\Bigl(\frac{g}{\omega U}\Bigr)^4\Bigr\}''')
    st.latex(r'''\alpha=8.10\times10^{-3}, \beta=0.74''')

    st.subheader('Plot')
    PM_fig  = plot_function(PM, title='P-M Spectrum')
    st.plotly_chart(PM_fig)

## ISSC
if spectrum == 'ISSC':
    st.header('ISSC')

    st.subheader('Formula')

    st.subheader('Plot')
    Hv = st.slider('Visually Observed Significant Wave Height', 0., 15., 7.5, 0.1)
    Tv = st.slider('Visually Observed Wave Period', 0., 15., 7.5, 0.1)
    ISSC_fig = plot_function(ISSC, Hv=Hv, Tv=Tv, title='Hyperbolic Tangent Function')
    st.plotly_chart(ISSC_fig)

## ITTC
if spectrum == 'ITTC':
    st.header('ITTC')

    st.subheader('Plot')
    Hs = st.slider('Significant Wave Height', 0., 15., 7.5, 0.1)
    ITTC_fig = plot_function(ITTC, Hs=Hs, title = 'ITTC')
    st.plotly_chart(ITTC_fig)
