class HTMLNode():
    def __init__(self, tag=None, value=None, children=None, props=None):
        self.tag = tag #tag name
        self.value = value #tag value
        self.children = children #list of child HTML objects
        self.props = props #key value pairs for attributes and values

    def to_html(self):
        raise NotImplementedError("to_html method not implemented")
    
    def props_to_html(self):
        return_string = ""
        if self.props is not None:
            for key, value in self.props.items():
                return_string += f" {key}=\"{value}\""
        return return_string
    
    def __repr__(self):
        return f"HTMLNode({self.tag}, Value:{self.value}, Children:{self.children}, {self.props_to_html()}"
    


class LeafNode(HTMLNode):
    def __init__(self, tag, value, props=None):
        super().__init__(tag, value, None, props)
    
    def to_html(self):
        if self.value is None:
            raise ValueError("invalid HTML: no value")
        if self.tag is None:
            return self.value
        return f"<{self.tag}{self.props_to_html()}>{self.value}</{self.tag}>"

    def __repr__(self):
        return f"LeafNode({self.tag}, Value: {self.value}, {self.props})"
        
class ParentNode(HTMLNode):
    def __init__(self, tag, children, props=None):
        super().__init__(tag, None, children, props)

    def to_html(self):
        if self.tag is None:
            raise ValueError("invalid HTML: no tag")
        if self.children is None:
            raise ValueError("invalid HTML: no children")
        children_html = ""
        for child in self.children:
            children_html += child.to_html()
        return f"<{self.tag}{self.props_to_html()}>{children_html}</{self.tag}>"
    
    def __repr__(self):
        return f"ParentNode({self.tag}, children: {self.children}, {self.props})"
            