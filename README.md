<picture>
  <source media="(prefers-color-scheme: dark)" srcset="https://github.com/MDU-C2/Intelligent-Drone-Swarm/blob/main/images/IDS-logo-white.png">
  <source media="(prefers-color-scheme: light)" srcset="https://github.com/MDU-C2/Intelligent-Drone-Swarm/blob/main/images/IDS-logo-black.png">
  <img alt="IDS Logo" width="500" src="https://github.com/MDU-C2/Intelligent-Drone-Swarm/blob/main/images/IDS-logo-black.png">
</picture>
<h1>Intelligent Replanning Drone Swarm</h1>
<i>Intelligent Replanning Protocol for a Fail-Operational Drone Swarm</i>

<h2>Introduction</h2>
This project addresses the implementation of swarm-level coordination logic that uses detailed health information from all UAVs in the swarm to ensure the overall mission can continue with maximum efficiency, even when individual UAVs are compromised.

<h2>This repository contains</h2>
<ul>
  <li><a href="https://github.com/MDU-C2/Intelligent-Drone-Swarm/tree/main/role-descriptions">Role descriptions</a> for all roles involved</li>
  <li><a href="https://github.com/MDU-C2/Intelligent-Drone-Swarm/tree/main/reference-literature">Reference literature</a> used during the project</li>
  <li><a href="https://github.com/MDU-C2/Intelligent-Drone-Swarm/tree/main/cheat-sheets">Cheat sheets</a> for frequently used HTML tags and GitHub code lines</li>
  <li><a href="https://github.com/MDU-C2/Intelligent-Drone-Swarm/tree/main/protocols">Protocols</a> from daily and weekly meetings</li>
  <li><a href="https://github.com/MDU-C2/Intelligent-Drone-Swarm/tree/main/images">Images</a> used in the project</li>
  <li><a href="https://github.com/MDU-C2/Intelligent-Drone-Swarm/tree/main/project-phases">Project phases</a></li>
  <li><a href="https://github.com/MDU-C2/Intelligent-Drone-Swarm/tree/main/plans">Plans</a></li>
</ul>

<h2>Background</h2>
<b>NOTE: Copied from PDF.</b>

Our previous research, "Design of a Fail-Operational Swarm of Drones for Search and Rescue Missions," introduced a novel conceptual architecture that bridges the critical gap between single-drone fault tolerance and collective drone swarm resilience. The framework's core innovation is a hierarchical design where an onboard Fault Management System (FMS) not only detects internal component failures but also reports the drone's specific health state to the wider swarm. This allows the collective to move beyond simply reacting to a total agent loss. This project addresses the next logical step: implementing the swarm-level coordination logic that uses this detailed health information to ensure the overall mission can continue with maximum efficiency, even when individual units are compromised.

<h2>Task</h2>
<b>NOTE: Copied from PDF.</b>

This project requires students to design, implement, and validate a decentralized protocol for secure and intelligent mission replanning. The primary task is to develop the distributed algorithms that allow the swarm to collectively respond to a drone's broadcasted 'degraded health' status. This involves investigating and implementing a robust consensus mechanism to ensure all agents securely agree on a new plan and designing the logic for re-allocating the compromised drone's tasks (e.g., its search area) to healthy agents. A key challenge is to also re-task the partially failed drone to a less critical but still useful role, such as a communications relay, thereby maximizing the utility of every asset. The final implementation must be validated in a high-fidelity simulation environment using fault-injection techniques to quantitatively measure the improvement in mission continuity.

<h2>Contributors</h2>
See list of <a href="https://github.com/Sir-Camp-A-Lot/Intelligent-Drone-Swarm/blob/main/CONTRIBUTORS.md">contributors</a>.

<h2>Meetings</h2>
<ul>
  <li>"Daily" Meetings, Tuesday - Friday, 8:40 - 9:00
  <ul>
    <li>What did I do yesterday?</li>
    <li>What am I going to do today?</li>
    <li>Are there any obstacles?</li>
  </ul>
  </li>
  <li>Weekly Meetings, Mondays 9:00 - 10:00</li>
  <li>Booked Meetings: 
    <ul>
    <li>2025-09-16, 14:00 - 15:00, Meeting with Luiz to discuss the project</li>  
    </ul>
    </li>
</ul>

<h2>Other</h2>
<ul>
  <li>Every Thursday 13:15 - 15:00: Bowling and other activities at Västerås 9-pin bowling (Lugna gatan 18)</li>
  <li>2026-01-08: Robotics students present their projects at C2</li>
</ul>

<h2>Important links</h2>
<ul>
  <li><a href="https://studentmdh.sharepoint.com/:x:/r/sites/IntelligentDroneSwarm/Delade%20dokument/FLA402-Time-Log.xlsx?d=wba6795dc4c9044099e3155889715a648&csf=1&web=1&e=tto7wd">Time Report</a></li>
  <li><a href="https://planner.cloud.microsoft/webui/v1/plan/-FjOsRy-VUum89rh3vkTmJYAD-J3?tid=a1795b64-dabd-4758-b988-b309292316cf">Kanban (Planner)</a></li>
  <li><a href="https://github.com/MDU-C2/Intelligent-Drone-Swarm/blob/project-plan/images/V-model-V1.png">Our V-model</a></li>
  <li><a href="https://drive.google.com/drive/folders/1vXKNkRGslyUG7h9t5cG3s3EqDK8taNg0?usp=sharing">Google Drive folder</a></li>
</ul>
