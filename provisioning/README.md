## Niquery+Nginx Deployment

- Requires Ansible 1.2 or newer
- Expects Ubuntu 12.04 hosts

These playbooks deploy a simple all-in-one configuration of the Niquery neuroimaging framework and frontend by the Nginx web server. To use, run the playbook from Vagrant, like this:

	vagrant up

The playbooks will configure Niquery and Nginx. When the run is complete, you can visit the application at 192.168.100.10
