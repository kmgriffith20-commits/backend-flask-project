
# Authentication Security Tests

## Attack #1: Incorrect Password Login

**Endpoint:** POST /login

**Test:** Attempt to log in using a valid email address and an incorrect password.

### Command

```bash
curl -i -X POST http://127.0.0.1:5001/login \
  -H "Content-Type: application/json" \
  -d '{"email":"maestro-test-2026@example.com","password":"DefinitelyWrongPassword123!"}'
```

### Actual HTTP Response

```text
HTTP/1.1 401 UNAUTHORIZED
Content-Type: application/json
Content-Length: 40

{"message":"Invalid email or password"}
```

### Result

PASS - The application rejected the incorrect password.

This is an authentication failure because the server could not verify the user's identity.

The application did not authenticate the user or return a successful login response.
