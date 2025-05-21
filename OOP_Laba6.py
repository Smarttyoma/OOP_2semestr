import json
from abc import ABC, abstractmethod

# ======= PATTERN: Command =======
class Command(ABC):
    @abstractmethod
    def execute(self):
        pass

    @abstractmethod
    def undo(self):
        pass

    @abstractmethod
    def redo(self):
        return self.execute()


class PrintCharCommand(Command):
    def __init__(self, receiver, char):
        self.receiver = receiver
        self.char = char

    def execute(self):
        self.receiver.print_char(self.char)
        return self.receiver.text_buffer

    def undo(self):
        self.receiver.remove_last_char()
        return self.receiver.text_buffer

    def redo(self):
        return self.execute()


class VolumeUpCommand(Command):
    def __init__(self, receiver, step=10):
        self.receiver = receiver
        self.step = step

    def execute(self):
        self.receiver.increase_volume(self.step)
        return f"volume increased +{self.step}%"

    def undo(self):
        self.receiver.decrease_volume(self.step)
        return f"volume decreased +{self.step}%"

    def redo(self):
        return self.execute()


class VolumeDownCommand(Command):
    def __init__(self, receiver, step=10):
        self.receiver = receiver
        self.step = step

    def execute(self):
        self.receiver.decrease_volume(self.step)
        return f"volume decreased +{self.step}%"

    def undo(self):
        self.receiver.increase_volume(self.step)
        return f"volume increased +{self.step}%"

    def redo(self):
        return self.execute()


class MediaPlayerCommand(Command):
    def __init__(self, receiver):
        self.receiver = receiver

    def execute(self):
        self.receiver.launch_media_player()
        return "media player launched"

    def undo(self):
        self.receiver.close_media_player()
        return "media player closed"

    def redo(self):
        return self.execute()


# ======= Receiver (Keyboard) =======
class Keyboard:
    def __init__(self):
        self.key_bindings = {}
        self.undo_stack = []
        self.redo_stack = []
        self.text_buffer = ""
        self.volume = 50
        self.is_media_player_running = False
        self.output = []

    def add_binding(self, key, command):
        self.key_bindings[key] = command

    def execute_command(self, key):
        if key not in self.key_bindings:
            msg = f"Unknown key: {key}"
            self.output.append(msg)
            print(msg)
            return
        cmd = self.key_bindings[key]
        result = cmd.execute()
        self.output.append(result)
        print(result)
        self.undo_stack.append(cmd)
        self.redo_stack.clear()

    def undo(self):
        if not self.undo_stack:
            return
        cmd = self.undo_stack.pop()
        result = cmd.undo()
        self.output.append(result)
        print(result)
        self.redo_stack.append(cmd)

    def redo(self):
        if not self.redo_stack:
            return
        cmd = self.redo_stack.pop()
        result = cmd.redo()
        self.output.append(result)
        print(result)
        self.undo_stack.append(cmd)

    def print_char(self, char):
        self.text_buffer += char

    def remove_last_char(self):
        self.text_buffer = self.text_buffer[:-1]

    def increase_volume(self, step):
        self.volume += step

    def decrease_volume(self, step):
        self.volume -= step

    def launch_media_player(self):
        self.is_media_player_running = True

    def close_media_player(self):
        self.is_media_player_running = False


# ======= PATTERN: Memento =======
class KeyboardStateSaver:
    def save(self, filename, keyboard):
        serialized = {}
        for key, cmd in keyboard.key_bindings.items():
            if isinstance(cmd, PrintCharCommand):
                serialized[key] = {'type': 'print', 'char': cmd.char}
            elif isinstance(cmd, VolumeUpCommand):
                serialized[key] = {'type': 'volume_up', 'step': cmd.step}
            elif isinstance(cmd, VolumeDownCommand):
                serialized[key] = {'type': 'volume_down', 'step': cmd.step}
            elif isinstance(cmd, MediaPlayerCommand):
                serialized[key] = {'type': 'media_player'}
        with open(filename, 'w') as f:
            json.dump(serialized, f)

    def load(self, filename, keyboard):
        try:
            with open(filename, 'r') as f:
                serialized = json.load(f)
            keyboard.key_bindings.clear()
            for key, data in serialized.items():
                if data['type'] == 'print':
                    cmd = PrintCharCommand(keyboard, data['char'])
                elif data['type'] == 'volume_up':
                    cmd = VolumeUpCommand(keyboard, data['step'])
                elif data['type'] == 'volume_down':
                    cmd = VolumeDownCommand(keyboard, data['step'])
                elif data['type'] == 'media_player':
                    cmd = MediaPlayerCommand(keyboard)
                else:
                    continue
                keyboard.add_binding(key, cmd)
        except FileNotFoundError:
            print("State file not found. Starting fresh.")


# ======= Демонстрация =======
def main():
    keyboard = Keyboard()
    saver = KeyboardStateSaver()

    # Привязки клавиш
    keyboard.add_binding('a', PrintCharCommand(keyboard, 'a'))
    keyboard.add_binding('b', PrintCharCommand(keyboard, 'b'))
    keyboard.add_binding('c', PrintCharCommand(keyboard, 'c'))
    keyboard.add_binding('d', PrintCharCommand(keyboard, 'd'))
    keyboard.add_binding('ctrl++', VolumeUpCommand(keyboard, 20))
    keyboard.add_binding('ctrl+-', VolumeDownCommand(keyboard, 20))
    keyboard.add_binding('ctrl+p', MediaPlayerCommand(keyboard))

    # Сохранить текущие привязки
    saver.save("keyboard_state.json", keyboard)

    # Симуляция ввода
    inputs = ['a', 'b', 'c', 'undo', 'undo', 'redo',
              'ctrl++', 'ctrl+-', 'ctrl+p', 'd', 'undo', 'undo']

    for key in inputs:
        if key == 'undo':
            keyboard.undo()
        elif key == 'redo':
            keyboard.redo()
        else:
            keyboard.execute_command(key)

    # Сохранение вывода
    with open("output.txt", "w") as f:
        for line in keyboard.output:
            f.write(f"{line}\n")

    print("\nRestored from file:")
    new_keyboard = Keyboard()
    saver.load("keyboard_state.json", new_keyboard)
    print("Available bindings:", list(new_keyboard.key_bindings.keys()))


if __name__ == "__main__":
    main()
