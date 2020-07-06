# appcoins-server-validator
Documentation for APPC purchases server to server validation.

Both this projects assumes Pipenv and Python3.8 are already installed. These are also prepared to distinguish production/development/local environments.

Also, we've included `supervisorctl` and `nginx` configurations to work out-of-the-box inside `/conf` directory.

## in-app-managed
Python project that will create a Flask API to validate AppCoins purchases server-side.

For detailed documentation: https://docs.catappult.io/docs/iap-validators-server-to-server-check

#### Settings things up
```
$ git clone https://github.com/Aptoide/appcoins-server-validator.git

$ cd appcoins-server-validator/in-app-managed

$ pipenv install
```

#### How to run
```
$ pipenv run python validator.py
or
$ PURCHASE_CHECKER=DEVELOPMENT pipenv run python validator.py
or
$ PURCHASE_CHECKER=PRODUCTION pipenv run python validator.py
```

## one-step-payment
Python project that will create a Flask API to validate AppCoins One-Step Payment purchases.

This project assumes that you already have ngrok setup on your machine (more info here: https://ngrok.com/download).

For detailed documentation: https://docs.catappult.io/docs/one-step-payment


#### Setting things up
```
$ git clone https://github.com/Aptoide/appcoins-server-validator.git

$ cd appcoins-server-validator/one-step-payment

$ pipenv install
```

#### How to run Flask API
```
$ pipenv run python run_flask.py
or
$ ONE_STEP_PAYMENT=DEVELOPMENT pipenv run python run_flask.py
or
$ ONE_STEP_PAYMENT=PRODUCTION pipenv run python run_flask.py
```

#### How to run purchase example
```
$ pipenv run python run_example.py
or
$ ONE_STEP_PAYMENT=DEVELOPMENT pipenv run python run_example.py
or
$ ONE_STEP_PAYMENT=PRODUCTION pipenv run python run_example.py
```