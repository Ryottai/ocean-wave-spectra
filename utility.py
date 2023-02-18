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
    sigma = omega
    sigma = np.where(sigma <= omega_m, 0.07, 0.09)
    return alpha * g**2/((2*np.pi)**4 * (omega/(2*np.pi))**5) * np.exp(-5/4*(omega/omega_m)**(-4)) * gamma**np.exp(-(omega-omega_m)**2/(2*sigma**2*omega_m**2))

def JONSWAP_wave(omega, Hs, Ts, gamma=3.3, alpha=0.0326):
    Tp = 1.05*Ts
    omega_p = 2*np.pi/Tp
    sigma = omega
    sigma = np.where(sigma <= omega_p, 0.07, 0.09)
    return alpha * Hs**2/(Tp**4 * (omega/(2*np.pi))**5) * np.exp(-5/4*(Tp * omega/(2*np.pi))**(-4)) * gamma**np.exp(-(Tp*omega/(2*np.pi)-1)**2/(2*sigma**2))

def Bretschneider_Mitsuyasu(omega, Hs, Ts):
    #H_bar = 0.625*Hs
    #T_bar = Ts/1.1
    #return 0.432/(2*np.pi) * (H_bar/(g*T_bar**2))**2 * g**2 * (omega/(2*np.pi))**5 * np.exp(-0.675/(T_bar*omega/(2*np.pi))**4)
    return 0.257 * Hs**2 *Ts**(-4) * omega**(-5) * np.exp(-1.03*(Ts*omega)**(-4))

def plot_function(func, Hv=None, Tv=None, Hs=None, Ts=None, U=None, X=None):
    fig = go.Figure()
    if func == PM:
        fig.add_trace(go.Scatter(x=omega, y=func(omega), mode='lines', line=dict(color='#008b8b', width=2)))
        max_S = np.max(func(omega)[1:])
    elif func == ISSC:
        fig.add_trace(go.Scatter(x=omega, y=func(omega, Hv, Tv), mode='lines', line=dict(color='#008b8b', width=2)))
        max_S = np.max(func(omega, Hv, Tv)[1:])
    elif func == ITTC:
        fig.add_trace(go.Scatter(x=omega, y=func(omega, Hs), mode='lines', line=dict(color='#008b8b', width=2)))
        max_S = np.max(func(omega, Hs)[1:])
    elif func == JONSWAP_wind:
        fig.add_trace(go.Scatter(x=omega, y=func(omega, U, X), mode='lines', line=dict(color='#008b8b', width=2)))
        max_S = np.max(func(omega, U, X)[1:])
    elif func == JONSWAP_wave:
        fig.add_trace(go.Scatter(x=omega, y=func(omega, Hs, Ts), mode='lines', line=dict(color='#008b8b', width=2)))
        max_S = np.max(func(omega, Hs, Ts)[1:])
    elif func == Bretschneider_Mitsuyasu:
        fig.add_trace(go.Scatter(x=omega, y=func(omega, Hs, Ts), mode='lines', line=dict(color='#008b8b', width=2)))
        max_S = np.max(func(omega, Hs, Ts)[1:])

    fig.update_layout({"plot_bgcolor": "#e6e6e6"},title = dict(x=0.5, xref='paper', xanchor='center'), xaxis_title='freakency [rad/s]', yaxis_title='energy density [m²sec]',width=700, height=500, font=dict(family="serif",size=18,color="white"), margin=dict(t=60, b=0, l=0, r=0))
    fig.update_xaxes(zeroline=True, zerolinewidth=1.5, zerolinecolor='black', gridcolor='gray', range=(0,2))
    fig.update_yaxes(zeroline=True, zerolinewidth=1.5, zerolinecolor='black', gridcolor='gray')

    return fig,max_S

def plot_function_derivative(func):
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=omega, y=derivative(func, omega), mode='lines', line=dict(color='navy', width=2)))
    fig.update_layout(xaxis_title='Z', width=700, height=400,font=dict(family="Courier New, monospace",size=18,color="black"), margin=dict(t=30, b=0, l=0, r=0))
    fig.update_xaxes(zeroline=True, zerolinewidth=2, zerolinecolor='gray', gridcolor='silver')
    fig.update_yaxes(zeroline=True, zerolinewidth=2, zerolinecolor='gray', gridcolor='silver')
    return fig

def integral(func, xmin, xmax, h, Hv=None, Tv=None, Hs=None, Ts=None, U=None, X=None):
    result = 0
    if func == PM:
        for x in np.arange(xmin, xmax, h):
            result += (func(x) + func(x+h)) * h / 2
    elif func == ISSC:
        for x in np.arange(xmin, xmax, h):
            result += (func(x, Hv, Tv) + func(x+h, Hv, Tv)) * h / 2
    elif func == ITTC:
        for x in np.arange(xmin, xmax, h):
            result += (func(x, Hs) + func(x+h, Hs)) * h / 2
    elif func == JONSWAP_wind:
        for x in np.arange(xmin, xmax, h):
            result += (func(x, U, X) + func(x+h, U, X)) * h / 2
    elif func == JONSWAP_wave:
        for x in np.arange(xmin, xmax, h):
            result += (func(x, Hs, Ts) + func(x+h, Hs, Ts)) * h / 2
    elif func == Bretschneider_Mitsuyasu:
        for x in np.arange(xmin, xmax, h):
            result += (func(x, Hs, Ts) + func(x+h, Hs, Ts)) * h / 2

    return result

# ステップdωの重心を求める場合
def integral_1d_momentum(func, xmin, xmax, h):
    result = 0
    for x in np.arange(xmin, xmax, h):
        result += (func(x)*x + func(x+h)*x) * h / 2
    return result