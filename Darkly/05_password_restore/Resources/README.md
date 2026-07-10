# Password Recovery Hidden Field Tampering

## Breach
The password recovery form stores the destination email in a hidden client-side field. Changing `mail=webmaster@borntosec.com` before submitting makes the server trust an attacker-controlled reset destination.

## Proof
1. Open `http://<IP>/?page=recover`.
2. Inspect the form and edit the hidden `mail` value.
3. Submit the form to trigger the flag.

## Fix
Never trust hidden fields for account recovery. The server must look up the target account and reset destination from trusted state after verifying identity.

