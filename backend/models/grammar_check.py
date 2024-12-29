import language_tool_python

# Load LanguageTool for English
tool = language_tool_python.LanguageTool("en-US")

def check_grammar(text):
    matches = tool.check(text)
    if not matches:
        return "Your sentence is correct!"
    feedback = " ".join([match.message for match in matches])
    return feedback
