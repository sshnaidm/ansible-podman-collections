%global collection_namespace containers
%global collection_name podman

Name:           ansible-collection-%{collection_namespace}-%{collection_name}
Version:        1.4.1
Release:        1%{?dist}
Summary:        Podman Ansible collection for Podman containers

License:        GPLv3+ and Python
URL:            %{ansible_collection_url}
Source:         https://github.com/containers/ansible-podman-collections/archive/%{version}.tar.gz

BuildRequires:  ansible >= 2.9.10

BuildArch:      noarch

%description
%{summary}.

%prep
%autosetup -n ansible-podman-collections-%{version}
sed -i -e 's/version:.*/version: %{version}/' galaxy.yml
find -type f ! -executable -type f -name '*.py' -print -exec sed -i -e '1{\@^#!.*@d}' '{}' +
rm -vr ci/ contrib/ tests/ ./galaxy.yml.in

%build
%ansible_collection_build

%install
%ansible_collection_install

%files
%license COPYING
%doc README.md
%{ansible_collection_files}

%changelog
* Tue Feb 09 2021 Sagi Shnaidman <sshnaidm@redhat.com> - 1.4.1
- Initial package

