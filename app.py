import streamlit as st
import pandas as pd

from fcfs import fcfs
from sjf import sjf
from srtn import srtn
from rr import round_robin
from gantt import create_gantt_chart, compress_gantt_data


# =========================================================
# PAGE CONFIGURATION
# =========================================================

st.set_page_config(
    page_title="CPU Scheduling Simulator",
    page_icon="⚙️",
    layout="wide"
)


# =========================================================
# TITLE
# =========================================================

st.markdown(
    """
    <h1 style="text-align:center;">
        ⚙️ CPU Scheduling Simulator
    </h1>
    """,
    unsafe_allow_html=True
)

st.markdown(
    """
    <p style="text-align:center;">
        FCFS • SJF • SRTN • Round Robin
    </p>
    """,
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
        "SJF",
        "SRTN",
        "Round Robin"
    ]
)


# =========================================================
# ALGORITHM INFORMATION
# =========================================================

if algorithm == "FCFS":

    st.sidebar.info(
        """
        **FCFS**

        First Come First Serve.

        The process that arrives first
        is executed first.

        Non-preemptive.
        """
    )


elif algorithm == "SJF":

    st.sidebar.info(
        """
        **SJF**

        Shortest Job First.

        Among the processes that have
        already arrived, the process
        with the shortest burst time
        is selected.

        Non-preemptive.
        """
    )


elif algorithm == "SRTN":

    st.sidebar.info(
        """
        **SRTN**

        Shortest Remaining Time Next.

        The process with the shortest
        remaining execution time is
        selected.

        Preemptive.
        """
    )


elif algorithm == "Round Robin":

    st.sidebar.info(
        """
        **Round Robin**

        Each process gets a fixed
        amount of CPU time called
        the Time Quantum.

        Preemptive.
        """
    )


# =========================================================
# TIME QUANTUM FOR ROUND ROBIN
# =========================================================

time_quantum = 2

if algorithm == "Round Robin":

    time_quantum = st.sidebar.number_input(
        "Time Quantum",
        min_value=1,
        value=2,
        step=1
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
# DEFAULT INPUT DATA
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
# INPUT TABLE
# =========================================================

st.write(
    "Enter the Arrival Time and Burst Time:"
)


edited_data = st.data_editor(

    default_data,

    use_container_width=True,

    num_rows="fixed",

    hide_index=True,

    column_config={

        "Process": st.column_config.TextColumn(
            "Process",
            help="Unique Process ID",
            required=True
        ),

        "Arrival Time": st.column_config.NumberColumn(
            "Arrival Time",
            help="Time at which process arrives",
            min_value=0,
            step=1,
            required=True
        ),

        "Burst Time": st.column_config.NumberColumn(
            "Burst Time",
            help="CPU execution time",
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
# RUN ALGORITHM
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

    if process_ids.eq("").any():

        st.error(
            "❌ Process IDs cannot be empty."
        )

        st.stop()


    if process_ids.duplicated().any():

        st.error(
            "❌ Process IDs must be unique."
        )

        st.stop()


    # -----------------------------------------------------
    # Validate Arrival Time
    # -----------------------------------------------------

    if edited_data["Arrival Time"].isna().any():

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

    if edited_data["Burst Time"].isna().any():

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
    # Convert input to Python list
    # -----------------------------------------------------

    processes = []

    for _, row in edited_data.iterrows():

        processes.append(
            {
                "pid": str(
                    row["Process"]
                ).strip(),

                "arrival_time": int(
                    row["Arrival Time"]
                ),

                "burst_time": int(
                    row["Burst Time"]
                )
            }
        )


    # =====================================================
    # SELECT ALGORITHM
    # =====================================================

    if algorithm == "FCFS":

        result, gantt_data = fcfs(
            processes
        )


    elif algorithm == "SJF":

        result, gantt_data = sjf(
            processes
        )


    elif algorithm == "SRTN":

        result, gantt_data = srtn(
            processes
        )


    elif algorithm == "Round Robin":

        result, gantt_data = round_robin(
            processes,
            int(time_quantum)
        )


    # =====================================================
    # DATAFRAME
    # =====================================================

    result_df = pd.DataFrame(result)


    # -----------------------------------------------------
    # Sort result according to original Process ID
    # -----------------------------------------------------

    original_order = {
        process["pid"]: i
        for i, process in enumerate(processes)
    }

    result_df["_order"] = result_df["Process"].map(
        original_order
    )

    result_df = (
        result_df
        .sort_values("_order")
        .drop(columns="_order")
        .reset_index(drop=True)
    )


    # =====================================================
    # TOTALS
    # =====================================================

    total_waiting_time = int(
        result_df["Waiting Time"].sum()
    )

    total_turnaround_time = int(
        result_df["Turnaround Time"].sum()
    )


    # =====================================================
    # AVERAGES
    # =====================================================

    process_count = len(result_df)

    average_waiting_time = (
        total_waiting_time / process_count
    )

    average_turnaround_time = (
        total_turnaround_time / process_count
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


    compressed_gantt = compress_gantt_data(
        gantt_data
    )


    execution_order = " → ".join(
        item["process"]
        for item in compressed_gantt
    )


    st.success(
        execution_order
    )