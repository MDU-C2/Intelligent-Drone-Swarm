# Rules and Guidelines for Git & GitHub

| Concept | Definition |
| ------- | ---------- |
| Repository (Repo) | Online "folder" on GitHub that stores your project’s files and remembers every change made to them. |
| Local Repository | A copy of the repo on GitHub stored locally on your computer, where you can work on files and track changes before syncing with the online "folder". |
| Commit | Save changes on your computer's local repo. |
| Push | Move/Save local commits to branch on repository. |
| Pull | Apply commits from same branch on repo to local branch. |
| Pull Request (PR) | Request to merge branch in to another branch. |

## Commit Standards
- Commits should be small, focused, and logically grouped.
- Commit messages must:
  - Use imperative mood (e.g., ''Add login validation'' instead of ''Added login validation'').
  - Clearly describe the purpose of the change.
- When committing work (locally), always write a clear and structured commit message.
- Follow this format:
  - Under "Commit message"/"Summary" the text should be structured as "*`type`* *`short summary`*"
  - *`type`*:
    - Add (when creating or uploading a file)
    - Update (when a big change was done)
    - Rename (rename or move file)
    - Style (when an irrelevant change was done, such asspacing, spelling, etc.) 
  - *`short summary`*:
    - Keep it short and use imperative mood (e.g., “Add test case for login” not “Added” or “Adding”).
  - Then under "Extended description" write a more detailed explanation if needed. Keep the text in imperative mood.
  - Full example:
    - *Commit message/Summary/git commit -m:* `Add function get-ids`
    - *Extended description/Description:*
      - `Add id-list.py`
      - `Update database-functions.py`
      - `Style main.py`

## Pull Requests
- All changes to the `main` branch must go through a Pull Request (PR).
- A PR may only be merged if it has been reviewed and approved by two people, none of whom may be the author of the change.
- All PRs must include:
  - A clear description of the change and its purpose.
  - References to related activities or tasks.
- The author of the PR is responsible for resolving all review comments before merging.
- Squash merges are preferred to keep the commit history clean, unless there is a reason to preserve individual commits.


## Branching Strategy
- The main branch should be seen as the <b><ins>public-ready</ins></b> state of the project.
- All changes must be done in feature branches.
  - Naming convention: feature/<short-description> (e.g., `feature/id-list`).
- Optionally, a develop branch may be used to integrate multiple changes before merging into main.
  - This branch represents the ''next public-ready candidate.''
  - There can only be one develop branch at a time.
- Branches should be deleted after merging to avoid clutter.