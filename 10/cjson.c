#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <Python.h>

int is_str(const char *str) {
    return (str[0] == '\"' && str[strlen(str) - 1] == '\"');
}

PyObject *create_python_str(const char *str) {
    size_t len = strlen(str);

    char str_value[len - 1];
    strncpy(str_value, str + 1, len - 2);
    str_value[len - 2] = '\0';

    PyObject *value = NULL;
    if (!(value = Py_BuildValue("s", str_value))) {
        return NULL;
    }
    return value;
}

PyObject *create_python_int(const char *str) {
    size_t len = strlen(str);

    for (size_t i = 0; i < len; i++) {
        if (!isdigit(str[i])) {
            return NULL;
        }
    }

    PyObject *value = NULL;
    if (!(value = Py_BuildValue("i", atoi(str)))) {
        return NULL;
    }
    return value;
}

PyObject *create_key(const char *str) {
    PyObject *key = NULL;

    if (!is_str(str)) {
        return NULL;
    }

    key = create_python_str(str);

    return key;
}

PyObject *create_value(const char *str) {
    PyObject *value = NULL;

    if (is_str(str)) {
        value = create_python_str(str);
     } else {
        value = create_python_int(str);
     }

    return value;
}

PyObject *cjson_loads(PyObject *self, PyObject *args) {

    char *input_str = NULL;
    if (!PyArg_ParseTuple(args, "s", &input_str)) {
        PyErr_Format(PyExc_TypeError, "ERROR: Expected str as argument\n");
        return NULL;
    }

    size_t len = strlen(input_str);

    if (input_str[0] != '{' && input_str[len - 2] != '}') {
        PyErr_Format(PyExc_TypeError, "ERROR: Expected json string\n");
    }

    char json_str[len - 2];
    strncpy(json_str, input_str + 1, len - 2);
    json_str[len - 2] = '\0';

    PyObject *dict = NULL;
    if (!(dict = PyDict_New())) {
        printf("ERROR: Failed to create Dict Object\n");
        return NULL;
    }

    PyObject *key = NULL;
    PyObject *value = NULL;

    char* token = strtok(json_str, ":, ");
    while (token != NULL) {
        if (key == NULL) {
            key = create_key(token);

            if (key == NULL) {
                PyErr_Format(PyExc_TypeError, "ERROR: Failed to load key from str\n");
                return NULL;
            }

        } else if (value == NULL) {
             value = create_value(token);

            if (value == NULL) {
                PyErr_Format(PyExc_TypeError, "ERROR: Failed to load value from str\n");
                return NULL;
            }

            if (PyDict_SetItem(dict, key, value) < 0) {
                printf("ERROR: Failed to set item\n");
                return NULL;
            }

            key = NULL;
            value = NULL;
        }
        token = strtok(NULL, ":, ");
    }

    return dict;
}

const char* string_from_PyObject(PyObject* obj) {
    PyObject* repr = PyObject_Repr(obj);
    PyObject* str = PyUnicode_AsEncodedString(repr, "utf-8", "~");
    char *string = PyBytes_AS_STRING(str);
    return string;
}

PyObject *cjson_dumps(PyObject *self, PyObject *args) {
    PyObject *dict = NULL;
    if (!PyArg_ParseTuple(args, "O", &dict)) {
        PyErr_Format(PyExc_TypeError, "ERROR: Expected dict as argument\n");
        return NULL;
    }

    if (!PyDict_CheckExact(dict)) {
        PyErr_Format(PyExc_TypeError, "ERROR: Expected dict as argument\n");
        return NULL;
    }

    PyObject *key;
    PyObject *value;
    Py_ssize_t pos = 0;

    while (PyDict_Next(dict, &pos, &key, &value)) {
        if (!PyUnicode_Check(key)) {
            PyErr_Format(PyExc_TypeError, "ERROR: Failed to dump key into str\n");
            return NULL;
        }

        if (!PyUnicode_Check(value) && !PyLong_Check(value)) {
            PyErr_Format(PyExc_TypeError, "ERROR: Failed to dump value into str\n");
            return NULL;
        }
    }

    char* str = string_from_PyObject(dict);

    char *found_char;
    while ((found_char = strchr(str, '\'')) != NULL) {
        *found_char = '\"';
    }

    return Py_BuildValue("s", str);
}

static PyMethodDef methods[] = {
    {"loads", cjson_loads, METH_VARARGS, "Parse json-string into python dict"},
    {"dumps", cjson_dumps, METH_VARARGS, "Parse json-dict into str"},
    {NULL, NULL, 0, NULL}
};


static struct PyModuleDef module_json = {
    PyModuleDef_HEAD_INIT,
    "cjson",
    "Self-written module instead of json. Keeps `loads()` and `dumps()`",
    -1,
    methods
};

PyMODINIT_FUNC PyInit_cjson() {
    return PyModule_Create(&module_json);
}


