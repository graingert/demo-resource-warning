when run on python 3.12:

```

python -m coverage run --parallel-mode -m pytest --memray --hide-memray-summary -vvv
================================================================================================================================== test session starts ===================================================================================================================================
platform linux -- Python 3.12.0+, pytest-7.4.3, pluggy-1.3.0 -- /home/graingert/.virtualenvs/testing312/bin/python
cachedir: .pytest_cache
rootdir: /home/graingert/projects/demo-resource-warning
configfile: pyproject.toml
plugins: memray-1.5.0
collected 2 items                                                                                                                                                                                                                                                                        

test_socketlevel.py::test_foo FAILED                                                                                                                                                                                                                                               [ 50%]
test_socketlevel.py::test_gc FAILED                                                                                                                                                                                                                                                [100%]

======================================================================================================================================== FAILURES ========================================================================================================================================
________________________________________________________________________________________________________________________________________ test_foo ________________________________________________________________________________________________________________________________________

cls = <class 'ssl.SSLSocket'>, sock = <socket.socket [closed] fd=-1, family=2, type=1, proto=6>, server_side = False, do_handshake_on_connect = True, suppress_ragged_eofs = True, server_hostname = 'localhost', context = <ssl.SSLContext object at 0x7ff3e36fd450>, session = None

    @classmethod
    def _create(cls, sock, server_side=False, do_handshake_on_connect=True,
                suppress_ragged_eofs=True, server_hostname=None,
                context=None, session=None):
        if sock.getsockopt(SOL_SOCKET, SO_TYPE) != SOCK_STREAM:
            raise NotImplementedError("only stream sockets are supported")
        if server_side:
            if server_hostname:
                raise ValueError("server_hostname can only be specified "
                                 "in client mode")
            if session is not None:
                raise ValueError("session can only be specified in "
                                 "client mode")
        if context.check_hostname and not server_hostname:
            raise ValueError("check_hostname requires server_hostname")
    
        kwargs = dict(
            family=sock.family, type=sock.type, proto=sock.proto,
            fileno=sock.fileno()
        )
        self = cls.__new__(cls, **kwargs)
        super(SSLSocket, self).__init__(**kwargs)
        sock_timeout = sock.gettimeout()
        sock.detach()
    
        self._context = context
        self._session = session
        self._closed = False
        self._sslobj = None
        self.server_side = server_side
        self.server_hostname = context._encode_hostname(server_hostname)
        self.do_handshake_on_connect = do_handshake_on_connect
        self.suppress_ragged_eofs = suppress_ragged_eofs
    
        # See if we are connected
        try:
>           self.getpeername()
E           OSError: [Errno 107] Transport endpoint is not connected

/usr/lib/python3.12/ssl.py:992: OSError

During handling of the above exception, another exception occurred:

    def test_foo():
        for i in range(100):
>           _test_ssl_failed_fingerprint_verification()

test_socketlevel.py:247: 
_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ 
test_socketlevel.py:243: in _test_ssl_failed_fingerprint_verification
    request2()
test_socketlevel.py:237: in request2
    return request()
test_socketlevel.py:210: in request
    _ssl_wrap_socket_and_match_hostname(
test_socketlevel.py:121: in _ssl_wrap_socket_and_match_hostname
    return context.wrap_socket(sock, server_hostname=server_hostname)
/usr/lib/python3.12/ssl.py:455: in wrap_socket
    return self.sslsocket_class._create(
/usr/lib/python3.12/ssl.py:1004: in _create
    notconn_pre_handshake_data = self.recv(1)
_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ 

self = <ssl.SSLSocket fd=15, family=2, type=1, proto=6, laddr=('127.0.0.1', 50258)>, buflen = 1, flags = 0

    def recv(self, buflen=1024, flags=0):
        self._checkClosed()
        if self._sslobj is not None:
            if flags != 0:
                raise ValueError(
                    "non-zero flags not allowed in calls to recv() on %s" %
                    self.__class__)
            return self.read(buflen)
        else:
>           return super().recv(buflen, flags)
E           ConnectionResetError: [Errno 104] Connection reset by peer

/usr/lib/python3.12/ssl.py:1237: ConnectionResetError
---------------------------------------------------------------------------------------------------------------------------------- Captured stderr call ----------------------------------------------------------------------------------------------------------------------------------
Memray WARNING: Correcting symbol for malloc from 0x420630 to 0x7ff3e5ea50a0
Memray WARNING: Correcting symbol for free from 0x420aa0 to 0x7ff3e5ea53e0
________________________________________________________________________________________________________________________________________ test_gc _________________________________________________________________________________________________________________________________________

cls = <class '_pytest.runner.CallInfo'>, func = <function call_runtest_hook.<locals>.<lambda> at 0x7ff3e3545f80>, when = 'call', reraise = (<class '_pytest.outcomes.Exit'>, <class 'KeyboardInterrupt'>)

    @classmethod
    def from_call(
        cls,
        func: "Callable[[], TResult]",
        when: "Literal['collect', 'setup', 'call', 'teardown']",
        reraise: Optional[
            Union[Type[BaseException], Tuple[Type[BaseException], ...]]
        ] = None,
    ) -> "CallInfo[TResult]":
        """Call func, wrapping the result in a CallInfo.
    
        :param func:
            The function to call. Called without arguments.
        :param when:
            The phase in which the function is called.
        :param reraise:
            Exception or exceptions that shall propagate if raised by the
            function, instead of being wrapped in the CallInfo.
        """
        excinfo = None
        start = timing.time()
        precise_start = timing.perf_counter()
        try:
>           result: Optional[TResult] = func()

../../.virtualenvs/testing312/lib/python3.12/site-packages/_pytest/runner.py:341: 
_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ 
../../.virtualenvs/testing312/lib/python3.12/site-packages/_pytest/runner.py:262: in <lambda>
    lambda: ihook(item=item, **kwds), when=when, reraise=reraise
../../.virtualenvs/testing312/lib/python3.12/site-packages/pluggy/_hooks.py:493: in __call__
    return self._hookexec(self.name, self._hookimpls, kwargs, firstresult)
../../.virtualenvs/testing312/lib/python3.12/site-packages/pluggy/_manager.py:115: in _hookexec
    return self._inner_hookexec(hook_name, methods, kwargs, firstresult)
../../.virtualenvs/testing312/lib/python3.12/site-packages/_pytest/unraisableexception.py:88: in pytest_runtest_call
    yield from unraisable_exception_runtest_hook()
_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ 

    def unraisable_exception_runtest_hook() -> Generator[None, None, None]:
        with catch_unraisable_exception() as cm:
            yield
            if cm.unraisable:
                if cm.unraisable.err_msg is not None:
                    err_msg = cm.unraisable.err_msg
                else:
                    err_msg = "Exception ignored in"
                msg = f"{err_msg}: {cm.unraisable.object!r}\n\n"
                msg += "".join(
                    traceback.format_exception(
                        cm.unraisable.exc_type,
                        cm.unraisable.exc_value,
                        cm.unraisable.exc_traceback,
                    )
                )
>               warnings.warn(pytest.PytestUnraisableExceptionWarning(msg))
E               pytest.PytestUnraisableExceptionWarning: Exception ignored in: <ssl.SSLSocket fd=-1, family=2, type=1, proto=6>
E               
E               Traceback (most recent call last):
E                 File "/home/graingert/projects/demo-resource-warning/test_socketlevel.py", line 253, in test_gc
E                   gc.collect()
E               ResourceWarning: unclosed <ssl.SSLSocket fd=15, family=2, type=1, proto=6, laddr=('127.0.0.1', 50258)>

../../.virtualenvs/testing312/lib/python3.12/site-packages/_pytest/unraisableexception.py:78: PytestUnraisableExceptionWarning
==================================================================================================================================== warnings summary ====================================================================================================================================
test_socketlevel.py::test_foo
  /home/graingert/projects/demo-resource-warning/test_socketlevel.py:140: DeprecationWarning: ssl.PROTOCOL_TLS is deprecated
    context = ssl.SSLContext(ssl_version)

-- Docs: https://docs.pytest.org/en/stable/how-to/capture-warnings.html
================================================================================================================================ short test summary info =================================================================================================================================
FAILED test_socketlevel.py::test_foo - ConnectionResetError: [Errno 104] Connection reset by peer
 ✘  graingert@conscientious  testing312  ~/projects/demo-resource-warning   main  
```
