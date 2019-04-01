import pandas as pd # Data-Frames

# Quantee colors
colors = {'blue': '#0b578e', 'light-blue': '#e6f2ff', 'dark-blue': '#264e86', 
          'intense-blue': '#119dff', 'yellow': '#f4b400'}

# =============================================================================
# Plotly Example: choropleth map for Dash          
# =============================================================================    
def dash_choropleth_map(df):
      
    data = [
        dict(
            type='choropleth',
            colorscale='Viridis',
            locations=df.country,
            z=df.spot_rate,
            text=pd.Series(['{0:.2f}%<br>{1}'.format(spot * 100, country) for spot, country in zip(df.spot_rate,df.country)], index = df.index),
            hoverinfo = 'text',
            locationmode='country names',
            marker=dict(line=dict(color='white', width=2)),
            colorbar=dict(tickformat='.2%')
        )
    ]

    layout = dict(
        geo=dict(
            scope='europe'
        ),
        margin=dict(l=10, r=10, t=0, b=0),
    )
        
    return dict(data=data, layout=layout)

# =============================================================================
# Plotly Example: surface plot for Dash          
# =============================================================================  
def dash_surface(df):
    
    df = df[df.country == 'United Kingdom']
    terms = df.term.unique()
    dates = df.date.unique()
    spots = [df[df.date == date].spot_rate for date in dates]
    
    # Change date format
    dates = pd.to_datetime([str(date) for date in dates])
    dates = dates.strftime('%b %Y')

    scl = [[0.0, colors['blue']], [1.0, colors['intense-blue']]]
    
    data = [
        dict(x=terms,
             y=dates,
             z=spots,
             colorscale=scl,
             name='y',
             showscale=False,
             type='surface'
        )
    ]
    
    layout = dict(
                autosize= False, 
                dragmode='turntable', 
                margin=dict(l=10, r=10, b=10, t=0),
                scene=dict(
                        camera=dict(
                                center=dict(x=0,y=0,z=-0.2),
                                eye=dict(x=-1.35,y=-1.4,z=0.2)
                                ),
                        xaxis=dict(title='Term'),
                        yaxis=dict(title=''),
                        zaxis=dict(title='Yield',tickformat='.2%')
                        ),
                showlegend=False
            )

    return dict(data=data, layout=layout)