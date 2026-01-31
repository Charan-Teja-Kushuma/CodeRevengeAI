# CodeRevengeAI 🚀

> **The Sentinel AI for Enterprise-Grade Code Auditing.**

**CodeRevengeAI** is an advanced, AI-powered code auditing tool designed to act as a rigorous "Sentinel" for your codebase. Unlike generic coding assistants, CodeRevengeAI focuses on **security**, **performance**, and **scalability**, providing critical feedback to elevate code to production standards.

Built with **FastAPI**, **TailwindCSS**, and powered by **Groq's LLaMA 3** models for ultra-fast inference.

![Project Status](https://img.shields.io/badge/Status-Active-emerald)
![Python](https://img.shields.io/badge/Backend-FastAPI-009688)
![AI](https://img.shields.io/badge/AI-Groq%20%2F%20LLaMA3-orange)

---

## ✨ Features

*   **🔍 Deep Technical Audit**: Scans for security vulnerabilities, anti-patterns, and performance bottlenecks.
*   **⚡ Ultra-Fast Analysis**: Powered by Groq's LPU inference engine for near-instant feedback.
*   **🛠️ Automated Refactoring**: Doesn't just find bugs—rewrites your code to be secure and optimized.
*   **📊 Insightful Metrics**: Categorizes issues by severity (Critical, High, Medium, Low).
*   **💎 Premium UI**: A "Glassmorphism" design with a responsive, dark-mode "Enterprise Grid" aesthetic.

## 🏗️ Architecture

*   **Frontend**: HTML5, Vanilla JavaScript, TailwindCSS (served statically via FastAPI).
*   **Backend**: Python 3.10+, FastAPI.
*   **AI Engine**: Groq API (LLaMA 3.3 70B Versatile).

## 🚀 Getting Started

### Prerequisites

*   Python 3.10 or higher
*   A [Groq API Key](https://console.groq.com/)

### Installation

1.  **Clone the repository**
    ```bash
    git clone https://github.com/Charan-Teja-Kushuma/CodeRevengeAI.git
    cd CodeRevengeAI
    ```

2.  **Set up the backend**
    ```bash
    cd backend
    python -m venv .venv
    # Windows
    .\.venv\Scripts\activate
    # Mac/Linux
    # source .venv/bin/activate
    
    pip install -r requirements.txt
    ```

3.  **Configure Environment Variables**
    Create a `.env` file in the `backend/` directory:
    ```ini
    GROQ_API_KEY=your_groq_api_key_here
    PORT=8000
    ```

### Running the App

1.  Start the server:
    ```bash
    # Inside the backend directory
    python main.py
    ```

2.  Open your browser and visit:
    *   **Landing Page:** `http://127.0.0.1:8000/`
    *   **App Interface:** `http://127.0.0.1:8000/app`

## 🤝 contributing

Contributions are welcome! Please fork the repository and create a pull request for any feature enhancements or bug fixes.

## 📄 License

This project is licensed under the MIT License.
