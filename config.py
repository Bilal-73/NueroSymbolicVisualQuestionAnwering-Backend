"""
Project configuration module for portable path handling.
All paths are relative to the project root directory.
"""
from pathlib import Path
import os

# Get the project root directory (where this file is located)
PROJECT_ROOT = Path(__file__).resolve().parent

# Model paths
MODELS_DIR = PROJECT_ROOT / "modelsNSVQA"
YOLO_MODEL_PATH = MODELS_DIR / "last.pt"
RELATION_CLASSIFIER_PATH = MODELS_DIR / "relation_classifier_fahad.pkl"
VECTORIZER_PATH = MODELS_DIR / "vectorizer_fahad.pkl"

# Grammar and Knowledge Graph paths
GRAMMER_DIR = PROJECT_ROOT / "Controllers" / "grammer"
QA_GRAMMAR_CFG_PATH = GRAMMER_DIR / "qa_grammer.cfg"
SCENE_QA_GRAMMAR_CFG_PATH = GRAMMER_DIR / "scene_qa_grammer.cfg"

KG_DIR = PROJECT_ROOT / "Controllers" / "KnowledgeGraphs"

# Static and upload paths
STATIC_DIR = PROJECT_ROOT / "static"
UPLOADS_DIR = PROJECT_ROOT / "uploads"

# Specific static subdirectories
IMAGE_ANSWERING_DEMO_DIR = STATIC_DIR / "ImageAnsweringDemoPics"
CONTACT_PICS_DIR = STATIC_DIR / "ContactPics"
ASSISTANT_PICS_DIR = STATIC_DIR / "AssistantPics"
ANSWER_PICS_DIR = STATIC_DIR / "AnswerPics"

# Ensure directories exist
for directory in [MODELS_DIR, GRAMMER_DIR, KG_DIR, STATIC_DIR, UPLOADS_DIR, 
                  CONTACT_PICS_DIR, ASSISTANT_PICS_DIR, ANSWER_PICS_DIR]:
    directory.mkdir(parents=True, exist_ok=True)
