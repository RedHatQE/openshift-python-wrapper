# Generated using https://github.com/RedHatQE/openshift-python-wrapper/blob/main/scripts/resource/README.md

from typing import Any, Dict, Optional
from ocp_resources.resource import Resource


class APIServer(Resource):
    """
    APIServer holds configuration (like serving certificates, client CA and CORS
    domains) shared by all API servers in the system, among them especially
    kube-apiserver and openshift-apiserver. The canonical name of an instance is
    'cluster'.
     Compatibility level 1: Stable within a major release for a minimum of 12
    months or 3 minor releases (whichever is longer).
    """

    api_group: str = Resource.ApiGroup.CONFIG_OPENSHIFT_IO

    def __init__(
        self,
        additional_cors_allowed_origins: Optional[Dict[str, Any]] = None,
        audit: Optional[Dict[str, Any]] = None,
        client_ca: Optional[Dict[str, Any]] = None,
        encryption: Optional[Dict[str, Any]] = None,
        serving_certs: Optional[Dict[str, Any]] = None,
        tls_security_profile: Optional[Dict[str, Any]] = None,
        **kwargs: Any,
    ) -> None:
        """
        Args:
            additional_cors_allowed_origins(Dict[Any, Any]): additionalCORSAllowedOrigins lists additional, user-defined regular
              expressions describing hosts for which the API server allows access using
              the CORS headers. This may be needed to access the API and the integrated
              OAuth server from JavaScript applications. The values are regular
              expressions that correspond to the Golang regular expression language.

            audit(Dict[Any, Any]): audit specifies the settings for audit configuration to be applied to all
              OpenShift-provided API servers in the cluster.

              FIELDS:
                customRules	<[]Object>
                  customRules specify profiles per group. These profile take precedence over
                  the top-level profile field if they apply. They are evaluation from top to
                  bottom and the first one that matches, applies.

                profile	<string>
                  profile specifies the name of the desired top-level audit profile to be
                  applied to all requests sent to any of the OpenShift-provided API servers in
                  the cluster (kube-apiserver, openshift-apiserver and oauth-apiserver), with
                  the exception of those requests that match one or more of the customRules.
                   The following profiles are provided: - Default: default policy which means
                  MetaData level logging with the exception of events (not logged at all),
                  oauthaccesstokens and oauthauthorizetokens (both logged at RequestBody
                  level). - WriteRequestBodies: like 'Default', but logs request and response
                  HTTP payloads for write requests (create, update, patch). -
                  AllRequestBodies: like 'WriteRequestBodies', but also logs request and
                  response HTTP payloads for read requests (get, list). - None: no requests
                  are logged at all, not even oauthaccesstokens and oauthauthorizetokens.
                   Warning: It is not recommended to disable audit logging by using the `None`
                  profile unless you are fully aware of the risks of not logging data that can
                  be beneficial when troubleshooting issues. If you disable audit logging and
                  a support situation arises, you might need to enable audit logging and
                  reproduce the issue in order to troubleshoot properly.
                   If unset, the 'Default' profile is used as the default.

            client_ca(Dict[Any, Any]): clientCA references a ConfigMap containing a certificate bundle for the
              signers that will be recognized for incoming client certificates in addition
              to the operator managed signers. If this is empty, then only operator
              managed signers are valid. You usually only have to set this if you have
              your own PKI you wish to honor client certificates from. The ConfigMap must
              exist in the openshift-config namespace and contain the following required
              fields: - ConfigMap.Data["ca-bundle.crt"] - CA bundle.

              FIELDS:
                name	<string> -required-
                  name is the metadata.name of the referenced config map

            encryption(Dict[Any, Any]): encryption allows the configuration of encryption of resources at the
              datastore layer.

              FIELDS:
                type	<string>
                  type defines what encryption type should be used to encrypt resources at the
                  datastore layer. When this field is unset (i.e. when it is set to the empty
                  string), identity is implied. The behavior of unset can and will change over
                  time.  Even if encryption is enabled by default, the meaning of unset may
                  change to a different encryption type based on changes in best practices.
                   When encryption is enabled, all sensitive resources shipped with the
                  platform are encrypted. This list of sensitive resources can and will change
                  over time.  The current authoritative list is:
                   1. secrets 2. configmaps 3. routes.route.openshift.io 4.
                  oauthaccesstokens.oauth.openshift.io 5.
                  oauthauthorizetokens.oauth.openshift.io

            serving_certs(Dict[Any, Any]): servingCert is the TLS cert info for serving secure traffic. If not
              specified, operator managed certificates will be used for serving secure
              traffic.

              FIELDS:
                namedCertificates	<[]Object>
                  namedCertificates references secrets containing the TLS cert info for
                  serving secure traffic to specific hostnames. If no named certificates are
                  provided, or no named certificates match the server name as understood by a
                  client, the defaultServingCertificate will be used.

            tls_security_profile(Dict[Any, Any]): tlsSecurityProfile specifies settings for TLS connections for externally
              exposed servers.
               If unset, a default (which may change between releases) is chosen. Note
              that only Old, Intermediate and Custom profiles are currently supported, and
              the maximum available minTLSVersion is VersionTLS12.

              FIELDS:
                custom	<Object>
                  custom is a user-defined TLS security profile. Be extremely careful using a
                  custom profile as invalid configurations can be catastrophic. An example
                  custom profile looks like this:
                   ciphers:
                   - ECDHE-ECDSA-CHACHA20-POLY1305
                   - ECDHE-RSA-CHACHA20-POLY1305
                   - ECDHE-RSA-AES128-GCM-SHA256
                   - ECDHE-ECDSA-AES128-GCM-SHA256
                   minTLSVersion: VersionTLS11

                intermediate	<Object>
                  intermediate is a TLS security profile based on:
                   https://wiki.mozilla.org/Security/Server_Side_TLS#Intermediate_compatibility_.28recommended.29
                   and looks like this (yaml):
                   ciphers:
                   - TLS_AES_128_GCM_SHA256
                   - TLS_AES_256_GCM_SHA384
                   - TLS_CHACHA20_POLY1305_SHA256
                   - ECDHE-ECDSA-AES128-GCM-SHA256
                   - ECDHE-RSA-AES128-GCM-SHA256
                   - ECDHE-ECDSA-AES256-GCM-SHA384
                   - ECDHE-RSA-AES256-GCM-SHA384
                   - ECDHE-ECDSA-CHACHA20-POLY1305
                   - ECDHE-RSA-CHACHA20-POLY1305
                   - DHE-RSA-AES128-GCM-SHA256
                   - DHE-RSA-AES256-GCM-SHA384
                   minTLSVersion: VersionTLS12

                modern	<Object>
                  modern is a TLS security profile based on:
                   https://wiki.mozilla.org/Security/Server_Side_TLS#Modern_compatibility
                   and looks like this (yaml):
                   ciphers:
                   - TLS_AES_128_GCM_SHA256
                   - TLS_AES_256_GCM_SHA384
                   - TLS_CHACHA20_POLY1305_SHA256
                   minTLSVersion: VersionTLS13

                old	<Object>
                  old is a TLS security profile based on:
                   https://wiki.mozilla.org/Security/Server_Side_TLS#Old_backward_compatibility
                   and looks like this (yaml):
                   ciphers:
                   - TLS_AES_128_GCM_SHA256
                   - TLS_AES_256_GCM_SHA384
                   - TLS_CHACHA20_POLY1305_SHA256
                   - ECDHE-ECDSA-AES128-GCM-SHA256
                   - ECDHE-RSA-AES128-GCM-SHA256
                   - ECDHE-ECDSA-AES256-GCM-SHA384
                   - ECDHE-RSA-AES256-GCM-SHA384
                   - ECDHE-ECDSA-CHACHA20-POLY1305
                   - ECDHE-RSA-CHACHA20-POLY1305
                   - DHE-RSA-AES128-GCM-SHA256
                   - DHE-RSA-AES256-GCM-SHA384
                   - DHE-RSA-CHACHA20-POLY1305
                   - ECDHE-ECDSA-AES128-SHA256
                   - ECDHE-RSA-AES128-SHA256
                   - ECDHE-ECDSA-AES128-SHA
                   - ECDHE-RSA-AES128-SHA
                   - ECDHE-ECDSA-AES256-SHA384
                   - ECDHE-RSA-AES256-SHA384
                   - ECDHE-ECDSA-AES256-SHA
                   - ECDHE-RSA-AES256-SHA
                   - DHE-RSA-AES128-SHA256
                   - DHE-RSA-AES256-SHA256
                   - AES128-GCM-SHA256
                   - AES256-GCM-SHA384
                   - AES128-SHA256
                   - AES256-SHA256
                   - AES128-SHA
                   - AES256-SHA
                   - DES-CBC3-SHA
                   minTLSVersion: VersionTLS10

                type	<string>
                  type is one of Old, Intermediate, Modern or Custom. Custom provides the
                  ability to specify individual TLS security profile parameters. Old,
                  Intermediate and Modern are TLS security profiles based on:
                   https://wiki.mozilla.org/Security/Server_Side_TLS#Recommended_configurations
                   The profiles are intent based, so they may change over time as new ciphers
                  are developed and existing ciphers are found to be insecure.  Depending on
                  precisely which ciphers are available to a process, the list may be reduced.
                   Note that the Modern profile is currently not supported because it is not
                  yet well adopted by common software libraries.

        """
        super().__init__(**kwargs)

        self.additional_cors_allowed_origins = additional_cors_allowed_origins
        self.audit = audit
        self.client_ca = client_ca
        self.encryption = encryption
        self.serving_certs = serving_certs
        self.tls_security_profile = tls_security_profile

    def to_dict(self) -> None:
        super().to_dict()

        if not self.yaml_file:
            self.res["spec"] = {}
            _spec = self.res["spec"]

            if self.additional_cors_allowed_origins:
                _spec["additionalCORSAllowedOrigins"] = self.additional_cors_allowed_origins

            if self.audit:
                _spec["audit"] = self.audit

            if self.client_ca:
                _spec["clientCA"] = self.client_ca

            if self.encryption:
                _spec["encryption"] = self.encryption

            if self.serving_certs:
                _spec["servingCerts"] = self.serving_certs

            if self.tls_security_profile:
                _spec["tlsSecurityProfile"] = self.tls_security_profile
