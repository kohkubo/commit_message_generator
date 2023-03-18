import os
import subprocess
import openai

def get_git_diff():
    result = subprocess.run(["git", "diff", "--cached"], capture_output=True, text=True)
    return result.stdout

def get_api_key():
    api_key = os.environ.get("OPENAI_API_KEY")
    if not api_key:
        raise ValueError("OPENAI_API_KEY environment variable not set")
    return api_key

def generate_commit_message(api_key, git_diff):
    openai.api_key = api_key

    messages = [
        {"role": "system", "content": "\
         You are a talented lead engineer.\n\
         I will throw a git diff --cached, and after explaining the contents of the diff, please propose 5 commit messages of 50 characters or less.\n\
         The proposal format should be plane text and line feed delimited.\n\
         "},
        {"role": "user", "content": f"\n{git_diff}"},
    ]
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=messages,
        max_tokens=1000,
        n=1,
        stop=None,
        temperature=0.5,
    )

    message = response.choices[0].message['content'].strip()
    return message

def main():
    api_key = get_api_key()
    git_diff = get_git_diff()
    if not git_diff:
        print("No git diff found")
        return
    commit_message = generate_commit_message(api_key, git_diff)
    print(commit_message)

if __name__ == "__main__":
    main()
