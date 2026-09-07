import plotly.graph_objects as go


def compress_gantt_data(gantt_data):
    """
    Merge consecutive Gantt chart blocks belonging
    to the same process.
    """

    if not gantt_data:
        return []

    compressed = []

    for item in gantt_data:

        process = item["process"]
        start = item["start"]
        end = item["end"]

        if (
            compressed
            and compressed[-1]["process"] == process
            and compressed[-1]["end"] == start
        ):

            compressed[-1]["end"] = end

        else:

            compressed.append({
                "process": process,
                "start": start,
                "end": end
            })

    return compressed


def create_gantt_chart(gantt_data):
    """
    Creates a Plotly Gantt chart.
    """

    # Merge consecutive blocks
    gantt_data = compress_gantt_data(gantt_data)

    fig = go.Figure()

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

    process_colors = {}

    color_index = 0

    for item in gantt_data:

        process = item["process"]

        if process not in process_colors:

            if process == "Idle":

                process_colors[process] = "#808080"

            else:

                process_colors[process] = (
                    colors[color_index % len(colors)]
                )

                color_index += 1

    # -----------------------------------------------------
    # Create bars
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

    # -----------------------------------------------------
    # Layout
    # -----------------------------------------------------

    final_time = gantt_data[-1]["end"]

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