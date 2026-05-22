# NSVQA-with-Reasoning - Neuro Symbolic Visual Question Answering Backend

A comprehensive Flask-based backend system for Neuro Symbolic Visual Question Answering (NSVQA) with advanced reasoning capabilities. This system combines multiple question-answering strategies (CFG-based, Regex-based, ML-based, and task-specific) with visual scene understanding, knowledge graphs, and emotion detection.

## Project Overview

NSVQA is an intelligent Visual Question Answering system designed to understand images, detect objects, build scene graphs, and answer complex questions about visual content. The system employs a hybrid reasoning engine that uses:

- **Context-Free Grammar (CFG)** for structured question parsing
- **Regex-based pattern matching** for flexible question matching
- **Machine Learning classifiers** for probabilistic reasoning
- **Knowledge Graphs** for semantic relationships
- **Scene Graph Construction** for spatial reasoning
- **Emotion Detection** for understanding subjects in images
- **Task-Based QA** for domain-specific query handling

### Key Features

- Multi-strategy hybrid QA engine with cascading fallback
- YOLO-based object detection and scene graph construction
- Portable, modular architecture for easy deployment
- RESTful API endpoints for all major operations
- Database integration for query history and user management
- Audio processing with speech-to-text (Whisper)
- Text-to-speech support for query responses
- Contact and blind user profile management

## Project Structure

```
├── main.py                    # Flask application entry point
├── config.py                  # Centralized configuration and path management
├── requirements.txt           # Python dependencies
│
├── Models/                    # Data models and database interactions
│   ├── config.py             # Database connection (SQL Server)
│   ├── BlindModel.py         # Blind user model
│   ├── AssistantModel.py     # Assistant user model
│   ├── ContactModel.py       # Contact management model
│   ├── BlindAssistantModel.py # Relationship model
│   ├── BlindQuery_models.py  # Query history model
│   ├── ContactPics.py        # Contact pictures storage
│   ├── cfg_models.py         # CFG model database operations
│   └── BlindModel.py         # Blind user database operations
│
├── Controllers/              # Core business logic and algorithms
│   ├── Answer_Engine.py      # Hybrid QA engine orchestration
│   ├── CFG_Answer.py         # Context-Free Grammar-based QA
│   ├── Regex_Answer.py       # Regex pattern-based QA
│   ├── ML_Answer.py          # Machine Learning-based QA
│   ├── AnswerHandler.py      # Main answer processing logic
│   ├── AnswerFunctions.py    # Utility functions for answers
│   ├── SceneGraphConfigure.py # Scene graph construction
│   ├── ObjectDetectionHandler.py # YOLO object detection wrapper
│   ├── PropertiesHandler.py  # Object property extraction (color, shape, emotion)
│   ├── ImageHandler.py       # Image loading and processing
│   ├── NlpHandler.py         # NLP preprocessing
│   ├── TaskQuestions.py      # Task-based question handling
│   ├── SceneHandler.py       # Scene understanding and reasoning
│   ├── scene_questions.py    # Scene-specific question templates
│   ├── ObjectAssociation.py  # Object relationship handling
│   ├── fahadSceneCheck.py    # Scene validation utility
│   ├── KnowledgeGraphs/      # Knowledge graph JSON files
│   └── grammer/              # CFG grammar files
│
├── Routes/                   # Flask blueprints and API endpoints
│   ├── answer_routes.py      # Main QA answer endpoint
│   ├── nlproutes.py          # NLP processing endpoints
│   ├── objectroutes.py       # Object detection endpoints
│   ├── emotionroute.py       # Emotion detection endpoints
│   ├── AudioRoutes.py        # Speech-to-text endpoints
│   ├── Blind_Assistant.py    # Blind user management endpoints
│   ├── BlindHistory.py       # Query history endpoints
│   ├── ContactPics.py        # Contact picture management endpoints
│   ├── DirectoryRoutes.py    # Static file serving
│   └── checkroute.py         # System health check
│
├── Services/                 # Utility services
│   ├── file_service.py       # File upload and storage
│   ├── image_service.py      # Image-related operations
│   └── emotion_services.py   # Emotion detection service
│
├── modelsNSVQA/              # Pre-trained ML models
│   ├── last.pt              # YOLOv8 object detection model
│   ├── relation_classifier_fahad.pkl # ML relation classifier
│   └── vectorizer_fahad.pkl # ML feature vectorizer
│
├── static/                   # Static assets
│   ├── ContactPics/         # Contact profile pictures
│   ├── AssistantPics/       # Assistant profile pictures
│   ├── AnswerPics/          # User-uploaded images for QA
│   ├── ImageAnsweringDemoPics/ # Sample images
│   └── answerreturned/      # Processed images with visualizations
│
├── uploads/                  # Temporary upload directory
└── __pycache__/             # Python cache (ignored in git)
```

