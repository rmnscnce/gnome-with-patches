# Tarfile created using git
# git clone git://git.gnome.org/gjs
# git archive --format=tar --prefix=%{name}-%{version}/ %{git_version} | bzip2 > ~/%{name}-%{version}-%{gitdate}.tar.bz2
%define gitdate 20100114
%define git_version b3b2053
%define tarfile %{name}-%{version}-%{gitdate}.tar.bz2

Name:           gjs
Version:        0.5
Release:        0.1%{?dist}
Summary:        Javascript Bindings for GNOME

Group:          System Environment/Libraries
# The following files contain code from Mozilla which
# is triple licensed under MPL1.1/LGPLv2+/GPLv2+:
# The console module (modules/console.c)
# Stack printer (gjs/stack.c)
License:        MIT and (MPLv1.1 or GPLv2+ or LGPLv2+)
URL:            http://live.gnome.org/Gjs/
# Source0:        ftp://ftp.gnome.org/pub/GNOME/sources/%{name}/0.4/%{name}-%{version}.tar.bz2
Source0:        %{tarfile}
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires: xulrunner-devel
BuildRequires: gobject-introspection-devel
BuildRequires: dbus-glib-devel
BuildRequires: pkgconfig

# For the git snaphot
BuildRequires: libtool
BuildRequires: gnome-common

%description
Gjs allows using GNOME libraries from Javascript. It's based on the
Spidermonkey Javascript engine from Mozilla and the GObject introspection
framework.

%package devel
Summary: Development package for %{name}
Group: Development/Libraries
Requires: %{name} = %{version}-%{release}
Requires: pkgconfig

%description devel
Files for development with %{name}.

%prep
%setup -q

# Don't run configure from autogen.sh
NOCONFIGURE=yes ./autogen.sh

./autogen.sh

%build
%configure --disable-static
# Remove rpath as per https://fedoraproject.org/wiki/Packaging/Guidelines#Beware_of_Rpath
sed -i 's|^hardcode_libdir_flag_spec=.*|hardcode_libdir_flag_spec=""|g' libtool
sed -i 's|^runpath_var=LD_RUN_PATH|runpath_var=DIE_RPATH_DIE|g' libtool

make %{?_smp_mflags}

%install
rm -rf %{buildroot}
make install DESTDIR=%{buildroot}

#Remove libtool archives.
find %{buildroot} -name '*.la' -exec rm -f {} ';'

%check
#make check

%clean
rm -rf %{buildroot}

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%files
%defattr(-,root,root,-)
%doc COPYING NEWS README
%{_bindir}/gjs
%{_bindir}/gjs-console
%{_libdir}/*.so.*
%{_libdir}/gjs-1.0
%{_datadir}/gjs-1.0

%files devel
%defattr(-,root,root,-)
%doc examples/*
%{_includedir}/gjs-1.0
%{_libdir}/pkgconfig/gjs-1.0.pc
%{_libdir}/pkgconfig/gjs-gi-1.0.pc
%{_libdir}/pkgconfig/gjs-dbus-1.0.pc
%{_libdir}/*.so

%changelog
* Thu Jan 14 2010 Peter Robinson <pbrobinson@gmail.com> 0.5-0.1
- Move to git snapshot to fix compile against xulrunner 1.9.2.1

* Thu Aug 27 2009 Peter Robinson <pbrobinson@gmail.com> 0.4-1
- New upstream 0.4 release

* Fri Aug  7 2009 Peter Robinson <pbrobinson@gmail.com> 0.3-2
- Updates from the review request

* Wed Jul  8 2009 Peter Robinson <pbrobinson@gmail.com> 0.3-1
- New upstream release. Clarify licensing for review

* Sat Jun 27 2009 Peter Robinson <pbrobinson@gmail.com> 0.2-1
- Initial packaging
