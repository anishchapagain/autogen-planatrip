# autogen-planatrip

AutoGen travel planner will utilize multiple AI agents, each with a specific role, to collaboratively create a comprehensive travel itinerary.

This project uses the [AutoGen](https://microsoft.github.io/autogen/) library to create a multi-agent system for planning trips. 

The agents work together in a round-robin group chat to generate a travel plan based on a user's request.

## Agents

The following agents are used in this project:

*   **planner_agent**: A helpful assistant that can plan trips.
*   **local_agent**: A local assistant that can suggest local activities or places to visit.
*   **language_agent**: A helpful assistant that can provide language tips for a given destination.
*   **travel_summary_agent**: A helpful assistant that can summarize the travel plan.

## How to run

To run the application, execute the following command:

```bash
python hello.py
```

This will start the multi-agent chat and stream the conversation to the console. 

# Example Prompt
**"Plan a 3 day trip to London. Do plan to visit a Caribbean Carnival if it is happening during the trip.".**