#!/bin/sh
x_res=1920                              # The resolution of your monitor(s). This assumes both monitors
y_res=1200                              # are the same size.

cd ~/Temporary
maim --opengl --geometry=${x_res}x${y_res}+0+0

