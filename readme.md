when run on python 3.12:
```
python -W error test_socketlevel.py
0
1
2
3
4
Traceback (most recent call last):
  File "/usr/lib/python3.12/ssl.py", line 992, in _create
    self.getpeername()
OSError: [Errno 107] Transport endpoint is not connected

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "/home/graingert/projects/demo-resource-warning/test_socketlevel.py", line 188, in <module>
    sys.exit(main())
             ^^^^^^
  File "/home/graingert/projects/demo-resource-warning/test_socketlevel.py", line 183, in main
    test_foo()
  File "/home/graingert/projects/demo-resource-warning/test_socketlevel.py", line 172, in test_foo
    _test_ssl_failed_fingerprint_verification()
  File "/home/graingert/projects/demo-resource-warning/test_socketlevel.py", line 166, in _test_ssl_failed_fingerprint_verification
    request()
  File "/home/graingert/projects/demo-resource-warning/test_socketlevel.py", line 155, in request
    ssl.create_default_context().wrap_socket(
  File "/usr/lib/python3.12/ssl.py", line 455, in wrap_socket
    return self.sslsocket_class._create(
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/usr/lib/python3.12/ssl.py", line 1004, in _create
    notconn_pre_handshake_data = self.recv(1)
                                 ^^^^^^^^^^^^
  File "/usr/lib/python3.12/ssl.py", line 1237, in recv
    return super().recv(buflen, flags)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^
ConnectionResetError: [Errno 104] Connection reset by peer
Exception ignored in: <ssl.SSLSocket fd=5, family=2, type=1, proto=6, laddr=('127.0.0.1', 54864)>
ResourceWarning: unclosed <ssl.SSLSocket fd=5, family=2, type=1, proto=6, laddr=('127.0.0.1', 54864)>
```
