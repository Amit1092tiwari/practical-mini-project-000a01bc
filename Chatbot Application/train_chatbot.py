"""
Headless Chatbot Training Script
Designed for scheduled retraining jobs (e.g., daily cron, Airflow, or GitHub Actions).
Trains the ChatterBot instance on corpus data and custom domain conversational pairs.

Usage:
    python train_chatbot.py --corpus english
    python train_chatbot.py --custom-data dialogues.json
"""

import argparse
import json
import logging
from pathlib import Path

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")


def train_bot(corpus_name: str = "chatterbot.corpus.english", custom_data_path: Path = None):
    try:
        from chatterbot import ChatBot
        from chatterbot.trainers import ChatterBotCorpusTrainer, ListTrainer
    except ImportError:
        logging.error(
            "ChatterBot is not installed. Please run on Python 3.7/3.8 with:\n"
            "pip install chatterbot==1.0.5 chatterbot-corpus==1.2.0"
        )
        return False

    logging.info("Initializing HackersRealmBot instance...")
    bot = ChatBot(
        name="HackersRealmBot",
        storage_adapter="chatterbot.storage.SQLStorageAdapter",
        database_uri=f"sqlite:///{Path(__file__).parent / 'db.sqlite3'}",
        logic_adapters=["chatterbot.logic.BestMatch"],
        read_only=False,
    )

    if corpus_name:
        logging.info("Training on corpus: %s", corpus_name)
        corpus_trainer = ChatterBotCorpusTrainer(bot)
        corpus_trainer.train(corpus_name)

    if custom_data_path and custom_data_path.exists():
        logging.info("Training on custom dialogue dataset from: %s", custom_data_path)
        with open(custom_data_path, "r", encoding="utf-8") as f:
            dialogue_list = json.load(f)
        list_trainer = ListTrainer(bot)
        list_trainer.train(dialogue_list)
    else:
        # Default baseline training list
        logging.info("Training on baseline domain training list...")
        baseline_dialogues = [
            "what is your name?",
            "I am Hackers Realm Bot. How can I help you?",
            "which language are you using?",
            "I am using Python language.",
        ]
        list_trainer = ListTrainer(bot)
        list_trainer.train(baseline_dialogues)

    logging.info("Model retraining complete. Knowledge base persisted.")
    return True


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Headless Chatbot Scheduled Training CLI")
    parser.add_argument("--corpus", default="chatterbot.corpus.english", help="Corpus to train on")
    parser.add_argument("--custom-data", type=Path, help="JSON file containing dialogue training pairs")
    args = parser.parse_args()

    train_bot(corpus_name=args.corpus, custom_data_path=args.custom_data)
