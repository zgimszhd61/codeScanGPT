import os
import time,re
os.environ["OPENAI_API_KEY"] = "sk-XXXX"
from openai import OpenAI

def detect(filecontent,file_path):
    client = OpenAI()

    response = client.chat.completions.create(
    model="gpt-3.5-turbo",
    messages=[
        {"role": "system", "content": "You are a helpful assistant designed to detect vulnerability."},
        {"role": "user", "content": """
        You are doing authorized vulnerability testing,let us think step by step ,can you figure out are there any vulnerabilities in code below in 1 sentense ? if Yes , reply one word 'yes' and then the type of vernability and the endpoint of the vernability,else reply one word 'no'
        ------
        {}
        """.format(filecontent)}
    ]
    )
    print(response.choices[0].message.content," ",file_path)

# Read the content of a file
def read_file(file_path):
    try:
        with open(file_path, 'r') as file:
            content = file.read()
            return content
    except FileNotFoundError:
        print("File not found")
        return None
    except IOError:
        print("Error reading file")
        return None

def remove_java_comments(content):
    pattern = r'//.*?$|/\*.*?\*/|\'(?:\\.|[^\\\'])*\'|"(?:\\.|[^\\"])*"'
    cleaned_content = re.sub(pattern, '', content, flags=re.MULTILINE|re.DOTALL)
    return cleaned_content

def traverse_directory(directory):
    for root, dirs, files in os.walk(directory):
        for file in files:
            file_path = os.path.join(root, file)
            #if file_path.endswith(".java") and "Controller" in file_path and not "/internal/" in file_path and not file_path.endswith("Test.java"):
            # if file_path.endswith(".js") or file_path.endswith(".ts"):
            if file_path.endswith(".py"):
                print(file_path)
                file_content = read_file(file_path)
                newContent = remove_java_comments(file_content)
                if newContent != "" and len(newContent)<10000:
                    try:
                        detect(newContent,file_path)
                    except:
                        pass
            
# Example usage
traverse_directory('/Users/a0000/mywork/commonLLM/opensource/mamba-chat/')


