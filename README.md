<picture>
  <source media="(prefers-color-scheme: dark)" srcset="https://github.com/MDU-C2/Intelligent-Drone-Swarm/blob/main/images/IDS-logo-white.png">
  <source media="(prefers-color-scheme: light)" srcset="https://github.com/MDU-C2/Intelligent-Drone-Swarm/blob/main/images/IDS-logo-black.png">
  <img alt="IDS Logo" width="500" src="https://github.com/MDU-C2/Intelligent-Drone-Swarm/blob/main/images/IDS-logo-black.png">
</picture>

# Intelligent Replanning Drone Swarm (IRDS)
*Intelligent Replanning Protocol for a Fail-Operational Drone Swarm*

Contributors to this project listed [here](CONTRIBUTORS.md)

## Introduction
This project addresses the implementation of swarm-level coordination logic that uses detailed health information from all UAVs in the swarm to ensure the overall mission can continue with maximum efficiency, even when individual UAVs are compromised.

The project requires students to design, implement, and validate a decentralized protocol for secure and intelligent mission replanning. The primary task is to develop the distributed algorithms that allow the swarm to collectively respond to a UAV's broadcasted 'degraded health' status. This involves investigating and implementing a robust consensus mechanism to ensure all agents securely agree on a new plan and designing the logic for re-allocating the compromised UAV's tasks (e.g., its search area) to healthy agents. A key challenge is to also re-task the partially failed UAV to a less critical but still useful role, such as a communications relay, thereby maximizing the utility of every asset. The final implementation must be validated in a high-fidelity simulation environment using fault-injection techniques to quantitatively measure the improvement in mission continuity.

## Reference Drone
Harris Aerial, Carrier H6HL: <a href ="https://harrisaerial.com/carrier-drones/carrier-h6hl/">Website</a>, <a href ="https://harrisaerial.com/wp-content/uploads/2025/09/H6HL_brochure_final_2025.pdf">Brochure</a>

## This repository contains
- [Cheat sheets](cheat-sheets)
  - LaTeX
  - GitHub
  - HTML
  - ID list
  - Microsoft
  - Risk Assessment
- [Database](database) <i>(and database code)</i>
- Some [images](images) used in the project
- [Project Plan and Management Plans](plans)
- [Protocols](protocols) from daily and weekly meetings
- [Role descriptions](role-descriptions) for all roles involved

## Meetings

### "Daily" Meetings, Tuesday - Friday, 8:40 - 9:00
  - AKA: Daily Scrum
    -  **Yesterday’s achievements:** Describe what you were able to do yesterday.
    -  **Today’s achievements:** Describe what you intend to do today.
    -  **Blockers:** Describe anything that you need answering or unblocking.

### Weekly Meeting, every Mondayy 9:00 - 10:00
  - AKA: Weekly Scrum/Sprint Review
    - **Progress:** Review all tasks done.
    - **Slowed down:** Tasks that have not made the progress we were expecting.
    - **Stopped:** Tasks stopped in their tracks.
  
### Meetings with Luiz
- Every Tuesday 14:00 - 15:00

## Other
- Every Thursday 13:15 - 15:00: Bowling and other activities at Västerås 9-pin bowling (Lugna gatan 18)
- 2026-01-08: Robotics students present their projects at C2. Dependable systems are invited to present their projects too.

## Important links
<ul>
  <li><a href="https://studentmdh.sharepoint.com/sites/IntelligentDroneSwarm/Delade%20dokument/Forms/AllItems.aspx">SharePoint</a></li>
  <ul>
    <li>Documents waiting for review</li>
    <li>Images</li>
    <li>Reference Literature</li>
    <li>Review Protocols</li>
  </ul>
  <li><a href="https://studentmdh.sharepoint.com/:x:/r/sites/IntelligentDroneSwarm/Delade%20dokument/FLA402-Time-Log.xlsx?d=wba6795dc4c9044099e3155889715a648&csf=1&web=1&e=tto7wd">Time Report</a></li>
  <li><a href="https://fla402-ids.atlassian.net/jira/software/projects/IDS/boards/2">Jira</a> (activity and task management + timeline)</li>
  <li><a href="https://drive.google.com/drive/folders/1vXKNkRGslyUG7h9t5cG3s3EqDK8taNg0?usp=sharing">Google Drive folder</a> (used for Draw.io)</li>
  <li><a href="https://github.com/luizgiacomossi/pybullet_search_rescue_uavs">gym-pybullet-drones</a></li>
</ul>
