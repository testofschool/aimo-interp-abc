from pathlib import Path
import fcntl,sys,os
root=Path(__file__).resolve().parents[2]
with (root/'v9-execution/official-upload.lock').open('a') as lock:
    try: fcntl.flock(lock.fileno(),fcntl.LOCK_EX|fcntl.LOCK_NB)
    except BlockingIOError:
        print('HOLD_EXISTING_UPLOADER_LOCK',flush=True);raise SystemExit(3)
    print('BROWSER_ROUTE_SINGLE_UPLOADER_LOCK_HELD pid='+str(os.getpid()),flush=True)
    for line in sys.stdin:
        if line.strip()=='release':break
