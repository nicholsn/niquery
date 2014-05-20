# Vagrantfile API/syntax version. Don't touch unless you know what you're doing!
VAGRANTFILE_API_VERSION = "2"

Vagrant.configure(VAGRANTFILE_API_VERSION) do |config|

  # Provision virtualbox with docker and container
  config.vm.define "base_config", primary: true do |base|
    base.vm.box = "precise64"
    base.vm.box_url = "http://files.vagrantup.com/precise64.box"
    base.vm.network :private_network, ip: "192.168.100.10"

    base.vm.provision :docker do |container|
      container.pull_images "ubuntu"
    end

    #base.vm.provision :shell,
    #  inline: "/usr/bin/docker build -t nicholsn/base /vagrant/provisioning/roles/common/files"

  end

  # Provision virtualbox with niquery using docker containers
  config.vm.define "niquery_config" do |niq|
    niq.vm.box = "precise64"
    niq.vm.box_url = "http://files.vagrantup.com/precise64.box"
    niq.vm.network :private_network, ip: "192.168.100.10"

    niq.vm.provision :docker do |container|
      container.pull_images "nicholsn/niquery"
      container.run "nicholsn/niquery"
    end

  end

  # Provision virtualbox with niquery (requires ansible)
  config.vm.define "vagrant_config" do |vagrant_config|
    vagrant_config.vm.box = "precise64"

    # The url from where the 'config.vm.box' box will be fetched if it
    # doesn't already exist on the user's system.

    vagrant_config.vm.box_url = "http://files.vagrantup.com/precise64.box"

    # Create a forwarded port mapping which allows access to a specific port
    # within the machine from a port on the host machine. In the example below,
    # accessing "localhost:8080" will access port 80 on the guest machine.
    # config.vm.network :forwarded_port, guest: 80, host: 8080

    # Create a private network, which allows host-only access to the machine
    # using a specific IP.

    vagrant_config.vm.network :private_network, ip: "192.168.100.10"

    # Create a public network, which generally matched to bridged network.
    # Bridged networks make the machine appear as another physical device on
    # your network.
    # config.vm.network :public_network

    # If true, then any SSH connections made will enable agent forwarding.
    # Default value: false
    # config.ssh.forward_agent = true

    # Share an additional folder to the guest VM. The first argument is
    # the path on the host to the actual folder. The second argument is
    # the path on the guest to mount the folder. And the optional third
    # argument is a set of non-required options.
    # config.vm.synced_folder "../data", "/vagrant_data"

    # Provider-specific configuration so you can fine-tune various
    # backing providers for Vagrant. These expose provider-specific options.
    # Example for VirtualBox:

    vagrant_config.vm.provider :virtualbox do |vb|

        #vb.customize ["modifyvm", :id, "--cpuexecutioncap", "50"]
        #vb.customize ["modifyvm", :id, "--ioapic", "on"]
        #vb.customize ["modifyvm", :id, "--memory", "1024"]
        #vb.customize ["modifyvm", :id, "--cpus", "2"]
    end

    # View the documentation for the provider you're using for more
    # information on available options.

    # Enable provisioning with Ansible.
    vagrant_config.vm.provision :ansible do |ansible|

      ansible.verbose = 'vvv'
      ansible.playbook = "provisioning/base.yml"
      ansible.inventory_path = "provisioning/hosts"
    end
  end
  
end
