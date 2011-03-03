This is the staging directory for the code demonstrated in the presentation at
the 2011 Developer Summit.

How to make it work:

The Python and TBX files are here and ready to go. You will need to compile the
two Visual Studio projects (in cplusplus and dotnet) and copy the compiled DLLs
into this directory. The cplusplus project depends on the DLL built in the
dotnet project, so build that and copy the DLL into the project directory for
cplusplus so it can correctly import/link it in.
