"""
CrewAI Multi-Agent System
========================

This module demonstrates a multi-agent system using CrewAI framework with Google's Gemini 2.5 Flash model.
The system coordinates between a Research Analyst and a Copywriter to perform sequential tasks.

Dependencies:
- crewai: Framework for orchestrating role-playing, autonomous AI agents
- os: For environment variable access
- Google Gemini API: Large language model provider

Author: Tayyab
Date: September 2025
"""

import os
from crewai import Agent, Task, Crew, Process, LLM

# =============================================================================
# Configuration and Setup
# =============================================================================

# Read the Gemini API key from environment variables
# This key is required to authenticate with Google's Gemini API
# Set this in your environment: export GEMINI_API_KEY="your_api_key_here"
gemini_api_key = os.getenv("GEMINI_API_KEY")

if not gemini_api_key:
    raise ValueError("GEMINI_API_KEY environment variable is not set. Please set it before running the script.")

# Initialize the Large Language Model (LLM) with Gemini 2.5 Flash
# This model will be shared across all agents in the crew
llm = LLM(
    model='gemini/gemini-2.5-flash',  # Google's fast and efficient model
    api_key=gemini_api_key,           # Authentication key
    temperature=0.0                   # Low temperature for deterministic, consistent results
)

# =============================================================================
# Agent Definitions
# =============================================================================

# Research Analyst Agent
# This agent specializes in conducting thorough research and analysis
researcher = Agent(
    role='Research Analyst',                           # Primary role/identity of the agent
    goal='Analyze and research topics thoroughly',     # Primary objective
    backstory='You are an experienced research analyst with expertise in gathering, '
              'analyzing, and synthesizing information from multiple sources. You have '
              'a keen eye for detail and can identify key trends and insights.',
    verbose=True,                                      # Enable detailed logging
    allow_delegation=False,                            # Prevent this agent from delegating tasks
    llm=llm                                           # Assign the configured LLM
)

# Copywriter Agent
# This agent specializes in creating compelling written content
copywriter = Agent(
    role='Copywriter',                                 # Primary role/identity of the agent
    goal='Write compelling and engaging copy for given topics', # Primary objective
    backstory='You are an experienced copywriter with a talent for crafting '
              'persuasive, clear, and engaging content. You understand how to '
              'adapt your writing style to different audiences and purposes.',
    verbose=True,                                      # Enable detailed logging
    allow_delegation=False,                            # Prevent this agent from delegating tasks
    llm=llm                                           # Assign the configured LLM
)

# =============================================================================
# Task Definitions
# =============================================================================

# Research Task
# This task instructs the Research Analyst to investigate AI trends
research_task = Task(
    description=(
        'Research the latest trends in artificial intelligence and provide a comprehensive summary. '
        'Focus on emerging technologies, market developments, key players, and potential impacts '
        'on various industries. Include recent breakthroughs and future predictions.'
    ),
    agent=researcher,                                          # Assign to the researcher agent
    expected_output=(
        'A detailed report on AI trends including key developments, market insights, '
        'and future predictions. The report should be concise but comprehensive, '
        'maximum 100 words, highlighting the most significant trends and their implications.'
    )
)

# Copywriting Task
# This task instructs the Copywriter to create marketing copy based on the research
copywriting_task = Task(
    description=(
        'Based on the research findings about AI trends, write compelling marketing copy '
        'that highlights the key opportunities and benefits of AI adoption. The copy should '
        'be engaging, professional, and targeted at business decision-makers who are '
        'considering AI implementation in their organizations.'
    ),
    agent=copywriter,                                          # Assign to the copywriter agent
    expected_output=(
        'Professional marketing copy that transforms the research insights into compelling '
        'business value propositions. The copy should be persuasive, clear, and actionable, '
        'suitable for use in marketing materials or business presentations.'
    )
)

# =============================================================================
# Crew Configuration and Execution
# =============================================================================

# Create the crew with agents and tasks
# The crew orchestrates the execution of tasks by coordinating multiple agents
crew = Crew(
    agents=[researcher, copywriter],        # List of agents participating in the crew
    tasks=[research_task, copywriting_task], # List of tasks to be executed
    process=Process.sequential,             # Execute tasks in sequential order
    verbose=True                            # Enable detailed logging of the execution process
)

# =============================================================================
# Main Execution Block
# =============================================================================

def main():
    """
    Main execution function that orchestrates the multi-agent workflow.

    The workflow follows these steps:
    1. Research Agent analyzes AI trends and creates a comprehensive report
    2. Copywriter Agent uses the research to create compelling marketing copy

    Returns:
        str: The final output from the crew execution
    """
    print("🚀 Starting CrewAI Multi-Agent System...")
    print("📋 Workflow: Research Analysis → Marketing Copy Creation")
    print("-" * 60)

    try:
        # Execute the crew and get results
        # The kickoff() method initiates the sequential execution of all tasks
        result = crew.kickoff()

        # Display the final results
        print("\n" + "="*60)
        print("🎯 FINAL RESULTS")
        print("="*60)
        print(result)
        print("="*60)
        print("✅ Multi-agent workflow completed successfully!")

        return result

    except Exception as e:
        print(f"❌ Error during execution: {str(e)}")
        raise

# Execute only when run directly (not when imported as a module)
if __name__ == "__main__":
    main()
