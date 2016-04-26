rdap.io
=======

What is this?
--------------

This is the source for rdap.io_ - an experiment on registrar
services discovery using RDAP. This is used by the great http://ten.pm site
to provide users with awesome domain name configuration options.

It uses dnsknife_ for TPDA.

.. _rdap.io: http://rdap.io/domain/ten.pm
.. _dnsknife: https://github.com/gandi/dnsknife


What does it do?
-----------------

If TPDA_ is available at the registrar, automatic domain name configuration
is started.

If not, we redirect the customer to registrar-specific documentation, which
is such an enormous added value, isn't it ?

What can I do here?
--------------------

If you're a registrar, or a third party service provider, help us work on a
better "TPDA" specification. RDAP is coming, and extends the currently
available protocols enough so we can fully automate and enhance customer experience
with name configuration.

If you want to help, help us add per-registrar documentation here.

.. _TPDA: https://github.com/Gandi/dnsknife/blob/master/docs/extending_registrar_functions.txt

What is the future of this awesome thing?
-----------------------------------------

This is obviously a temporary workaround to a missing RDAP infrastructure.

We hope that RDAP extensions on registrar services will help everyone achieve the very same result
from their own RDAP servers and documentation websites soon. In the meantime, this experiment is
the opportunity to work on a common protocol and have a working thing.

Moving from hardcoded "rdap.io" entrypoint to the actual RDAP infrastructure, when it's ready,
will be painless. So let's work on how we'll use it right away.
