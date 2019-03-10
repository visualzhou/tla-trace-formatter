from lark import Lark, Transformer, v_args
import jinja2

class TreeToString(Transformer):
    def __init__(self, text):
        self.text = text

    def get_str(metd):
        return self.text[meta.start_pos:meta.end_pos] if not meta.empty else ""

    @v_args(meta=True)
    def show_text(self, children, meta):
        return self.text[meta.start_pos:meta.end_pos] if not meta.empty else ""

    # Stop at "value" rule and return the string under it.
    value = show_text
    state_name = show_text

    def state(self, children):
        print(children[0])
        return (children[0], children[1:])

class State:
    def __init__(self, name, variables):
        self.name = name
        self.variables = variables

def parse_output(text):
    with open("output-grammar.lark", "r") as grammar:
        parser = Lark(grammar, start='behavior', propagate_positions=True)
        tree = parser.parse(text)
        print(tree.pretty())
        result = TreeToString(text).transform(tree)
        print(result)
        return result

def generate_html(states):
    env = jinja2.Environment(
        loader=jinja2.FileSystemLoader(searchpath="./"),
        autoescape=jinja2.select_autoescape(['html', 'xml'])
    )
    template = env.get_template("template.html")
    print(template.render(states=states, header=states[0].variables.keys()))


def test_html():
    state = State("State 1", {"log": "<here is log>", "term": "terms"})
    generate_html([state, state])

def main():
    # with open("tla.out", "r") as tla_output:
    #     text = tla_output.read()
    #     behavior = parse_output(text)
    test_html()

if __name__ == "__main__":
    main()
