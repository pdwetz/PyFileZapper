PyFileZapper
============

Port of FileZapper (https://github.com/pdwetz/FileZapper) to python, primarily as an exercise of working with that language. Includes basic functionality of the original: given specific folder(s), it will parse all subfolders and files to remove duplicates.

Features:
* Performs a hash only for files it thinks are duplicates (same extension and file size)
* Uses a simple scoring mechanism to determine who the "winner" is
* Sends "losers" to the recycling/trash bin
* Output is verbose (it'll tell you what it's doing to various files)

Missing Features (from C# version):
* No config settings; need to update code to point to desired folder(s) and no support for skipping/deleting specific extensions or folder names
* Single threaded
* No error logging
* No dump of results to CSV file
