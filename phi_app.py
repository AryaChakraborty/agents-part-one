import streamlit as st 
from phi.agent import Agent
from phi.model.google import Gemini
from phi.tools.duckduckgo import DuckDuckGo
from phi.tools.youtube_tools import YouTubeTools
from phi.tools.googlecalendar import GoogleCalendarTools
from google.generativeai import upload_file,get_file
import google.generativeai as genai

import datetime
from tzlocal import get_localzone_name

import time
from pathlib import Path

import tempfile

from dotenv import load_dotenv
load_dotenv()

import os

API_KEY=os.getenv("GOOGLE_API_KEY")
if API_KEY:
    genai.configure(api_key=API_KEY)

# Page configuration
st.set_page_config(
    page_title="Multimodal AI Agent - Media Summarizer",
    page_icon="🎥",
    layout="wide"
)

def video_processor():

    st.title("Video AI Summarizer Agent")


    @st.cache_resource
    def initialize_agent():
        return Agent(
            name="Video AI Summarizer",
            model=Gemini(id="gemini-2.0-flash-exp"),
            tools=[DuckDuckGo()],
            markdown=True,
        )

    ## Initialize the agent
    multimodal_Agent=initialize_agent()

    # File uploader
    video_file = st.file_uploader(
        "Upload a video file", type=['mp4', 'mov', 'avi'], help="Upload a video for AI analysis"
    )

    if video_file:
        with tempfile.NamedTemporaryFile(delete=False, suffix='.mp4') as temp_video:
            temp_video.write(video_file.read())
            video_path = temp_video.name

        st.video(video_path, format="video/mp4", start_time=0)

        user_query = st.text_area(
            "What information are you seeking from the video?",
            placeholder="Ask anything about the video content.",
            help="Provide specific questions or insights you want from the video."
        )

        if st.button("🔍 Analyze Video", key="analyze_video_button"):
            if not user_query:
                st.warning("Please enter a question to analyze the video.")
            else:
                try:
                    with st.spinner("Processing video and getting insights..."):
                        # Upload and process video file
                        processed_video = upload_file(video_path)
                        while processed_video.state.name == "PROCESSING":
                            time.sleep(1)
                            processed_video = get_file(processed_video.name)

                        # Prompt generation for analysis
                        analysis_prompt = (
                            f"""
                            Analyze the uploaded video for content and context.
                            Respond to the following query using video insights and supplementary web research:
                            {user_query}

                            Provide a detailed, user-friendly, and actionable response.
                            """
                        )

                        # AI agent processing
                        response = multimodal_Agent.run(analysis_prompt, videos=[processed_video])

                    # Display the result
                    st.subheader("Analysis Result")
                    st.markdown(response.content)

                except Exception as error:
                    st.error(f"An error occurred during analysis: {error}")
                finally:
                    # Clean up temporary video file
                    Path(video_path).unlink(missing_ok=True)
    else:
        st.info("Upload a video file to begin analysis.")

    # Customize text area height
    st.markdown(
        """
        <style>
        .stTextArea textarea {
            height: 100px;
        }
        </style>
        """,
        unsafe_allow_html=True
    )

def image_processor():
    st.title("Image Processor AI Agent")


    @st.cache_resource
    def initialize_agent():
        return Agent(
            name="Image AI Processor",
            model=Gemini(id="gemini-2.0-flash-exp"),
            tools=[DuckDuckGo()],
            markdown=True,
        )

    ## Initialize the agent
    multimodal_Agent=initialize_agent()

    # File uploader
    image_file = st.file_uploader(
        "Upload an image file", type=['jpg', 'jpeg', 'png'], help="Upload an Image for AI analysis"
    )

    if image_file:
        with tempfile.NamedTemporaryFile(delete=False, suffix='.jpeg') as temp_image:
            temp_image.write(image_file.read())
            image_path = temp_image.name

        st.image(image_path, output_format="auto", channels="RGB")

        user_query = st.text_area(
            "What information are you seeking from the Image?",
            placeholder="Ask anything about the Image content.",
            help="Provide specific questions or insights you want from the Image."
        )

        if st.button("🔍 Analyze Image", key="analyze_image_button"):
            if not user_query:
                st.warning("Please enter a question to analyze the Image.")
            else:
                try:
                    with st.spinner("Processing image and getting insights..."):
                        # Upload and process video file
                        processed_image = upload_file(image_path)
                        while processed_image.state.name == "PROCESSING":
                            time.sleep(1)
                            processed_image = get_file(processed_image.name)

                        # Prompt generation for analysis
                        analysis_prompt = (
                            f"""
                            Analyze the uploaded image for content and context.
                            Respond to the following query using image insights and supplementary web research:
                            {user_query}

                            Provide a detailed, user-friendly, and actionable response.
                            """
                        )

                        # AI agent processing
                        response = multimodal_Agent.run(analysis_prompt, images=[processed_image])

                    # Display the result
                    st.subheader("Analysis Result")
                    st.markdown(response.content)

                except Exception as error:
                    st.error(f"An error occurred during analysis: {error}")
                finally:
                    # Clean up temporary video file
                    Path(image_path).unlink(missing_ok=True)
    else:
        st.info("Upload an image file to begin analysis.")

    # Customize text area height
    st.markdown(
        """
        <style>
        .stTextArea textarea {
            height: 100px;
        }
        </style>
        """,
        unsafe_allow_html=True
    )

