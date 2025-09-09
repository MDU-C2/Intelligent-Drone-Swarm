# Format every other row
<ol>
  <li>Select rows</li>
  <li>Go to Conditional Formatting → New Rule...</li>
  <li>Select "Use a formula to determine which cells to format"</li>
  <li>Insert <i>=MOD(ROW();2)=0</i> under "Format values where this formula is true:"</li>
  <blockquote>This formula will format every even numbered row</blockquote>
  <li>Click on "Format..." and choose how you want every other row to be formatted</li>
</ol>
