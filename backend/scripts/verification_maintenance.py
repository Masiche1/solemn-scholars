"""Run verification malware/retention maintenance from a scheduler."""
import argparse

from app import create_app
from app.services.verification import purge_verification_data


parser = argparse.ArgumentParser(description="Purge retained Tutorly verification data.")
parser.add_argument("--config", default="production", choices=("development", "production"))
args = parser.parse_args()

app = create_app(args.config)
with app.app_context():
    submissions, documents = purge_verification_data()
    print(f"Purged {documents} verification documents and {submissions} submissions.")