## Requirements

### Python Version
- **Python 3.8+** (Python 3.10+ recommended)

### Core Dependencies

```
Flask==2.3.2                  # Web framework
Flask-CORS==4.0.0             # CORS support
ultralytics==8.0.100          # YOLO object detection
opencv-python==4.8.0.74       # Image processing
Pillow==10.0.0                # Image manipulation
nltk==3.8.1                   # NLP toolkit
numpy==1.24.3                 # Numerical computing
pandas==2.0.2                 # Data manipulation
scikit-learn==1.3.0           # ML utilities
joblib==1.3.0                 # ML model serialization
pyttsx3==2.90                 # Text-to-speech
deepface==0.0.79              # Emotion detection
openai-whisper==20230314      # Audio-to-text
pyodbc==4.0.39                # SQL Server driver
Werkzeug==2.3.6               # WSGI utilities
```

## Installation

### 1. Clone the Repository

```bash
git clone https://github.com/Bilal-73/NSVQA-with-Reasoning.git
cd NSVQA-with-Reasoning
```

### 2. Create Virtual Environment (Recommended)

```bash
python -m venv venv

# On Windows:
venv\Scripts\activate

# On Linux/macOS:
source venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Download NLTK Data

The system requires NLTK corpora for NLP operations:

```bash
python -m nltk.downloader punkt averaged_perceptron_tagger wordnet omw-1.4
```

### 5. Download Pre-trained Models

The `modelsNSVQA/` folder contains pre-trained models required for the system. Due to file size constraints, this folder is hosted on Google Drive and not included in the repository.

**Required Models** - Ensure these files are in `modelsNSVQA/`:
- `last.pt` - YOLOv8 object detection model (~100+ MB)
- `relation_classifier_fahad.pkl` - Relation classifier
- `vectorizer_fahad.pkl` - Feature vectorizer

**Download**: Get the `modelsNSVQA/` folder from Google Drive: [**Google Drive Link**](https://drive.google.com/drive/folders/1EqbpX7u_mlYzEOFdFNx1IPGCgY9igfcr?usp=sharing) *(Replace with actual Google Drive link)*

Extract it to the project root directory. The folder structure should be:
```
NSVQA-with-Reasoning/
├── modelsNSVQA/
│   ├── last.pt
│   ├── relation_classifier_fahad.pkl
│   └── vectorizer_fahad.pkl
├── main.py
└── ...
```

**Note**: The `modelsNSVQA/` folder is not pushed to GitHub.

## Environment Setup

### Database Configuration

Edit `Models/config.py` to configure SQL Server connection:

```python
# Example configuration for local SQL Server
pyodbc.connect(
    'DRIVER={ODBC Driver 17 for SQL Server};'
    'SERVER=localhost\\SQLEXPRESS;'
    'DATABASE=NSVQA_APP;'
    'Trusted_Connection=yes;'
)
```

For remote databases, modify `SERVER` and `DATABASE` values accordingly.

### Automatic Directory Creation

The `config.py` module automatically creates required directories on first run:
- `modelsNSVQA/` - Model storage
- `Controllers/grammer/` - Grammar files
- `Controllers/KnowledgeGraphs/` - Knowledge graph data
- `static/ContactPics/` - Contact images
- `static/AssistantPics/` - Assistant images
- `static/AnswerPics/` - Answer processing images
- `uploads/` - Temporary files

## How to Run

### Backend Server

Start the Flask development server:

```bash
python main.py
```

The API will be available at:
- **Base URL**: `http://localhost:5000`
- **Health Check**: `http://localhost:5000/` (returns "API is running!")

Server runs with:
- Host: `0.0.0.0` (accessible from any interface)
- Port: `5000`
- Debug Mode: `True` (auto-reload on code changes)
- Reloader: Disabled (set `use_reloader=False`)

### API Endpoints

#### Question Answering
- `POST /answers/getanswer/<blind_id>` - Get answer to a visual question

#### Object Detection
- `POST /images/detect` - Detect objects in uploaded image
- `POST /images/scene-graph` - Build scene graph from image

#### NLP Processing
- `POST /nlp/process` - Process text with NLP
- `POST /nlp/tokenize` - Tokenize text

#### Emotion Detection
- `POST /emotion/detect` - Detect emotion in image

#### Audio Processing
- `POST /audio/transcribe` - Convert speech-to-text

#### User Management
- `POST /users/create` - Create blind user profile
- `GET /users/<user_id>` - Get user profile
- `POST /contacts/add` - Add contact
- `GET /contacts/<contact_id>` - Get contact

