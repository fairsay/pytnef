from ctypes import *

__all__ = ("TNEFStruct", "dtr", "renddata", "variableLength", "TNEFIOStruct", "MAPIProperty", "Attachment")

DWORD = c_uint # unsigned int
BYTE = c_ubyte   # unsigned char
WORD =  c_ushort # unsigned short int
ULONG = c_uint # unsigned int
#DDWORD unsigned long long


class dtr(Structure):
   _fields_ = [
      ("wYear", WORD),
      ("wMonth", WORD),
      ("wDay", WORD),
      ("wHour", WORD),
      ("wMinute", WORD),
      ("wSecond", WORD),
      ("wDayOfWeek", WORD)
   ]


class renddata(Structure):

   _fields_ = [
      ("atyp", WORD),
      ("ulPosition", ULONG),
      ("dxWidth", WORD),
      ("dyHeight", WORD),
      ("dwFlags", DWORD)
   ]


class variableLength(Structure):

   _fields_ = [
      ("data", c_char_p),
      ("size", c_int)
   ]


class _TNEFIOStruct(Structure):
   
   _fields_ = [
      #int (*InitProc) (struct _TNEFIOStruct *IO);
      #int (*ReadProc) (struct _TNEFIOStruct *IO, int size, int count, void *dest);
      #int (*CloseProc) (struct _TNEFIOStruct *IO);
      ("data", c_void_p),
   ]

_TNEFIOStruct._fields_.insert(0, ("InitProc", CFUNCTYPE(c_int, POINTER(_TNEFIOStruct))))
_TNEFIOStruct._fields_.insert(1, ("ReadProc", CFUNCTYPE(c_int, POINTER(_TNEFIOStruct), c_int, c_int, c_void_p)))
_TNEFIOStruct._fields_.insert(2, ("CloseProc", CFUNCTYPE(c_int, POINTER(_TNEFIOStruct))))


class TNEFIOStruct(_TNEFIOStruct):
   "a trick to get the structure properly initialized"

   _fields_ = _TNEFIOStruct._fields_


class MAPIProperty(Structure):

   _fields_ = [
      ("custom", DWORD),
      ("guid", BYTE*16),
      ("id", DWORD),
      ("count", ULONG),
      ("namedproperty", c_int),
      ("propnames", POINTER(variableLength)),
      ("data", POINTER(variableLength))
   ]


class MAPIProps(Structure):
   
   _fields_ = [
      ("count", DWORD),
      ("properties", POINTER(MAPIProperty)),
   ]


class Attachment(Structure):
   
   _fields_ = [
      ("Date", dtr),
      ("Title", variableLength),
      ("MetaFile", variableLength),
      ("CreateDate", dtr),
      ("ModifyDate", dtr),
      ("TransportFilename", variableLength),
      ("RenderData", renddata),
      ("MAPI", MAPIProps),
      #("next", POINTER(Attachment)), # struct Attachment *next
      ("FileData", variableLength),
      ("IconData", variableLength)
   ]

Attachment._fields_.insert(8, ("next", POINTER(Attachment)))


class TNEFStruct(Structure):

   _fields_ = [   
      ("version", c_char*10),
      ("from",variableLength),
      ("subject",variableLength),
      ("dateSent", dtr),
      ("dateReceived", dtr),
      ("messageStatus", c_char*10),
      ("messageClass", c_char*50),
      ("messageID", c_char*50),
      ("parentID", c_char*50),
      ("conversationID", c_char*50),
      ("body", variableLength),
      ("priority", c_char*10),
      ("starting_attach", Attachment),
      ("dateModified", dtr),
      ("MapiProperties", MAPIProps),
      ("CodePage", variableLength),
      ("OriginalMessageClass", variableLength),
      ("Owner", variableLength),
      ("SentFor", variableLength),
      ("Delegate", variableLength),
      ("DateStart", dtr),
      ("DateEnd", dtr),
      ("AidOwner", variableLength),
      ("RequestRes", c_int),
      ("Debug", c_int) ,
      ("IO", TNEFIOStruct),
   ]
