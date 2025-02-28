"""
The _compat module is used for code which requires branching between different
Python environments. It is excluded from the code coverage checks.
"""
import ssl
import sys

# `contextlib.asynccontextmanager` exists from Python 3.7 onwards.
# For 3.6 we require the `async_generator` package for a backported version.
try:
    from contextlib import asynccontextmanager  # type: ignore
except ImportError:
    from async_generator import asynccontextmanager  # type: ignore # noqa

if sys.version_info >= (3, 10) or (
    sys.version_info >= (3, 7) and ssl.OPENSSL_VERSION_INFO >= (1, 1, 0, 7)
):

    def set_minimum_tls_version_1_2(context: ssl.SSLContext) -> None:
        # The OP_NO_SSL* and OP_NO_TLS* become deprecated in favor of
        # 'SSLContext.minimum_version' from Python 3.7 onwards, however
        # this attribute is not available unless the ssl module is compiled
        # with OpenSSL 1.1.0g or newer.
        # https://docs.python.org/3.10/library/ssl.html#ssl.SSLContext.minimum_version
        # https://docs.python.org/3.7/library/ssl.html#ssl.SSLContext.minimum_version
        context.minimum_version = ssl.TLSVersion.TLSv1_2


else:

    def set_minimum_tls_version_1_2(context: ssl.SSLContext) -> None:
        # If 'minimum_version' isn't available, we configure these options with
        # the older deprecated variants.
        context.options |= ssl.OP_NO_SSLv2
        context.options |= ssl.OP_NO_SSLv3
        context.options |= ssl.OP_NO_TLSv1
        context.options |= ssl.OP_NO_TLSv1_1
