# Planner
| Name | ID |
| - | - |
| Plan ID | -FjOsRy-VUum89rh3vkTmJYAD-J3 |
| Bucket ID "Planned" | 2QXh8mOxM0C7stZ9S5tGEZYAMKjo |
| Bucket ID "In Progress" | aPcauA28AUOgEAhTDweT0pYABBVG |
| Bucket ID "Done" | scInLrRWhkiie7Eiwp98DJYAA7y1 |

# Excel
## Format every other row
<ol>
  <li>Select rows</li>
  <li>Go to Conditional Formatting → New Rule...</li>
  <li>Select "Use a formula to determine which cells to format"</li>
  <li>Insert <i>=MOD(ROW();2)=0</i> under "Format values where this formula is true:"</li>
  <blockquote>This formula will format every even numbered row</blockquote>
  <li>Click on "Format..." and choose how you want every other row to be formatted</li>
</ol>
