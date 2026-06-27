class Tween:
    def __init__(self, start, end, duration):
        self.start = start
        self.end = end
        self.duration = duration

        self.elapsed = 0.0
        self.finished = False

        self.value = start

    def reset(self):
        self.elapsed = 0.0
        self.finished = False
        self.value = self.start

    def update(self, dt):

        if self.finished:
            return self.value

        self.elapsed += dt

        t = min(self.elapsed / self.duration, 1.0)

        self.value = self.start + (self.end - self.start) * t

        if t >= 1.0:
            self.finished = True

        return self.value