#### Query History
- `GET /history/<user_id>` - Get query history

## Example Workflow

### 1. User Uploads Image with Question

```bash
curl -X POST http://localhost:5000/answers/getanswer/1 \
  -F "image=@photo.jpg" \
  -F "question=What color is the car?"
```

### 2. Backend Processing Pipeline

1. **Image Reception** - Receive and store uploaded image
2. **Object Detection** - YOLO detects all objects (car, person, tree, etc.)
3. **Property Extraction** - Extract color, shape, size, emotion for each object
4. **Scene Graph Construction** - Determine spatial relationships (on, left_of, near, etc.)
5. **Question Analysis** - Parse question using CFG/Regex/ML strategies
6. **Answer Generation** - Query knowledge graph with detected objects and relations
7. **Response** - Return answer with visualization (bounding boxes) and confidence

### 3. Hybrid QA Engine Flow

```
Question Input
    ↓
[1] Try CFG-based QA (most precise)
    ├─ If match found → Return answer ✓
    └─ If no match → Continue
    ↓
[2] Try Regex-based QA (pattern matching)
    ├─ If match found → Return answer ✓
    └─ If no match → Continue
    ↓
[3] Try ML-based QA (probabilistic)
    ├─ If confident → Return answer ✓
    └─ If low confidence → Continue
    ↓
[4] Return "Incorrect" (final fallback)
```

## Common Issues

### Issue: "ModuleNotFoundError: No module named 'ultralytics'"
**Solution**: Install YOLO dependencies:
```bash
pip install ultralytics
```

### Issue: "YOLO model file not found"
**Solution**: Ensure `modelsNSVQA/last.pt` exists or download YOLOv8:
```bash
python -c "from ultralytics import YOLO; YOLO('yolov8x.pt')"
```

### Issue: "Database connection failed"
**Solution**: 
- Verify SQL Server is running
- Check database credentials in `Models/config.py`
- Ensure database and tables are created

### Issue: "nltk_data not found"
**Solution**: Download NLTK resources:
```bash
python -m nltk.downloader punkt averaged_perceptron_tagger wordnet omw-1.4
```

### Issue: CORS errors
**Solution**: CORS is enabled via `flask_cors.CORS(app)` for all origins. If issues persist, check request headers.

## Notes for Contributors

### Architecture Principles

1. **Modularity** - Each component has single responsibility
2. **Portability** - All paths are relative via `config.py`
3. **Extensibility** - Easy to add new QA strategies or detection methods
4. **Robustness** - Graceful fallbacks for missing models/features

### Adding New QA Strategy

1. Create new file in `Controllers/` (e.g., `NewStrategy_Answer.py`)
2. Implement class with `answer(question)` method
3. Integrate into `Answer_Engine.py` hybrid flow
4. Add tests in `Controllers/test.py`

### Adding New API Endpoint

1. Create route function in `Routes/`
2. Use `@<blueprint>.route()` decorator
3. Register blueprint in `main.py`
4. Document in this README

### Path Management

All file paths should use the `config.py` module:

```python
from config import YOLO_MODEL_PATH, KG_DIR, STATIC_DIR
# Use: YOLO_MODEL_PATH, not hardcoded paths
```

### Testing

Test modules are in `Controllers/test.py`:

```bash
python -m pytest Controllers/test.py -v
```

## Deployment

### Production Setup

1. Use production WSGI server (Gunicorn/Waitress):
   ```bash
   pip install gunicorn
   gunicorn -w 4 -b 0.0.0.0:5000 main:app
   ```

2. Configure proper database credentials (use environment variables)

3. Set `debug=False` in `main.py`

4. Use HTTPS/SSL certificates

5. Set up proper logging and monitoring

### Docker Setup

Create `Dockerfile`:
```dockerfile
FROM python:3.10-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
CMD ["python", "main.py"]
```

Build and run:
```bash
docker build -t nsvqa-backend .
docker run -p 5000:5000 nsvqa-backend
```

## Performance Optimization

- **Object Detection**: YOLOv8x model is large; consider YOLOv8s for faster inference
- **Scene Graph**: Cache computed matrices for repeated images
- **ML Models**: Load once at startup (already implemented)
- **Knowledge Graphs**: Pre-index JSON for O(1) lookups

## License

[Specify License - e.g., MIT, Apache 2.0]

## Authors

- **Team** - Bilal-73 (GitHub)
- **Contributors** - Fahad, Azka, Daniyal

## Support & Contact

For issues, questions, or contributions:
- GitHub Issues: https://github.com/Bilal-73/NSVQA-with-Reasoning/issues
- Email: [acc.bilalimran@example.com]
