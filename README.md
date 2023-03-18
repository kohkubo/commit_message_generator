# commit_message_generator

commit_message_generator is a tool to generate commit messages for git.

## Installation

```sh
$ export OPENAI_API_KEY={your openai api key}
$ git clone https://github.com/kohkubo/commit_message_generator.git
$ cd commit_message_generator
$ pip install -e .
```

## Usage

```sh
$ git add .
$ gcm
The diff shows a change in the README file where a new line has been added indicating to add all files before using the gcm command.

Proposed commit messages:
1. Add git command to README
2. Update README
3. Include README instructions
4. Add usage instructions
5. Update usage in README
```
