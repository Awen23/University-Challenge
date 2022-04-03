import pygame

class Game(object):
    def __init__(self, screen, states, start_state):
        self.done = False # When true, the game will be over and will exit
        self.screen = screen
        self.clock = pygame.time.Clock()
        self.fps = 60
        self.states = states
        self.state_name = start_state
        self.state = self.states[self.state_name]

    def event_loop(self):
        for event in pygame.event.get():
            self.state.get_event(event)

    # When state is done
    # Handles transition to next state
    def flip_state(self):
        current_state = self.state_name
        next_state = self.state.next_state
        self.state.done = False
        self.state_name = next_state
        persistent = self.state.persist # Passes along persistent values
        self.state = self.states[self.state_name]
        # Starts up next state
        self.state.startup(persistent)

    def update(self, dt):
        #self.state.other_states = self.states
        if self.state.quit:
            self.done = True
        elif self.state.done:
            self.flip_state()
        self.state.update(dt)
    
    def draw(self):
        self.state.draw(self.screen)

    def run(self):
        # Main game loop
        while not self.done:
            # Advance game time
            dt = self.clock.tick(self.fps)
            # Handle any events (key presses etc)
            self.event_loop()
            # Flip state
            self.update(dt)
            self.draw()
            pygame.display.update()