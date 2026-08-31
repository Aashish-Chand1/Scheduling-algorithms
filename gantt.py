import plotly.graph_objects as go


def create_gantt_chart(gantt_data):
    """
    Creates a Gantt chart for CPU scheduling.

    Parameters:
        gantt_data:
            [
                {
                    "process": "P1",
                    "start": 0,
                    "end": 5
                },
                ...
            ]

    Returns:
        Plotly Figure
    """

    fig = go.Figure()

    # Colors for processes
    colors = [
        "#636EFA",
        "#EF553B",
        "#00CC96",
        "#AB63FA",
        "#FFA15A",
        "#19D3F3",
        "#FF6692",
        "#B6E880",
        "#FF97FF",
        "#FECB52"
    ]

    # Create a color for each process
    process_colors = {}

    color_index = 0

    for item in gantt_data:

        process = item["process"]

        if process not in process_colors:

            if process == "Idle":
                process_colors[process] = "#808080"

            else:
                process_colors[process] = colors[
                    color_index % len(colors)
                ]

                color_index += 1

    # -----------------------------------------------------
    # Add bars
    # -----------------------------------------------------

    for item in gantt_data:

        process = item["process"]

        start = item["start"]
        end = item["end"]

        duration = end - start

        fig.add_trace(
            go.Bar(
                x=[duration],
                y=["CPU"],
                base=[start],
                orientation="h",

                marker=dict(
                    color=process_colors[process],
                    line=dict(
                        color="white",
                        width=2
                    )
                ),

                text=[process],
                textposition="inside",

                hovertemplate=(
                    "<b>%{text}</b><br>"
                    f"Start Time: {start}<br>"
                    f"End Time: {end}<br>"
                    f"Duration: {duration}"
                    "<extra></extra>"
                ),

                showlegend=False
            )
        )

    # Final CPU time
    final_time = gantt_data[-1]["end"]

    # -----------------------------------------------------
    # Layout
    # -----------------------------------------------------

    fig.update_layout(
        title={
            "text": "CPU Scheduling Gantt Chart",
            "x": 0.5,
            "xanchor": "center"
        },

        xaxis=dict(
            title="Time",
            range=[0, final_time],
            dtick=1,
            showgrid=True,
            zeroline=True
        ),

        yaxis=dict(
            title="",
            showticklabels=False,
            fixedrange=True
        ),

        barmode="overlay",

        height=300,

        margin=dict(
            l=50,
            r=50,
            t=80,
            b=60
        )
    )

    return fig