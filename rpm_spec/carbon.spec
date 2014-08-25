%define name carbon
%define version 0.9.12
%define unmangled_version 0.9.12
%define release 1

Summary: Backend data caching and persistence daemon for Graphite
Name: %{name}
Version: %{version}
Release: %{release}
Source0: %{name}-%{unmangled_version}.tar.gz
License: Apache Software License 2.0
Group: Development/Libraries
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-buildroot
Prefix: %{_prefix}
BuildArch: noarch
Vendor: Chris Davis <chrismd@gmail.com>
Packager: Tim Hunter <tim@thunter.ca>
Provides: carbon
Requires: python-twisted whisper
Obsoletes: 0.9.11
Url: http://graphite-project.github.com

%description
Backend data caching and persistence daemon for Graphite

%prep
%setup -n %{name}-%{unmangled_version}

%build
python setup.py build

%install
python setup.py install -O1 --root=$RPM_BUILD_ROOT --record=INSTALLED_FILES

%clean
rm -rf $RPM_BUILD_ROOT

%post
# Configure init scripts
INIT_SCRIPTS="carbon-cache carbon-relay carbon-aggregator";
for s in $INIT_SCRIPTS; do
    /bin/chmod +x /etc/init.d/${s};

    if [ -x /sbin/chkconfig ]; then
        /sbin/chkconfig --add ${s};
    fi;
done;

GRAPHITE_PATH=/opt/graphite
CONFFILES="carbon.conf relay-rules.conf storage-schemas.conf storage-aggregation.conf"
for i in $CONFFILES; do
    if [ ! -e ${GRAPHITE_PATH}/conf/$i ]; then
        /bin/echo "No pre-existing $i - creating from example."
        /bin/cp ${GRAPHITE_PATH}/conf/$i.example ${GRAPHITE_PATH}/conf/$i;
    fi;
done;


%files -f INSTALLED_FILES
%defattr(-,root,root)
