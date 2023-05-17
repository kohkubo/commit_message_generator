import os
import subprocess
import openai


import logging


def get_git_diff():
    result = subprocess.run(["git", "diff", "--cached"],
                            capture_output=True, text=True)
    return result.stdout


def get_api_key():
    api_key = os.environ.get("OPENAI_API_KEY")
    if not api_key:
        raise ValueError("OPENAI_API_KEY environment variable not set")
    return api_key


def count_tokens(text):
    return len(text.split())


# Error: This model's maximum context length is 4097 tokens. However, your messages resulted in 5388 tokens. Please reduce the length of the messages.
def check_text_length(text):
    count = count_tokens(text)
    if count > 4097:
        logging.warning(
            f"Warning: This model's maximum context length is 4097 tokens. However, your messages resulted in {len(text)} tokens. Please reduce the length of the messages.")
        return False
    return True


def generate_commit_message(api_key, git_diff):
    if not check_text_length(git_diff):
        return ""
    openai.api_key = api_key

    messages = [
        {"role": "system", "content": "\
        You are a talented engineer at Google, and we will use abbreviations to describe basic engineering terms.\n\
        "},
        {"role": "user", "content": f"\
        You are to create a commit message to be used in Git, and the changes will be given to you as git diff --cached.\n\
        First, please describe in words the change in the current situation.\n\
        Next, please suggest five summaries of the change, no more than 50 characters, in a format that is easy to copy-paste because it will be used as the commit message as is.\n\
        Finally, please translate the results into Japanese.\n\
        git diff --cached\n\
        {git_diff}\n\
        "},
    ]
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=messages,
            n=1,
            stop=None,
        )

        message = response.choices[0].message['content'].strip()
        return message
    except Exception as e:
        print(f"Error: {e}")
        if openai.error.RateLimitError == type(e):
            print("アクセス過多です。しばらく待ってから再度実行してください。")
        return ""


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
