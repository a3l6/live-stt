from livestt import Recorder, transcribe, wait
import time


filename = "test.wav"

r = Recorder(filename)


def record_and_wait_for_three_seconds():
    r.start()
    time.sleep(3)
    r.end()
    return transcribe(filename)


listener = wait(callback=record_and_wait_for_three_seconds)

for segment in listener:
    print(segment)
