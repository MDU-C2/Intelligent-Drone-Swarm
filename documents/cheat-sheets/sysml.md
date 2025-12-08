# SysML Diagram Description Template

---

## 🧩 Block Definition Diagram (BDD)

**Diagram Name:**  
<insert name here>

**Purpose:**  
<state what this diagram is meant to show — e.g., overall system structure, high-level relationships, inheritance, etc.>

### Blocks & Stereotypes
- **<BlockName>** «stereotype»  
  • **Description:** <brief explanation of its role>  
  • **Attributes (optional):**  
    - <name>: <type>  
  • **Operations (optional):**  
    - <operationName()>

(repeat for each block)

### Relations
1. `<BlockA>` —(**relation type**)→ `<BlockB>` [multiplicity]  
   • **Rationale:** <why this relationship exists>  

2. ... (add more relations as needed)

---

## ⚙️ Internal Block Diagram (IBD)

**Diagram Name:**  
<insert name here>

**Context Block:**  
<name of the block this IBD represents internally>

**Purpose:**  
<describe what internal structure this diagram represents — e.g., data flow, component interaction, etc.>

### Internal Parts (Properties)
- **<part name>**: <BlockName> [multiplicity]  
  • **Role:** <short role description>

### Connectors
1. `<partA.portX>` ↔ `<partB.portY>` : <connection type or signal>  
   • **Rationale:** <why this connection exists>

2. ... (add more connectors as needed)

### Ports (optional)
- **<port name>**: <FlowType> [direction: in/out/inout]  
  • **Description:** <short note>

---

## ✍️ Notes (optional)
<add any additional clarifications, constraints, assumptions, or questions here>
