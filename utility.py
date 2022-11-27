import numpy as np
import plotly.graph_objects as go
from scipy.special import erfc

omega = np.linspace(0,20,4000)
g = 9.81

def derivative(f, omega, eps=0.000001):
    return (f(omega + eps) - f(omega - eps))/(2 * eps)

def PM(omega, alpha=8.10*10**(-3), beta=0.74, U=19.5):
    return alpha*g**2/omega**5 * np.exp(-beta*(g/(omega*U))**4)

def ISSC(omega, Hv, Tv):
    return 0.11/(2*np.pi) * Hv**2 * Tv * (Tv*omega/(2*np.pi))**(-5) * np.exp(-0.44*((Tv*omega)/(2*np.pi))**(-4))

def ITTC(omega, Hs):
    return 8.1*10**(-3) * g**2 * omega**(-5) * np.exp(-3.11/(Hs**2*omega**4))

#def JONSWAP(omega, ):
#    return scale * elu(z, alpha)

def plot_function(func, title, Hv=None, Tv=None, Hs=None):
    fig = go.Figure()
    if Hv:
        fig.add_trace(go.Scatter(x=omega, y=func(omega, Hv=Hv, Tv=Tv), mode='lines', line=dict(color='navy', width=2)))
    elif Hs:
        fig.add_trace(go.Scatter(x=omega, y=func(omega, Hs=Hs), mode='lines', line=dict(color='navy', width=2)))
    else:
        fig.add_trace(go.Scatter(x=omega, y=func(omega), mode='lines', line=dict(color='navy', width=2)))
    fig.update_layout(title = title, xaxis_title='freakency',width=700, height=400, font=dict(family="Courier New, monospace",size=18,color="black"), margin=dict(t=30, b=0, l=0, r=0))
    fig.update_xaxes(zeroline=True, zerolinewidth=2, zerolinecolor='gray', gridcolor='silver', range=(0,2))
    fig.update_yaxes(zeroline=True, zerolinewidth=2, zerolinecolor='gray', gridcolor='silver')

    return fig

def plot_function_derivative(func, title):
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=omega, y=derivative(func, omega), mode='lines', line=dict(color='navy', width=2)))
    fig.update_layout(title = title, xaxis_title='Z', width=700, height=400,font=dict(family="Courier New, monospace",size=18,color="black"), margin=dict(t=30, b=0, l=0, r=0))
    fig.update_xaxes(zeroline=True, zerolinewidth=2, zerolinecolor='gray', gridcolor='silver')
    fig.update_yaxes(zeroline=True, zerolinewidth=2, zerolinecolor='gray', gridcolor='silver')
    return fig