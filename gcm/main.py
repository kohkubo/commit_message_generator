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

    prompt = f"Given the following git diff, suggest a concise and informative commit message that summarizes the changes made:\n{git_diff}\nCommit message:"
    response = openai.Completion.create(
        engine="davinci-codex",
        prompt=prompt,
        max_tokens=10,
        n=1,
        stop=None,
        temperature=0.5,
    )

    message = response.choices[0].text.strip()
    return message

def main():
    api_key = get_api_key()
    git_diff = get_git_diff()
    commit_message = generate_commit_message(api_key, git_diff)
    print(commit_message)

if __name__ == "__main__":
    main()
