class HTMLNode():
    def __init__(self, tag=None, value=None, children=None, props=None):
        self.tag = tag #tag name
        self.value = value #tag value
        self.children = children #list of child HTML objects
        self.props = props #key value pairs for attributes and values

    def to_html(self):
        raise NotImplementedError
    
    def props_to_html(self):
        return_string = ""
        if self.props is not None:
            for key, value in self.props.items():
                return_string += f" {key}=\"{value}\""
        return return_string
    def __repr__(self):
        return f"Tag:{self.tag} \nValue:{self.value} \nChildren:{self.children} \nProps:{self.props_to_html()}"
    