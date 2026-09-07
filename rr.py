from collections import deque


def round_robin(processes, time_quantum):
    """
    Round Robin CPU Scheduling.

    Parameters:
        processes:
            List of dictionaries containing:
            pid, arrival_time, burst_time

        time_quantum:
            Time quantum used by Round Robin.

    Returns:
        result:
            Scheduling results.

        gantt_data:
            Data used to create Gantt chart.
    """

    if time_quantum <= 0:
        raise ValueError(
            "Time quantum must be greater than 0."
        )

    processes = [p.copy() for p in processes]

    # Sort according to arrival time
    processes.sort(
        key=lambda p: (
            p["arrival_time"],
            p["pid"]
        )
    )

    n = len(processes)

    remaining = [
        p["burst_time"]
        for p in processes
    ]

    completion_times = [0] * n

    queue = deque()

    current_time = 0
    next_process = 0
    completed = 0

    gantt_data = []

    while completed < n:

        # -------------------------------------------------
        # If queue is empty, CPU is idle
        # -------------------------------------------------

        if not queue:

            if (
                next_process < n
                and current_time < processes[next_process]["arrival_time"]
            ):

                idle_start = current_time

                current_time = processes[
                    next_process
                ]["arrival_time"]

                gantt_data.append({
                    "process": "Idle",
                    "start": idle_start,
                    "end": current_time
                })

        # -------------------------------------------------
        # Add all processes that have arrived
        # -------------------------------------------------

        while (
            next_process < n
            and processes[next_process]["arrival_time"]
            <= current_time
        ):

            queue.append(next_process)

            next_process += 1

        # -------------------------------------------------
        # If still no process is available
        # -------------------------------------------------

        if not queue:
            continue

        # -------------------------------------------------
        # Select first process from ready queue
        # -------------------------------------------------

        current_process = queue.popleft()

        start_time = current_time

        execution_time = min(
            time_quantum,
            remaining[current_process]
        )

        # -------------------------------------------------
        # Execute process
        # -------------------------------------------------

        current_time += execution_time

        remaining[current_process] -= execution_time

        gantt_data.append({
            "process": processes[current_process]["pid"],
            "start": start_time,
            "end": current_time
        })

        # -------------------------------------------------
        # Add processes that arrived during execution
        # -------------------------------------------------

        while (
            next_process < n
            and processes[next_process]["arrival_time"]
            <= current_time
        ):

            queue.append(next_process)

            next_process += 1

        # -------------------------------------------------
        # Process completed
        # -------------------------------------------------

        if remaining[current_process] == 0:

            completion_times[current_process] = current_time

            completed += 1

        else:

            # Process did not finish.
            # Put it at the end of the ready queue.
            queue.append(current_process)

    # -----------------------------------------------------
    # Calculate CT, TAT and WT
    # -----------------------------------------------------

    result = []

    for i, process in enumerate(processes):

        arrival_time = process["arrival_time"]
        burst_time = process["burst_time"]

        completion_time = completion_times[i]

        turnaround_time = (
            completion_time - arrival_time
        )

        waiting_time = (
            turnaround_time - burst_time
        )

        result.append({
            "Process": process["pid"],
            "Arrival Time": arrival_time,
            "Burst Time": burst_time,
            "Completion Time": completion_time,
            "Turnaround Time": turnaround_time,
            "Waiting Time": waiting_time
        })

    # Return results in Process ID order
    result.sort(
        key=lambda x: x["Process"]
    )

    return result, gantt_data