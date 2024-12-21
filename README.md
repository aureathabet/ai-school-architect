# AI School Architect

## Overview

AI School Architect is an innovative platform designed to orchestrate AI agents that perform various educational tasks. These tasks include research, code review, testing, and coding, all aimed at enhancing productivity by delegating specific tasks to specialized agents. The platform streamlines workflows and ensures accuracy and efficiency in educational content creation and management.

## LLM Graph Capabilities

The core of the AI School Architect is its LLM (Large Language Model) graph, which is a sophisticated workflow engine that manages the interaction between different AI agents. The graph is built using the `StateGraph` from the `langgraph` library and includes nodes for research, coding, reviewing, and supervision. Each node represents a specialized agent that performs tasks based on the input it receives.

### Key Features

- **Custom Agent Creation**: Develop new custom agents to match specific workflow needs, such as automating repetitive tasks or integrating with specific APIs.
- **Advanced Task Automation**: Enhance agents to perform complex tasks like data analysis, report generation, and project management.
- **Context-Aware Assistance**: Enable agents to understand the context of tasks better, offering more accurate suggestions and task executions.
- **Collaboration Features**: Implement tools that facilitate better collaboration among team members.
- **Continuous Improvement**: Integrate feedback loops for agents to learn from their actions and improve over time.

## Building and Launching with Docker Compose

To build and launch the application using Docker Compose, follow these steps:

1. **Clone the Repository**: Ensure you have the repository cloned to your local machine.

2. **Navigate to the Project Directory**: Open a terminal and navigate to the root directory of the project.

3. **Build the Docker Image**: Run the following command to build the Docker image:
   ```bash
   docker-compose build
   ```

4. **Launch the Application**: Start the application using Docker Compose:
   ```bash
   docker-compose up
   ```

5. **Access the Application**: Once the application is running, you can access it by navigating to `http://localhost:8080/playground` in your web browser.

## Input Format for Grade Level and Topic

When creating lessons or tasks, the input should be formatted as a JSON object with the following structure:
```
{
"grade_level": "<number>",
"topic": "<topic>"
}
```
- **grade_level**: A numerical value representing the educational grade level.
- **topic**: A string representing the subject or topic of the lesson.

This format is used to guide the AI agents in generating content that is appropriate for the specified grade level and topic.

Some example outputs are present in the `app/projects` folder.