%if 0%{?fedora}
%global with_devel 1
%global with_bundled 0
%global with_debug 1
%global with_check 1
%global with_unit_test 1
%else
%global with_devel 1
%global with_bundled 1
%global with_debug 0
%global with_check 1
%global with_unit_test 1
%endif

# Determine if systemd will be used
%if ( 0%{?fedora} && 0%{?fedora} > 16 ) || ( 0%{?rhel} && 0%{?rhel} > 6 )
%global with_systemd 1
%endif

%if 0%{?with_debug}
%global _dwz_low_mem_die_limit 0
%else
%global debug_package   %{nil}
%endif

%global provider        github
%global provider_tld    com
%global project         heketi
%global repo            heketi
# https://github.com/heketi/heketi
%global provider_prefix %{provider}.%{provider_tld}/%{project}/%{repo}
%global import_path     %{provider_prefix}
%global commit          3f4a5b1b6edff87232e8b24533c53b4151ebd9c7
%global shortcommit     %(c=%{commit}; echo ${c:0:7})

Name:           %{repo}
Version:        1.0.0
Release:        1%{?dist}
Summary:        RESTful based volume management framework for GlusterFS
License:        ASL 2.0
URL:            https://%{provider_prefix}
Source0:        https://%{provider_prefix}/archive/%{commit}/%{repo}-%{shortcommit}.tar.gz
Source1:        %{name}.service
Source2:        %{name}.json
Source3:        %{name}-godeps-%{shortcommit}.tar.gz
Source4:        %{name}.initd

# e.g. el6 has ppc64 arch without gcc-go, so EA tag is required
ExclusiveArch:  %{?go_arches:%{go_arches}}%{!?go_arches:%{ix86} x86_64 %{arm}}
# If go_compiler is not set to 1, there is no virtual provide. Use golang instead.
BuildRequires:  %{?go_compiler:compiler(go-compiler)}%{!?go_compiler:golang}

Requires(pre):  shadow-utils

%if 0%{?with_systemd}
BuildRequires:  systemd
Requires(post): systemd
Requires(preun): systemd
Requires(postun): systemd
%else
Requires(post):   /sbin/chkconfig
Requires(preun):  /sbin/service
Requires(preun):  /sbin/chkconfig
Requires(postun): /sbin/service
%endif

%description
Heketi provides a RESTful management interface which can be used to manage
the life cycle of GlusterFS volumes.  With Heketi, cloud services like
OpenStack Manila, Kubernetes, and OpenShift can dynamically provision
GlusterFS volumes with any of the supported durability types.  Heketi
will automatically determine the location for bricks across the cluster,
making sure to place bricks and its replicas across different failure
domains.  Heketi also supports any number of GlusterFS clusters, allowing
cloud services to provide network file storage without being limited to a
single GlusterFS cluster.

%if 0%{?with_devel}
%package devel
Summary:       %{summary}
BuildArch:     noarch

%if 0%{?with_check} && ! 0%{?with_bundled}
BuildRequires: golang(github.com/auth0/go-jwt-middleware)
BuildRequires: golang(github.com/boltdb/bolt)
BuildRequires: golang(github.com/codegangsta/negroni)
BuildRequires: golang(github.com/dgrijalva/jwt-go)
BuildRequires: golang(github.com/gorilla/context)
BuildRequires: golang(github.com/gorilla/mux)
BuildRequires: golang(github.com/lpabon/godbc)
BuildRequires: golang(golang.org/x/crypto/ssh)
BuildRequires: golang(golang.org/x/crypto/ssh/agent)
%endif

