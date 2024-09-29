import oss
import g


def to_ts(old_name, new_name):
    """
    使用ffmpeg把视频转ts
    """

    def _to_ts(_old_name, _new_name):
        # ffmpeg -i 3.ts -c copy -map 0:v -map 0:a -bsf:a aac_adtstoasc 3.mp4  // ts-mp4
        # ffmpeg -i 4.mp4 -vcodec copy -acodec copy -vbsf h264_mp4toannexb 4.ts // mp4-ts
        cmd = f'ffmpeg -loglevel quiet -y -i {_old_name} -codec libx264 -vbsf h264_mp4toannexb {_new_name}'
        try:
            oss.system(cmd)
            oss.remove(_old_name)
        except WindowsError as err:
            print('ffmpeg_to_ts error:', err)

    g.go(_to_ts, args=(old_name, new_name))
