Name:           grub-btrfs-timeshift
Version:        {{{ git_dir_version }}}
Release:        1%{?dist}
Summary:        Improves grub by adding "btrfs snapshots" to the grub menu.

License:        GPLv3
URL:            https://github.com/KyleGospo/grub-btrfs

VCS:            {{{ git_dir_vcs }}}
Source:        	{{{ git_dir_pack }}}
BuildArch:      noarch

Patch0:         no_root.patch
Patch1:         fedora.patch
Patch2:         timeshift.patch

Requires:       grub2-common
Requires:       timeshift

BuildRequires:  make
BuildRequires:  systemd-rpm-macros

# Don't allow this package to be used along-side the snapshot/snapper package.
Conflicts:      grub-btrfs

%description
Improves grub by adding "btrfs snapshots" to the grub menu.

You can boot your system on a "snapshot" from the grub menu.
Supports snapshots created with Timeshift

# Disable debug packages
%define debug_package %{nil}

%prep
{{{ git_dir_setup_macro }}}
%patch0
%patch1
%patch2

# This will copy the files generated by the `make` command above into
# the installable rpm package.
%install
make DESTDIR=%buildroot PKGNAME=%{name} install

# Do post-installation
%post
%systemd_post grub-btrfs.path

# Do before uninstallation
%preun
%systemd_preun grub-btrfs.path

# Do after uninstallation
%postun
%systemd_postun_with_restart grub-btrfs.path

# This lists all the files that are included in the rpm package and that
# are going to be installed into target system where the rpm is installed.
%files
%license LICENSE
%doc README.md
%doc initramfs-overlayfs.md
%{_sysconfdir}/grub.d/41_snapshots-btrfs
%{_sysconfdir}/default/grub-btrfs/config
%{_unitdir}/grub-btrfs.path
%{_unitdir}/grub-btrfs.service

# Finally, changes from the latest release of your application are generated from
# your project's Git history. It will be empty until you make first annotated Git tag.
%changelog
{{{ git_dir_changelog }}}