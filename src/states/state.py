class State:

    def __init__(self, game):
        self.game = game

    def enter(self):
        """Called when entering this state."""
        pass

    def exit(self):
        """Called when leaving this state."""
        pass

    def handle_events(self, events):
        pass

    def update(self, dt):
        pass

    def draw(self, screen):
        pass