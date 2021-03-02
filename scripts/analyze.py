#!/usr/bin/env python3
from typing import List, NamedTuple
import sys

import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import typer


class DataPoint(NamedTuple):
    timestamp: float
    total_recv: int
    recv: int
    sent: int
    rssi: int


def parse_line(line: str) -> DataPoint:
    """Parse one line of valid NRF_LOG_XXXX output to a DataPoint
    Raises ValueError if parse failed.
    """
    l = line.strip().split("\t")
    if len(l) == 2:  # valid  line, e.g. "123456.789\t<info> app: 108800 1700/1700 202"
        timestamp, log_line = l
        lst = log_line.split()
        if len(lst) == 5:  # valid log line, e.g. "<info> app: 108800 1700/1700 202"
            total_recv = int(lst[2])
            recv, sent = map(int, lst[3].split("/"))
            rssi = int(lst[4])
            return DataPoint(
                timestamp=float(timestamp),
                total_recv=total_recv,
                recv=recv,
                sent=sent,
                rssi=rssi,
            )

    raise ValueError("Invalid input: %s" % line)


def test_parse_line() -> None:
    s = "123456.789\t<info> app: 108800 1700/1700 202"
    pt = parse_line(s)
    assert pt.timestamp == 123456.789
    assert pt.total_recv == 108800
    assert pt.recv == 1700
    assert pt.sent == 1700
    assert pt.rssi == 202
    print("test_parse_line passed")


# test_parse_line()


def parse_file(fname: str):
    """Parse given file to DataFrame"""
    with open(fname, "r") as fd:
        raw_data = fd.read().strip()

    pts = []
    for line in raw_data.split("\n"):
        try:
            pt = parse_line(line)
        except ValueError:  # ignore malformed lines
            #             print(f"Ignoring malformed line: {line}", file=sys.stderr)
            continue
        pts.append(pt)

    pts = pts[1:]  # discard first one
    df = pd.DataFrame(pts)
    df.timestamp -= df.timestamp[0]  # normalize timestamp
    return df


def plot_total_recv(df, ax=None):
    if not ax:
        _, ax = plt.subplots()
    ax.plot(df.timestamp, df.total_recv)
    ax.set_ylabel("Total # of recv'ed bytes")
    ax.set_xlabel("Time (s)")


def get_segments(df: pd.DataFrame) -> List[int]:
    """There may be disconnects in the recording where the total recv
    counter resets. Find those segments and return a list of indices splitting them.
    """
    tr_diff = df.total_recv.diff()
    zero_starts = list(tr_diff.index.values[tr_diff < 0])
    return zero_starts


def plot_throughput(df, ax=None):
    if not ax:
        _, ax = plt.subplots()
    tp = df.total_recv.diff()[1:] / df.timestamp.diff()[1:]
    avg = tp.mean()
    ax.plot(df.timestamp[1:], tp, label=f"Avg. Throughput: {avg:.2f}")
    ax.set_ylabel("Throughput (bytes/s)")
    ax.set_xlabel("Time (s)")
    ax.legend()


def plot_col(df, col, title, ax=None):
    if not ax:
        _, ax = plt.subplots()
    avg = df[col].mean()
    ax.plot(df.timestamp, df.rssi, label=f"Avg. {col}: {avg:.2f}")
    ax.set_ylabel(title)
    ax.set_xlabel("Time (s)")
    ax.legend()


def plot_one_file(ifname: str, ofname: str = ""):
    df = parse_file(ifname)
    zero_starts = get_segments(df)

    fig, axes = plt.subplots(2, 1, figsize=(9, 7))
    i = 0
    for j in zero_starts:
        plot_throughput(df[i:j], ax=axes[0])
        plot_col(df[i:j], col="rssi", title="RSSI", ax=axes[1])
        i = j

    plot_throughput(df[i:], ax=axes[0])
    plot_col(df[i:], col="rssi", title="RSSI", ax=axes[1])
    if not ofname:
        ofname = ifname.rsplit(".", 1)[0] + ".png"
    plt.savefig(ofname)
    plt.show()


if __name__ == "__main__":
    typer.run(plot_one_file)
