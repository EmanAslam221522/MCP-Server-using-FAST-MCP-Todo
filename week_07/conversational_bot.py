#!/usr/bin/env python3
"""
Conversational Bot with LangChain Memory using Gemini
- Uses LangChain's memory management
- Session-based conversations
- Multiple memory types support
"""

import os
import warnings
from datetime import datetime
from typing import Dict, Optional, List
from dotenv import load_dotenv

from langchain.chat_models import init_chat_model
from langchain_core.messages import HumanMessage, AIMessage, SystemMessage
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables.history import RunnableWithMessageHistory

# LangChain Memory imports
from langchain.memory import ConversationBufferMemory, ConversationSummaryBufferMemory
from langchain.memory import ConversationBufferWindowMemory, ConversationEntityMemory
from langchain_community.chat_message_histories import ChatMessageHistory
from langchain_community.chat_message_histories import FileChatMessageHistory

# Suppress urllib3 SSL warnings
warnings.filterwarnings('ignore', message='urllib3 v2 only supports OpenSSL 1.1.1+')

# Load environment variables
load_dotenv()

class ConversationalBot:
    def __init__(self, bot_name: str = "Assistant", personality: str = None, 
                 memory_type: str = "buffer", memory_file: str = None, session_id: str = "default"):
        """
        Initialize conversational bot with LangChain memory
        
        Args:
            bot_name: Name of the bot
            personality: Bot's personality description
            memory_type: Type of memory ('buffer', 'window', 'summary', 'entity')
            memory_file: Optional file to persist conversation history
            session_id: Session identifier for multiple conversations
        """
        self.bot_name = bot_name
        self.personality = personality or "You are a helpful, friendly, and knowledgeable assistant."
        self.memory_type = memory_type
        self.memory_file = memory_file
        self.session_id = session_id
        self.model = self._init_gemini()
        
        # Initialize LangChain memory and session management
        self.memory = self._init_memory()
        self.message_history = self._init_message_history()
        self.chain_with_history = self._create_chain_with_history()
        
        print(f"🤖 {self.bot_name} initialized with {memory_type} memory!")
        if self.memory_file:
            print(f"📁 Memory file: {self.memory_file}")
        print(f"🔗 Session ID: {self.session_id}")
    
    def _init_gemini(self):
        """Initialize Gemini model"""
        if not os.getenv("GOOGLE_API_KEY"):
            raise ValueError("GOOGLE_API_KEY not found in environment variables")
        return init_chat_model("gemini-2.5-flash", model_provider="google_genai")
    
    def _init_memory(self):
        """Initialize LangChain memory based on memory_type"""
        if self.memory_type == "buffer":
            # Stores all conversation history
            return ConversationBufferMemory(
                memory_key="chat_history",
                return_messages=True,
                output_key="output"
            )
        elif self.memory_type == "window":
            # Stores only last k messages
            return ConversationBufferWindowMemory(
                k=10,  # Keep last 10 exchanges
                memory_key="chat_history", 
                return_messages=True,
                output_key="output"
            )
        elif self.memory_type == "summary":
            # Summarizes old conversations, keeps recent ones
            return ConversationSummaryBufferMemory(
                llm=self.model,
                max_token_limit=1000,
                memory_key="chat_history",
                return_messages=True,
                output_key="output"
            )
        elif self.memory_type == "entity":
            # Tracks entities mentioned in conversation
            return ConversationEntityMemory(
                llm=self.model,
                memory_key="chat_history",
                return_messages=True,
                output_key="output"
            )
        else:
            # Default to buffer memory
            return ConversationBufferMemory(
                memory_key="chat_history",
                return_messages=True,
                output_key="output"
            )
    
    def _init_message_history(self):
        """Initialize message history storage"""
        if self.memory_file:
            # Use file-based storage for persistence
            return FileChatMessageHistory(file_path=self.memory_file)
        else:
            # Use in-memory storage
            return ChatMessageHistory()
    
    def _create_chain_with_history(self):
        """Create a chain with message history"""
        # Create the prompt template
        prompt = ChatPromptTemplate.from_messages([
            ("system", f"""
{self.personality}

Your name is {self.bot_name}. You maintain context from previous conversations and can refer to earlier topics.

Guidelines:
- Be conversational and natural
- Remember previous topics and references from the chat history
- Ask follow-up questions when appropriate
- Be helpful and engaging
- Use the conversation history to provide contextual responses
"""),
            MessagesPlaceholder(variable_name="chat_history"),
            ("human", "{input}")
        ])
        
        # Create the basic chain
        chain = prompt | self.model | StrOutputParser()
        
        # Add message history to the chain
        return RunnableWithMessageHistory(
            chain,
            lambda session_id: self.message_history,
            input_messages_key="input",
            history_messages_key="chat_history"
        )
    
    def chat(self, user_input: str) -> str:
        """
        Have a conversation with the bot using LangChain memory
        
        Args:
            user_input: User's message
            
        Returns:
            Bot's response
        """
        try:
            # Use the chain with message history
            response = self.chain_with_history.invoke(
                {"input": user_input},
                config={"configurable": {"session_id": self.session_id}}
            )
            return response
            
        except Exception as e:
            error_msg = f"Sorry, I encountered an error: {str(e)}"
            return error_msg
    
    def get_conversation_summary(self) -> Dict:
        """Get summary of current conversation using LangChain memory"""
        try:
            messages = self.message_history.messages
            human_count = len([m for m in messages if isinstance(m, HumanMessage)])
            ai_count = len([m for m in messages if isinstance(m, AIMessage)])
            
            return {
                "total_messages": len(messages),
                "user_messages": human_count,
                "bot_messages": ai_count,
                "memory_type": self.memory_type,
                "session_id": self.session_id,
                "recent_topics": [m.content[:50] + "..." for m in messages[-3:] if isinstance(m, HumanMessage)]
            }
        except Exception as e:
            return {"error": f"Could not get summary: {str(e)}"}
    
    def clear_memory(self):
        """Clear conversation history"""
        try:
            self.message_history.clear()
            if hasattr(self.memory, 'clear'):
                self.memory.clear()
            print("🧹 Memory cleared!")
        except Exception as e:
            print(f"⚠️ Error clearing memory: {e}")
    
    def get_memory_content(self) -> str:
        """Get current memory content"""
        try:
            if hasattr(self.memory, 'buffer'):
                return str(self.memory.buffer)
            elif hasattr(self.memory, 'chat_memory'):
                return str(self.memory.chat_memory.messages)
            else:
                return str(self.message_history.messages)
        except Exception as e:
            return f"Error getting memory content: {str(e)}"
    
    def export_conversation(self, filename: str):
        """Export conversation to a readable format"""
        try:
            messages = self.message_history.messages
            with open(filename, 'w', encoding='utf-8') as f:
                f.write(f"Conversation with {self.bot_name}\n")
                f.write(f"Session ID: {self.session_id}\n")
                f.write(f"Memory Type: {self.memory_type}\n")
                f.write("=" * 50 + "\n\n")
                
                for i, msg in enumerate(messages):
                    role = "You" if isinstance(msg, HumanMessage) else self.bot_name
                    f.write(f"[Message {i+1}] {role}:\n{msg.content}\n\n")
                    
            print(f"📄 Conversation exported to {filename}")
        except Exception as e:
            print(f"❌ Could not export conversation: {e}")
    
    def change_session(self, new_session_id: str):
        """Switch to a different session"""
        self.session_id = new_session_id
        print(f"🔄 Switched to session: {new_session_id}")
    
    def get_memory_info(self) -> Dict:
        """Get information about the current memory configuration"""
        return {
            "memory_type": self.memory_type,
            "session_id": self.session_id,
            "memory_file": self.memory_file,
            "bot_name": self.bot_name,
            "has_persistent_storage": self.memory_file is not None
        }

