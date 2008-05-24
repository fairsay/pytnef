%module ytnef

%{
#include "/usr/include/ytnef.h"
%}

%include "tnef-types.i"
%include "/usr/include/ytnef.h"


%inline %{

TNEFStruct parseFile(char *filename) {
   TNEFStruct TNEF;
   TNEFInitialize(&TNEF);
   TNEFParseFile(filename, &TNEF);
   return TNEF;
}

MAPIProperty *getMAPIProperty(MAPIProps *p, int i) {
   return &(p->properties[i]);
}

%}

