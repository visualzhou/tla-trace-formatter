from lark import Lark, Transformer, v_args
import jinja2
import html
import sys

class State:
    def __init__(self, name, variables):
        self.name = name
        self.variables = variables

    def __str__(self):
        return "{0}\n{1}".format(
            self.name,
            " ".join("{0} = {1}".format(k, v) for k, v in self.variables.items()))

    def __repr__(self):
        return self.__str__()

class TreeToStates(Transformer):
    def __init__(self, text):
        self.text = text

    def get_str(self, meta):
        text = self.text[meta.start_pos:meta.end_pos] if not meta.empty else ""
        return html.escape(text).replace("\n", "<br />")

    @v_args(meta=True)
    def show_text(self, children, meta):
        return self.get_str(meta)

    # Stop at "value" rule and return the string under it.
    value = show_text
    state_name = show_text
    # behavior is a list of states.
    behavior = list

    def state(self, children):
        name = children[0]
        variables = {v.children[0]: v.children[1] for v in children[1:]}
        return State(name, variables)

def parse_output(text):
    with open("output-grammar.lark", "r") as grammar:
        parser = Lark(grammar, start='behavior', propagate_positions=True)
        tree = parser.parse(text)
        # print(tree.pretty())
        result = TreeToStates(text).transform(tree)
        # print(result)
        return result

def generate_html(states):
    env = jinja2.Environment(
        loader=jinja2.FileSystemLoader(searchpath="./"),
        # autoescape=jinja2.select_autoescape(['html', 'xml'])
    )
    template = env.get_template("template.html")
    generated = template.render(states=states, header=states[0].variables.keys())
    print(generated)


def test_html():
    state = State("State 1", {"log": "<here is log>", "term": "terms"})
    generate_html([state, state])

def parse_and_generate_html(tla_output_file_name):
    with open(tla_output_file_name, "r") as tla_output:
        text = tla_output.read()
        behavior = parse_output(text)
        generate_html(behavior)

if __name__ == "__main__":
    tla_output_file_name = "tla.out"
    if len(sys.argv) > 1:
        tla_output_file_name = sys.argv[1]
    parse_and_generate_html(tla_output_file_name)

