import multiprocessing
import time


class CLI_Spinner:
    def __init__(self, message: str, speed: float):
        self.message = message
        self.speed = speed

        self.process = multiprocessing.Process(
            target=self.spin, args=(), name="CLI Spinner")

    def spin(self):
        spinner = ['-', '\\', '|', '/']
        n = 0
        while True:
            print(f'\r{spinner[n]} {self.message}', end='')
            n += 1
            if n >= len(spinner):
                n = 0
            time.sleep(self.speed)

    def start(self):
        self.process.start()

    def stop(self):
        # TODO: add condition to avoid exception
        self.process.terminate()
