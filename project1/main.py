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


@tool
def calculator(a: float, b: float) -> str:
    """Useful for when you need to perform calculations"""
    print("tool has been called")
    return f"The sum of {a} and {b} is {a + b}"

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

           if "agent" in chunk and "messages" in chunk["agent"]:
               # if the chunk contains agent messages
            # we iterate through each message in the chunk

               for message in chunk["agent"]["messages"]:
                       print(message.content, end="")
                       # we print the text of each agent message without a newline

        print()
        # we print a newline after the agent's response is complete

if __name__ == "__main__":
    main()
    # if this script is run directly we call the main function to start the program 
