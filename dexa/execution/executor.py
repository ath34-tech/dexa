import sys
import io

class Executor:
    def run(self, code: str, context: dict):
        # redirect stdout
        old_stdout = sys.stdout
        new_stdout = io.StringIO()
        sys.stdout = new_stdout
        
        try:
            exec(code, {}, context)
            sys.stdout = old_stdout
            output = new_stdout.getvalue()
            
            # if no output, provide a summary of context changes
            if not output:
                # filter out private items and long strings
                summary = {k: str(v)[:100] for k, v in context.items() if not k.startswith("__")}
                output = f"Code executed successfully. Context summary: {summary}"
                
            return output
        except Exception as e:
            sys.stdout = old_stdout
            return f"Execution error: {str(e)}"