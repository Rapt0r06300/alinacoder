from __future__ import annotations

import ctypes
import os
from ctypes import wintypes


class SecretProtectionError(RuntimeError):
    pass


class _DATA_BLOB(ctypes.Structure):
    _fields_ = [("cbData", wintypes.DWORD), ("pbData", ctypes.POINTER(ctypes.c_ubyte))]


def _make_blob(data: bytes) -> tuple[_DATA_BLOB, ctypes.Array[ctypes.c_char]]:
    buffer = ctypes.create_string_buffer(data)
    blob = _DATA_BLOB(len(data), ctypes.cast(buffer, ctypes.POINTER(ctypes.c_ubyte)))
    return blob, buffer


class DPAPIProtector:
    CRYPTPROTECT_LOCAL_MACHINE = 0x4

    def __init__(self, *, machine_scope: bool = False) -> None:
        if os.name != "nt":
            raise OSError("DPAPIProtector is only available on Windows")
        self._crypt32 = ctypes.WinDLL("crypt32", use_last_error=True)
        self._kernel32 = ctypes.WinDLL("kernel32", use_last_error=True)
        self._flags = self.CRYPTPROTECT_LOCAL_MACHINE if machine_scope else 0
        self._crypt32.CryptProtectData.argtypes = [ctypes.POINTER(_DATA_BLOB), wintypes.LPCWSTR, ctypes.c_void_p, ctypes.c_void_p, ctypes.c_void_p, wintypes.DWORD, ctypes.POINTER(_DATA_BLOB)]
        self._crypt32.CryptProtectData.restype = wintypes.BOOL
        self._crypt32.CryptUnprotectData.argtypes = [ctypes.POINTER(_DATA_BLOB), ctypes.POINTER(wintypes.LPWSTR), ctypes.c_void_p, ctypes.c_void_p, ctypes.c_void_p, wintypes.DWORD, ctypes.POINTER(_DATA_BLOB)]
        self._crypt32.CryptUnprotectData.restype = wintypes.BOOL
        self._kernel32.LocalFree.argtypes = [ctypes.c_void_p]
        self._kernel32.LocalFree.restype = ctypes.c_void_p

    def protect(self, plaintext: bytes) -> bytes:
        if not plaintext:
            raise ValueError("plaintext cannot be empty")
        in_blob, keepalive = _make_blob(plaintext)
        _ = keepalive
        out_blob = _DATA_BLOB()
        ok = self._crypt32.CryptProtectData(ctypes.byref(in_blob), None, None, None, None, self._flags, ctypes.byref(out_blob))
        if not ok:
            raise SecretProtectionError(f"CryptProtectData failed: {ctypes.get_last_error()}")
        try:
            return ctypes.string_at(out_blob.pbData, out_blob.cbData)
        finally:
            self._kernel32.LocalFree(out_blob.pbData)

    def unprotect(self, ciphertext: bytes) -> bytes:
        if not ciphertext:
            raise ValueError("ciphertext cannot be empty")
        in_blob, keepalive = _make_blob(ciphertext)
        _ = keepalive
        out_blob = _DATA_BLOB()
        ok = self._crypt32.CryptUnprotectData(ctypes.byref(in_blob), None, None, None, None, 0, ctypes.byref(out_blob))
        if not ok:
            raise SecretProtectionError(f"CryptUnprotectData failed: {ctypes.get_last_error()}")
        try:
            return ctypes.string_at(out_blob.pbData, out_blob.cbData)
        finally:
            self._kernel32.LocalFree(out_blob.pbData)
