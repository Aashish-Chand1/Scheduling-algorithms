import streamlit as st
import pandas as pd

from fcfs import fcfs
from sjf import sjf
from gantt import create_gantt_chart


# =========================================================
# PAGE CONFIGURATION
# =========================================================

st.set_page_config(
    page_title="CPU Scheduling Simulator",
    page_icon="⚙️",
    layout="wide"
)


# =========================================================
# CUSTOM CSS
# =========================================================

st.markdown(
    """
    <style>

    .main-title {
        font-size: 42px;
        font-weight: 700;
        text-align: center;
        margin-bottom: 5px;
    }

    .subtitle {
        text-align: center;
        font-size: 18px;
        color: #777;
        margin-bottom: 30px;
    }

    </style>
    """,
    unsafe_allow_html=True
)


# =========================================================
# TITLE
# =========================================================

st.markdown(
    '<div class="main-title">⚙️ CPU Scheduling Simulator</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="subtitle">'
    'FCFS and Non-Preemptive SJF Scheduling'
    '</div>',
    unsafe_allow_html=True
)


# =========================================================
# SIDEBAR
# =========================================================

st.sidebar.header("⚙️ Scheduling Configuration")


algorithm = st.sidebar.selectbox(
    "Select Scheduling Algorithm",
    [
        "FCFS",
        "SJF"
    ]
)


st.sidebar.markdown("---")


if algorithm == "FCFS":

    st.sidebar.info(
        """
        **FCFS - First Come First Serve**

        The process that arrives first
        gets executed first.

        FCFS is non-preemptive.
        """
    )

else:

    st.sidebar.info(
        """
        **SJF - Shortest Job First**

        Among the processes that have already
        arrived, the process with the shortest
        burst time is selected.

        This implementation is non-preemptive.
        """
    )


# =========================================================
# PROCESS INPUT
# =========================================================

st.header("📥 Enter Process Information")


number_of_processes = st.number_input(
    "Number of Processes",
    min_value=1,
    max_value=20,
    value=4,
    step=1
)


# =========================================================
# CREATE DEFAULT DATA
# =========================================================

default_data = pd.DataFrame(
    {
        "Process": [
            f"P{i + 1}"
            for i in range(number_of_processes)
        ],

        "Arrival Time": [
            0
            for _ in range(number_of_processes)
        ],

        "Burst Time": [
            1
            for _ in range(number_of_processes)
        ]
    }
)


# =========================================================
# USER INPUT TABLE
# =========================================================

st.write(
    "Enter the Arrival Time and Burst Time for each process:"
)


edited_data = st.data_editor(
    default_data,

    use_container_width=True,

    num_rows="fixed",

    hide_index=True,

    column_config={

        "Process": st.column_config.TextColumn(
            "Process",
            help="Unique process ID",
            required=True
        ),

        "Arrival Time": st.column_config.NumberColumn(
            "Arrival Time",
            help="Time at which the process arrives",
            min_value=0,
            step=1,
            required=True
        ),

        "Burst Time": st.column_config.NumberColumn(
            "Burst Time",
            help="CPU execution time required by process",
            min_value=1,
            step=1,
            required=True
        )
    }
)


# =========================================================
# RUN BUTTON
# =========================================================

st.markdown("")

run_button = st.button(
    "▶ Run Scheduling",
    type="primary",
    use_container_width=True
)


# =========================================================
# WHEN USER CLICKS RUN
# =========================================================

if run_button:

    # -----------------------------------------------------
    # Validate Process IDs
    # -----------------------------------------------------

    process_ids = (
        edited_data["Process"]
        .astype(str)
        .str.strip()
    )

    # Empty process ID
    if process_ids.eq("").any():

        st.error(
            "❌ Process IDs cannot be empty."
        )

        st.stop()


    # Duplicate process ID
    if process_ids.duplicated().any():

        st.error(
            "❌ Process IDs must be unique."
        )

        st.stop()


    # -----------------------------------------------------
    # Validate Arrival Time
    # -----------------------------------------------------

    if (
        edited_data["Arrival Time"]
        .isna()
        .any()
    ):

        st.error(
            "❌ Arrival Time cannot be empty."
        )

        st.stop()


    if (
        edited_data["Arrival Time"] < 0
    ).any():

        st.error(
            "❌ Arrival Time cannot be negative."
        )

        st.stop()


    # -----------------------------------------------------
    # Validate Burst Time
    # -----------------------------------------------------

    if (
        edited_data["Burst Time"]
        .isna()
        .any()
    ):

        st.error(
            "❌ Burst Time cannot be empty."
        )

        st.stop()


    if (
        edited_data["Burst Time"] <= 0
    ).any():

        st.error(
            "❌ Burst Time must be greater than 0."
        )

        st.stop()


    # -----------------------------------------------------
    # Convert input table into Python list
    # -----------------------------------------------------

    processes = []

    for _, row in edited_data.iterrows():

        processes.append(
            {
                "pid": str(row["Process"]).strip(),

                "arrival_time": int(
                    row["Arrival Time"]
                ),

                "burst_time": int(
                    row["Burst Time"]
                )
            }
        )


    # =====================================================
    # RUN FCFS
    # =====================================================

    if algorithm == "FCFS":

        result, gantt_data = fcfs(processes)


    # =====================================================
    # RUN SJF
    # =====================================================

    else:

        result, gantt_data = sjf(processes)


    # =====================================================
    # CREATE RESULT DATAFRAME
    # =====================================================

    result_df = pd.DataFrame(result)


    # =====================================================
    # CALCULATE TOTALS
    # =====================================================

    total_waiting_time = int(
        result_df["Waiting Time"].sum()
    )

    total_turnaround_time = int(
        result_df["Turnaround Time"].sum()
    )


    # =====================================================
    # CALCULATE AVERAGES
    # =====================================================

    number_of_processes = len(result_df)

    average_waiting_time = (
        total_waiting_time /
        number_of_processes
    )

    average_turnaround_time = (
        total_turnaround_time /
        number_of_processes
    )


    # =====================================================
    # RESULTS
    # =====================================================

    st.divider()

    st.header(
        f"📊 {algorithm} Scheduling Results"
    )


    # =====================================================
    # METRICS
    # =====================================================

    col1, col2, col3, col4 = st.columns(4)


    with col1:

        st.metric(
            "Total Waiting Time",
            total_waiting_time
        )


    with col2:

        st.metric(
            "Total Turnaround Time",
            total_turnaround_time
        )


    with col3:

        st.metric(
            "Average Waiting Time",
            f"{average_waiting_time:.2f}"
        )


    with col4:

        st.metric(
            "Average Turnaround Time",
            f"{average_turnaround_time:.2f}"
        )


    # =====================================================
    # RESULT TABLE
    # =====================================================

    st.subheader(
        "📋 Scheduling Result Table"
    )


    st.dataframe(
        result_df,
        use_container_width=True,
        hide_index=True
    )


    # =====================================================
    # GANTT CHART
    # =====================================================

    st.subheader(
        "📈 Gantt Chart"
    )


    fig = create_gantt_chart(
        gantt_data
    )


    st.plotly_chart(
        fig,
        use_container_width=True
    )


    # =====================================================
    # EXECUTION ORDER
    # =====================================================

    st.subheader(
        "🔄 Execution Order"
    )


    execution_order = " → ".join(
        item["process"]
        for item in gantt_data
        if item["process"] != "Idle"
    )


    st.success(
        execution_order
    )