def fcfs(processes):
    """
    FCFS - First Come First Serve Scheduling

    Processes are executed in the order of their
    arrival time.

    Parameters:
        processes: list of dictionaries
                   containing pid, arrival_time, burst_time

    Returns:
        result: scheduling result for every process
        gantt_data: data required for Gantt chart
    """

    # Sort processes according to arrival time
    # If arrival times are same, use process ID
    sorted_processes = sorted(
        processes,
        key=lambda p: (p["arrival_time"], p["pid"])
    )

    current_time = 0

    result = []
    gantt_data = []

    for process in sorted_processes:

        pid = process["pid"]
        arrival_time = process["arrival_time"]
        burst_time = process["burst_time"]

        # If CPU is idle because the next process
        # has not arrived yet
        if current_time < arrival_time:

            gantt_data.append({
                "process": "Idle",
                "start": current_time,
                "end": arrival_time
            })

            current_time = arrival_time

        # Process starts execution
        start_time = current_time

        # Process finishes execution
        completion_time = start_time + burst_time

        # Turnaround Time
        turnaround_time = completion_time - arrival_time

        # Waiting Time
        waiting_time = turnaround_time - burst_time

        result.append({
            "Process": pid,
            "Arrival Time": arrival_time,
            "Burst Time": burst_time,
            "Completion Time": completion_time,
            "Turnaround Time": turnaround_time,
            "Waiting Time": waiting_time
        })

        # Store information for Gantt chart
        gantt_data.append({
            "process": pid,
            "start": start_time,
            "end": completion_time
        })

        # Update CPU time
        current_time = completion_time

    return result, gantt_data