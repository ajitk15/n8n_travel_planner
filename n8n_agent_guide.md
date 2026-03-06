# AI Travel Itinerary Planner Document & Guide

## 1. What is n8n?
- **Workflow Automation:** n8n is a powerful, flexible automation tool that allows you to visually connect any app or API together without heavy coding.
- **How Workflows Function:** Workflows consist of "nodes" mapped together on a graphical canvas. A workflow always starts with a `Trigger` node, and the output data from one node flows seamlessly into the next core node down the chain to perform operations on that data.
- **Agentic AI Systems:** By incorporating advanced LangChain nodes, n8n moves beyond rigid, pre-programmed flows to create **Agentic** workflows. The AI becomes the "brain" routing the conversation, reading the user intent, dynamically deciding which external tools to call (like web searches or API hooks), and reasoning entirely on its own to achieve the user's implicit goal.

---

## 2. Types of Nodes in n8n
- **Trigger Nodes:** The starting points of workflows. They launch the flow automatically based on events. 
  - *Example:* A `Chat Trigger` waits for a user to type a message to start an interactive chat session, or a `Webhook` waits for an HTTP request.
- **Action Nodes (Basic Nodes):** Standard nodes performing a single distinct, pre-programmed job. 
  - *Example:* An `HTTP Request` fetching server data, a `Set` node to format outputs, or a `Gmail/SMTP` node to fire an email off in the background.
- **AI Agent Nodes:** The decision-makers that take a connected Language Model (LLM) and a set of system instructions, interacting autonomously to solve prompts. 
  - *Example:* The `Agent` node acts as the conversational travel planner.
- **Language Model Nodes:** The actual AI brains connected to the an Agent. 
  - *Example:* The `OpenAI Chat Model` securely passes instructions to underlying base models like GPT-4o.
- **Memory Nodes:** Nodes that track and store previous interactions so the chatbot can handle follow-up questions natively without losing context. 
  - *Example:* `Window Buffer Memory` stores the last few messages tied uniquely to the current user's chat session ID.
- **Tool Nodes:** Specialized capabilities granted to the Agent so it can interact with the outside world. The agent chooses when to execute these functions.
  - *Example:* The `Search (SerpAPI)` searches live Google results, or the `Calculator` strictly processes tight budgets mathematically.
- **Logic Nodes:** These control the flow of data depending on conditions.
  - *Example:* The `If` node branches the workflow down path A or path B based on checking true/false field values.

---

## 3. Manual Workflow Creation Guide: "AI Travel Itinerary Planner with Email Delivery"
You can manually re-build the specific **AI Travel Itinerary Planner** natively inside your n8n workspace by re-creating the structure defined in your `.json` file. Follow these exact node instructions:

**Step 1: Start the Conversation (Chat Interface)**
- Add a **Chat Trigger** node. 
- **What it does:** This provides the interactive chat window UI for the end-user and automatically passes an ongoing `sessionId` parameter to track the conversation.

**Step 2: Add the Agent Brain**
- Add an **AI Agent** node.
- Name it **Travel Itinerary Planner**.
- Wire the output of the **Chat Trigger** directly into the `Main` input of the Agent.
- **Prompt Setup:** In the options, set the System Message to:
  > *"You are an expert travel planner assistant. Speak naturally with the user to discover their destination, budget, duration, and preferences. Once you have enough information, use your tools (like SerpAPI and Calculator) to generate a detailed day-by-day itinerary. CRITICAL INSTRUCTION: You MUST format the final itinerary exclusively as a Markdown table with exactly these three columns: | Day | Plan | Cost |"*

**Step 3: Connect the LLM**
- Add an **OpenAI Chat Model** node.
- Select your OpenAI Credentials and set the model block to `gpt-4o`.
- Wire the output point straight to the `Language Model` port on your AI Agent.

**Step 4: Enable Chat Memory for the Trip Planning**
- Add a **Window Buffer Memory** node.
- Link it to the `Memory` port of the AI Agent.
- **Configuration:** Click into the node. Change the Session ID setting explicitly to `={{ $('Chat Trigger').item.json.sessionId }}` (or select the "Connected Chat Trigger Node" dropdown). 
- **What it does:** This ensures the AI remembers user budgets and preferences mid-conversation rather than forgetting between messages.

**Step 5: Provide External Tools to the Trip Planner**
- **Tool 1: Search Travel Info**
  - Add a **Search (SerpAPI)** tool and enter your SerpAPI credentials.
  - Wire it into the `Tools` port of your AI Agent. This allows the bot to search current real-world flight prices, top-rated hotels, and active local events instead of halluncinating data.
- **Tool 2: Calculate Costs**
  - Add a **Calculator** tool.
  - Wire it onto the same `Tools` port of the AI Agent. The agent will use this to accurately calculate the day-by-day cost against the user's hard budget limitation without making math errors.

**Summary of Data Flow:**
User inputs text in **Chat Trigger** -> Flows into **Travel Planner Agent** -> The Agent utilizes **OpenAI** to reason, pulls past context from **Window Buffer**, and actively queries **SerpAPI** and the **Calculator** to structure the response mathematically back to the user as a Markdown table.

---

## 4. Sample Prompts for Different Agentic Use Cases
Test out your new chatbot's capabilities natively in the n8n interface using these examples:

### 1. Memory Usage (Window Buffer Context)
*Prompt 1:* "I want to take my partner on a 3-day anniversary trip to Rome. We absolutely despise seafood, and love classical architecture."
*Prompt 2 (Sent immediately after):* "Actually, Paris might be more romantic. Change the destination to Paris, but keep the 3-day duration and the deep food constraints the exact same."

### 2. Tool Calling (Search & Calculate)
*Prompt:* "I have exactly $2,500 for a 4-day trip to London. I want to see a popular play in the West End taking place this month. Use your search to find the price for one, use your calculator to determine how much I'd have left over for a modest hotel, and lay it out in the table."

### 3. Multi-Agent Workflows (Handoffs to Specialists)
*Prompt:* "I need a full content strategy for a new coffee brand. Have your Research Agent find 5 trending coffee topics, have your SEO Agent write the keywords, and then have your Writer Agent generate the blog post drafts."
*(Note: This requires explicitly connecting multiple sub-Agents as 'tools' to one master Supervisor Agent node!)*

### 4. Data Retrieval (Live API Querying)
*Prompt:* "What is the detailed live weather forecast for Helsinki over the coming weekend? Recommend an itinerary entirely based on whether it is going to rain or be sunny."

### 5. Decision-Making Agents (Reasoning)
*Prompt:* "I need to travel from Chicago to Miami next week for a conference. Search for the absolute cheapest travel method, and search for the fastest travel method. Use the calculator to explain the robust time-vs-money difference, and decide which is a better overall value if I value my time specifically at $75 per hour."
