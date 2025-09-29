# Patron Saint Finder 🙏✨
Ever wondered which saint would be the best match for you?
Preparing for Confirmation and not sure who to choose? You're in the right place!

## Overview

This is a Streamlit app that helps users discover their patron saint based on their preferences and personal information. The app asks guiding questions (e.g., saint’s gender, profession, challenges, devotions, and favorite themes) and then calls the OpenAI Assistants API to generate a thoughtful recommendation.

## Installation

1. Clone the repository
2. Create and activate virtual environment
    On Windows: 
    `python -m venv myenv`
    `myenv\Scripts\activate`
    On Mac:
    `python -m venv myenv`
    `source myenv/bin/activate`
3. Install Dependencies
    `pip install -r requirements.txt`
4. Set up API Key
    `OPENAI_API_KEY=your_api_key_here`
5. Run the app
    `streamlit run main.py`