%if 0%{?with_bundled} && 0%{?fedora}
Provides: bundled(golang(github.com/auth0/go-jwt-middleware)) = 8c897f7c3631a9e9405b9496fd8ce241acdef230
Provides: bundled(golang(github.com/boltdb/bolt)) = 980670afcebfd86727505b3061d8667195234816
Provides: bundled(golang(github.com/codegangsta/negroni)) = c7477ad8e330bef55bf1ebe300cf8aa67c492d1b
Provides: bundled(golang(github.com/dgrijalva/jwt-go)) = 5ca80149b9d3f8b863af0e2bb6742e608603bd99
Provides: bundled(golang(github.com/gorilla/context)) = 215affda49addc4c8ef7e2534915df2c8c35c6cd
Provides: bundled(golang(github.com/gorilla/mux)) = f15e0c49460fd49eebe2bcc8486b05d1bef68d3a
Provides: bundled(golang(github.com/lpabon/godbc)) = 9577782540c1398b710ddae1b86268ba03a19b0c
Provides: bundled(golang(golang.org/x/crypto/ssh)) = fcdb74e78f2621098ebc0376bbadffcf580ccfe4
Provides: bundled(golang(golang.org/x/crypto/ssh/agent)) = fcdb74e78f2621098ebc0376bbadffcf580ccfe4
%endif

Provides:      golang(%{import_path}/apps) = %{version}-%{release}
Provides:      golang(%{import_path}/apps/glusterfs) = %{version}-%{release}
Provides:      golang(%{import_path}/client/api/go-client) = %{version}-%{release}
Provides:      golang(%{import_path}/client/cli/go/commands) = %{version}-%{release}
Provides:      golang(%{import_path}/executors) = %{version}-%{release}
Provides:      golang(%{import_path}/executors/mockexec) = %{version}-%{release}
Provides:      golang(%{import_path}/executors/sshexec) = %{version}-%{release}
Provides:      golang(%{import_path}/middleware) = %{version}-%{release}
Provides:      golang(%{import_path}/rest) = %{version}-%{release}
Provides:      golang(%{import_path}/tests) = %{version}-%{release}
Provides:      golang(%{import_path}/utils) = %{version}-%{release}
Provides:      golang(%{import_path}/utils/ssh) = %{version}-%{release}

%description devel
%{summary}

This package contains library source intended for
building other packages which use import path with
%{import_path} prefix.
%endif

%if 0%{?with_unit_test} && 0%{?with_devel}
%package unit-test-devel
Summary:         Unit tests for %{name} package
# If go_compiler is not set to 1, there is no virtual provide. Use golang instead.
BuildRequires:  %{?go_compiler:compiler(go-compiler)}%{!?go_compiler:golang}

%if 0%{?with_check}
#Here comes all BuildRequires: PACKAGE the unit tests
#in %%check section need for running
%endif

# test subpackage tests code from devel subpackage
Requires:        %{name}-devel = %{version}-%{release}

%description unit-test-devel
%{summary}

This package contains unit tests for project
providing packages with %{import_path} prefix.
%endif

%prep
%setup -q -n %{repo}-%{commit}

%build
mkdir -p src/%{provider}.%{provider_tld}/%{project}
ln -s $(pwd) src/%{provider}.%{provider_tld}/%{project}/%{repo}

# ! Bundled
%if ! 0%{?with_bundled}
export GOPATH=$(pwd):%{gopath}
export LDFLAGS="-X main.HEKETI_VERSION %{version}"
%gobuild -o %{name}

export LDFLAGS="-X main.HEKETI_CLI_VERSION %{version}"
cd client/cli/go
%gobuild -o %{name}-cli
%else

# Bundled
export GOPATH=$(pwd):%{gopath}
tar xzf %{SOURCE3}

%define gohash %(head -c20 /dev/urandom | od -An -tx1 | tr -d '\ \\n')

go build -ldflags "-X main.HEKETI_VERSION %{version} -B 0x%{gohash}" -o %{name}

cd client/cli/go
go build -ldflags "-X main.HEKETI_CLI_VERSION %{version} -B 0x%{gohash}" -o %{name}-cli

%endif

%install
install -D -p -m 0755 %{name} %{buildroot}%{_bindir}/%{name}
install -D -p -m 0755 client/cli/go/%{name}-cli %{buildroot}%{_bindir}/%{name}-cli
install -d -m 0755 %{buildroot}%{_sysconfdir}/%{name}
install -m 644 -t %{buildroot}%{_sysconfdir}/%{name} %{SOURCE2}
%if 0%{?with_systemd}
install -D -p -m 0644 %{SOURCE1} %{buildroot}%{_unitdir}/%{name}.service
%else
install -D -p -m 0755 %{SOURCE4} %{buildroot}%{_sysconfdir}/init.d/%{name}
%endif

