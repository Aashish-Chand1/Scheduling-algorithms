def sjf(processes):
    """
    SJF - Shortest Job First Scheduling

    This implementation is NON-PREEMPTIVE.

    At every decision point, among all processes
    that have already arrived, the process with the
    shortest burst time is selected.

    Parameters:
        processes: list of dictionaries
                   containing pid, arrival_time, burst_time

    Returns:
        result: scheduling result
        gantt_data: data required for Gantt chart
    """

    # Make a copy so that the original input is not modified
    processes = [p.copy() for p in processes]

    n = len(processes)

    # Keep track of completed processes
    completed = [False] * n

    current_time = 0
    completed_count = 0

    result = []
    gantt_data = []

    while completed_count < n:

        # Find processes that have arrived
        available_processes = []

        for i in range(n):

            if (
                not completed[i]
                and processes[i]["arrival_time"] <= current_time
            ):
                available_processes.append(i)

        # -------------------------------------------------
        # If no process is available, CPU remains idle
        # -------------------------------------------------

        if not available_processes:

            # Find the next process that will arrive
            next_process = min(
                (
                    i for i in range(n)
                    if not completed[i]
                ),
                key=lambda i: (
                    processes[i]["arrival_time"],
                    processes[i]["pid"]
                )
            )

            idle_start = current_time

            current_time = processes[next_process]["arrival_time"]

            # Add idle period to Gantt chart
            gantt_data.append({
                "process": "Idle",
                "start": idle_start,
                "end": current_time
            })

            continue

        # -------------------------------------------------
        # Select process with shortest burst time
        # -------------------------------------------------

        selected = min(
            available_processes,
            key=lambda i: (
                processes[i]["burst_time"],
                processes[i]["arrival_time"],
                processes[i]["pid"]
            )
        )

        process = processes[selected]

        pid = process["pid"]
        arrival_time = process["arrival_time"]
        burst_time = process["burst_time"]

        # Start execution
        start_time = current_time

        # Completion time
        completion_time = start_time + burst_time

        # Turnaround Time
        turnaround_time = completion_time - arrival_time

        # Waiting Time
        waiting_time = turnaround_time - burst_time

        # Store result
        result.append({
            "Process": pid,
            "Arrival Time": arrival_time,
            "Burst Time": burst_time,
            "Completion Time": completion_time,
            "Turnaround Time": turnaround_time,
            "Waiting Time": waiting_time
        })

        # Store Gantt chart information
        gantt_data.append({
            "process": pid,
            "start": start_time,
            "end": completion_time
        })

        # Update current CPU time
        current_time = completion_time

        # Mark process as completed
        completed[selected] = True
        completed_count += 1

    return result, gantt_data