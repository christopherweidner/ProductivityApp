# Deep Work Agent 🧠

> A ruthless, AI-powered productivity enforcer for macOS.

The **Deep Work Agent** is a desktop application designed to enforce strict focus sessions. It combines a **Pomodoro timer** with **active monitoring** to detect and block distractions in real-time. If you stray from productive work, the agent intervenes—closing tabs, sending alerts, and keeping you accountable.

![License](https://img.shields.io/badge/license-MIT-blue.svg)
![Platform](https://img.shields.io/badge/platform-macOS-lightgrey.svg)
![Status](https://img.shields.io/badge/status-active-green.svg)

---

## ✨ Features

- **🍅 Pomodoro Workflow**: Automatically cycles between **25-minute Deep Work** sessions and **5-minute Breaks**.
- **🛡️ Active Distraction Blocking**: Monitors your active window and browser tabs. If "Wasteful" activity is detected during a work session, it is immediately terminated.
- **🤖 Intelligent Classification**: Uses heuristics (and optional LLM integration) to classify apps and websites as "Productive" or "Wasteful".
- **📊 Activity Dashboard**: A minimalist React frontend to visualize your productivity, view logs, and control the agent.
- **🔔 Modal Alerts**: Uses system-level modal dialogs to ensure you never miss a warning.
- **🍏 macOS Native Control**: Leverages AppleScript for seamless OS integration (closing tabs, checking windows).

## 🛠️ Tech Stack

- **Backend**: Python (Flask)
- **Frontend**: React (Vite) + Tailwind CSS
- **OS Integration**: AppleScript (`osascript`)
- **Data**: CSV Logging & JSON State Management

## 🚀 Getting Started

### Prerequisites

- **macOS** (Required for AppleScript integration)
- **Python 3.8+**
- **Node.js & npm**

### Installation

1.  **Clone the repository**:
    ```bash
    git clone https://github.com/christopherweidner/ProductivityApp.git
    cd ProductivityApp
    ```

2.  **Run the Startup Script**:
    The included script handles setting up the Python virtual environment, installing dependencies, and launching both the backend and frontend.
    ```bash
    ./start_app.sh
    ```

    *Note: The first run may take a moment to install `node_modules` and python packages.*

## 🕹️ Usage

1.  Open the app in your browser (automatically opens at `http://localhost:5173`).
2.  Click **Start Focus** to begin a session.
3.  **Work Phase (25m)**: Focus on your task. If you open a distraction (e.g., social media, entertainment sites), the agent will alert you and close the tab.
4.  **Break Phase (5m)**: The timer turns green. You are free to browse the web or relax.
5.  Check the **Analytics** card to see your Productive vs. Wasteful blocks.

## 📂 Project Structure

```
.
├── deep_work_agent.py      # Main agent logic (monitoring & intervention)
├── server.py               # Flask API for UI communication
├── start_app.sh            # One-click startup script
├── execution/              # Modular scripts for OS actions
│   ├── close_tab.py        # Closes browser tabs via AppleScript
│   ├── get_active_window.py # Detects current app/window
│   └── ...
├── frontend/               # React Dashboard
│   ├── src/
│   │   ├── App.jsx         # Main UI Component
│   │   └── index.css       # Tailwind Styles
│   └── ...
└── activity_log.csv        # Local log of all activity
```

## 🛡️ Privacy

This application runs entirely **locally** on your machine. Activity logs are stored in `activity_log.csv` and are not sent to any external server.

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
