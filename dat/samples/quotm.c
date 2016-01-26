/*
 * quotm.c
 *
 * quotm - Manage your quotations library.
 * Copyright (c) 2015 Ammon Smith
 * 
 * quotm is free software: you can redistribute it and/or modify
 * it under the terms of the GNU General Public License as published by
 * the Free Software Foundation, either version 2 of the License, or
 * (at your option) any later version.
 * 
 * quotm is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU General Public License for more details.
 * 
 * You should have received a copy of the GNU General Public License
 * along with quotm.  If not, see <http://www.gnu.org/licenses/>.
 */

#include <libgen.h>
#include <stdbool.h>
#include <stdlib.h>
#include <stdio.h>

#include "arguments.h"
#include "sighandler.h"
#include "quotm.h"

char* secure_getenv(const char* var);
static const char* determine_editor();

const char* program_name;

int main(int argc, const char* argv[])
{
    /* Set up signal handlers */
    set_up_handlers();

    /* Discover name of the executable */
    program_name = basename((char*)argv[0]);

    /* Parse command line arguments */
    options* options = parseargs(argc, argv);

    /* Load program settings */
    options->editor = determine_editor();

    printf("$ %s %s\n", options->editor, options->file);

    return 0;
}

/*
 * Safely exit the application.
 */
void cleanup(int ret)
{
    exit(ret);
}

/*
 * Determine which editor to use.
 * If the user has $VISUAL set, then use that. Otherwise use $EDITOR.
 * As a last resort, use vi and hope that it's installed. If they don't
 * even have vi, god help them.
 */
static const char* determine_editor()
{
    char* editor = secure_getenv("VISUAL");
    if (!editor) {
        editor = secure_getenv("EDITOR");
        if (!editor) {
            editor = "vi";
        }
    }

    return editor;
}

