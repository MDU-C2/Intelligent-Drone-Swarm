<img src="https://github.com/MDU-C2/Intelligent-Drone-Swarm/blob/main/IDS-logo.png" alt="IDS-logo.png">
<h1>Intelligent Drone Swarm Protocol</h1>
<i>Intelligent Replanning Protocol for a Fail-Operational Drone Swarm</i>

<h2>Introduction</h2>
This project addresses the implementation of swarm-level coordination logic that uses detailed health information to ensure the overall mission can continue with maximum efficiency, even when individual drones are compromised.

Pre-study

Project plan

<h2>Background</h2>
<b>NOTE: Copied from PDF.</b>

Our previous research, "Design of a Fail-Operational Swarm of Drones for Search and Rescue Missions," introduced a novel conceptual architecture that bridges the critical gap between single-drone fault tolerance and collective drone swarm resilience. The framework's core innovation is a hierarchical design where an onboard Fault Management System (FMS) not only detects internal component failures but also reports the drone's specific health state to the wider swarm. This allows the collective to move beyond simply reacting to a total agent loss. This project addresses the next logical step: implementing the swarm-level coordination logic that uses this detailed health information to ensure the overall mission can continue with maximum efficiency, even when individual units are compromised.

<h2>Task</h2>
<b>NOTE: Copied from PDF.</b>

This project requires students to design, implement, and validate a decentralized protocol for secure and intelligent mission replanning. The primary task is to develop the distributed algorithms that allow the swarm to collectively respond to a drone's broadcasted 'degraded health' status. This involves investigating and implementing a robust consensus mechanism to ensure all agents securely agree on a new plan and designing the logic for re-allocating the compromised drone's tasks (e.g., its search area) to healthy agents. A key challenge is to also re-task the partially failed drone to a less critical but still useful role, such as a communications relay, thereby maximizing the utility of every asset. The final implementation must be validated in a high-fidelity simulation environment using fault-injection techniques to quantitatively measure the improvement in mission continuity.

<h2>Standards</h2>
Standards applied in project:
<ul><li>ISO</li></ul>
<ul><li>ARP</li></ul>

<h2>Contributors</h2>
See list of <a href="https://github.com/Sir-Camp-A-Lot/Intelligent-Drone-Swarm/blob/main/CONTRIBUTORS.md">contributors</a>.
