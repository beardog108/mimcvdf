#define PY_SSIZE_T_CLEAN
#include <Python.h>

#include <stdbool.h>
#include <gmp.h>

/*
C Version by github.com/cartr
This module adapted from https://github.com/OlegJakushkin/deepblockchains/blob/master/vdf/mimc/python/mimc.py by Sourabh Niyogi https://github.com/sourabhniyogi

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <https://www.gnu.org/licenses/>.
*/

static mpz_t MODULUS;
static mpz_t LITTLE_FERMAT_EXPT;
#define ROUND_CONSTANTS_COUNT 64
static mpz_t ROUND_CONSTANTS[ROUND_CONSTANTS_COUNT];

static void
mimc_init_constants()
{
    mpz_t fortytwo;

    mpz_init(fortytwo);
    mpz_set_ui(fortytwo, 42);

    // Set MODULUS to hex(2**256 - 2**32 * 351 + 1)
    mpz_init(MODULUS);
    mpz_set_str(MODULUS,
                "ffffffffffffffffffffffffffffffff"
                "fffffffffffffffffffffea100000001",
                16);

    // Set LITTLE_FERMAT_EXPT to hex((MODULUS * 2 - 1) // 3)
    mpz_init(LITTLE_FERMAT_EXPT);
    mpz_set_str(LITTLE_FERMAT_EXPT,
                "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa"
                "aaaaaaaaaaaaaaaaaaaaa9c0aaaaaaab",
                16);

    // Set all the constants to (i**7 ^ 42)
    for (unsigned long int i = 0; i < ROUND_CONSTANTS_COUNT; i++) {
       mpz_init(ROUND_CONSTANTS[i]);
       mpz_ui_pow_ui(ROUND_CONSTANTS[i], i, 7);
       mpz_xor(ROUND_CONSTANTS[i], ROUND_CONSTANTS[i], fortytwo);
    }

    mpz_clear(fortytwo);
}

static bool
unpack_args(PyObject *args, mpz_t input, unsigned int *steps)
{
    const char *data_bytes;
    Py_ssize_t count;

    if (!PyArg_ParseTuple(args, "y#I", &data_bytes, &count, steps)) {
        return false;
    }

    mpz_import(input, count, 1, 1, 0, 0, data_bytes);
    return true;
}


static PyObject *
convert_mpz_to_bytes(mpz_t op)
{
    char string[34];
    size_t size;

    mpz_export(string, &size, 1, 1, 0, 0, op);
    PyObject *result = PyBytes_FromStringAndSize(string, size);
    return result;
}

static PyObject *
forward_mimc(PyObject *_self, PyObject *args)
{
    mpz_t result;
    unsigned int steps;

    mpz_init(result);
    if (!unpack_args(args, result, &steps)) {
        mpz_clear(result);
        return NULL;
    }

    for (unsigned int i = 1; i < steps; ++i) {
        mpz_powm_ui(result, result, 3, MODULUS);
        mpz_add(result, result, ROUND_CONSTANTS[i % ROUND_CONSTANTS_COUNT]);
        if (mpz_cmp(result, MODULUS) >= 0) {
            mpz_sub(result, result, MODULUS);
        }
    }

    PyObject *result_obj = convert_mpz_to_bytes(result);
    mpz_clear(result);
    return result_obj;
}

static PyObject *
reverse_mimc(PyObject *_self, PyObject *args)
{
    mpz_t result;
    unsigned int steps;

    mpz_init(result);
    if (!unpack_args(args, result, &steps)) {
        mpz_clear(result);
        return NULL;
    }

    for (unsigned int i = steps - 1; i > 0; --i) {
        mpz_sub(result, result, ROUND_CONSTANTS[i % ROUND_CONSTANTS_COUNT]);
        mpz_powm(result, result, LITTLE_FERMAT_EXPT, MODULUS);
    }

    PyObject *result_obj = convert_mpz_to_bytes(result);
    mpz_clear(result);
    return result_obj;
}

static PyMethodDef Methods[] = {
    {"forward_mimc", forward_mimc, METH_VARARGS,
     "Run MIMC forward (the fast direction)"},
    {"reverse_mimc", reverse_mimc, METH_VARARGS,
     "Run MIMC in reverse (the slow direction)"},
    {NULL, NULL, 0, NULL}
};

static struct PyModuleDef moduledef = {
    PyModuleDef_HEAD_INIT,
    "native",
    "Fast native implementation of MIMC.",
    -1,
    Methods,
    NULL
};

PyMODINIT_FUNC
PyInit_native()
{
    mimc_init_constants();

    return PyModule_Create(&moduledef);
}
