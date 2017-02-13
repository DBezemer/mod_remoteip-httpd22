#   Licensed to the Apache Software Foundation (ASF) under one or more
#   contributor license agreements.  See the NOTICE file distributed with
#   this work for additional information regarding copyright ownership.
#   The ASF licenses this file to You under the Apache License, Version 2.0
#   (the "License"); you may not use this file except in compliance with
#   the License.  You may obtain a copy of the License at
#
#       http://www.apache.org/licenses/LICENSE-2.0
#
#   Unless required by applicable law or agreed to in writing, software
#   distributed under the License is distributed on an "AS IS" BASIS,
#   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#   See the License for the specific language governing permissions and
#   limitations under the License.

%define apache_user    apache
%define apache_group   %{apache_user}
%define apache_conf    %{_sysconfdir}/httpd/conf.d/

%if 0%{?rhel} == 7
    # CentOS 7 forces ".el7.centos", wtf CentOS maintainers...
    %define dist .el7
%endif

%if 0%{?rhel} < 7
    %{!?__global_ldflags: %global __global_ldflags -Wl,-z,relro}
%endif

Summary: This is a backport of apache 2.4.1 mod_remoteip to apache 2.2.x.
Name: mod_remoteip-httpd22
Version: %{version}
Release: %{release}%{?dist}
License: Apache License, Version 2.0
Group: Development/Libraries
URL: http://httpd.apache.org/docs/2.4/mod/mod_remoteip.html
Source0: mod_remoteip.c
Source1: mod_remoteip.conf
Source2: Makefile
BuildRoot: %{_tmppath}/%{name}-%{version}-root
BuildRequires: pcre-devel pcre-devel make gcc httpd-devel
Requires: httpd

%description
This module is used to treat the useragent which initiated the request as the originating useragent as identified by httpd for the purposes of authorization and logging, even where that useragent is behind a load balancer, front end server, or proxy server.

The module overrides the client IP address for the connection with the useragent IP address reported in the request header configured with the RemoteIPHeader directive.

Once replaced as instructed, this overridden useragent IP address is then used for the mod_authz_host Require ip feature, is reported by mod_status, and is recorded by mod_log_config %a and core %a format strings. The underlying client IP of the connection is available in the %{c}a format string.

%prep
%setup -q

%build
%{__make} 

%install
[ "%{buildroot}" != "/" ] && %{__rm} -rf %{buildroot}

%{__install} -c -m 755 %{SOURCE1} %{buildroot}%{apache_conf}/mod_remoteip.conf
%{__install} -c -m 755 %{buildroot}/mod_remoteip.so %{_libdir}/httpd/modules/mod_remoteip.so
 
%clean
[ "%{buildroot}" != "/" ] && %{__rm} -rf %{buildroot}

%post
%if 0%{?el7}
%systemd_post httpd.service
%endif

%if 0%{?el6}
/sbin/service httpd condrestart >/dev/null 2>&1 || :
%endif

%postun
%if 0%{?el7}
%systemd_postun_with_restart httpd.service
%endif

%if 0%{?el6}
if [ "$1" -ge "1" ]; then
  /sbin/service httpd condrestart >/dev/null 2>&1 || :
fi
%endif

%files
%defattr(-,root,root)
%attr(0755,root,root) %config %{apache_conf}/mod_remoteip.conf
%attr(0755,root,root) %{_libdir}/httpd/modules/mod_remoteip.so

%changelog
* Mon Feb 13 2017 David Bezemer <info@davidbezemer.nl>
- Initial version
