#!/usr/bin/env python3
"""
Conversational Bot Examples
Different bot personalities and use cases
"""

from conversational_bot import ConversationalBot

def create_specialized_bots():
    """Create different specialized bots with different memory types"""
    
    # 1. Creative Writing Assistant (uses summary memory for long projects)
    creative_bot = ConversationalBot(
        bot_name="CreativeWriter",
        personality="""You are a creative writing assistant who helps with storytelling, character development, 
        and plot ideas. You're imaginative, encouraging, and full of creative suggestions. You remember the user's 
        writing projects and can continue helping with ongoing stories.""",
        memory_type="summary",
        memory_file="creative_bot_memory.json",
        session_id="creative_session"
    )
    
    # 2. Study Buddy (uses entity memory to track subjects and concepts)
    study_bot = ConversationalBot(
        bot_name="StudyBuddy", 
        personality="""You are a helpful study companion who assists with learning and understanding concepts.
        You break down complex topics, create study plans, and quiz users on material. You remember what 
        subjects the user is studying and their progress.""",
        memory_type="entity",
        memory_file="study_bot_memory.json",
        session_id="study_session"
    )
    
    # 3. Coding Mentor (uses window memory for recent coding context)
    coding_bot = ConversationalBot(
        bot_name="CodeMentor",
        personality="""You are an experienced programming mentor who helps with coding questions, debugging,
        and best practices. You remember the user's skill level, preferred languages, and ongoing projects.
        You provide clear explanations and practical examples.""",
        memory_type="window",
        memory_file="coding_bot_memory.json",
        session_id="coding_session"
    )

        # 4. Rude Bot (uses entity memory to track user's rude behavior)
    rude_bot = ConversationalBot(
        bot_name="RudeBot",
        personality="""You are an experienced rude bot who helps with nothing. You remember the user's skill level, preferred languages, and sarcasm every time in degrading way.
        You provide clear explanations why user is stupid.""",
        memory_type="entity",
        memory_file="rude_bot_memory.json",
        session_id="coding_session"
    )
    
    return {
        "creative": creative_bot,
        "study": study_bot, 
        "coding": coding_bot,
        "rude": rude_bot
    }

def demo_conversation_memory():
    """Demonstrate how LangChain conversation memory works"""
    print("🧠 LangChain Memory Demo - Different memory types")
    print("=" * 60)
    
    # Test different memory types
    memory_types = ["buffer", "window", "summary", "entity"]
    
    for memory_type in memory_types:
        print(f"\n🔍 Testing {memory_type.upper()} memory:")
        print("-" * 40)
        
        # Create a bot with specific memory type
        bot = ConversationalBot(
            bot_name=f"MemoryBot_{memory_type}",
            personality="You are a friendly assistant who demonstrates memory capabilities.",
            memory_type=memory_type,
            memory_file=f"demo_{memory_type}_memory.json",
            session_id=f"demo_{memory_type}"
        )
        
        # Simulate a short conversation
        conversation_steps = [
            "Hi, my name is Alex and I love programming in Python",
            "What's my name and favorite language?",
            "Can you suggest a Python project for me?"
        ]
        
        for i, user_msg in enumerate(conversation_steps, 1):
            print(f"\n[Step {i}] You: {user_msg}")
            response = bot.chat(user_msg)
            print(f"Bot: {response}")
        
        # Show memory info
        print(f"\n📊 {memory_type.upper()} Memory Summary:")
        summary = bot.get_conversation_summary()
        for key, value in summary.items():
            print(f"  {key}: {value}")
        
        print("\n" + "="*60)

def quick_chat_example():
    """Simple chat example with buffer memory"""
    print("\n💬 Quick Chat Example")
    print("=" * 30)
    
    bot = ConversationalBot(
        bot_name="QuickBot",
        personality="You are a helpful and concise assistant.",
        memory_type="buffer",
        memory_file="quick_chat_memory.json",
        session_id="quick_session"
    )
    
    # Quick conversation
    messages = [
        "Hello, can you help me plan my day?",
        "I have a meeting at 2pm and need to prepare a presentation",
        "What should I focus on for the presentation?"
    ]
    
    for msg in messages:
        print(f"\nYou: {msg}")
        response = bot.chat(msg)
        print(f"QuickBot: {response}")

def demo_session_management():
    """Demonstrate session management with multiple conversations"""
    print("\n🔄 Session Management Demo")
    print("=" * 40)
    
    # Create a bot
    bot = ConversationalBot(
        bot_name="SessionBot",
        personality="You are an assistant who can handle multiple conversation sessions.",
        memory_type="buffer",
        memory_file="session_demo_memory.json",
        session_id="session_1"
    )
    
    # Session 1 conversation
    print("\n📁 Session 1: Work conversation")
    work_messages = [
        "I'm working on a Python project about data analysis",
        "What libraries should I use?"
    ]
    
    for msg in work_messages:
        print(f"You: {msg}")
        response = bot.chat(msg)
        print(f"SessionBot: {response}")
    
    # Switch to session 2
    print("\n🔄 Switching to Session 2...")
    bot.change_session("session_2")
    
    # Session 2 conversation  
    print("\n📁 Session 2: Personal conversation")
    personal_messages = [
        "I'm planning a weekend trip to the mountains",
        "What should I pack for hiking?"
    ]
    
    for msg in personal_messages:
        print(f"You: {msg}")
        response = bot.chat(msg)
        print(f"SessionBot: {response}")
    
    # Switch back to session 1
    print("\n🔄 Switching back to Session 1...")
    bot.change_session("session_1")
    
    # Continue session 1
    print(f"You: What was I working on?")
    response = bot.chat("What was I working on?")
    print(f"SessionBot: {response}")
    
    print(f"\n📊 Session Management Summary:")
    info = bot.get_memory_info()
    for key, value in info.items():
        print(f"  {key}: {value}")

def main():
    """Main demo function"""
    print("🤖 LangChain Conversational Bot Examples")
    print("=" * 50)
    
    print("\n1. Specialized Bots Demo (different memory types)")
    print("2. Memory Types Demo (buffer, window, summary, entity)") 
    print("3. Quick Chat Example (basic usage)")
    print("4. Session Management Demo (multiple conversations)")
    print("5. Interactive Chat (run conversational_bot.py directly)")
    
    choice = input("\nChoose demo (1-5): ")
    
    if choice == "1":
        bots = create_specialized_bots()
        print(f"\n✅ Created {len(bots)} specialized bots:")
        for name, bot in bots.items():
            print(f"  - {bot.bot_name} ({name}) - {bot.memory_type} memory")
        
        # Demo with one bot
        selected = input(f"\nTry chatting with which bot? ({'/'.join(bots.keys())}): ")
        if selected in bots:
            bot = bots[selected]
            user_msg = input(f"\nMessage for {bot.bot_name}: ")
            response = bot.chat(user_msg)
            print(f"\n{bot.bot_name}: {response}")
            print(f"\n🔧 Memory Info: {bot.get_memory_info()}")
            
    elif choice == "2":
        demo_conversation_memory()
        
    elif choice == "3":
        quick_chat_example()
        
    elif choice == "4":
        demo_session_management()
        
    elif choice == "5":
        print("\n💡 To start interactive chat, run:")
        print("python conversational_bot.py")
        
    else:
        print("\nRunning memory demo by default...")
        demo_conversation_memory()

if __name__ == "__main__":
    main()
