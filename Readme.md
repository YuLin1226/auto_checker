# Auto checker
This is an auto checker spider for ntu RD.

# Install 

### Install selenium
```
pip3 install selenium
```
### Install google browser

 下載

$ wget -c https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb

安裝

$ sudo dpkg -i google-chrome-stable_current_amd64.deb


### Install google driver 

Error: [Post](https://blog.csdn.net/m0_62298204/article/details/120802053)

ChromeDriver has to be updated.

The chromedriver in this repo may not match yours, so you have to change the file on your own.


## Usage 
```
python3 auto_checker.py
```
## auto start
Put this line in /etc/rc.local

```
sudo -i -u ken python3 /home/ken/auto_checker/auto_checker.py >> rc.out &
```

