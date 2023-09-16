import plotly.graph_objects as go

def get_footer():
    style = """
    <style>
      # MainMenu {visibility: hidden;}
      footer {visibility: hidden;}
     .stApp { bottom: 0px; }
    </style>
    """
    return style

def get_about():

    about = """

    Feito por: Marcelo Cardozo  
    GitHub: https://github.com/marcelogcardozo  
    LinkedIn: https://www.linkedin.com/in/marcelogcardozo/  

    """
    return about


def set_chart(col_widget, abaco: dict) -> None:
    
    fig = go.Figure()
        
    for ecr2, pontos in abaco.items():
        
        xs = [p.ler for p in pontos]
        ys = [p.pa for p in pontos]

        line_trace = go.Line(x=xs, y=ys, name=f"{ecr2:.2f}")

        fig.add_trace(line_trace)

    fig.update_layout(
        title= 'Ábaco de Euler e Secante',
        xaxis_title="Le/r",
        yaxis_title="P/A",
        legend_title="Ecr2",
        yaxis_range=[0, 300],
        xaxis_range=[0, 200],
    )

    col_widget.plotly_chart(fig, use_container_width=True)


def set_table(col_widget, ecr2, abaco) -> None:

    data_for_dataframe = {
        'Le/r': [p.ler for p in abaco[ecr2]],
        'P/A': [p.pa for p in abaco[ecr2]],
    }

    col_widget.dataframe(data_for_dataframe)