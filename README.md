# Python-Projects

A curated collection of practical Python mini-projects with video tutorial walkthroughs covering GUI networking, computer vision, utilities, and natural language processing. Now upgraded with enterprise **CI/CD pipelines**, **headless batch processing**, and **daily scheduled automation**.

### Video Tutorials Playlist
- **YouTube Playlist:** [Python Projects Playlist](http://bit.ly/pythonprojectsplaylist)

---

## Project Directory

| Project | Description | Interactive / Desktop | Batch Processing Mode | Core Technologies |
| :--- | :--- | :--- | :--- | :--- |
| [Python GUI Chat Application](./Python%20GUI%20Chat%20Application/) | Two-way desktop chat client and server using socket programming and multi-threading | GUI Client & Server | — | `tkinter`, `socket`, `threading`, `queue` |
| [QR Code Generator](./QR%20Code%20Generator/) | Generate standard and customized/logo-embedded QR codes | Standalone script | `batch_qr_generator.py` | `qrcode`, `Pillow`, `myqr` |
| [Contour Detection - OpenCV](./Contour%20Detection%20-%20OpenCV/) | Image thresholding and contour detection pipeline | Window preview | `batch_contour_processor.py` | `opencv-python` |
| [Edge Detection - OpenCV](./Edge%20Detection%20-%20OpenCV/) | Canny and Laplacian edge detection with Gaussian blur filtering | Window preview | `batch_edge_processor.py` | `opencv-python` |
| [Chatbot Application](./Chatbot%20Application/) | Conversational chatbot trained on corpus and custom dialogues | Jupyter Notebook | `train_chatbot.py` (CLI / Scheduled) | `chatterbot`, `jupyter` |

---

## Architecture & Workload Classification

### 1. CI/CD Pipeline ([`.github/workflows/ci.yml`](./.github/workflows/ci.yml))
Triggered on **every pull request and push to `main`**:
- Multi-version matrix validation across Python 3.10, 3.11, and 3.12.
- Syntax and fatal error validation with `flake8`.
- Automated headless compilation checks for all application scripts.
- Headless smoke testing for the QR code generator and batch image processors.

### 2. Daily Scheduled Audit ([`.github/workflows/daily-schedule.yml`](./.github/workflows/daily-schedule.yml))
Triggered via **cron schedule daily at 02:00 UTC**:
- Automates vulnerability scanning using `pip-audit` to detect published CVEs across project dependencies.

### 3. Batch Processing Modes
Headless processors designed for automated, non-interactive execution on directories of files:

```bash
# 1. Batch Edge Detection (Canny & Laplacian on a folder of images)
python "Edge Detection - OpenCV/batch_edge_processor.py" --input-dir "Edge Detection - OpenCV" --output-dir "./output/edges"

# 2. Batch Contour Detection & Statistical Analysis
python "Contour Detection - OpenCV/batch_contour_processor.py" --input-dir "Contour Detection - OpenCV" --output-dir "./output/contours"

# 3. Bulk QR Code Generation
python "QR Code Generator/batch_qr_generator.py" --items "https://github.com" "https://python.org" --output-dir "./output/qrs"

# 4. Headless Chatbot Training (Scheduled Re-training)
python "Chatbot Application/train_chatbot.py" --corpus chatterbot.corpus.english
```

---

## Quickstart

### 1. Clone the repository
```bash
git clone https://github.com/Amit1092tiwari/Python-Projects.git
cd Python-Projects
```

### 2. Set up a virtual environment (recommended)
```bash
python -m venv .venv

# On Windows:
.venv\Scripts\activate

# On Linux/macOS:
source .venv/bin/activate
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

---

## License & Attribution
Tutorials and projects created for the Hackers Realm video series.
