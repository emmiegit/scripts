#!/usr/bin/env bash
set -eu

usage_and_exit() {
	local program_name="$(basename "$0")"
	printf >&2 'Usage: %s [-t TEMPLATE-NAME] [OPTIONS]\n' "$program_name"
	printf >&2 '       %s --help\n' "$program_name"
	printf >&2 '       %s --list-templates\n' "$program_name"
	exit 1
}

help_and_exit() {
	local program_name="$(basename "$0")"
	printf 'Usage: %s [-t TEMPLATE-NAME] [OPTIONS]\n' "$program_name"
	printf '       %s --help\n' "$program_name"
	printf '       %s --list-templates\n\n' "$program_name"
	cat <<- EOF
	Execution options:
	  -t, --template      TEMPLATE_NAME          Choose default options based on the specified
	                                             templates. You can use --list-templates to get
	                                             a list of in-built template names.
      -o, --output        OUTPUT_FILE            Write the data to a file other than "Makefile".
      -f, --force                                Overwrite an existing Makefile.
      -q, --quiet                                Suppress warning output.
	      --strict                               Do not use default options, but instead quit if
	                                             if a value is not specified.

	Makefile customization options:
	  -c, --compiler      EXECUTABLE_NAME        Specify which compiler to use.
	  -T, --target-file   TARGET                 Specify the name of the target binary object.
	  -S, --src-ext       SOURCE_FILE_EXT        Specify which extension to use for source files.
	  -H, --hdr-ext       HEADER_FILE_EXT        Specify which extension to use for header files.
	  -O, --obj-ext       OBJECT_FILE_EXT        Specify which extension to use for object files.
	  -D, --dep-ext       DEPEND_FILE_EXT        Specify which extension to use for dependency files.
	  -F, --flags         COMPILER_FLAGS         Specify which flags to use every time.
	  -C, --compile-flags COMPILE_FLAGS          Specify which flags to use when creating object files.
	  -L, --link-flags    LINKER_FLAGS           Specify which flags to use when linking.
	  -d, --debug-flags   DEBUG_FLAGS            Specify which flags to use in debug mode.

	Program options:
	  --help                                     Print this help message.
	  --list-templates                           Print a list of templates and their options.
	EOF

	exit 0
}

list_templates_and_exit() {
	cat <<- EOF
	Available templates and their default options:
	  c         For projects using ANSI C.
                 Compiler:         gcc
                 Source extension: c
                 Header extension: h
                 Object extension: o
                 Depend extension: d
                 Flags:            -pipe -O3 
                 Compile flags:    -ansi -Wall -Wextra
                 Linking flags:    
                 Debug flags:      -g

	  c++       For projects using C++.
                 Compiler:         g++
                 Source extension: cpp
                 Header extension: hpp
                 Object extension: cpp.o
                 Depend extension: d
                 Flags:            -pipe -O3 
                 Compile flags:    -std=c++11 -Wall -Wextra
                 Linking flags:    
                 Debug flags:      -g
	EOF
}

requires_an_argument() {
	if [[ $# -lt 2 ]]; then
		printf >&2 '%s requires an argument.\n' "$1"
		usage_and_exit
	fi
}

set_defaults() {
	# Options for the program
	FORCE=false
	STRICT=false
	QUIET=false
	TEMPLATE=
	OUTPUT=Makefile

	# Options for make
	COMPILER=
	TARGET_NAME=
	SRC_EXT=
	HDR_EXT=
	OBJ_EXT=
	DEP_EXT=
	COMPILE_FLAGS=
	OBJECT_FLAGS=
	LINK_FLAGS=
	DEBUG_FLAGS=
}

set_template_options() {
	[[ -z "$TEMPLATE" ]] && return

	case "$TEMPLATE" in
		c) template_c ;;
		c++) template_c++ ;;
		*)
			printf >&2 'Unknown template: %s. Try --list-templates.\n' "$TEMPLATE"
			exit 1
			;;
	esac
}

