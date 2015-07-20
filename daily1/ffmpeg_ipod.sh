#!/bin/bash
ffmpeg -f image2 -i output_%03d.png -acodec libfaac -ab 128k -vcodec mpeg4 -b 1200k -mbd 2 -flags +mv4+aic -trellis 2 -cmp 2 -subcmp 2 -s 320x180 -metadata title=X output.mp4
