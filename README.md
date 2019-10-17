# NeutronLab 
NeutronLab is an educational software package developed for National Research Center 
"Kurchatov Institute". \
NeutronLab replicates user interfaces of eight neutron instruments:
* SANS
* Cold Neutron Diffractometer
* Polarized Neutron Reflectometer
* Triple-Axis Spectrometer
* Thermal Neutron Diffractometer
* Double Crystal Diffractometer
* Single Crystal Diffractometer
* Stress Diffractometer

NeutronLab users can run simulated experiments with various samples and setup 
parameters and perform analysis of the simulated data. 
This software is intended for students of neutron scattering techniques as part of 
their course work. The language is Russian, but the instrument schemes are duplicated in English in folder 
`NeutronLab/mcstas_data/images/EN`, and examples of using the software can be found at 
https://youtu.be/hcb8EIq7yXc (SANS) and https://youtu.be/ze3CFfcohfI (Thermal Neutron Diffractometer).

# Установка (Windows 10 x64):

## Подготовка системы:
Следовать инструкциям с https://docs.microsoft.com/en-us/windows/wsl/install-win10 для установки Debian на Windows 10 \
Отключить опцию Fast Startup для корректной работы Debian: https://www.intowindows.com/how-to-turn-on-or-off-fast-startup-in-windows-10/ \
Установить X-Ming x-сервер: https://sourceforge.net/projects/xming/

## В терминале Debian выполнить следуюшие команды:

### Обновление системы:
`sudo apt-get update && sudo apt-get upgrade`

### Установка McStas
`cd /etc/apt/sources.list.d` \
`sudo wget http://packages.mccode.org/debian/mccode.list` \
`sudo apt-get update` \
`sudo apt-get install bzip2 libgl1-mesa-glx mcstas-2.5 mcstas-tools-python-mcrun-2.5 mcstas-tools-python-mccodelib-2.5 mpich`

### Установка Anaconda Python:
`cd ~` \
`wget https://repo.anaconda.com/archive/Anaconda3-5.2.0-Linux-x86_64.sh --no-check-certificate` \
`chmod +x Anaconda3-5.2.0-Linux-x86_64.sh` \
`./Anaconda3-5.2.0-Linux-x86_64.sh` \

### Установка витруальной лаборатории NeutronLab:
`sudo apt-get install git` \
`cd ~` \
`git clone -b master https://github.com/glebdovzhenko/NeutronLab.git` \
`anaconda3/bin/pip install --upgrade pip` \
`anaconda3/bin/pip install -r ~/NeutronLab/requirements.txt --upgrade` \
`sudo apt-get install python-pyqt5` \
`chmod +x *.sh`

### Запуск:
В Windows необходимо запустить X-Ming.
В терминале Debian: \
`cd ~/NeutronLab` \
`./NeutronLab.sh`