template_c() {
	"$QUIET" || echo 'Using template "c".'

	COMPILER=gcc
	SRC_EXT=c
	HDR_EXT=h
	OBJ_EXT=o
	DEP_EXT=d
	COMPILE_FLAGS='-pipe -O3'
	OBJECT_FLAGS='-ansi -Wall -Wextra'
	LINK_FLAGS=
	DEBUG_FLAGS='-g'
}

template_c++() {
	"$QUIET" || echo 'Using template "c++".'

	COMPILER=g++
	SRC_EXT=cpp
	HDR_EXT=hpp
	OBJ_EXT=cpp.o
	DEP_EXT=d
	COMPILE_FLAGS='-pipe -O3'
	OBJECT_FLAGS='-std=c++11 -Wall -Wextra'
	LINK_FLAGS=
	DEBUG_FLAGS='-g'
}

check_arguments() {
	if [[ -z $COMPILER ]]; then
		if ! "$STRICT"; then
			COMPILER=gcc
			"$QUIET" || printf >&2 'No compiler specified, using "%s".\n' "$COMPILER"
		else
			printf >&2 'No compiler specified, quitting.\n'
			exit 1
		fi
	fi

	if [[ -z $TARGET_NAME ]]; then
		if ! "$STRICT"; then
			TARGET_NAME=myprogram
			"$QUIET" || printf >&2 'No output specified, using "%s".\n' "$TARGET_NAME"
		else
			printf >&2 'No output specified, quitting.\n'
			exit 1
		fi
	fi

	if [[ -z $SRC_EXT ]]; then
		if ! "$STRICT"; then
			SRC_EXT=c
			"$QUIET" || printf >&2 'No source extension specified, using "%s".\n' "$SRC_EXT"
		else
			printf >&2 'No source extension specified, quitting.\n'
			exit 1
		fi
	fi

	if [[ -z $HDR_EXT ]]; then
		if ! "$STRICT"; then
			HDR_EXT=h
			"$QUIET" || printf >&2 'No header extension specified, using "%s".\n' "$HDR_EXT"
		else
			printf >&2 'No header extension specified, quitting.\n'
			exit 1
		fi
	fi

	if [[ -z $OBJ_EXT ]]; then
		if ! "$STRICT"; then
			OBJ_EXT=o
			"$QUIET" || printf >&2 'No object extension specified, using "%s".\n' "$OBJ_EXT"
		else
			printf >&2 'No object extension specified, quitting.\n'
			exit 1
		fi
	fi

	if [[ -z $DEP_EXT ]]; then
		if ! "$STRICT"; then
			DEP_EXT=d
			"$QUIET" || printf >&2 'No dependency extension specified, using "%s".\n' "$DEP_EXT"
		else
			printf >&2 'No dependency extension specified, quitting.\n'
			exit 1
		fi
	fi

	if [[ -z $COMPILE_FLAGS ]]; then
		COMPILE_FLAGS='-O3'
	fi

	if [[ -z $OBJECT_FLAGS ]]; then
		OBJECT_FLAGS='-Wall'
	fi

	if [[ -z $LINK_FLAGS ]]; then
		LINK_FLAGS=''
	fi

	if [[ -z $DEBUG_FLAGS ]]; then
		DEBUG_FLAGS='-g'
	fi
}

write_makefile() {
	cat << EOF > "$OUTPUT"
# Makefile
# 
# Available for use under the terms of the MIT License.
#

.PHONY: all debug clean

CC := $COMPILER
CFLAGS += $COMPILE_FLAGS
CCFLAGS += $OBJECT_FLAGS
LDFLAGS += $LINK_FLAGS

SOURCES := \$(wildcard *.$SRC_EXT)
OBJECTS := \$(SOURCES:.$SRC_EXT=.$OBJ_EXT)
DEPENDS := \$(SOURCES:.$SRC_EXT=.$DEP_EXT)
EXE := $TARGET_NAME

all: \$(EXE)

\$(EXE): \$(OBJECTS)
	@echo '[LD]' \$@'
	@\$(CC) \$(CFLAGS) \$(LDFLAGS) -o \$@ \$^

%.$OBJ_EXT: %.$SRC_EXT
	@echo '[CC] \$@'
	@\$(CC) \$(CFLAGS) \$(CCFLAGS) -c -o \$@ \$<

%.$DEP_EXT: %.$SRC_EXT
	@echo '[DEP] \$@'
	@\$(CC) \$(CFLAGS) -MM -MF \$@ \$<

debug:
	make CFLAGS+='$DEBUG_FLAGS'

clean:
	@echo '[CLEAN]'
	@rm -f *.$OBJ_EXT *.$DEP_EXT \$(EXE) core core.* vgcore.*

-include \$(DEPENDS)
EOF
}

