%{?scl:%scl_package rubygem-%{gem_name}}
%{!?scl:%global pkg_name %{name}}

%global gem_name builder

Summary: Builders for MarkUp
Name: %{?scl_prefix}rubygem-%{gem_name}
Version: 3.2.2
Release: 6%{?dist}
Group: Development/Languages
License: MIT
URL: http://onestepback.org
Source0: http://rubygems.org/gems/%{gem_name}-%{version}.gem

# Builder carries copy of Blankslate, which was in the meantime extracted into
# independent gem.
# https://github.com/jimweirich/builder/issues/24
#
# Moreover, rubygem-blankslate is not yet in Fedora.
# https://bugzilla.redhat.com/show_bug.cgi?id=771316
#
# Requires: %{?scl_prefix}rubygem(blankslate)
Requires: %{?scl_prefix_ruby}ruby(release)
Requires: %{?scl_prefix_ruby}ruby(rubygems)
BuildRequires: %{?scl_prefix_ruby}ruby(release)
BuildRequires: %{?scl_prefix_ruby}rubygems-devel
BuildRequires: %{?scl_prefix_ruby}ruby
BuildRequires: %{?scl_prefix_ruby}rubygem(minitest)
BuildArch: noarch
Provides: %{?scl_prefix}rubygem(%{gem_name}) = %{version}

%description
Builder provides a number of builder objects that make creating structured
data simple to do. Currently the following builder objects are supported:
* XML Markup
* XML Events

%package doc
Summary: Documentation for %{pkg_name}
Group: Documentation
Requires: %{?scl_prefix}%{pkg_name} = %{version}-%{release}
BuildArch: noarch

%description doc
Documentation for %{pkg_name}

%prep
%setup -n %{pkg_name}-%{version} -q -c -T
%{?scl:scl enable %{scl} - << \EOF}
%gem_install -n %{SOURCE0}
%{?scl:EOF}


%build

%install
mkdir -p %{buildroot}%{gem_dir}
cp -a .%{gem_dir}/* \
        %{buildroot}%{gem_dir}/

# Fix anything executable that does not have a shebang.
for file in `find %{buildroot}/%{gem_instdir} -name "*.rb"`; do
    [ ! -z "`head -n 1 $file | grep \"^#!\"`" ] && chmod +x $file
done

chmod -x %{buildroot}%{gem_instdir}/doc/releases/builder-2.1.1.rdoc

%check
pushd .%{gem_instdir}

# @xml.name overwritten by @xml.'bob'
sed -i 's|def name|def bobs_name|' ./test/test_markupbuilder.rb
sed -i 's|(name)|("bob")|' ./test/test_markupbuilder.rb

%{?scl:scl enable %{scl} - << \EOF}
ruby -rminitest/autorun -rrubygems -I.:lib:test - << \EOR
  module Kernel
    alias orig_require require
    remove_method :require

    def require path
      orig_require path unless path == 'test/unit'
    end

    def assert_nothing_raised
      yield
    end

    def assert_not_nil exp, msg=nil
      msg = message(msg) { "<#{mu_pp(exp)}> expected to not be nil" }
      assert(!exp.nil?, msg)
    end
  end
  Test = Minitest
  module Minitest::Assertions
    alias assert_raise assert_raises
  end
  Dir.glob "./test/test_*.rb", &method(:require)
EOR
%{?scl:EOF}
popd

%files
%dir %{gem_instdir}
%doc %{gem_instdir}/MIT-LICENSE
%{gem_libdir}
%exclude %{gem_cache}
%{gem_spec}

%files doc
%doc %{gem_docdir}
%doc %{gem_instdir}/CHANGES
%doc %{gem_instdir}/README.md
%doc %{gem_instdir}/Rakefile
%doc %{gem_instdir}/doc/
%doc %{gem_instdir}/rakelib/
%{gem_instdir}/test/

%changelog
* Fri Feb 19 2016 Pavel Valena <pvalena@redhat.com> - 3.2.2-6
- Add scl macros

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 3.2.2-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.2.2-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Tue May 26 2015 Josef Stribny <jstribny@redhat.com> - 3.2.2-3
- Fix tests to run with Minitest

* Sun Jun 08 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.2.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Tue May 20 2014 Vít Ondruch <vondruch@redhat.com> - 3.2.2-1
- Update to Builder 3.2.2.

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.1.4-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Sat Feb 23 2013 Vít Ondruch <vondruch@redhat.com> - 3.1.4-3
- Rebuild for https://fedoraproject.org/wiki/Features/Ruby_2.0.0

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.1.4-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Wed Oct 17 2012 Vít Ondruch <vondruch@redhat.com> - 3.1.4-1
- Update to Builder 3.1.4.

* Thu Oct 11 2012 Vít Ondruch <vondruch@redhat.com> - 3.1.3-1
- Update to Builder 3.1.3.

* Wed Jul 18 2012 Vít Ondruch <vondruch@redhat.com> - 3.0.0-1
- Update to Builder 3.0.0.

* Fri Feb 03 2012 Vít Ondruch <vondruch@redhat.com> - 2.1.2-9
- Fixed license.

* Thu Jan 19 2012 Vít Ondruch <vondruch@redhat.com> - 2.1.2-8
- Rebuilt for Ruby 1.9.3.

* Sat Jan 14 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.1.2-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Fri Nov 25 2011 Vít Ondruch <vondruch@redhat.com> - 2.1.2-6
- Fix FTBFS rhbz#712927.

* Wed Feb 09 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.1.2-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Sun Jul 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.1.2-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Wed Feb 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.1.2-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Tue Jul 29 2008 Jeroen van Meeuwen <kanarip@kanarip.com> - 2.1.2-2
- Rebuild for review

* Sun Jul 13 2008 root <root@oss1-repo.usersys.redhat.com> - 2.1.2-1
- Initial package
