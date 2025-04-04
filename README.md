# AI-Powered Bug Detection OS

An operating system monitoring tool that uses AI to detect and report system anomalies and bugs in real-time.

## Features

- Real-time system metrics monitoring (CPU, Memory, Disk usage)
- AI-powered anomaly detection using Isolation Forest algorithm
- Bug reporting system with a modern UI
- Responsive dashboard with Tailwind CSS
- Real-time updates and alerts

## Prerequisites

- Python 3.7 or higher
- pip (Python package manager)

## Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd ai-bug-detection-os
```

2. Create a virtual environment (recommended):
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install the required packages:
```bash
pip install -r requirements.txt
```

## Running the Application

1. Start the Flask backend:
```bash
python app.py
```

2. Open your web browser and navigate to:
```
http://localhost:5000
```

## Project Structure

```
ai-bug-detection-os/
├── app.py              # Flask backend application
├── requirements.txt    # Python dependencies
├── static/
│   └── js/
│       └── main.js    # Frontend JavaScript
└── templates/
    └── index.html     # Main HTML template
```

## Technologies Used

- Backend:
  - Flask (Python web framework)
  - scikit-learn (AI/ML library)
  - psutil (System monitoring)

- Frontend:
  - HTML5
  - Tailwind CSS
  - JavaScript (ES6+)

## Contributing

1. Fork the repository
2. Create your feature branch
3. Commit your changes
4. Push to the branch
5. Create a new Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details. 