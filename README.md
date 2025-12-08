<picture>
  <source media="(prefers-color-scheme: dark)" srcset="https://github.com/MDU-C2/Intelligent-Drone-Swarm/blob/main/images/IDS-logo-white.png">
  <source media="(prefers-color-scheme: light)" srcset="https://github.com/MDU-C2/Intelligent-Drone-Swarm/blob/main/images/IDS-logo-black.png">
  <img alt="IDS Logo" width="500" src="https://github.com/MDU-C2/Intelligent-Drone-Swarm/blob/main/images/IDS-logo-black.png">
</picture>

# Intelligent Replanning Drone Swarm (IRDS)
*Intelligent Replanning Protocol for a Fail-Operational Drone Swarm*

[Contributors in this project](CONTRIBUTORS.md)

[Commonly used terms in the project](documents/cheat-sheets/commonly-used-terms.md)

## Introduction
This project addressed the conceptual design of swarm-level coordination logic that uses detailed health information from all UAVs in a swarm to ensure the overall mission can continue with maximum efficiency, even when individual UAVs are compromised.

The project required students to design and validate a decentralised protocol for secure and intelligent mission replanning. The primary task was to develop concepts for distributed algorithms that allow the swarm to collectively respond to a UAV's broadcasted `degraded health` status, which involved investigating and conceptualising a robust consensus mechanism to ensure all agents securely agree on a new plan and designing the conceptual logic for re-allocating the compromised UAV's tasks (e.g., its sectors) to healthy agents. A key challenge was to also re-task the partially failed UAV to a less critical but still useful role, such as a communications relay, thereby maximising the utility of every asset. Parts of the conceptual system design was implemented and validated using a simulation environment with fault-injections.


## Reference Drone
Harris Aerial, Carrier H6HL: <a href ="https://harrisaerial.com/carrier-drones/carrier-h6hl/">Website</a>, <a href ="https://harrisaerial.com/wp-content/uploads/2025/09/H6HL_brochure_final_2025.pdf">Brochure</a>

## This repository contains
- [Database](database) <i>(and database code)</i>
- [Documents](documents)
  - Pre-Study
  - System Design Description
  - Final Report
  - Release Notes
  - [Cheat sheets](documents/cheat-sheets)
    - Commonly used terms in the project
    - GitHub text formatting + adding/renaming folders
    - HTML text formatting
    - List of IDs used in the project
    - Quality checklist for reports
  - [LaTeX](documents/latex)
    - Instructions on how to use LaTeX locally
    - Template files
    - LaTeX projects
  - [Plans](documents/plans)
    - Project Plan
    - Management Plans
  - [Requirements](documents/requirements)
    - PDF versions of the database
    - Requirements Specification Guide
    - Traceability Matrix: Requirements to System Design Elements
  - [Safety](documents/safety)
    - Preliminary Safety Assurance Case
    - Preliminary Safety Assessment
    - Flight Safety Assessment
    - Safety Assessment
    - Safety Goals & Requirements
    - Safety Assurance Case
  - [Validation & Verification](documents/validation-verification)
    - Validations & Verifications
    - Test Specification
- [Images](images) used in the project
- [Swarm Simulation](swarm-simulation)
  - Code files for simulating a swarm