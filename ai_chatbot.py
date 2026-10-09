import os
import io

import pandas as pd
from openai import OpenAI

from config import (
    OPENAI_MODEL,
    TRANSCRIPTION_MODEL
)


# ============================================================
# CLIENT
# ============================================================

def get_client():

    api_key = os.getenv(
        "OPENAI_API_KEY"
    )

    if not api_key:
        return None

    return OpenAI(
        api_key=api_key
    )


# ============================================================
# DATASET CONTEXT
# ============================================================

def build_dataset_context(df):

    numeric = df.select_dtypes(
        include="number"
    )

    categorical = df.select_dtypes(
        include=[
            "object",
            "category",
            "bool"
        ]
    )

    context = {
        "shape": {
            "rows": int(df.shape[0]),
            "columns": int(df.shape[1])
        },

        "columns": [
            {
                "name": str(col),
                "dtype": str(df[col].dtype),
                "missing": int(
                    df[col].isna().sum()
                ),
                "unique": int(
                    df[col].nunique()
                )
            }

            for col in df.columns
        ],

        "numeric_columns": [
            str(c)
            for c in numeric.columns
        ],

        "categorical_columns": [
            str(c)
            for c in categorical.columns
        ],

        "duplicates": int(
            df.duplicated().sum()
        ),

        "missing_total": int(
            df.isna().sum().sum()
        )
    }

    # --------------------------------------------------------
    # Numeric statistics
    # --------------------------------------------------------

    if not numeric.empty:

        statistics = (
            numeric
            .describe()
            .round(3)
            .to_dict()
        )

        context[
            "numeric_statistics"
        ] = statistics

        context[
            "correlations"
        ] = (
            numeric
            .corr()
            .round(3)
            .to_dict()
        )

    # --------------------------------------------------------
    # Categorical examples
    # --------------------------------------------------------

    categorical_examples = {}

    for col in categorical.columns[:20]:

        values = (
            df[col]
            .value_counts()
            .head(10)
            .to_dict()
        )

        categorical_examples[
            str(col)
        ] = {
            str(k): int(v)
            for k, v in values.items()
        }

    context[
        "categorical_top_values"
    ] = categorical_examples

    return context


# ============================================================
# AI RESPONSE
# ============================================================

def ask_ai(question, df, history):

    client = get_client()

    if client is None:

        return (
            "⚠️ OpenAI API key is not configured.\n\n"
            "Set the `OPENAI_API_KEY` environment variable "
            "and restart the application."
        )

    context = build_dataset_context(df)

    instructions = """
You are an expert Data Analyst and Data Science mentor.

You are the AI analyst inside a professional Exploratory
Data Analysis application.

Your job is to answer questions about the user's uploaded
dataset.

IMPORTANT RULES:

1. Use the provided dataset context.
2. Never invent statistics that are not present.
3. Clearly say when the available information is insufficient.
4. Explain technical concepts in beginner-friendly language.
5. When appropriate, provide actionable recommendations.
6. If the user asks for EDA, structure the answer clearly.
7. If the user asks about a visualization, recommend the
   correct chart and explain why.
8. If the user asks whether data is suitable for ML, discuss
   missing values, duplicates, data types, outliers,
   categorical variables and potential target leakage.
9. When comparing columns or groups, use available statistics.
10. Be concise but useful.
11. Use Markdown headings and bullet points.
12. Do not claim that you actually ran code unless the
    provided context proves it.
"""

    user_prompt = f"""
DATASET CONTEXT:

{context}

USER QUESTION:

{question}
"""

    try:

        response = client.responses.create(
            model=OPENAI_MODEL,
            instructions=instructions,
            input=user_prompt
        )

        return response.output_text

    except Exception as e:

        return (
            f"❌ AI request failed.\n\n"
            f"Error: `{e}`"
        )


# ============================================================
# VOICE → TEXT
# ============================================================

def transcribe_audio(audio_file):

    client = get_client()

    if client is None:

        return (
            None,
            "OpenAI API key is not configured."
        )

    try:

        audio_bytes = audio_file.getvalue()

        file_object = io.BytesIO(
            audio_bytes
        )

        file_object.name = (
            "voice_input.wav"
        )

        transcription = (
            client.audio.transcriptions.create(
                model=TRANSCRIPTION_MODEL,
                file=file_object
            )
        )

        return (
            transcription.text,
            None
        )

    except Exception as e:

        return (
            None,
            str(e)
        )
