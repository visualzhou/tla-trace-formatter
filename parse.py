from lark import Lark, Transformer, v_args

text = 'log = (N1 :> <<>> @@ N2 :> <<>> @@ N3 :> <<>> @@ N4 :> <<>> @@ N5 :> <<>>)'

text2 = r"""
state = ( N1 :> Leader @@
         N2 :> Follower @@
         N3 :> Follower @@
         N4 :> Follower @@
         N5 :> Follower )
"""

text3 = r"""
/\ globalCurrentTerm = 1
/\ log = (N1 :> <<>> @@ N2 :> <<>> @@ N3 :> <<>> @@ N4 :> <<>> @@ N5 :> <<>>)
"""

text4 = r"""
log = (N1 :> <<>> @@ N2 :> <<>> @@ N3 :> <<>> @@ N4 :> <<>> @@ N5 :> <<>>)
"""

text5 = r"""
/\ globalCurrentTerm = 0
/\ log = (N1 :> <<>> @@ N2 :> <<>> @@ N3 :> <<>> @@ N4 :> <<>> @@ N5 :> <<>>)
/\ state = ( N1 :> Follower @@
  N2 :> Follower @@
  N3 :> Follower @@
  N4 :> Follower @@
  N5 :> Follower )
/\ commitPoint = ( N1 :> [index |-> 0, term |-> 0] @@
  N2 :> [index |-> 0, term |-> 0] @@
  N3 :> [index |-> 0, term |-> 0] @@
  N4 :> [index |-> 0, term |-> 0] @@
  N5 :> [index |-> 0, term |-> 0] )
"""

text6 = r"""
[index |-> 0, term |-> 0]
"""

class TreeToString(Transformer):
    def __init__(self, text):
        self.text = text

    @v_args(meta=True)
    def show_text(self, children, meta):
        return self.text[meta.start_pos:meta.end_pos] if not meta.empty else ""

    # Stop at "value" rule and return the string under it.
    value = show_text

    def delegate_to_children(self, children):
        return children

    states = delegate_to_children
    statement = delegate_to_children

def parse_output(text):
    with open("output-grammar.lark", "r") as grammar:
        parser = Lark(grammar, start='states', propagate_positions=True)
        return parser.parse(text)


def main():
    tree = parse_output(text5)
    print(tree.pretty())
    print(TreeToString(text5).transform(tree))

main()