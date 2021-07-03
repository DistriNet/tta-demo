## Demo for Timeless Timing Attacks

To run the demo, use following steps.

1. Obtain a certificate for the domain on which you want to run the demo
2. Place `fullchain.pem` and `privkey.pem` in the `demo/certs` folder. Also place a `ssl-dhparams.pem` file there (generate via e.g. `openssl dhparam -out ssl-dhparams.pem 4096`)
3. In `demo`, run `docker-compose up --build`

The attack can then be run by first updating `demo-attack/attack.py` with the targeted server, and then simply running `python attack.py` (with Python version 3.7.x or higher, with hyper-h2 installed: `pip install h2`).

The `h2time.py` file originates from the original [Timeless Timing Attack repository](https://github.com/DistriNet/timeless-timing-attacks).