def youtube_processor():

    st.title("YouTube Summarizer AI Agent")

    youtube_link = st.text_input(
            "Paste the YouTube link here",
            placeholder="https://www.youtube.com/watch?v=video_id"
        )

    if youtube_link:
        agent = Agent(
            name="youtube_agent",
            model=Gemini(id="gemini-2.0-flash-exp"),
            tools=[YouTubeTools()],
            show_tool_calls=False,
            description="You are a YouTube agent. Obtain the captions of a YouTube video and answer questions.",
        )

        user_query = st.text_area(
                "What information are you seeking from the YouTube Video?",
                placeholder="Ask anything about the Video content.",
                help="Provide specific questions or insights you want from the Video."
            )
        
        if st.button("🔍 Analyze Video", key="analyze_youtube_button"):
            if not user_query:
                st.warning("Please enter a question to analyze the video link.")
            else:
                try:
                    with st.spinner("Processing video and getting insights..."):
                        analysis_prompt = f"""
                                        Analyze the YouTube video for content and context.
                                        {youtube_link}

                                        Respond to the following user query using video insights and supplementary web research:
                                        {user_query}

                                        Provide a detailed, user-friendly, and actionable response.
                                        """

                        response = agent.run(analysis_prompt, markdown=True)

                        st.subheader("Analysis Result")
                        st.markdown(response.content)

                except Exception as error:
                    st.error(f"An error occurred during analysis: {error}")
    
    else:
        st.info("Put the source YouTube link to begin analysis.")

    # Customize text area height
    st.markdown(
        """
        <style>
        .stTextArea textarea {
            height: 100px;
        }
        </style>
        """,
        unsafe_allow_html=True
    )

def g_calendar_processor():

    st.title("Google Calendar AI Agent")

    agent = Agent(
        model=Gemini(id="gemini-2.0-flash-exp"),
        tools=[GoogleCalendarTools(credentials_path="google_credentials.json")],
        show_tool_calls=False,
        instructions=[
            f"""
            You are scheduling assistant . Today is {datetime.datetime.now()} and the users timezone is {get_localzone_name()}.
            You should help users with answers from their queries and from their Google calendar.
            """
        ],
        add_datetime_to_instructions=True,
    )

    user_query = st.text_area(
            "What do you want to know about your calendar events?",
            placeholder="Ask anything about your upcoming or past events.",
            help="Provide specific questions or insights you want from your schedule."
        )

    if st.button("🔍 Ask", key="ask_calendar_button"):
        if not user_query:
            st.warning("Please enter a question to ask from your schedule.")
        else:
            try:
                with st.spinner("Fetching Calendar results and getting insights..."):
                    response = agent.run(user_query, markdown=True)
                    st.subheader("Results")
                    st.markdown(response.content)

            except Exception as error:
                st.error(f"An error occurred during analysis: {error}")
    
    
    st.info("Ask a question to begin with.")

    # Customize text area height
    st.markdown(
        """
        <style>
        .stTextArea textarea {
            height: 100px;
        }
        </style>
        """,
        unsafe_allow_html=True
    )


# sidebar for selecting the task
option = st.sidebar.selectbox("Select File Type", 
                              ["Video", "Image", "YouTube", "Calendar"],
                              index=1)

# Display the corresponding interface based on the selected option
if option == "Video":
    video_processor()
elif option == "Image":
    image_processor()
elif option == "YouTube":
    youtube_processor()
elif option == "Calendar":
    g_calendar_processor()