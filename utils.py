import pandas as pd # Data-Frames

from plotly.offline import iplot, init_notebook_mode # Interactive graphs
import plotly.graph_objs as go 

import warnings # Ignore annoying warnings
warnings.filterwarnings('ignore')

init_notebook_mode(connected=True) # Required for Jupyter to produce in-line Plotly graphs

# Quantee colors
colors = {'blue': '#0b578e', 'light-blue': '#e6f2ff', 'dark-blue': '#264e86', 
          'intense-blue': '#119dff', 'yellow': '#f4b400'}

# =============================================================================
# Plotly Example: surface plot          
# =============================================================================
def plot_example_surface():
    
    # Read data from a csv
    z_data = pd.read_csv('https://raw.githubusercontent.com/plotly/datasets/master/api_docs/mt_bruno_elevation.csv')
    
    data = [
        dict(
            z=z_data.as_matrix(),
            colorscale='Viridis',
            contours=go.surface.Contours(
                z=go.surface.contours.Z(
                  show=True,
                  usecolormap=True,
                  highlightcolor="#42f462",
                  project=dict(z=True)
                )
            ),
            type='surface'
        )
    ]
    
    layout = dict(
        title='Mt Bruno Elevation',
        autosize=False,
        scene=dict(camera=dict(eye=dict(x=1.87, y=0.88, z=-0.64))),
        width=500,
        height=500,
        margin=dict(
            l=65,
            r=50,
            b=65,
            t=90
        )
    )
    fig = go.Figure(data=data, layout=layout)
    iplot(fig)

# =============================================================================
# Plotly Example: NN history of learning         
# =============================================================================
def plot_nn_history(history, metric_name, epoch_start=1):
    
    train_y = history[metric_name][epoch_start:]
    val_y = history['val_'+metric_name][epoch_start:]
    x = list(range(1,len(train_y)+1))
    
    trace1 = dict(
                y=train_y,
                x=x,        
                type='scatter',
                name='Train ' + metric_name
                )

    trace2 = dict(
                y=val_y,
                x=x,        
                type='scatter',
                name='Val ' + metric_name
                )
    
    layout = dict(
        xaxis=dict(title='Epochs',                                   
                   showgrid=False),
        yaxis=dict(title=metric_name),
        paper_bgcolor='white',
        plot_bgcolor='white',
    )
    
    # Produce plot
    fig = go.Figure(data=[trace1, trace2], layout=layout)
    iplot(fig)

# =============================================================================
# Plotly Example: surface plot for grid search          
# =============================================================================    
def plot_gs_surface(gs, x_axis, y_axis, z_axis='CV score',  
                    greater_is_better=True):
    
    # Get dict of parameter values
    p = gs.cv_results_['params']
    # Get k-fold scores
    score = gs.cv_results_['mean_test_score']
    # In case GridSearchCV multpiled scoring function by (-1) recover signs
    if not greater_is_better: 
        score = (-1) * score
        
    # As parameters are in dictionary we produce a 2D data-frame with results
    dct = {}
    for i, d in enumerate(p):
        v_x, v_y = d[x_axis], d[y_axis]
        if not v_x in dct.keys():
            dct[v_x] = {}
        dct[v_x].update({v_y: score[i]})
    df = pd.DataFrame(dct)
    # Axis values. Note that to maintain the equally spaced scale, the actual 
    # values of parameters will be in tick values
    x, y, z = list(range(df.columns.values.size)), list(range(df.index.values.size)), df.values.tolist()
    x_tick_text, y_tick_text = df.columns.values.tolist(), df.index.values.tolist()
     
    # Data for Plotly surface plot
    data = [
        dict(x=x,
             y=y,
             z=z,
             colorscale='Viridis',
             reversescale=True,
             showscale=False,
             type='surface'
        )
    ]
    
    # Layout settings
    layout = dict(
                autosize= False, 
                dragmode='turntable', 
                margin=dict(l=10, r=10, b=10, t=0),
                scene=dict(
                        xaxis=dict(title=x_axis, 
                                   ticktext=x_tick_text, 
                                   tickvals=x),
                        yaxis=dict(title=y_axis, 
                                   ticktext=y_tick_text, 
                                   tickvals=y),
                        zaxis=dict(title='5-fold CV MAE')
                        ),
                showlegend=False
            )
    
    # Produce plot
    fig = go.Figure(data=data, layout=layout)
    iplot(fig)
 
# =============================================================================
# Plotly Example: line plot for grid search      
# =============================================================================
def plot_gs_scatter(gs, x_axis, y_axis='CV score', greater_is_better=True):
    
    # Get dict of parameter values
    p = gs.cv_results_['params']
    # Get k-fold scores
    score = gs.cv_results_['mean_test_score']
    # In case GridSearchCV multpiled scoring function by (-1) recover signs
    if not greater_is_better: 
        score = (-1) * score

    x, y = list(range(len(p))), score
    x_tick_text = [d[x_axis] for d in p]

    data = [
        dict(
            x=x,
            y=y,        
            type='scatter'
        )
    ]

    layout = dict(
        xaxis=dict(title=x_axis,                                   
                   ticktext=x_tick_text, 
                   tickvals=x,
                   showgrid=False),
        yaxis=dict(title=y_axis),
        paper_bgcolor='white',
        plot_bgcolor='white',
    )
    
    # Produce plot
    fig = go.Figure(data=data, layout=layout)
    iplot(fig)