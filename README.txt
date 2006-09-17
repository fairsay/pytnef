This package contains:

- a wrapper to the unix tnef command-line tool (using Python 2.4 subprocess module); see http://tnef.sourceforge.net

- a simple parser built using pyparsing (http://pyparsing.wikispaces.com) that extracts HTML from TNEF-encoded RTF message body sometimes found in email messages sent by MS Outlook

Todo:

Interface directly with the tnef code. Another nice option would be adding some code to interface with the ytnef library. Furthermore, it would be nice to have these compiled for Win32 platform, or otherwise acquire ability to decode tnef on Windows, without having a copy of MS Outlook. Perhaps integrate with the WMDecode program from Steve Beadle (http://www.biblet.com). Not sure if WMDecode just extracts files (vs. body extraction).

Non-maintained stuff:

- conversion of a Ruby tnef library (in turn based on a C version) to Python; see the "lib" directory of the 0.2 tag. Since interfacing with the unix command does all I need, this pure-Python library has not received any effort. Nor will I have time to work on it. Feel free to pick up the code. 