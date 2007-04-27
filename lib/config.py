"""
This module contains only configuration settings.
"""

# the only way to list tnef body is via --save-body
# that unfortunately also extracts the body"
# we need to set the name statically to be able
# to remove it

TNEF_BODYFILENAME = "__tnef_body"

# default tnef preference is rht
TNEF_BODYPREFERENCE = "rht"

TNEF_DIRECTORY = "__tnef_dir"

TNEF_ARGUMENTS = {
   "contents": "--list",
   "body": "--save-body",
   "directory": "--target-dir",
   "overwrite": "--overwrite",
   "mimeinfo": "--list-with-mime-types",
   "preference": "--body-pref",
}
