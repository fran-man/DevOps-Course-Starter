# -*- mode: ruby -*-
# vi: set ft=ruby :

# All Vagrant configuration is done below. The "2" in Vagrant.configure
# configures the configuration version (we support older styles for
# backwards compatibility). Please don't change it unless you know what
# you're doing.
Vagrant.configure("2") do |config|
  config.vm.box = "hashicorp/bionic64"

  # Create a forwarded port mapping which allows access to a specific port
  # within the machine from a port on the host machine and only allow access
  # via 127.0.0.1 to disable public access
  config.vm.network "forwarded_port", guest: 5000, host: 8080, host_ip: "127.0.0.1"

  # Create a private network, which allows host-only access to the machine
  # using a specific IP.
  # config.vm.network "private_network", ip: "192.168.33.10"

  # Share an additional folder to the guest VM. The first argument is
  # the path on the host to the actual folder. The second argument is
  # the path on the guest to mount the folder. And the optional third
  # argument is a set of non-required options.
  # config.vm.synced_folder "../data", "/vagrant_data"

  config.vm.provision "shell", privileged: false, inline: <<-SHELL
    sudo apt-get update

    sudo apt-get install -y build-essential libssl-dev zlib1g-dev libbz2-dev \
    libreadline-dev libsqlite3-dev wget curl llvm libncurses5-dev libncursesw5-dev \
    xz-utils tk-dev libffi-dev liblzma-dev python-openssl git

    # TODO: See if these can be combined together. Keeping separate as I am not sure of the
    # impact of --no-install-recommends etc.
    sudo apt-get install -y --no-install-recommends make build-essential libssl-dev \
    zlib1g-dev libbz2-dev libreadline-dev libsqlite3-dev wget curl llvm libncurses5-dev \
    xz-utils tk-dev libxml2-dev libxmlsec1-dev libffi-dev liblzma-dev

    mkdir .pyenv
    git clone https://github.com/pyenv/pyenv.git .pyenv

    echo 'export PYENV_ROOT="$HOME/.pyenv"' >> .profile
    echo 'export PATH="$PYENV_ROOT/bin:$PATH"' >> .profile
    echo -e 'if command -v pyenv 1>/dev/null 2>&1; then\n  eval "$(pyenv init -)"\nfi' >> .profile

    # Reload the changes we made into our current shell
    source .profile

    pyenv install 3.8.6
    pyenv global 3.8.6

    curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py | python

    # Due to issues running on a windows host, we need to move this to a native
    # directory inside the vm...
    mkdir Devops-Starter
    cp -r /vagrant/* Devops-Starter/
    cp /vagrant/.env Devops-Starter/
  SHELL

  config.trigger.after :up do |trigger|
  trigger.name = "Launching App"
  trigger.info = "Setting up and running the flask application"
  trigger.run_remote = {privileged: false, inline: "
    cd /home/vagrant/Devops-Starter
    /home/vagrant/.poetry/bin/poetry add requests
    /home/vagrant/.poetry/bin/poetry install
    # Set 0.0.0.0 to allow access from outside (i.e. host machine)
    poetry run flask run --host=0.0.0.0
  "}
  end
end
