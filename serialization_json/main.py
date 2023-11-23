from enum import Enum


class Alignment(Enum):
    HORIZONTAL = 1
    VERTICAL = 2


class Widget:

    def __init__(self, parent):
        self.parent = parent
        self.children = []
        if self.parent is not None:
            self.parent.add_child(self)

    def add_child(self, child: "Widget"):
        self.children.append(child)

    def to_json(self):
        return {
            "type": self.__class__.__name__,
            "children": [child.to_json() for child in self.children]
        }

    @classmethod
    def from_json(cls, data):
        if "type" in data:
            class_name = data["type"]
            if class_name == "MainWindow":
                return MainWindow.from_json(data)
            elif class_name == "Layout":
                return Layout.from_json(data)
            elif class_name == "LineEdit":
                return LineEdit.from_json(data)
            elif class_name == "ComboBox":
                return ComboBox.from_json(data)
        return None

    def __str__(self):
        return f"{self.__class__.__name__}{self.children}"

    def __repr__(self):
        return str(self)


class MainWindow(Widget):

    def __init__(self, title: str):
        super().__init__(None)
        self.title = title

    def to_json(self):
        data = super().to_json()
        data["title"] = self.title
        return data

    @classmethod
    def from_json(cls, data):
        title = data.get("title", "")
        new_main_window = MainWindow(title)
        for child_data in data.get("children", []):
            child = Widget.from_json(child_data)
            if child:
                new_main_window.add_child(child)
        return new_main_window


class Layout(Widget):

    def __init__(self, parent, alignment: Alignment):
        super().__init__(parent)
        self.alignment = alignment

    def to_json(self):
        data = super().to_json()
        data["alignment"] = self.alignment.name
        return data

    @classmethod
    def from_json(cls, data):
        alignment = Alignment[data["alignment"]]
        new_layout = Layout(None, alignment)
        for child_data in data.get("children", []):
            child = Widget.from_json(child_data)
            if child:
                new_layout.add_child(child)
        return new_layout


class LineEdit(Widget):

    def __init__(self, parent, max_length):
        super().__init__(parent)
        self.max_length = max_length

    def to_json(self):
        data = super().to_json()
        data["option"] = self.max_length
        return data

    @classmethod
    def from_json(cls, data):
        max_length = data.get("option")
        return LineEdit(None, max_length)


class ComboBox(Widget):

    def __init__(self, parent, items):
        super().__init__(parent)
        self.items = items

    def to_json(self):
        data = super().to_json()
        data["items"] = self.items
        return data

    @classmethod
    def from_json(cls, data):
        items = data.get("items", [])
        return ComboBox(None, items)


app = MainWindow("Application")
layout1 = Layout(app, Alignment.HORIZONTAL)
layout2 = Layout(app, Alignment.VERTICAL)

edit1 = LineEdit(layout1, 20)
edit2 = LineEdit(layout1, 30)

box1 = ComboBox(layout2, [1, 2, 3, 4])
box2 = ComboBox(layout2, ["a", "b", "c"])

print(f"The app: {app}")

app_json = app.to_json()
print("Serialized to json:", app_json)

new_app = Widget.from_json(app_json)
print("Deserialized from json:", new_app)

print(new_app.children[1].children[1].items)  # ['a', 'b', 'c']
