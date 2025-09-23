from langchain_core.messages import HumanMessage
# represents a chat message from a human in the langchain schema. 
# basically makes the agent sound like a human texting
from langchain_openai import ChatOpenAI
# gives us access to openai's chat models inside our langchain code
from langchain.tools import tool
#gives us a decorator to create tools for our agent
from langgraph.prebuilt import create_react_agent
# gives us a function to create a react(reason + act) agent. 
# it reasones about what to do and then acts on it
#it is a pre built agent
from dotenv import load_dotenv  
# loads environment variables from a .env file into the environment
  

load_dotenv()
# load environment variables from a .env file into the environment

def main():
    # main function to run the agent
    
    model = ChatOpenAI(temperature=0)
    #here we are setting the temperature of the model we are getting to use .
    #  0 means we want less randomeness. and we are save it inside a model variable
   
    tools = []
    # we are creating an empty list to store our tools

    agent_executor = create_react_agent(model, tools)
    # we are  creating a react agent using the model and tools we defined above
    # and saving it inside a variable called agent_executor

    print("Welcome to the REACT Agent. Type 'exit' to quit.")
    print("You can ask me to perform calculations or chat with me")

#these two lines above are just welcoming messages to the user

    while True:
        user_input = input("\nYou: ").strip()
        # we are taking input from the user and stripping any leading 
        # or trailing whitespace

        if user_input.lower() == 'exit':
            print("Goodbye!")
            break
        # if the user types exit we break the loop and end the program

        print("\nAssistant: ", end="")
    # we are printing assistant without a newline at the end
    #so that the agent's response appears on the same line

        for chunk in agent_executor.stream(
            {"messages": [HumanMessage(content=user_input)]}):
           # we are streaming the agent's response in chunks
           # we are passing the user's input as a HumanMessage inside a list
           # inside a dictionary with the key "messages" 
           if "agent" in chunk and "messages" in chunk["agent"]:
               for message in chunk["agent"]["messages"]:
                       print(message["text"], end="")

        print()
        # we print a newline after the agent's response is complete