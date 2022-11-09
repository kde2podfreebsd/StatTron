# Stattron

## [TG User Agent Bot Documentation](https://github.com/bubblesortdudoser/Stattron/blob/dev/UserBot/README.md) ⬅️

## Installation & Preparation
#### 1. Clone repo
```.sh
git clone https://github.com/bubblesortdudoser/Stattron
cd Statron
```
#### 2. Create venv
```.sh
python -m venv venv
```

#### 3. Install deps
```.sh
cd UserBot/
make deps
```

#### 4. Create database
```.sh
cd TGUserAgent/database/
python dbworker.py init

python dbworker.py rebuild # rebuild db
```


