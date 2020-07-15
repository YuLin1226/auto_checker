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
Error: https://sites.google.com/a/chromium.org/chromedriver/home

Or if your google browser is same as below, you don't have to install a new one.
because repo already include this version.
```
Version 84.0.4147.89 (Official Build) (64-bit)
```
## Usage 
```
python3 auto_checker.py
```
## auto start
Put this line in /etc/rc.local

```
sudo -i -u ken python3 /home/ken/auto_checker/auto_checker.py >> rc.out &
```

