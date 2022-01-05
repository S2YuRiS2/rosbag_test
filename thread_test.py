import threading
from time import sleep


def main():
    t = Test()
    t.go()
    try:
        join_threads(t.threads)
    except KeyboardInterrupt:
        print("\nKeyboardInterrupt catched.")
        print("Terminate main thread.")
        print("If only daemonic threads are left, terminate whole program.")


class Test(object):
    def __init__(self):
        self.running = True
        self.threads = []

    def foo(self):
        while(self.running):
            print('\nHello\n')
            sleep(2)

    def get_user_input(self):
        while True:
            x = input("Enter 'e' for exit: ")
            if x.lower() == 'e':
               self.running = False
               break

    def go(self):
        t1 = threading.Thread(target=self.foo)
        t2 = threading.Thread(target=self.get_user_input)
        # Make threads daemonic, i.e. terminate them when main thread
        # terminates. From: http://stackoverflow.com/a/3788243/145400
        t1.daemon = True
        t2.daemon = True
        t1.start()
        t2.start()
        self.threads.append(t1)
        self.threads.append(t2)


def join_threads(threads):
    """
    Join threads in interruptable fashion.
    From http://stackoverflow.com/a/9790882/145400
    """
    for t in threads:
        while t.is_alive():
            t.join(5)
            # print(t)


if __name__ == "__main__":
    main()