# And create /var/lib/heketi
install -d -m 0755 %{buildroot}%{_sharedstatedir}/%{name}


# source codes for building projects
%if 0%{?with_devel}
install -d -p %{buildroot}/%{gopath}/src/%{import_path}/
echo "%%dir %%{gopath}/src/%%{import_path}/." >> devel.file-list
# find all *.go but no *_test.go files and generate devel.file-list
for file in $(find . -iname "*.go" \! -iname "*_test.go") ; do
    echo "%%dir %%{gopath}/src/%%{import_path}/$(dirname $file)" >> devel.file-list
    install -d -p %{buildroot}/%{gopath}/src/%{import_path}/$(dirname $file)
    cp -pav $file %{buildroot}/%{gopath}/src/%{import_path}/$file
    echo "%%{gopath}/src/%%{import_path}/$file" >> devel.file-list
done
%endif

# testing files for this project
%if 0%{?with_unit_test} && 0%{?with_devel}
install -d -p %{buildroot}/%{gopath}/src/%{import_path}/
# find all *_test.go files and generate unit-test-devel.file-list
for file in $(find . -iname "*_test.go"); do
    echo "%%dir %%{gopath}/src/%%{import_path}/$(dirname $file)" >> devel.file-list
    install -d -p %{buildroot}/%{gopath}/src/%{import_path}/$(dirname $file)
    cp -pav $file %{buildroot}/%{gopath}/src/%{import_path}/$file
    echo "%%{gopath}/src/%%{import_path}/$file" >> unit-test-devel.file-list
done
%endif

%if 0%{?with_devel}
sort -u -o devel.file-list devel.file-list
%endif

%check
%if 0%{?with_check} && 0%{?with_unit_test} && 0%{?with_devel}

%if ! 0%{?with_bundled}
export GOPATH=%{buildroot}/%{gopath}:%{gopath}
%gotest %{import_path}/apps/glusterfs
%gotest %{import_path}/client/api/go-client
%gotest %{import_path}/middleware
%gotest %{import_path}/rest
%gotest %{import_path}/utils
%else
export GOPATH=$(pwd):%{gopath}
go test -v %{import_path}/apps/glusterfs
go test -v %{import_path}/client/api/go-client
go test -v %{import_path}/middleware
go test -v %{import_path}/rest
go test -v %{import_path}/utils
%endif
%endif

%pre
getent group %{name} >/dev/null || groupadd -r %{name}
getent passwd %{name} >/dev/null || useradd -r -g %{name} -d %{_sharedstatedir}/%{name} -s /sbin/nologin -c "heketi user" %{name}

%post
%if 0%{?with_systemd}
%systemd_post %{name}.service
%else
/sbin/chkconfig --add %{name}
%endif

%preun
%if 0%{?with_systemd}
%systemd_preun %{name}.service
%else
/sbin/service %{name} stop &> /dev/null
%endif

%postun
%if 0%{?with_systemd}
%systemd_postun %{name}.service
%else
/sbin/chkconfig --del %{name}
%endif


#define license tag if not already defined
%{!?_licensedir:%global license %doc}

%files
%license LICENSE
%doc README.md AUTHORS
%config(noreplace) %{_sysconfdir}/%{name}
%{_bindir}/%{name}
%{_bindir}/%{name}-cli
%dir %attr(-,%{name},%{name}) %{_sharedstatedir}/%{name}
%if 0%{?with_systemd}
%{_unitdir}/%{name}.service
%else
%{_sysconfdir}/init.d/%{name}
%endif

%if 0%{?with_devel}
%files devel -f devel.file-list
%license LICENSE
%doc README.md AUTHORS
%dir %{gopath}/src/%{provider}.%{provider_tld}/%{project}
%dir %{gopath}/src/%{import_path}
%endif

%if 0%{?with_unit_test} && 0%{?with_devel}
%files unit-test-devel -f unit-test-devel.file-list
%license LICENSE
%doc README.md AUTHORS
%endif

%changelog
* Mon Oct 12 2015 lpabon <lpabon@redhat.com> - 1.0.0-1
- First package for Fedora


