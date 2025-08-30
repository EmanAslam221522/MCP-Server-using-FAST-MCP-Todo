#!/usr/bin/env python3
"""
Story Writer Examples - Different story topics and genres
"""

from story_writer import StoryWriter

def run_story_examples():
    """Run various story examples"""
    writer = StoryWriter()
    
    examples = [
        {
            "topic": "A robot discovers emotions",
            "genre": "science fiction drama"
        },
        {
            "topic": "A chef competes in a magical cooking tournament", 
            "genre": "fantasy adventure"
        },
        {
            "topic": "Two strangers get stuck in an elevator",
            "genre": "romantic comedy"
        },
        {
            "topic": "A detective solves crimes with their psychic cat",
            "genre": "mystery comedy"
        }
    ]
    
    print("🎯 Story Writer Examples")
    print("=" * 50)
    
    for i, example in enumerate(examples, 1):
        print(f"\n🔹 Example {i}: {example['topic']}")
        print("-" * 30)
        
        # Create the story
        result = writer.create_complete_story(
            topic=example["topic"],
            genre=example["genre"]
        )
        
        if result:
            print("✅ Story created successfully!")
        else:
            print("❌ Failed to create story")
        
        print("\n" + "=" * 70 + "\n")

def create_custom_story():
    """Create a story with custom input"""
    writer = StoryWriter()
    
    print("🎨 Custom Story Creator")
    print("=" * 30)
    
    topic = input("Enter your story topic: ")
    genre = input("Enter genre (or press Enter for 'adventure'): ") or "adventure"
    
    result = writer.create_complete_story(topic=topic, genre=genre)
    
    if result:
        print("\n🎉 Your custom story has been created!")
        
        # Option to save to file
        save = input("\nWould you like to save this story to a file? (y/n): ")
        if save.lower() == 'y':
            filename = f"story_{topic.replace(' ', '_').lower()}.txt"
            with open(filename, 'w') as f:
                f.write(f"TOPIC: {result['topic']}\n")
                f.write(f"GENRE: {result['genre']}\n\n")
                f.write("OUTLINE:\n")
                f.write(result['outline'])
                f.write("\n\nSTORY:\n")
                f.write(result['story'])
                f.write(f"\n\nHASHTAGS:\n{result['hashtags']}\n")
            print(f"📁 Story saved to {filename}")

if __name__ == "__main__":
    print("Welcome to Story Writer!")
    print("1. Run example stories")
    print("2. Create custom story")
    
    choice = input("\nChoose an option (1 or 2): ")
    
    if choice == "1":
        run_story_examples()
    elif choice == "2":
        create_custom_story()
    else:
        print("Invalid choice. Running examples...")
        run_story_examples()
