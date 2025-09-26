# CrewAI Multi-Agent System

A comprehensive demonstration of CrewAI framework for orchestrating autonomous AI agents. This project showcases both single-agent and multi-agent workflows for AI-powered research and content creation.

## 🚀 Overview

This project contains two main implementations:

1. **Multi-Agent System** (`multiAgents.py`) - Demonstrates collaboration between a Research Analyst and Copywriter
2. **Single-Agent System** (`simpleAgent.py`) - Shows basic single-agent workflow for learning purposes

## 📋 Features

- **Multi-Agent Collaboration**: Research Analyst → Copywriter workflow
- **Sequential Task Processing**: Tasks executed in logical order
- **Comprehensive Logging**: Detailed execution tracking
- **Error Handling**: Robust error management with helpful feedback
- **Flexible LLM Integration**: Support for both OpenAI GPT-5 and Google Gemini models
- **Professional Output Formatting**: Clean, readable results presentation

## 🔧 Prerequisites

### Required Dependencies

```bash
pip install crewai
```

### API Keys Required

Choose one of the following LLM providers:

#### For Multi-Agent System (Gemini)
```bash
export GEMINI_API_KEY="your_gemini_api_key_here"
```

#### For Simple Agent System (OpenAI)
```bash
export OPENAI_API_KEY="your_openai_api_key_here"
```

### Getting API Keys

- **Google Gemini**: Visit [Google AI Studio](https://makersuite.google.com/app/apikey)
- **OpenAI**: Visit [OpenAI Platform](https://platform.openai.com/account/api-keys)

## 📁 Project Structure

```
CrewAgents/
├── README.md                 # This documentation
├── multiAgents.py           # Multi-agent system (Gemini)
└── simpleAgent.py           # Single-agent system (OpenAI)
```

## 🏃‍♂️ Quick Start

### Running the Multi-Agent System

1. Set up your Gemini API key:
```bash
export GEMINI_API_KEY="your_api_key"
```

2. Run the multi-agent workflow:
```bash
python multiAgents.py
```

**What happens:**
- Research Analyst analyzes latest AI trends
- Copywriter creates marketing copy based on research
- Sequential execution with detailed logging

### Running the Simple Agent System

1. Set up your OpenAI API key:
```bash
export OPENAI_API_KEY="your_api_key"
```

2. Run the single-agent workflow:
```bash
python simpleAgent.py
```

**What happens:**
- Single Research Analyst performs AI trend analysis
- Generates comprehensive research report
- Ideal for learning CrewAI basics

## 🎭 Agent Roles

### Research Analyst
- **Role**: Experienced research analyst
- **Goal**: Analyze and research topics thoroughly
- **Capabilities**:
  - Trend analysis
  - Market insights
  - Data synthesis
  - Future predictions

### Copywriter (Multi-Agent Only)
- **Role**: Professional copywriter
- **Goal**: Create compelling marketing copy
- **Capabilities**:
  - Business value propositions
  - Persuasive content creation
  - Audience-targeted messaging

## 📊 Expected Outputs

### Multi-Agent System
1. **Research Report**: Comprehensive AI trends analysis (max 100 words)
2. **Marketing Copy**: Professional copy highlighting AI opportunities for businesses

### Single-Agent System
1. **Research Report**: Detailed AI trends analysis with market insights and predictions

## 🔧 Configuration Options

### Temperature Settings
- **Multi-Agent**: `temperature=0.0` (deterministic results)
- **Single-Agent**: Default OpenAI settings

### Verbosity
Both systems run with `verbose=True` for detailed execution logging.

### Process Type
Both systems use `Process.sequential` for ordered task execution.

## 🐛 Troubleshooting

### Common Issues

1. **Missing API Key**
```
ValueError: GEMINI_API_KEY environment variable is not set
```
**Solution**: Set the appropriate environment variable for your chosen LLM

2. **Import Errors**
```
ModuleNotFoundError: No module named 'crewai'
```
**Solution**: Install CrewAI: `pip install crewai`

3. **API Authentication Failures**
- Verify your API key is valid and has sufficient credits
- Check that the API key corresponds to the correct service (OpenAI vs Google)

### Debug Tips

- Enable detailed logging by ensuring `verbose=True` in agent configurations
- Check the console output for step-by-step execution details
- Verify network connectivity for API calls

## 🎨 Customization

### Adding New Agents

```python
new_agent = Agent(
    role='Your Agent Role',
    goal='Define the agent\'s primary objective',
    backstory='Provide context and personality',
    verbose=True,
    allow_delegation=False,
    llm=llm
)
```

### Creating Custom Tasks

```python
custom_task = Task(
    description='Detailed task description',
    agent=your_agent,
    expected_output='Define expected output format and content'
)
```

### Switching LLM Providers

#### To use OpenAI in multi-agent system:
```python
llm = LLM(model="gpt-4")  # or "gpt-5" when available
```

#### To use Gemini in single-agent system:
```python
llm = LLM(
    model='gemini/gemini-2.5-flash',
    api_key=os.getenv("GEMINI_API_KEY"),
    temperature=0.0
)
```

## 📈 Performance Considerations

- **Multi-Agent**: Longer execution time due to sequential agent coordination
- **Single-Agent**: Faster execution, suitable for simple workflows
- **Token Usage**: Monitor API usage, especially with detailed verbose logging

## 🔮 Future Enhancements

Potential improvements and extensions:

- [ ] Add parallel task processing capabilities
- [ ] Implement agent memory for context retention
- [ ] Add support for additional LLM providers (Anthropic Claude, etc.)
- [ ] Create web interface for easier interaction
- [ ] Add task result caching
- [ ] Implement dynamic agent role assignment
- [ ] Add integration with external data sources

## 📚 Learning Resources

- [CrewAI Official Documentation](https://docs.crewai.com/)
- [CrewAI GitHub Repository](https://github.com/joaomdmoura/crewAI)
- [Google Gemini API Documentation](https://ai.google.dev/docs)
- [OpenAI API Documentation](https://platform.openai.com/docs)

## 🤝 Contributing

Feel free to fork this project and submit pull requests for improvements:

1. Fork the repository
2. Create a feature branch
3. Make your changes with detailed comments
4. Test your modifications
5. Submit a pull request

## 📄 License

This project is for educational and demonstration purposes. Please ensure compliance with the terms of service of your chosen LLM provider.

## 👨‍💻 Author

**Tayyab**
Date: September 2025

---

*Happy coding with CrewAI! 🎉*