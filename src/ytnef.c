#include <stdio.h>
#include <string.h>
#include <Python.h>
#include <ytnef.h>
#include <tnef-types.h>


static PyObject *TNEFError;


static PyObject * get_info(PyObject *self, PyObject *args)
{
   BYTE *tnefinput;
   int size; // size of passed TNEF data string
   if (!PyArg_ParseTuple(args, "s#", &tnefinput))
      return NULL;

   size = strlen(tnefinput);
      
   //TNEFStruct TNEF;
   //const char *parseresult;
   //parseresult = TNEFParseMemory(tnefdata, size, &TNEF);

   return Py_BuildValue("i", size);
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
