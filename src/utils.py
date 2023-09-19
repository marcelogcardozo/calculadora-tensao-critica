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

def set_chart(col_widget, ecr2_base: float, abaco: dict, gerar_abaco_completo: bool) -> None:
    
    fig = go.Figure()
        
    for ecr2, pontos in abaco.items():
        
        xs = [p.ler for p in pontos]
        ys = [p.pa for p in pontos]

        dash = 'dash' if (ecr2 == ecr2_base and gerar_abaco_completo) else None
        line_trace = go.Line(x=xs, y=ys, name=f"{ecr2:.2f}", line=dict(dash=dash))

        fig.add_trace(line_trace)

    fig.update_layout(
        title= 'Ábaco de Euler e Secante',
        xaxis_title="Le/r",
        yaxis_title="P/A",
        legend_title="Ecr2",
        yaxis_range=[0, 300.1],
        xaxis_range=[0, 200.1],
    )

    col_widget.plotly_chart(fig, use_container_width=True)


def set_table(col_widget, ecr2, abaco) -> None:

    data_for_dataframe = {
        'Le/r': [round(p.ler, 2) for p in abaco[ecr2]],
        'P/A': [round(p.pa, 2) for p in abaco[ecr2]],
    }

    col_widget.dataframe(data_for_dataframe)