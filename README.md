# react-atomicdex-wasm

## Pre-requisites

- NodejsV16 or newer. Recommendation: use `nvm`: https://www.freecodecamp.org/news/node-version-manager-nvm-install-guide/

## Build steps

- `npm ci` -> the first time
- `npm run dev` -> starts a server at http://localhost:1234/

## Misc notes

Best to open/reopen the url: http://localhost:1234/ in a private/incognito window when testing code/mm2 changes, to be completely sure that cached mm2 bins/other code aren't interfering

To update the API version and coins file, use `./update_wasm.py -a API_HASH -b API_BRANCH -c COINS_BRANCH`. API_BRANCH and COINS_BRANCH are optional, default to `main`/`master` if not provided
