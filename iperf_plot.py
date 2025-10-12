#!/usr/bin/env python3
import sys
import re
import platform
import time
import pandas as pd
import numpy as np
import plotly.express as px

def load_runs_from_csv(path):
    df = pd.read_csv(path, engine="python", encoding="utf-8-sig", skip_blank_lines=True)

    if df.empty:
        raise ValueError(f"{path}: no data rows found")

    row_vals = df.iloc[0].dropna().astype(str).tolist()
    joined = " ".join(row_vals)

    nums = re.findall(r"-?\d+(?:\.\d+)?", joined)
    if len(nums) < 7:
        raise ValueError(f"{path}: expected at least 7 numeric values, got {nums}")

    values = [float(x) for x in nums]
    distance = values[0]
    runs = values[1:6]
    avg = values[6]
    return distance, runs, avg

def main():
    if len(sys.argv) != 6:
        print("Usage: python iperf_plot.py 1 3 5 6 10")
        sys.exit(1)

    distances = [str(d) for d in sys.argv[1:6]]

    print(f"[{time.strftime('%Y-%m-%d %H:%M:%S')}] Running on {platform.platform()}")
    print(f"Preparing plots for distances (m): {', '.join(distances)}")

    for d in distances:
        tcp_file = f"iperf_tcp_{d}m.csv"
        udp_file = f"iperf_udp_{d}m.csv"

        dist_tcp, tcp_runs, tcp_avg = load_runs_from_csv(tcp_file)
        dist_udp, udp_runs, udp_avg = load_runs_from_csv(udp_file)

        if int(float(dist_tcp)) != int(float(dist_udp)):
            print(f"Warning: distance mismatch between {tcp_file} and {udp_file}")

        run_labels = [f"Run{i}" for i in range(1, 6)]

        df = pd.DataFrame({
            "Run": run_labels * 2,
            "Throughput (Mbps)": tcp_runs + udp_runs,
            "Protocol": ["TCP"] * 5 + ["UDP"] * 5,
        })

        title = f"TCP & UDP Throughput at {d}m Distance"
        fig = px.line(
            df,
            x="Run",
            y="Throughput (Mbps)",
            color="Protocol",
            markers=True,
            title=title,
        )
        fig.update_layout(
            legend_title_text="",
            xaxis_title="Test Runs",
            yaxis_title="Throughput (Mbps)",
        )

        out_html = f"throughput_{d}m.html"
        fig.write_html(out_html)
        print(f"Saved: {out_html}")

    print("All plots generated.")

if __name__ == "__main__":
    main()