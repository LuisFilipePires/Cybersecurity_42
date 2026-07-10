Stored XSS In Feedback
Breach
The feedback form stores user-controlled text and reflects it back into the page without proper validation and output encoding. Submitting XSS-related content such as script or alert triggers the challenge response and reveals the flag.

Proof
Open http://<IP>/?page=feedback.
Submit a feedback entry containing script or alert.
The application stores the input and displays the flag.
Fix
Validate input server-side and HTML-encode all output. Add a restrictive Content Security Policy and make session cookies HttpOnly.f
