# HTTP Header

On copyright page, I used curl to find some comments.

The first interesting comment was:

```“Let's use this browser : ft_bornToSec. It will help you a lot.”```

This is a hint about the **User-Agent** HTTP Header. The website expects a specific browser identification, so we need to send: 

```‘ User-Agent: ft_bornToSec’```


The second interesting comment was:

```“You must come from : https://www.nsa.gov/.”```

This is a hint about the **Referer** HTTP Header. The website checks were the request came from, so we need to send:

`Referer: https://www.nsa.gov/`

Using curl, we can modify these headers with:

- `-A` or `--user-agent` → sets the User-Agent header
- `-e` or `--referer` → sets the Referer header

Example:

curl -A "ft_bornToSec" -e "https://www.nsa.gov/" URL

curl "http://10.18.200.104/?page=----" -A "ft_bornToSec" -H "referer: https://www.nsa.gov/" | grep "flag"
