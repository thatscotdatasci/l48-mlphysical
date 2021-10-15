import numpy as np
import streamlit as st
import scipy.stats as stat
import plotly.graph_objects as go

from streamlit_app.abstract_classes.abstract_navigation_radio import AbstractNavigationRadio


class Introduction(AbstractNavigationRadio):

    name = "1. Introduction"

    def _action(self):
        st.markdown("""
        ## 1.1 Bernoulli Trial

        ### Setup

        """)

        # Create multi-columns layout
        col1, col2 = st.columns((3,2))

        size = int(col2.number_input("Number of points to draw from each distribution", min_value=0, value=10000, step=1))

        bias = col2.number_input("Specify the true bias", min_value=0.0, max_value=1.0, value=0.3)

        true_dist = stat.bernoulli(bias)
        x = true_dist.rvs(size=size)

        fig = go.Figure()
        fig.add_trace(go.Histogram(x=x, nbinsx=10))
        fig.update_layout(
            title={
                'text': "Draws from the True Distribution",
                'y':0.9,
                'x':0.5,
                'xanchor': 'center',
                'yanchor': 'top'
            },
            xaxis_title="Theta",
            yaxis_title='Count',
        )
        col1.plotly_chart(fig, use_container_width=True)

        """
        ### Prior Specification

        We'll be using a beta prior - specify parameters alpha and beta.
        """
        a = st.number_input("Alpha", min_value=0, value=30, step=1)
        b = st.number_input("Beta", min_value=0, value=30, step=1)

        prior_dist = stat.beta(a, b)
        prior = prior_dist.rvs(size=size)

        fig = go.Figure()
        fig.add_trace(go.Histogram(x=prior, nbinsx=10))
        st.plotly_chart(fig, use_container_width=True)

        """
        ### Posterior Distribution

        """

        param_range = np.linspace(0,1,100)
        index = np.arange(0,size,100)
        fig = go.Figure()

        error = []
        for i in index:
            post_dist = stat.beta(np.sum(x[:i])+a,i-np.sum(x[:i])+b)
            post_pdf = post_dist.pdf(param_range)
            fig.add_trace(go.Scatter(x=param_range, y=post_pdf))
            error.append((i,np.abs(post_dist.mean()-bias)))
            
        post_dist = stat.beta(np.sum(x)+a,size-np.sum(x)+b)
        post_pdf = post_dist.pdf(param_range)


        fig.add_trace(go.Scatter(x=param_range, y=post_pdf))
        st.plotly_chart(fig, use_container_width=True)

        post_dist.mean()


        """
        Impact of iterations
        """

        iterations = int(st.number_input("Number of iterations to perform", min_value=100, max_value=10000, value=100, step=100))
        map_preds = []

        for i in np.arange(iterations):
            x = true_dist.rvs(size=size)
            map_preds.append((stat.beta(np.sum(x)+a,size-np.sum(x)+b).mean()))

        fig = go.Figure()
        fig.add_trace(go.Histogram(x=map_preds))
        st.plotly_chart(fig, use_container_width=True)
