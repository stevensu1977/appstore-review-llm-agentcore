from strands import Agent
from strands_tools.browser import AgentCoreBrowser


# Create browser tool
browser = AgentCoreBrowser(region="us-west-2")
region="us-west-2"
agent = Agent(tools=[browser.browser])

print("🧪 Testing Amazon product search tool...")
#result = agent("Analyse latedest 10 Ratings and reviews for Pokémon UNITE  in google play ")
result = agent("Capture Top 5 pokemon game and get thier game title in google play")



print("📋 Search Results:")
print(result)