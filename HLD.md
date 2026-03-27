# High-Level Design (HLD) Document
## System Architecture
The Dexa system will follow a modular, multi-agent architecture. The main components include:
* **CLI Layer**: Handles user input and output through a terminal interface built with Typer.
* **Agent Layer**: Consists of multiple independent agents, each responsible for a specific task, such as intent classification, planning, profiling, reasoning, visualization, execution, and response synthesis.
* **Orchestration Layer**: Manages the state and execution graph of the agents.
* **Data Layer**: Handles dataset loading, schema detection, and profiling.
* **Execution Layer**: Executes code in a sandboxed environment.
* **Visualization Layer**: Generates visualizations using Plotly.
* **Memory Layer**: Stores session context and conversation history.
* **LLM Abstraction Layer**: Provides an abstraction for multiple LLM providers.

## Component Design
The key components of the system are:
* **Intent Agent**: Classifies and interprets user queries.
* **Planner Agent**: Breaks complex queries into multi-step execution plans.
* **Dataset Profiler Agent**: Analyzes schema, column types, distributions, missing values, and statistical summaries.
* **Reasoning Agent**: Generates insights, detects patterns, and recommends preprocessing strategies.
* **Visualization Agent**: Determines appropriate chart types and generates plotting instructions.
* **Code Execution Agent**: Safely generates and executes Python code in a sandboxed environment.
* **Response Synthesizer Agent**: Combines outputs into clear, structured natural language responses.
* **Orchestrator**: Manages the state and execution graph of the agents.
* **Data Loader**: Loads structured datasets (primarily CSV, extensible to parquet/SQL later).
* **Executor**: Executes code in a sandboxed environment.
* **Renderer**: Generates visualizations using Plotly.
* **Session Manager**: Stores session context and conversation history.
* **LLM Abstraction**: Provides an abstraction for multiple LLM providers.

## Data Flow
The data flow through the system is as follows:
1. The user loads a dataset through the CLI interface.
2. The dataset is analyzed by the Dataset Profiler Agent.
3. The user enters a query through the CLI interface.
4. The query is classified and interpreted by the Intent Agent.
5. The Planner Agent breaks the query into a multi-step execution plan.
6. The Reasoning Agent generates insights and recommends preprocessing strategies.
7. The Visualization Agent determines the appropriate chart types and generates plotting instructions.
8. The Code Execution Agent safely generates and executes Python code in a sandboxed environment.
9. The Response Synthesizer Agent combines the outputs into a clear, structured natural language response.
10. The response is returned to the user through the CLI interface.

## API Design (Conceptual)
The main endpoints are:
* **/load**: Loads a dataset.
* **/query**: Enters a query.
* **/execute**: Executes a code block in a sandboxed environment.
* **/visualize**: Generates a visualization.
* **/response**: Returns a response to the user.

## Database Schema
The key tables and relationships are:
* **Datasets**: Stores information about the loaded datasets.
	+ **id** (primary key): Unique identifier for the dataset.
	+ **name**: Name of the dataset.
	+ **schema**: Schema of the dataset.
* **Queries**: Stores information about the user queries.
	+ **id** (primary key): Unique identifier for the query.
	+ **text**: Text of the query.
	+ **intent**: Intent of the query (e.g., data exploration, preprocessing, ML strategy design).
* **Executions**: Stores information about the code executions.
	+ **id** (primary key): Unique identifier for the execution.
	+ **code**: Code block executed.
	+ **output**: Output of the execution.
* **Visualizations**: Stores information about the generated visualizations.
	+ **id** (primary key): Unique identifier for the visualization.
	+ **type**: Type of visualization (e.g., histogram, scatter plot, boxplot).
	+ **data**: Data used to generate the visualization.
* **Responses**: Stores information about the responses returned to the user.
	+ **id** (primary key): Unique identifier for the response.
	+ **text**: Text of the response.
	+ **query_id** (foreign key): Identifier of the query that generated the response.