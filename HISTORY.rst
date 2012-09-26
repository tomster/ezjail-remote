0.2.2 - Unreleased
------------------

 * provide a base class representing a jail for more convenient API usage
 * Use ezjail version 3.2.2 feature to create ZFS jails by default
 * Make use and configuration of sshd in created jail optional

0.2.1 - 2012-09-10
------------------

 * add support for creating ZFS (and other image based) jails

0.2 - 2012-09-07
----------------

 * split installation into ``bootstrap`` (which has proven itself useful outside of a ezjail setup) and ``install``
 * added support for ZFS
 * can install ezjail from CVS
 * added support for flavours outside the ezjail-remote package itself (using namespace packages for ezjailremote.flavours.\*)
 * added `start`, `stop` and `jls` commands.

0.1 - 2011-07-29
----------------

Initial release. Provides 'pass through' of all commands, as well as enhanced versions for ``create`` and ``destroy``.
