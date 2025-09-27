

class HTMLNode:

    def __init__(self, tag=None, value=None, children=None, props=None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def to_html(self):
        raise NotImplementedError("Not implemented")

    def props_to_html(self):
        if not self.props:
            return ""
        return " ".join(f'{k}="{v}"' for k, v in self.props.items())    

    def __eq__(self, other):
        return True if (other.tag == self.tag) and (other.value == self.value) and (other.children == self.children) and (other.props == self.props) else False
    
    def __repr__(self):
        return f"HTMLNode({self.tag},{self.value},{self.children},{self.props})"
    

class LeafNode(HTMLNode):

    def __init__(self, tag, value, props=None):
        super().__init__(tag, value, [], props)

    def to_html(self):
        if self.tag is None:
            if self.value is None:
                raise ValueError("invalid HTML: no value")
            return self.value

        if self.value is None:
            raise ValueError("invalid HTML: no value")

        props = self.props_to_html()
        space = f" {props}" if props else ""

        void_tags = {"img", "br", "hr", "input", "meta", "link"}
        if self.tag in void_tags:
            return f"<{self.tag}{space}>"

        return f"<{self.tag}{space}>{self.value}</{self.tag}>"


class ParentNode(HTMLNode):

    def __init__(self, tag, children, props=None):
        
        if tag is None:
            raise ValueError("Missing required Tag")
        if children is None:
            raise ValueError(f"Children missing")
        
        super().__init__(tag, None, children, props)

    def to_html(self):
        if self.tag is None:
            raise ValueError("invalid HTML: no tag")
        if self.children is None:
            raise ValueError("invalid HTML: no children")

        props = self.props_to_html()
        space = f" {props}" if props else ""

        inner = "".join(child.to_html() for child in self.children)
        return f"<{self.tag}{space}>{inner}</{self.tag}>"