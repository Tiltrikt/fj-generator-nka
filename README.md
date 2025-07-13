This program generates a Nondeterministic Finite Automaton (NFA) by parsing an input regular expression. For more details, please refer to the [documentation](/documentation)

```
    regular ::= 'ε' | alternative
alternative ::= sequence {'|' sequence}
   sequence ::= element {element}
    element ::= symbol | '(' alternative ')' | '[' alternative ']' | '{' alternative '}'
```
