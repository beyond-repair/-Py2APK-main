"""Graphical user interface for Py2APK (optional; requires tkinter)."""
from __future__ import annotations

import logging
import queue
from logging.handlers import QueueHandler, QueueListener
from pathlib import Path
from threading import Thread

import tkinter as tk
from tkinter import filedialog, messagebox, ttk

from ..builder import APKBuilder

logger = logging.getLogger(__name__)


class MainWindow(tk.Tk):
    """Main application window."""

    def __init__(self) -> None:
        super().__init__()
        self.title("Py2APK Converter (Claim-0)")
        self.geometry("800x600")

        self.style = ttk.Style()
        self.style.configure("TButton", padding=6)
        self.style.configure("TLabel", padding=6)

        self.log_queue: queue.Queue = queue.Queue()
        self.queue_handler = QueueHandler(self.log_queue)
        self.listener = QueueListener(self.log_queue, GUILogHandler(self))
        self.listener.start()

        self._create_widgets()

    def _create_widgets(self) -> None:
        self.project_path = tk.StringVar()
        ttk.Label(self, text="Python Project:").pack(pady=5)
        ttk.Entry(self, textvariable=self.project_path, width=50).pack(pady=5)
        ttk.Button(self, text="Browse", command=self._browse_project).pack(pady=5)

        self.log_text = tk.Text(self, wrap=tk.WORD)
        self.log_text.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        btn_frame = ttk.Frame(self)
        btn_frame.pack(pady=10)
        ttk.Button(btn_frame, text="Dry-run scaffold", command=self._start_build).pack(
            side=tk.LEFT, padx=5
        )
        ttk.Button(btn_frame, text="Exit", command=self.destroy).pack(side=tk.RIGHT, padx=5)

    def _browse_project(self) -> None:
        path = filedialog.askdirectory(title="Select Python Project")
        if path:
            self.project_path.set(path)

    def _log_message(self, message: str) -> None:
        self.log_text.insert(tk.END, message + "\n")
        self.log_text.see(tk.END)
        self.update_idletasks()

    def _start_build(self) -> None:
        def build_thread() -> None:
            try:
                project_path = Path(self.project_path.get())
                output_dir = Path.cwd() / "dist"
                builder = APKBuilder(project_path, output_dir, require_sdk=False)
                if builder.create_android_project(dry_run=True):
                    self._log_message(f"Dry-run scaffold written to {output_dir}")
                    messagebox.showinfo(
                        "Done",
                        "Scaffold written (Claim-0). No APK was built.",
                    )
                else:
                    messagebox.showerror("Error", "Scaffold failed - check logs")
            except Exception as e:
                self._log_message(f"Error: {e}")

        Thread(target=build_thread, daemon=True).start()

    def destroy(self) -> None:  # type: ignore[override]
        self.listener.stop()
        super().destroy()


class GUILogHandler(logging.Handler):
    """Redirect logs to the GUI text widget."""

    def __init__(self, gui: MainWindow) -> None:
        super().__init__()
        self.gui = gui

    def emit(self, record: logging.LogRecord) -> None:
        msg = self.format(record)
        self.gui._log_message(msg)


def launch_gui() -> None:
    """Start the graphical interface."""
    window = MainWindow()
    root_logger = logging.getLogger()
    root_logger.addHandler(window.queue_handler)
    window.mainloop()