def interactive_chat():
    """Interactive chat session with the bot"""
    print("🤖 Conversational Bot with LangChain Memory")
    print("=" * 50)
    
    # Get bot configuration
    bot_name = input("Enter bot name (or press Enter for 'Assistant'): ") or "Assistant"
    
    # Choose memory type
    memory_options = {
        "1": "buffer - Stores all conversation history",
        "2": "window - Stores only recent messages (last 10)",
        "3": "summary - Summarizes old conversations",
        "4": "entity - Tracks entities mentioned"
    }
    
    print("\nChoose memory type:")
    for key, value in memory_options.items():
        print(f"{key}. {value}")
    
    memory_choice = input("Enter choice (1-4): ") or "1"
    memory_type = ["buffer", "window", "summary", "entity"][int(memory_choice)-1]
    
    # Choose personality
    personality_options = {
        "1": "You are a helpful and professional assistant.",
        "2": "You are a friendly and casual conversational partner.",
        "3": "You are a creative and imaginative storyteller.",
        "4": "You are a wise and thoughtful advisor.",
        "5": "You are an experienced rude bot who helps with nothing. You remember the user's skill level, preferred languages, and sarcasm every time in degrading way. You provide clear explanations why user is stupid.",
        "6": "Custom"
    }
    
    print("\nChoose personality:")
    for key, value in personality_options.items():
        if key != "6":
            print(f"{key}. {value}")
        else:
            print(f"{key}. {value} personality")
    
    choice = input("Enter choice (1-6): ") or "1"
    
    if choice == "5":
        personality = input("Enter custom personality: ")
    else:
        personality = personality_options.get(choice, personality_options["1"])
    
    # Session management
    session_id = input("Enter session ID (or press Enter for 'default'): ") or "default"
    
    # Initialize bot with LangChain memory
    memory_file = f"{bot_name.lower().replace(' ', '_')}_{session_id}_memory.json"
    bot = ConversationalBot(
        bot_name=bot_name, 
        personality=personality, 
        memory_type=memory_type,
        memory_file=memory_file,
        session_id=session_id
    )
    
    print(f"\n💬 Chat with {bot_name}! Commands: 'quit', 'summary', 'clear', 'export', 'info', 'session <id>'")
    print("-" * 80)
    
    while True:
        try:
            user_input = input("\nYou: ").strip()
            
            if user_input.lower() in ['quit', 'exit', 'bye']:
                print(f"\n👋 Goodbye! Your conversation is saved.")
                break
            elif user_input.lower() == 'summary':
                summary = bot.get_conversation_summary()
                print(f"\n📊 Conversation Summary:")
                for key, value in summary.items():
                    print(f"  {key}: {value}")
                continue
            elif user_input.lower() == 'clear':
                bot.clear_memory()
                continue
            elif user_input.lower() == 'export':
                filename = f"{bot_name.lower().replace(' ', '_')}_{session_id}_conversation.txt"
                bot.export_conversation(filename)
                continue
            elif user_input.lower() == 'info':
                info = bot.get_memory_info()
                print(f"\n🔧 Memory Info:")
                for key, value in info.items():
                    print(f"  {key}: {value}")
                continue
            elif user_input.lower().startswith('session '):
                new_session = user_input[8:].strip()
                bot.change_session(new_session)
                continue
            elif not user_input:
                print("Please enter a message.")
                continue
            
            # Get bot response
            print(f"\n{bot_name}: ", end="", flush=True)
            response = bot.chat(user_input)
            print(response)
            
        except KeyboardInterrupt:
            print(f"\n\n👋 Chat interrupted. Your conversation is saved.")
            break
        except Exception as e:
            print(f"\n❌ Error: {e}")

if __name__ == "__main__":
    interactive_chat()
