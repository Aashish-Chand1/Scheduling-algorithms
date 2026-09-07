def srtn(processes):
    """
    SRTN - Shortest Remaining Time Next

    Preemptive CPU scheduling algorithm.

    At every unit of CPU time, the process with the
    shortest remaining burst time is selected.
    """

    processes = [p.copy() for p in processes]

    n = len(processes)

    remaining = [
        p["burst_time"]
        for p in processes
    ]

    completed = [False] * n

    completion_times = [0] * n

    current_time = 0
    completed_count = 0

    gantt_data = []

    while completed_count < n:

        # Find all processes that have arrived
        available = [
            i
            for i in range(n)
            if (
                not completed[i]
                and processes[i]["arrival_time"] <= current_time
                and remaining[i] > 0
            )
        ]

        # -------------------------------------------------
        # CPU IDLE
        # -------------------------------------------------

        if not available:

            next_arrival = min(
                processes[i]["arrival_time"]
                for i in range(n)
                if not completed[i]
            )

            gantt_data.append({
                "process": "Idle",
                "start": current_time,
                "end": next_arrival
            })

            current_time = next_arrival

            continue

        # -------------------------------------------------
        # Select shortest remaining time
        # -------------------------------------------------

        selected = min(
            available,
            key=lambda i: (
                remaining[i],
                processes[i]["arrival_time"],
                processes[i]["pid"]
            )
        )

        # Execute for ONE unit of time
        gantt_data.append({
            "process": processes[selected]["pid"],
            "start": current_time,
            "end": current_time + 1
        })

        remaining[selected] -= 1
        current_time += 1

        # -------------------------------------------------
        # Process completed
        # -------------------------------------------------

        if remaining[selected] == 0:

            completed[selected] = True

            completion_times[selected] = current_time

            completed_count += 1

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

    return result, gantt_data