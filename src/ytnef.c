#include <stdio.h>
#include <string.h>
#include <Python.h>
#include <ytnef.h>
#include <tnef-types.h>

static PyObject *TNEFError;

// GET_INFO IMPLEMENTATION

static PyObject * get_info(PyObject *self, PyObject *args)
{
   BYTE *tnefinput;
   long size; // size of passed TNEF data string
   if (!PyArg_ParseTuple(args, "s#", &tnefinput, &size))
      return NULL;
     
   TNEFStruct TNEF;
   TNEFInitialize(&TNEF);
   //TNEF.Debug = 2;
   int result = TNEFParseMemory(tnefinput, size, &TNEF);  
   TNEFFree(&TNEF);
   return Py_BuildValue("s#", tnefinput, size);
}


// MODULE METHOD TABLE

static PyMethodDef TNEFMethods[] = {
   {"get_info",  get_info, METH_VARARGS, "Retrieve information about the TNEF attachment."},
   {NULL, NULL, 0, NULL}        /* Sentinel */
};


// MODULE INITIALIZATION

PyMODINIT_FUNC initytnef(void) {

   PyObject *m;
   m = Py_InitModule("ytnef", TNEFMethods);

   TNEFError = PyErr_NewException("ytnef.error", NULL, NULL);
   Py_INCREF(TNEFError);
   PyModule_AddObject(m, "error", TNEFError);  
}

