from __future__ import annotations

import sys
import contextlib
import socket
import ssl
import typing

import threading
import os
import warnings

ALPN_PROTOCOLS = ["http/1.1"]

CERTS_PATH = os.path.join(os.path.dirname(__file__), "certs")
DEFAULT_CERTS: dict[str, typing.Any] = {
    "certfile": os.path.join(CERTS_PATH, "server.crt"),
    "keyfile": os.path.join(CERTS_PATH, "server.key"),
    "cert_reqs": ssl.CERT_OPTIONAL,
    "ca_certs": os.path.join(CERTS_PATH, "cacert.pem"),
    "alpn_protocols": ALPN_PROTOCOLS,
}
DEFAULT_CA = os.path.join(CERTS_PATH, "cacert.pem")
DEFAULT_CA_KEY = os.path.join(CERTS_PATH, "cacert.key")


class SocketServerThread(threading.Thread):
    """
    :param socket_handler: Callable which receives a socket argument for one
        request.
    :param ready_event: Event which gets set when the socket handler is
        ready to receive requests.
    """

    USE_IPV6 = False

    def __init__(
        self,
        socket_handler: typing.Callable[[socket.socket], None],
        host: str = "localhost",
        ready_event: threading.Event | None = None,
    ) -> None:
        super().__init__()
        self.daemon = True

        self.socket_handler = socket_handler
        self.host = host
        self.ready_event = ready_event

    def _start_server(self) -> None:
        sock = socket.socket(socket.AF_INET)
        if sys.platform != "win32":
            sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

        with sock:
            sock.bind((self.host, 0))
            self.port = sock.getsockname()[1]

            # Once listen() returns, the server socket is ready
            sock.listen(1)

            if self.ready_event:
                self.ready_event.set()

            self.socket_handler(sock)

    def run(self) -> None:
        self._start_server()




class NewConnectionError(Exception):
    pass


if typing.TYPE_CHECKING:
    from _typeshed import StrOrBytesPath
else:
    StrOrBytesPath = object

def _ssl_wrap_socket_and_match_hostname(
    sock: socket.socket,
    *,
    cert_reqs: None | str | int,
    ssl_version: None | str | int,
    ssl_minimum_version: int | None,
    ssl_maximum_version: int | None,
    cert_file: str | None,
    key_file: str | None,
    key_password: str | None,
    ca_certs: str | None,
    ca_cert_dir: str | None,
    ca_cert_data: None | str | bytes,
    assert_hostname: None | str | Literal[False],
    assert_fingerprint: str | None,
    server_hostname: str | None,
    ssl_context: ssl.SSLContext | None,
    tls_in_tls: bool = False,
) -> _WrappedAndVerifiedSocket:
    """Logic for constructing an SSLContext from all TLS parameters, passing
    that down into ssl_wrap_socket, and then doing certificate verification
    either via hostname or fingerprint. This function exists to guarantee
    that both proxies and targets have the same behavior when connecting via TLS.
    """
    default_ssl_context = False
    if ssl_context is None:
        default_ssl_context = True
        # context = create_urllib3_context(
        #     ssl_version=resolve_ssl_version(ssl_version),
        #     ssl_minimum_version=ssl_minimum_version,
        #     ssl_maximum_version=ssl_maximum_version,
        #     cert_reqs=resolve_cert_reqs(cert_reqs),
        # )
        context = ssl.create_default_context()
    else:
        context = ssl_context

    context.verify_mode = ssl.CERT_REQUIRED

    return context.wrap_socket(sock, server_hostname=server_hostname)


def original_ssl_wrap_socket(
    sock: socket.socket,
    keyfile: StrOrBytesPath | None = None,
    certfile: StrOrBytesPath | None = None,
    server_side: bool = False,
    cert_reqs: ssl.VerifyMode = ssl.CERT_NONE,
    ssl_version: int = ssl.PROTOCOL_TLS,
    ca_certs: str | None = None,
    do_handshake_on_connect: bool = True,
    suppress_ragged_eofs: bool = True,
    ciphers: str | None = None,
) -> ssl.SSLSocket:
    if server_side and not certfile:
        raise ValueError("certfile must be specified for server-side operations")
    if keyfile and not certfile:
        raise ValueError("certfile must be specified")
    context = ssl.SSLContext(ssl_version)
    context.verify_mode = cert_reqs
    if ca_certs:
        context.load_verify_locations(ca_certs)
    if certfile:
        context.load_cert_chain(certfile, keyfile)
    if ciphers:
        context.set_ciphers(ciphers)
    return context.wrap_socket(
        sock=sock,
        server_side=server_side,
        do_handshake_on_connect=do_handshake_on_connect,
        suppress_ragged_eofs=suppress_ragged_eofs,
    )


@contextlib.contextmanager
def _socket_server(handler):
    ready_event = threading.Event()
    server_thread = SocketServerThread(
        socket_handler=handler,
        ready_event=ready_event,
        host="localhost"
    )
    server_thread.start()
    ready_event.wait(5)
    if not ready_event.is_set():
        raise Exception("timeout")
    try:
        yield server_thread.port
    finally:
        server_thread.join()


def _test_ssl_failed_fingerprint_verification() -> None:
    def socket_handler(listener: socket.socket) -> None:
        for i in range(2):
            with listener.accept()[0] as sock:
                try:
                    ssl_sock = original_ssl_wrap_socket(
                        sock,
                        server_side=True,
                        keyfile=DEFAULT_CERTS["keyfile"],
                        certfile=DEFAULT_CERTS["certfile"],
                        ca_certs=DEFAULT_CA,
                    )
                except (ssl.SSLError, ConnectionResetError):
                    if i == 1:
                        raise
                    return
                else:
                    with ssl_sock:
                        ssl_sock.send(
                            b"HTTP/1.1 200 OK\r\n"
                            b"Content-Type: text/plain\r\n"
                            b"Content-Length: 5\r\n\r\n"
                            b"Hello"
                        )

    with _socket_server(socket_handler) as port:
        # GitHub's fingerprint. Valid, but not matching.
        def request() -> None:
            try:
                try:
                    sock = socket.create_connection(
                       ("localhost", port),
                        source_address=None,
                    )
                except OSError as e:
                    raise NewConnectionError(None, None)
                _ssl_wrap_socket_and_match_hostname(
                    sock=sock,
                    cert_reqs=None,
                    ssl_version=None,
                    ssl_minimum_version=None,
                    ssl_maximum_version=None,
                    ca_certs=None,
                    ca_cert_dir=None,
                    ca_cert_data=None,
                    cert_file=None,
                    key_file=None,
                    key_password=None,
                    server_hostname="localhost",
                    ssl_context=None,
                    tls_in_tls=False,
                    assert_hostname=None,
                    assert_fingerprint=None,
                ).close()
            except BaseException as e:
                err = e
                raise


        def request1():
            return request()

        def request2():
            return request()

        with contextlib.suppress(ssl.SSLCertVerificationError):
            request1()
        # Should not hang, see https://github.com/urllib3/urllib3/issues/529
        with contextlib.suppress(NewConnectionError):
            request2()

def test_foo():
    for i in range(100):
        _test_ssl_failed_fingerprint_verification()


def test_gc():
    import gc
    for i in range(5):
        gc.collect()


def main():
    test_foo()
    test_gc()

if __name__ == "__main__":
    sys.exit(main())
