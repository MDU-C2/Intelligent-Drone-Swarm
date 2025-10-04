<h1>Rules and Guidelines for Git & GitHub</h1>

| Concept | Definition |
| ------- | ---------- |
| Repository (Repo) | Online "folder" on GitHub that stores your project’s files and remembers every change made to them. |
| Local Repository | A copy of the repo on GitHub stored locally on your computer, where you can work on files and track changes before syncing with the online "folder". |
| Commit | Save changes on your computer's local repo. |
| Push | Move/Save local commits to branch on repository. |
| Pull | Apply commits from same branch on repo to local branch. |
| Pull Request (PR) | Request to merge branch in to another branch. |

<h2>Commit Standards</h2>
<ul>
  <li>Commits should be small, focused, and logically grouped.</li>
  <li>Commit messages must:</li>
  <ul>
    <li>Use imperative mood (e.g., ''Add login validation'' instead of ''Added login validation'').</li>
    <li>Clearly describe the purpose of the change.</li>
  </ul>
</ul>

<h3>When committing work (locally), always write a clear and structured commit message.</h3>
Follow this format:
<ul>
  <li>Under "Commit message"/"Summary" the text should be structure shuch as "*type* *short summary*"</li>
  <li>*type*:</li>
  <ul>
    <li> Add (Use this when creating or uploading a file) </li>
    <li> Update (Use this when a big change was done)</li>
    <li> Rename (rename or move file)
    <li> Style (Use this when an irrelevant change was done - Could be spacing, spelling, etc.) </li>
  </ul>
  <li>*short summary*:</li>
    <ul>
    <li> Keep it short and use imperative mood (e.g., “Add test case for login” not “Added” or “Adding”).</li>
  </ul>
  <li>Then under "Extended description" write a more detailed explanation if needed. Keep the text in imperative mood.</li>
  <li>Full example:</li>
  <ul>
    <li><i>Commit message/Summary/git commit -m:</i> "Add function get-ids"</li>
    <li><i>Extended description/Description:</i></li>
    <ul>
      <li>Add id-list.py</li>
      <li>Update database-functions.py</li>
      <li>Style main.py</li>
    </ul>
</ul>









<h2>Pull Requests</h2>
<ul>
  <li>All changes to the <b><ins>main</ins></b> branch must go through a Pull Request (PR).</li>
  <li>A PR may only be merged if:</li>
  <ul>
    <li>It has been approved by the Chief Engineer.</li>
    <li>It has been approved by at least one other reviewer who is not the author of the change.</li>
  </ul>
  <li>All PRs must include:</li>
  <ul>
    <li>A clear description of the change and its purpose.</li>
    <li>References to related activities or tasks.</li>
  </ul>
  <li>The author of the PR is responsible for resolving all review comments before merging.</li>
  <li>Squash merges are preferred to keep the commit history clean, unless there is a reason to preserve individual commits.</li>
</ul>

<h2>Branching Strategy</h2>
<ul>
  <li>The main branch represents the <b><ins>public-ready</ins></b> state of the project and is visible to the public.</li>
  <li>All changes must be done in feature branches.</li>
  <ul>
    <li>Naming convention: feature/<short-description> (e.g., feature/id-list).</li>
  </ul>
  <li>Optionally, a develop branch may be used to integrate multiple changes before merging into main.</li>
  <ul>
    <li>This branch represents the ''next public-ready candidate.''</li>
    <li>There can only be one develop branch at a time.</li>
  </ul>
      <li>Branches should be deleted after merging to avoid clutter.</li>
</ul>
