import streamlit as st

from ai_chatbot import ask_ai, transcribe_audio



def show_ai_analyst():

    df = st.session_state.df

    st.title("🤖 AI Data Analyst")

    st.caption(
        "Ask questions about your dataset in natural language."
    )

    if df is None:

        st.warning(
            "Upload a dataset from the sidebar first."
        )

        return

    # ========================================================
    # HEADER
    # ========================================================

    c1, c2 = st.columns(
        [4, 1]
    )

    with c1:

        st.markdown(
            """
            ### Your personal data analyst

            Ask anything about the uploaded dataset.
            The AI can help you understand patterns,
            data quality, statistics and visualizations.
            """
        )

    with c2:

        if st.button(
            "🗑️ Clear Chat"
        ):

            st.session_state.chat_history = []

            st.rerun()

    st.divider()

    # ========================================================
    # SUGGESTED QUESTIONS
    # ========================================================

    st.markdown(
        "**Try asking:**"
    )

    suggestions = [
        "Give me a complete EDA summary.",
        "Which columns need cleaning?",
        "What are the most important insights?",
        "Is this dataset ready for machine learning?"
    ]

    cols = st.columns(4)

    for i, question in enumerate(
        suggestions
    ):

        with cols[i]:

            if st.button(
                question,
                key=f"suggestion_{i}",
                use_container_width=True
            ):

                st.session_state.pending_question = question

                st.rerun()

    st.divider()

    # ========================================================
    # CHAT HISTORY
    # ========================================================

    for message in st.session_state.chat_history:

        with st.chat_message(
            message["role"]
        ):

            st.markdown(
                message["content"]
            )

    # ========================================================
    # PENDING SUGGESTION
    # ========================================================

    if (
        "pending_question"
        in st.session_state
    ):

        question = (
            st.session_state
            .pop("pending_question")
        )

        st.session_state.chat_history.append(
            {
                "role": "user",
                "content": question
            }
        )

        with st.chat_message("user"):

            st.markdown(question)

        with st.chat_message(
            "assistant"
        ):

            with st.spinner(
                "Analyzing your dataset..."
            ):

                response = ask_ai(
                    question,
                    df,
                    st.session_state.chat_history
                )

            st.markdown(response)

        st.session_state.chat_history.append(
            {
                "role": "assistant",
                "content": response
            }
        )

        st.rerun()

    # ========================================================
    # CHAT INPUT
    # ========================================================

    prompt = st.chat_input(
        "Ask your dataset anything...",
        accept_audio=True,
        audio_sample_rate=16000
    )

    if prompt is None:
        return

    question = None

    # ========================================================
    # TEXT
    # ========================================================

    if prompt.text:

        question = prompt.text

    # ========================================================
    # VOICE
    # ========================================================

    elif prompt.audio:

        with st.spinner(
            "🎙️ Converting your voice to text..."
        ):

            question, error = (
                transcribe_audio(
                    prompt.audio
                )
            )

        if error:

            st.error(
                f"Voice transcription failed: {error}"
            )

            return

        if question:

            st.info(
                f"🎙️ You said: **{question}**"
            )

    # ========================================================
    # PROCESS
    # ========================================================

    if not question:

        return

    st.session_state.chat_history.append(
        {
            "role": "user",
            "content": question
        }
    )

    with st.chat_message(
        "user"
    ):

        st.markdown(question)

    with st.chat_message(
        "assistant"
    ):

        with st.spinner(
            "🧠 Thinking..."
        ):

            response = ask_ai(
                question,
                df,
                st.session_state.chat_history
            )

        st.markdown(response)

    st.session_state.chat_history.append(
        {
            "role": "assistant",
            "content": response
        }
    )

