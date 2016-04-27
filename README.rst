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

If you are a domain name operator, you could setup a TPDA entry on your Nameservers:

.. code:: bind

    record._tpda._tcp.ns1.example.com.  IN  URI "http://doc.example.com/zonerecordsetup"
    email._tpda._tcp.ns1.example.com.   IN  URI "http://doc.example.com/settingup_mx.html"
    website._tpda._tcp.ns1.example.com. IN  URI "https://api.example.com/tpda/v1"

This would redirect your users to the appropriate documentation, or TPDA service if you
have one. Note that you need a nameserver supporting the RFC7533 format (from
draft-faltstrom-uri-08), and there is a bind bug fixed in bind 9.9.6 or 9.10.1

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
