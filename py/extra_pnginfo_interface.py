GROUP = 'ts_utility_nodes'
CLIP_SNAPSHOT = 'clip_snapshot'
PATH = 'path'
MESSAGE = 'message'

def get_clip_snapshot(extra_pnginfo)->dict:
    return extra_pnginfo[GROUP][CLIP_SNAPSHOT]
     
def set_clip_snapshot(extra_pnginfo, path, message):
    clip_snapshot = extra_pnginfo.setdefault(GROUP, {}).setdefault(CLIP_SNAPSHOT, {})
    clip_snapshot[PATH] = path
    clip_snapshot[MESSAGE] = message