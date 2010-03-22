from __future__ import print_function

def humanize_seconds(seconds):
    if not isinstance(seconds,int):
        seconds = float(seconds)
    (minutes, seconds) = divmod(seconds, 60)
    (hours, minutes) = divmod(minutes, 60)
    return "%02d:%02d:%02d" % (hours,minutes,seconds)

if __name__ == "__main__":
    import sys
    for arg in sys.argv[1:]:
        print(humanize_seconds(arg))
