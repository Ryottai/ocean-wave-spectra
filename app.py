import streamlit as st
import numpy as np
import plotly.graph_objects as go

from utility import derivative, PM, ISSC, ITTC, plot_function, plot_function_derivative

########################################
# Utility Code
omega = np.linspace(0,2,200)
#########################################

st.title('Ocean-Wave Spectrum')

spectrum = st.selectbox('Choose a spectrum', ['None', 'P-M (Pierson-Moskowitz)', 'ISSC', 'ITTC', 'JONSWAP', 'Bretschneider'])

## PM
if spectrum == 'P-M (Pierson-Moskowitz)':
    st.header('P-M (Pierson-Moskowitz) Spectrum')

    st.subheader('Description')
    st.write('It is a sigmoid function with a characteristic "S"-shaped curve.')
    st.markdown(r'**$sigmoid(z)=\frac{1}{1+exp(-z)}$**')
    st.write('The output of the logistic (sigmoid) function is always between 0 and 1.')   

    st.subheader('Plot')
    PM_fig  = plot_function(PM, title='P-M Spectrum')
    st.plotly_chart(PM_fig)
    with st.expander('Plot Explanation'):
        st.write('- The logistic function saturates as the inputs become larger (either positive or negative).')
        st.write('- For large positive and negative values, the function gets asymptotically close to 1 and 0, respectively.')
        st.write('- When the function saturates, its gradient becomes very close to zero, which slows down learning.')

    st.subheader('Derivative')
    st.markdown(r'$sigmoid^{\prime}(z)=sigmoid(z)(1−sigmoid(z))$')
    st.text("")
    PM_der_fig = plot_function_derivative(PM, title='Derivative of the P-M Spectrum')
    st.plotly_chart(PM_der_fig)
    with st.expander('Plot Explanation'):
        st.write('Notice that the derivative of the logistic function gets very close to zero for large positive and negative inputs.')

    st.subheader('Pros')
    st.write('1. The logistic function introduces non-linearity into the network which allows it to solve more complex problems than linear activation functions.\n2. It is continuous and differentiable everywhere.\n3. Because its output is between 0 and 1, it is very common to use in the output layer in binary classification problems.')

    st.subheader('Cons')
    st.write("1. Limited Sensitivity\n- The logistic function saturates across most of its domain.\n- It is only sensitive to inputs around its midpoint 0.5.")
    st.write("2. Vanishing Gradients in Deep Neural Networks\n- Because the logistic function can get easily saturated with large inputs, its gradient gets very close to zero. This causes the gradients to get smaller and smaller as backpropagation progresses down to the lower layers of the network.\n- Eventually, the lower layers' weights receive very small updates and never converge to their optimal values.")

## ISSC
if spectrum == 'ISSC':
    st.header('ISSC')

    st.subheader('Description')
    st.write('The tanh function is also a sigmoid "S"-shaped function.')
    st.markdown(r'$tanh(z)=\frac{e^{z} - e^{-z}}{e^{z} + e^{-z}}$')
    st.write('The range of the tanh function is between -1 and 1.')

    st.subheader('Plot')
    Hv = st.slider('目視観測有義波高', 0., 15., 7.5, 0.1)
    Tv = st.slider('目視観測波周期', 0., 15., 7.5, 0.1)
    ISSC_fig = plot_function(ISSC, Hv=Hv, Tv=Tv, title='Hyperbolic Tangent Function')
    st.plotly_chart(ISSC_fig)
    with st.expander('Plot Explanation'):
        st.write('- The tanh function saturates as the inputs become larger (either positive or negative).')
        st.write('- For large positive and negative values, the function gets asymptotically close to 1 and -1, respectively.')
        st.write('- When the function saturates, its gradient becomes very close to zero, which slows down learning.')
    
    st.subheader('Pros')
    st.write("1. The tanh function introduces non-linearity into the network which allows it to solve more complex problems than linear activation functions.\n2. It is continuous, differentiable, and have non-zero derivatives everywhere.\n3. Because its output value ranges from -1 to 1, that makes each layer's output more or less centered around 0 at the beginning of training, whcih speed up convergence.")

    st.subheader('Cons')
    st.write("1. Limited Sensitivity\nThe tanh function saturates across most of its domain. It is only sensitive to inputs around its midpoint 0.")
    st.write("2. Vanishing Gradients in Deep Neural Networks\n- Because the tanh function can get easily saturated with large inputs, its gradient gets very close to zero.\n- This causes the gradients to get smaller and smaller as backpropagation progresses down to the lower layers of the network.\n- Eventually, the lower layers' weights receive very small updates and never converge to their optimal values.")

    st.markdown("**Note**: the vanishing gradient problem is less severe with the tanh function because it has a mean of 0 (instead of 0.5 like the logistic function).")

## ITTC
if spectrum == 'ITTC':
    st.header('ITTC')

    st.subheader('Description')
    st.write('It is a piecewise linear function with two linear pieces that will output the input directly is it is positive (identity function), otherwise, it will output zero.')
    st.markdown('$$ReLU(z) = max(0, z)$$')
    st.write('It has become the default activation function for many neural netowrks because it is easier to train and achieves better performance.')

    st.subheader('Plot')
    Hs = st.slider('有義波高', 0., 15., 7.5, 0.1)
    ITTC_fig = plot_function(ITTC, Hs=Hs, title = 'ITTC')
    st.plotly_chart(ITTC_fig)

    st.subheader('Pros')
    st.write("1. Computationally Efficient\n- The ReLU function does not require a lot of computation (Unlike the logistic and the tanh function which include an exponential function).\n- Because the ReLU function mimics a linear function when the input is positive, it is very easy to optimize.")
    st.write("2. Sparse Representaion\n- The ReLU function can output true zero values when the input is negative. This results in sparse weight matricies which help simplify the model architecure and speed up the learning process.\n- In contrast, the logistic and the tanh function always output non-zero values (sometimes the output is very close to zero, but not a true zero), which results in a dense representation.")
    st.write("3. Avoid Vanishing Gradients\n- The ReLU function does not saturate for positive values which helps avoid the vanishing gradient problem.\n- Switching from the logistic (sigmoid) activation function to ReLU has helped revolutionize the field of deep learning.")

    st.subheader('Cons')
    st.write("1. Dying ReLUs\n- A problem where ReLU neurons become inactive and only output 0 for any input.\n- This usually happens when the weighted sum of the inputs for all training examples is negative, coupled with a large learning rate.\n- This causes the ReLU function to only output zeros and gradient descent algorithm can not affect it anymore.\n- One of the explanations of this phenomenon is using symmetirc weight distributions to initialize weights and biases.")
    st.write("2. Not differentiable at 0.\n- An abrupt change in the slope causes gradient descent to bounce around.")
