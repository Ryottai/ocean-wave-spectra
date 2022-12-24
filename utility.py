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

def JONSWAP_wind(omega, U, X, gamma=3.3):
    X_tilde = X*g/U**2
    alpha = 0.066*X_tilde**(-0.22)
    omega_m = 2*np.pi*3.5*g*X_tilde**(-0.32)/U
    if omega <= omega_m:
        sigma = 0.07
    else:
        sigma = 0.09
    return alpha * g**2/((2*np.pi)**5 * (omega/(2*np.pi))**5) * np.exp(-5/4*(omega/omega_m)**(-4)) * gamma**np.exp(-(omega-omega_m)**2/(2*sigma**2*omega_m**2))

def JONSWAP_wave(omega, Hs, Ts, gamma=3.3, alpha=0.0326):
    Tp = 1.05*Ts
    omega_p = 2*np.pi/Tp
    if omega <= omega_p:
        sigma = 0.07
    else:
        sigma = 0.09
    return alpha * Hs**2/(Tp**4 * (omega/(2*np.pi))**5) * np.exp(-5/4*(Tp * omega/(2*np.pi))**(-4)) * gamma**np.exp(-(Tp*omega/(2*np.pi)-1)**2/(2*sigma**2))

def Bretschneider_Mitsuyasu(omega, Hs, Ts):
    H_bar = 0.625*Hs
    T_bar = Ts/1.1
    return 0.432/(2*np.pi) * (H_bar/(g*T_bar**2))**2 * g**2 * (omega/(2*np.pi))**5 * np.exp(-0.675/(T_bar*omega/(2*np.pi))**4)

def plot_function(func, title, Hv=None, Tv=None, Hs=None, Ts=None, U=None, X=None):
    fig = go.Figure()
    if func == PM:
        fig.add_trace(go.Scatter(x=omega, y=func(omega), mode='lines', line=dict(color='navy', width=2)))
    elif func == ISSC:
        fig.add_trace(go.Scatter(x=omega, y=func(omega, Hv, Tv), mode='lines', line=dict(color='navy', width=2)))
    elif func == ITTC:
        fig.add_trace(go.Scatter(x=omega, y=func(omega, Hs), mode='lines', line=dict(color='navy', width=2)))
    elif func == JONSWAP_wind:
        fig.add_trace(go.Scatter(x=omega, y=func(omega, U, X), mode='lines', line=dict(color='navy', width=2)))
    elif func == JONSWAP_wave:
        fig.add_trace(go.Scatter(x=omega, y=func(omega, Hs, Ts), mode='lines', line=dict(color='navy', width=2)))
    elif func == Bretschneider_Mitsuyasu:
        fig.add_trace(go.Scatter(x=omega, y=func(omega, Hs, Ts), mode='lines', line=dict(color='navy', width=2)))

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