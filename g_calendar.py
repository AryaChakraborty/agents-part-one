# from phi.agent import Agent
# from phi.model.google import Gemini
# from phi.tools.googlecalendar import GoogleCalendarTools
# import datetime
# import os
# from tzlocal import get_localzone_name
# import google.generativeai as genai

# from dotenv import load_dotenv
# load_dotenv()

# API_KEY=os.getenv("GOOGLE_API_KEY")
# if API_KEY:
#     genai.configure(api_key=API_KEY)

# agent = Agent(
#     model=Gemini(id="gemini-2.0-flash-exp"),
#     tools=[GoogleCalendarTools(credentials_path="google_credentials.json")],
#     show_tool_calls=True,
#     instructions=[
#         f"""
#         You are scheduling assistant . Today is {datetime.datetime.now()} and the users timezone is {get_localzone_name()}.
#         You should help users with answers from their queries and from their Google calendar.
#         """
#     ],
#     add_datetime_to_instructions=True,
# )

# agent.print_response("Give me the list of tomorrow's events", markdown=True)


