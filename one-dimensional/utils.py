from enum import Enum
import time
import tkinter as tk
from tkinter import ttk


class ReportTarget(Enum):
    CONSOLE = 0
    FILE = 1


class ProgramTimer:
    def __init__(self, targets=[ReportTarget.CONSOLE]):
        self.init_time = time.time()
        self.counter = time.time()
        self.start_time = None
        self.targets = targets

    def start(self):
        self.start_time = time.time()

    def get_time_since_start(self):
        return time.time() - self.start_time

    def get_time_since_init(self):
        return time.time() - self.init_time

    def get_counter_time(self):
        return time.time() - self.counter

    def reset_counter(self, step=None):
        print(f"Counter reset on {step}")
        self.counter = time.time()

    def report_step(self, step):

        report = self._generate_report(step)

        if ReportTarget.CONSOLE in self.targets:
            self._console_log_report(report)
        if ReportTarget.FILE in self.targets:
            self._file_log_report(report)

    def _generate_report(self, step: str) -> str:
        now_time = time.time()
        i_time = now_time - self.init_time
        s_time = now_time - (self.start_time or now_time)
        c_time = now_time - self.counter
        report = f"\nStep {step} report:"
        report += f"\nTime since init: {i_time:.2f}"
        report += f"\nTime since start: {s_time:.2f}"
        report += f"\nTime since counter reset: {c_time:.2f}\n"
        return report

    def _console_log_report(self, report: str):
        print(report)

    def _file_log_report(self, report: str):
        with open("./timer.log", "a") as f:
            print(f.write(report))


class ProgressBar:
    def __init__(self, master, max_count=100, current_count=0, bar_row=0, label_row=0, bar_col=0, label_col=3):
        self.max_count = max_count
        self.current_count = current_count
        self.master = master

        self.progress_bar = ttk.Progressbar(
            master, orient='horizontal', mode='determinate')
        self.progress_bar.grid(row=bar_row, column=bar_col, columnspan=3,
                               padx=10, pady=10, sticky='ew')

        percentage = self._get_current_percent()
        self.progress_label = tk.Label(
            master, text=f'{percentage}%')
        self.progress_label.grid(
            row=label_row, column=label_col, padx=10, pady=10, sticky='w')

        self._update()

    def _get_current_percent(self):
        return int((self.current_count / self.max_count) * 100)

    def update_progress(self, count=None, max_count=None):
        if max_count:
            self.max_count = max_count
        if count:
            self.current_count = count
        self._update()

    def increment_progress(self):
        self.current_count += 1
        self._update()

    def clear_progress(self):
        self.current_count = 0
        self._update()

    def _update(self):
        percent = self._get_current_percent()
        self.progress_bar['maximum'] = self.max_count
        self.progress_bar['value'] = self.current_count
        self.progress_label.config(text=f'{percent}%')
        self.master.update_idletasks()
