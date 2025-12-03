import asyncio
import os
import sys
import ollama
import json
from datetime import datetime

# Add mcp_server to path
sys.path.append(os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "mcp_server"))
import server

class SQLAgent:
    def __init__(self):
        self.feedback_file = os.path.join(os.path.dirname(__file__), "feedback.json")
        if not os.path.exists(self.feedback_file):
            with open(self.feedback_file, "w") as f:
                json.dump([], f)

    async def get_context(self):
        # Direct call to server module (Simulating MCP connection)
        schema_content = server.get_schema()
        rules_content = server.get_business_logic()
        return schema_content, rules_content

    def save_feedback(self, query: str, sql: str, rating: str):
        """Saves user feedback to a JSON file."""
        entry = {
            "query": query,
            "sql": sql,
            "rating": rating,
            "timestamp": datetime.now().isoformat()
        }
        
        try:
            with open(self.feedback_file, "r") as f:
                data = json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            data = []
            
        data.append(entry)
        
        with open(self.feedback_file, "w") as f:
            json.dump(data, f, indent=2)
            
    def get_few_shot_examples(self) -> str:
        """Retrieves 'Good' examples for few-shot prompting."""
        try:
            with open(self.feedback_file, "r") as f:
                data = json.load(f)
                
            # Filter for "Good" ratings
            good_examples = [d for d in data if d.get("rating") == "Good"]
            
            # Take last 3 examples
            recent_examples = good_examples[-3:]
            
            if not recent_examples:
                return ""
                
            examples_text = "\n### Examples of Correct SQL (Few-Shot Learning)\nUse these examples as a reference for style and logic:\n"
            for ex in recent_examples:
                examples_text += f"\nUser: {ex['query']}\nSQL:\n{ex['sql']}\n"
                
            return examples_text
        except Exception:
            return ""

    async def generate_sql(self, user_query: str, history: list = []) -> str:
        schema, rules = await self.get_context()
        few_shot_examples = self.get_few_shot_examples()
        
        # System Prompt
        system_prompt = f"""
You are an expert SQL generator for the 'ccs-aquila-tahoe' database.

### Database Schema
{schema}

### Available Views (Virtual Tables)
The following **VIEWS** are already created in the database. You can query them directly.
**DO NOT attempt to define them using `WITH`.**

1. `nontest_user`: View of users excluding test domains.
2. `nontest_customer`: View of customers excluding test workspaces.
3. `dsdefinedacct`: View of platform account details.
4. `active_sub`: View of active subscriptions.
5. `active_dev`: **PRIMARY VIEW** for device queries. Contains `serial_number`, `BU_device_type`, `application_name`, etc.

{few_shot_examples}

### Instructions
1. **Start your query directly with `SELECT`**.
2. **DO NOT** write `WITH nontest_user AS...`. These views already exist.
3. Use `active_dev` for queries related to devices, types, or apps.
4. Always filter by `if_test_workspace = 'non Test Workspace'` unless asked for test data.
5. Return **ONLY** the valid SQL query.
"""
        
        # Construct Messages
        messages = []
        
        # Add history (ensure valid roles)
        for msg in history:
            if msg.get('role') in ['user', 'assistant']:
                messages.append(msg)
        
        # Embed System Prompt into the User Message
        user_content = f"""{system_prompt}

User Request: {user_query}

IMPORTANT: 
1. Treat `active_dev`, `nontest_user`, etc., as **EXISTING VIEWS**.
2. **DO NOT** define them.
3. Start your query directly with `SELECT` (or `WITH` for *new* CTEs only).
"""
        messages.append({'role': 'user', 'content': user_content})
        
        print(f"--- MESSAGES SENT TO OLLAMA (llama3) ---\n{messages}\n---------------------------")
        
        try:
            response = ollama.chat(model='llama3', messages=messages, options={
                'num_ctx': 16384,
                'num_predict': 8192,
                'temperature': 0.1
            })
            
            sql_response = response['message']['content']
            
            # Clean up response if it contains markdown code blocks
            if "```sql" in sql_response:
                sql_response = sql_response.split("```sql")[1].split("```")[0].strip()
            elif "```" in sql_response:
                sql_response = sql_response.split("```")[1].split("```")[0].strip()

            # --- CTE INJECTION LOGIC (OPTIMIZED) ---
            # Extract standard CTEs from rules
            standard_ctes = ""
            if "```sql" in rules:
                standard_ctes = rules.split("```sql")[1].split("```")[0].strip()
            
            if standard_ctes:
                print("--- PREPENDING STANDARD CTES ---")
                
                # If generated SQL starts with WITH, merge
                if sql_response.upper().startswith("WITH"):
                    # Remove 'WITH' from generated SQL and prepend standard CTEs + comma
                    generated_ctes = sql_response[4:].strip()
                    sql_response = f"{standard_ctes},\n{generated_ctes}"
                else:
                    # Just prepend standard CTEs
                    sql_response = f"{standard_ctes}\n{sql_response}"
            # ---------------------------
                
            return sql_response
            
        except Exception as e:
            print(f"Error calling Ollama: {e}")
            return f"-- Error generating SQL: {str(e)}"
