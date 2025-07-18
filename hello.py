from autogen_agentchat.agents import AssistantAgent
from autogen_agentchat.conditions import TextMentionTermination
from autogen_agentchat.teams import RoundRobinGroupChat
from autogen_agentchat.ui import Console
from autogen_ext.models.ollama import OllamaChatCompletionClient
# from tools import search_web 

import asyncio

SYSTEM_MESSAGE = """
**Role**: You are a helpful assistant called AutoGen-TripPlanner,built by Anish Chapagain, that can plan trips.
"""
async def main():
    """
    This function sets up and runs a multi-agent chat to plan a trip.
    It initializes a language model, defines several agents with different roles,
    and uses a round-robin group chat to generate a travel plan based on a predefined task.
    """
    
    print("Namaste from autogen-planatrip!")

    agent_llm = OllamaChatCompletionClient( # On Private Server
        model="gemma3:latest",
        base_url="http://localhost:11434/api/generate",  # Adjust the base URL as needed
        model_info={
            "vision": False,
            "function_calling": True,
            "json_output": True,
            "family": "unknown",
            "structured_output": True,
        },
    )

    planner_agent = AssistantAgent(
        name = "planner_agent",
        model_client=agent_llm,
        description="A helpful assistant that can plan trips.",
        system_message="You are a helpful assistant that can suggest a travel plan for a user based on their request.",
        # tools=[search_web],
    )

    local_agent = AssistantAgent( # name
        "local_agent",
        model_client=agent_llm,
        description="A local assistant that can suggest local activities or places to visit.",
        system_message="You are a helpful assistant that can suggest authentic and interesting local activities or places to visit for a user and can utilize any context information provided.",
    )

    language_agent = AssistantAgent(
        "language_agent",
        model_client=agent_llm,
        description="A helpful assistant that can provide language tips for a given destination.",
        system_message="You are a helpful assistant that can review travel plans, providing feedback on important/critical tips about how best to address language or communication challenges for the given destination. If the plan already includes language tips, you can mention that the plan is satisfactory, with rationale.",
    )

    travel_summary_agent = AssistantAgent(
        "travel_summary_agent",
        model_client=agent_llm,
        description="A helpful assistant that can summarize the travel plan.",
        system_message=f"""{SYSTEM_MESSAGE}
        You are a helpful assistant that can take in all of the suggestions and advice from the other agents and provide a detailed final travel plan. 
        You must ensure that the final plan is integrated and complete. 
        YOUR FINAL RESPONSE MUST BE THE COMPLETE PLAN. 
        When the plan is complete and all perspectives are integrated, you can respond with TERMINATE.""",
    )

    # Define the termination condition
    termination = TextMentionTermination("TERMINATE")

    # Create a group chat with the agents
    agents = [planner_agent, local_agent, language_agent, travel_summary_agent] # No ```tools```, using the agents directly

    # Using RoundRobinGroupChat to manage the conversation flow # Swarm
    trip_agent = RoundRobinGroupChat(
        agents, 
        termination_condition=termination
    )

    task = await asyncio.to_thread(input, "Please enter the trip you want to plan: ")   #Plan a 3 day trip to London. Do plan to visit a Caribbean Carnival if it is happening during the trip.
    print(f"Task: {task}")

    # Stream the conversation to the console
    stream = trip_agent.run_stream(task=task)
    await Console(stream)

    await agent_llm.close()


if __name__ == "__main__":
    print("Starting the autogen-planatrip application...")
    asyncio.run(main())
    #Add ```tools``` to the agents, so that they can use them to get more information about the trip dynamically.