parse_arguments() {
	while [[ $# -gt 0 ]]; do
		case "$1" in
			--help)
				help_and_exit
				;;
			--list-templates)
				list_templates_and_exit
				;;
			--)
				break
				;;
			--strict)
				STRICT=true
				;;
			-f)
				FORCE=true
				;;
			--force)
				FORCE=true
				;;
			-o)
				requires_an_argument "$@"
				shift
				OUTPUT="$1"
				;;
			--output)
				requires_an_argument "$@"
				shift
				OUTPUT="$1"
				;;
			-t)
				requires_an_argument "$@"
				shift
				TEMPLATE="$1"
				;;
			--template)
				requires_an_argument "$@"
				shift
				TEMPLATE="$1"
				;;
			-c)
				requires_an_argument "$@"
				shift
				COMPILER="$1"
				;;
			--compiler)
				requires_an_argument "$@"
				shift
				COMPILER="$1"
				;;
			-T)
				requires_an_argument "$@"
				shift
				TARGET_NAME="$1"
				;;
			--target-file)
				requires_an_argument "$@"
				shift
				TARGET_NAME="$1"
				;;
			-S)
				requires_an_argument "$@"
				shift
				SRC_EXT="$1"
				;;
			--src-ext)
				requires_an_argument "$@"
				shift
				SRC_EXT="$1"
				;;
			-H)
				requires_an_argument "$@"
				shift
				HDR_EXT="$1"
				;;
			--hdr-ext)
				requires_an_argument "$@"
				shift
				HDR_EXT="$1"
				;;
			-O)
				requires_an_argument "$@"
				shift
				OBJ_EXT="$1"
				;;
			--obj-ext)
				requires_an_argument "$@"
				shift
				OBJ_EXT="$1"
				;;
			-D)
				requires_an_argument "$@"
				shift
				DEP_EXT="$1"
				;;
			--dep-ext)
				requires_an_argument "$@"
				shift
				DEP_EXT="$1"
				;;
			--F)
				requires_an_argument "$@"
				shift
				COMPILE_FLAGS="$1"
				;;
			--flags)
				requires_an_argument "$@"
				shift
				COMPILE_FLAGS="$1"
				;;
			-C)
				requires_an_argument "$@"
				shift
				OBJECT_FLAGS="$1"
				;;
			--compile-flags)
				requires_an_argument "$@"
				shift
				OBJECT_FLAGS="$1"
				;;
			-L)
				requires_an_argument "$@"
				shift
				LINK_FLAGS="$1"
				;;
			--link-flags)
				requires_an_argument "$@"
				shift
				LINK_FLAGS="$1"
				;;
			-d)
				requires_an_argument "$@"
				shift
				DEBUG_FLAGS="$1"
				;;
			--debug-flags)
				requires_an_argument "$@"
				shift
				DEBUG_FLAGS="$1"
				;;
			-*)
				printf 'Unknown option: %s\n' "$1"
				usage_and_exit
				;;
			*)
				break
				;;
		esac
		shift
	done
}

main() {
	set_defaults
	parse_arguments "$@"
	set_template_options

	if [[ -f $OUTPUT ]] && ! "$FORCE"; then
		printf >&2 '"%s" already exists. Use "--force" to overwrite it.\n' "$OUTPUT"
		exit 1
	fi

	check_arguments
	write_makefile
}

main "$@"

