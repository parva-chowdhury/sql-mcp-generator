import asyncio
import os
import sys
import ollama

# Add mcp_server to path
sys.path.append(os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "mcp_server"))
import server

class SQLAgent:
    def __init__(self):
        pass

    async def get_context(self):
        # Direct call to server module (Simulating MCP connection)
        schema_content = server.get_schema()
        rules_content = server.get_business_logic()
        return schema_content, rules_content

    async def generate_sql(self, user_query: str) -> str:
        schema, rules = await self.get_context()
        
        # Construct Prompt
        prompt = f"""
You are an expert SQL generator for the 'ccs-aquila-tahoe' database.
Generate a SQL query for the following user request: "{user_query}"

### Database Schema
{schema}

### Standard Business Logic (CTEs)
{rules}

### Instructions
1. You **MUST** start your query with the **Standard Business Logic CTEs** provided above. Copy them exactly.
2. After the CTEs, write a final `SELECT` statement to answer the user's request.
3. Use the `active_dev` CTE for queries related to active devices, device types, or applications.
4. Always filter by `if_test_workspace = 'non Test Workspace'` unless the user asks for test data.
5. Return **ONLY** the valid SQL query. Do not include markdown formatting, explanations, or code blocks.
"""
        
        print(f"--- PROMPT SENT TO OLLAMA (llama3) ---\n{prompt}\n---------------------------")
        
        try:
            response = ollama.chat(model='llama3', messages=[
                {
                    'role': 'user',
                    'content': prompt,
                },
            ])
            
            sql_response = response['message']['content']
            
            # Clean up response if it contains markdown code blocks
            if "```sql" in sql_response:
                sql_response = sql_response.split("```sql")[1].split("```")[0].strip()
            elif "```" in sql_response:
                sql_response = sql_response.split("```")[1].split("```")[0].strip()
                
            return sql_response
            
        except Exception as e:
            print(f"Error calling Ollama: {e}")
            return f"-- Error generating SQL: {str(e)}"
