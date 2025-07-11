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

class LeafNode(HTMLNode):
    def __init__(self, tag, value, props=None):
        super().__init__(tag=tag, value=value, children=None, props=props)
    
    def to_html(self):
        if self.value is None:
            raise ValueError("LeafNode requires a value")
        if self.tag is None:
            return f"{self.value}"
        if self.props is None:
            return f"<{self.tag}>{self.value}</{self.tag}>"
            
        else:
            props_string = ""
            props_string = " ".join(f'{key}="{value}"' for key, value in self.props.items())
            if props_string:
                opening_tag = f"<{self.tag} {props_string}>"
            else:
                opening_tag = f"<{self.tag}>"
            return f"{opening_tag}{self.value}</{self.tag}>"
        

