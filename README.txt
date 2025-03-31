    regular ::= 'ε' | alternative
alternative ::= sequence {'|' sequence}
   sequence ::= element {element}
    element ::= symbol | '(' alternative ')' | '[' alternative ']' | '{' alternative '}'