"""
Text Editor Feature:

1. Insert 
2. Delete
3. Move Cursor
4. Undo
5. Redo

"""

class Momento:
    def __init__(self, text, current_position):
        self.text = text
        self.current_position = current_position
    
class TextEditor:
    def __init__(self):
        self.text = ""
        self.current_position = 0
        self.redo = []
        self.undo = []
    
    def insert(self, text_to_insert):
        self.text = self.text[:self.current_position] + text_to_insert + self.text[self.current_position:]
        self.current_position += len(text_to_insert)
        self.save_state()
    
    def save_state(self):
        self.undo.append(Momento(self.text, self.current_position))
    
    def delete(self):
        if self.current_position <= 0:
            return
        self.text = self.text[:self.current_position-1] + self.text[self.current_position:]
        self.current_position -= 1
        self.save_state()
    
    def Undo(self):
        if len(self.undo) > 1:
            self.redo.append(self.undo.pop())
            self.text = self.undo[-1].text
            self.current_position = self.undo[-1].current_position
    
    def Redo(self):
        if len(self.redo) > 1:
            self.undo.append(self.redo.pop())
            self.text = self.redo[-1].text
            self.current_position = self.redo[-1].current_position

    def move_cursor_left(self):
        if (self.current_position) > 0:
            self.current_position -= 1
    
    def move_cursor_right(self):
        if self.current_position < len(self.text):
            self.current_position += 1

    def display(self):
        print(self.text)
        print(self.current_position)

text_editor = TextEditor()
text_editor.insert('a')
text_editor.insert('b')
text_editor.insert('c')

text_editor.delete()

text_editor.move_cursor_left()
text_editor.move_cursor_left()

text_editor.Undo()
text_editor.Redo()
text_editor.display()