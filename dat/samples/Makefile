# Makefile
#
# quotm - Manage your quotations library.
# Copyright (c) 2015 Ammon Smith
# 
# quotm is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 2 of the License, or
# (at your option) any later version.
# 
# quotm is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
# 
# You should have received a copy of the GNU General Public License
# along with quotm.  If not, see <http://www.gnu.org/licenses/>.
#

.PHONY: all clean

CC=gcc
FLAGS=-Wall -Wextra -ansi -I.
OBJECTS=arguments.o  \
		data.o       \
		help.o       \
		quotm.o      \
		sighandler.o

all: quotm

%.o: %.c
	$(CC) $(FLAGS) $(EXTRA_FLAGS) -c -o $@ $<

quotm: $(OBJECTS)
	$(CC) $(FLAGS) $(EXTRA_FLAGS) -o quotm $(OBJECTS)


clean:
	rm -f *.o *.d *~ core
