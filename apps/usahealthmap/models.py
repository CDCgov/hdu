from django.db import models
from django.conf import settings
import json
from django.utils.translation import gettext_lazy as _


# wellknowns
# /.well-known/smart-configuration
# /.well-known/udap
# /.well-known/oauth-authorization-server/issuer1
# /.well-known/healthmap/dukehealth.com


class APIEndpointType(models.Model):
    code = models.CharField(max_length=50, unique=True)
    description = models.CharField(max_length=255)

    def __str__(self):
        return self.code

class APIEndpoint(models.Model):
    title = models.CharField(max_length=100)
    api_type = models.ForeignKey(APIEndpointType, on_delete=models.CASCADE)
    common_name = models.CharField(max_length=100, unique=True, db_index=True)
    root_url = models.URLField(unique=True)
    description = models.TextField(blank=True)
    requires_authentication = models.TextField(blank=True)
    authorization_details = models.TextField(blank=True)
    documentation_url = models.URLField(blank=True)
    contact_name = models.CharField(max_length=100, blank=True)
    contact_email = models.EmailField(blank=True)
    email_endpoint = models.EmailField(blank=True)
    public_keys = models.ManyToManyField('PublicKey', blank=True)
    issuer = models.CharField(max_length=512, blank=True)
    authorization_endpoint = models.CharField(max_length=512, blank=True)
    token_endpoint = models.CharField(max_length=512, blank=True)
    token_endpoint_auth_methods_supported = models.CharField(max_length=255, blank=True)
    token_endpoint_auth_signing_alg_values_supported = models.CharField(max_length=255, blank=True)
    userinfo_endpoint = models.CharField(max_length=255, blank=True)
    jwks_uri = models.URLField(blank=True)
    registration_endpoint = models.CharField(max_length=255, blank=True)
    scopes_supported = models.CharField(max_length=255, blank=True)
    response_types_supported = models.CharField(max_length=255, blank=True)
    service_documentation = models.CharField(max_length=255, blank=True)
    ui_locales_supported = models.CharField(max_length=255, blank=True)
    fhir_base_url = models.URLField(blank=True)
    date_created = models.DateField(auto_now_add=True)
    date_updated = models.DateField(auto_now=True)

    class Meta:
        verbose_name = "Endpoint and API"
        verbose_name_plural = "Endpoints and APIs"

    def __str__(self):
        return f'{self.common_name} - {self.api_type}'
    

class PublicKeyType(models.Model):
    code = models.CharField(max_length=50, unique=True)
    description = models.CharField(max_length=255)

    def __str__(self):
        return self.code

class PublicKey(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, default=None, null=True, blank=True)
    identifier = models.CharField(max_length=255, default='', unique=True)
    public_key_type = models.ForeignKey(PublicKeyType, on_delete=models.SET_NULL, null=True)
    kid = models.CharField(max_length=255, default='', unique=True, editable=False,
                           help_text=_('The Key ID for the public keys. This is often an thumbprint of the private key or FQDN.'))
    public_key = models.TextField(default='')
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    description = models.CharField(max_length=255, blank=True)
    date_last_used = models.DateField(null=True, blank=True)
    date_created = models.DateField(auto_now_add=True)
    date_updated = models.DateField(auto_now=True)

    class Meta:
        verbose_name = "Public Key"
        verbose_name_plural = "Public Keys"

    def __str__(self):
        return self.identifier

    def save(self, commit=True, **kwargs):

        if commit:
            if not self.kid:
                k = self.as_jwks
                self.kid = k['kid']
            super(PublicKey, self).save(**kwargs)

    @property
    def as_jwks(self):
        return json.loads(self.public_key)

class PrivateKey(models.Model):
    identifier = models.CharField(max_length=255, default='', unique=True)
    kid = models.CharField(max_length=255, default='', unique=True, editable=False,
                           help_text=_('The Key ID for the private key. This is often an thumbprint of the private key or FQDN.'))
    private_key = models.TextField(default='', editable=False)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.identifier

    def save(self, commit=True, **kwargs):

        if commit:
            if not self.kid:
                k = self.as_jwks
                self.kid = k['kid']
            super(PrivateKey, self).save(**kwargs)

    @property
    def as_jwks(self):
        return json.loads(self.private_key)

class EntityType(models.Model):
    code = models.CharField(max_length=50, unique=True)
    description = models.CharField(max_length=255)

    def __str__(self):
        return self.code

class Entity(models.Model):
    uuid = models.UUIDField(primary_key=True, editable=False)
    entity_type = models.ForeignKey(EntityType, on_delete=models.CASCADE)
    subject = models.CharField(max_length=1024, blank=True, db_index=True)
    common_name = models.CharField(max_length=1024, blank=True, db_index=True)
    subject_alternative_name = models.CharField(max_length=2048, blank=True)
    digest = models.TextField(blank=True)
    root_url = models.URLField(blank=True)
    title = models.CharField(max_length=256, blank=True)
    description = models.TextField()
    public_keys = models.ManyToManyField(PublicKey, blank=True)
    apis = models.ManyToManyField(APIEndpoint, blank=True)
    date_created = models.DateField(auto_now_add=True)
    date_updated = models.DateField(auto_now=True)

    class Meta:
        verbose_name = "Entity"
        verbose_name_plural = "Entities"

    def __str__(self):
        return self.common_name

    def url(self):
        return f"{settings.HOSTNAME_URL}/.well-known/{self.common_name}"        

class LegalBusinessEntity(models.Model):
    entity = models.ForeignKey(Entity, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    fein = models.CharField(max_length=20,db_index=True, blank=True)
    dba = models.CharField(max_length=255, blank=True)
    organization_type = models.CharField(max_length=100, blank=True)
    address_1 = models.CharField(max_length=255, blank=True)
    address_2 = models.CharField(max_length=255, blank=True)
    city = models.CharField(max_length=100, blank=True)
    state = models.CharField(max_length=50, blank=True)
    postal_code = models.CharField(max_length=20, blank=True)
    phone_number = models.CharField(max_length=20, blank=True)
    email = models.EmailField(blank=True)
    url = models.URLField(blank=True)
    public_keys = models.ManyToManyField(PublicKey, blank=True)
    apis = models.ManyToManyField(APIEndpoint, blank=True)
    date_created = models.DateField(auto_now_add=True)
    date_updated = models.DateField(auto_now=True)

    class Meta:
        verbose_name = "Legal Business Entity"
        verbose_name_plural = "Legal Business Entities"

    def __str__(self):
        return f'{self.fein} - {self.name}'

class NPI2(models.Model):
    common_name = models.CharField(max_length=10, unique=True, db_index=True)
    subject_alternative_name = models.CharField(max_length=1024, blank=True)
    entity = models.ForeignKey(Entity, on_delete=models.CASCADE)
    legal_business_entity = models.ForeignKey(LegalBusinessEntity, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    npi = models.CharField(max_length=100, db_index=True)
    description = models.TextField(blank=True)
    postal_code = models.CharField(max_length=10, blank=True)
    url_prefix = models.URLField(blank=True)
    is_subpart = models.BooleanField(default=False)
    is_a_facility = models.BooleanField(default=True)
    is_main_api_source = models.BooleanField(default=False)
    direct_secure_messaging_inbound_email = models.EmailField(blank=True)
    public_keys = models.ManyToManyField(PublicKey, blank=True)
    apis = models.ManyToManyField(APIEndpoint, blank=True)
    date_created = models.DateField(auto_now_add=True)
    date_updated = models.DateField(auto_now=True)

    class Meta:
        verbose_name = "NPI2 - Organization or Facility Code"
        verbose_name_plural = "NPI2 - Organization or Facility Code"

    def __str__(self):
        return f'{self.code}-{self.name}'
    
    @property
    def code(self):
        return self.npi

    @property
    def to_json(self):
        return {
            "npi": self.npi,
            "npi_type": "2",
            "name": self.name,
            "is_main_api_source": self.is_main_api_source,            
            "is_a_facility": self.is_a_facility,
            "is_subpart": self.is_subpart,
            "description": self.description,
            "postal_code": self.postal_code,
            "direct_secure_messaging_inbound_email": self.direct_secure_messaging_inbound_email,
            "apis": self.apis.count(),
            "public_keys": [pk.common_name for pk in self.public_keys.all()],
            "legal_business_entity": self.legal_business_entity.name if self.legal_business_entity else None,
            "date_created": self.date_created,
            "date_updated": self.date_updated,
        }

    @property
    def facility_name(self):
        return self.name

    def save(self, *args, **kwargs):
        self.url = f"{settings.HOSTNAME_URL}/usahealthmap/npi2/{self.code}"
        super().save(*args, **kwargs)

class OrganizationOther(models.Model):
    """These are organizations without an NPI. A common name is established."""
    common_name = models.CharField(max_length=100, unique=True, db_index=True)
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    address_1 = models.CharField(max_length=255, blank=True)
    address_2 = models.CharField(max_length=255, blank=True)
    city = models.CharField(max_length=100, blank=True)
    state = models.CharField(max_length=50, blank=True)
    postal_code = models.CharField(max_length=20, blank=True)
    phone_number = models.CharField(max_length=20, blank=True)
    email = models.EmailField(blank=True)
    url = models.URLField(blank=True)
    date_created = models.DateField(auto_now_add=True)
    date_updated = models.DateField(auto_now=True)

    class Meta:
        verbose_name = "Organization Other"
        verbose_name_plural = "Organizations Other"

    def __str__(self):
        return f'{self.common_name} - {self.name}'
    
    @property
    def organization_name(self):
        return self.name

    @property
    def to_json(self):
        return {
            "common_name": self.common_name,
            "name": self.name,
            "description": self.description,
            "address_1": self.address_1,
            "address_2": self.address_2,
            "city": self.city,
            "state": self.state,
            "postal_code": self.postal_code,
            "phone_number": self.phone_number,
            "email": self.email,
            "url": self.url,
        }
    
    def save(self, *args, **kwargs):
        self.url = f"{settings.HOSTNAME_URL}/.well-known/{self.common_name}"
        super().save(*args, **kwargs)


class Payer(models.Model):
    name = models.CharField(max_length=255, unique=True, db_index=True)
    entity = models.ForeignKey(Entity, on_delete=models.CASCADE)
    legal_business_entity = models.ForeignKey(LegalBusinessEntity, on_delete=models.CASCADE)

    
    class Meta:
        verbose_name = "Payer"
        verbose_name_plural = "Payers"

    def __str__(self):
        return self.name
    

class PayerPlan(models.Model):
    common_name = models.CharField(max_length=1024, unique=True, db_index=True)
    plan_id = models.CharField(max_length=255, unique=True, db_index=True)
    payer = models.ForeignKey(Payer, on_delete=models.CASCADE)
    name = models.CharField(max_length=255, unique=True, db_index=True)
    description = models.TextField(blank=True)
    url = models.URLField(blank=True)
    date_created = models.DateField(auto_now_add=True)
    date_updated = models.DateField(auto_now=True)

    class Meta:
        verbose_name = "Payer Plan"
        verbose_name_plural = "Payer Plans"

    def __str__(self):
        return f'{self.name}'
    
class NPI1(models.Model):
    npi = models.CharField(max_length=20, unique=True, db_index=True)
    common_name = models.CharField(max_length=20, unique=True, db_index=True)
    profile = models.ImageField(upload_to='individual_npis/profiles/', blank=True, null=True)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    credential = models.CharField(max_length=50, blank=True)
    taxonomy_code = models.CharField(max_length=50, blank=True)
    taxonomy_description = models.CharField(max_length=255, blank=True)
    url = models.URLField(blank=True)
    date_created = models.DateField(auto_now_add=True)
    date_updated = models.DateField(auto_now=True)

    class Meta:
        verbose_name = "NPI1 - Individual"
        verbose_name_plural = "NPI1 Individuals"


    def __str__(self):
        return f'{self.npi} - {self.first_name} {self.last_name}'
    
    @property
    def full_name(self):
        return f'{self.first_name} {self.last_name}'

    @property
    def to_json(self):
        return {
            "npi": self.npi,
            "first_name": self.first_name,
            "last_name": self.last_name,
            "credentials": self.credential,
            "taxonomy_code": self.taxonomy_code,
            "taxonomy_description": self.taxonomy_description,
            "organization_name": self.organization_name,
            "address_1": self.address_1,
            "address_2": self.address_2,
            "city": self.city,
            "state": self.state,
            "postal_code": self.postal_code,
            "phone_number": self.phone_number,
            "email": self.email,
            "public_keys": [pk.common_name for pk in self.entity.public_keys.all()],
            "direct_secure_messaging_inbound_email": self.direct_secure_messaging_inbound_email,
            "url": self.url,
        }
    
    def save(self, *args, **kwargs):
        self.common_name = self.npi
        self.url = f"{settings.HOSTNAME_URL}/.well-known/{self.npi}"
        super().save(*args, **kwargs)

class IndividualOther(models.Model):
    """These are individuals without an NPI. A common name is established."""
    entity = models.ForeignKey(Entity, on_delete=models.SET_NULL, null=True, blank=True)
    common_name = models.CharField(max_length=100, unique=True, db_index=True)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    profile = models.ImageField(upload_to='individual_others/profiles/', blank=True, null=True)
    credential = models.CharField(max_length=50, blank=True)
    organization_name = models.CharField(max_length=255, blank=True)
    address_1 = models.CharField(max_length=255, blank=True)
    address_2 = models.CharField(max_length=255, blank=True)
    city = models.CharField(max_length=100, blank=True)
    state = models.CharField(max_length=50, blank=True)
    postal_code = models.CharField(max_length=20, blank=True)
    phone_number = models.CharField(max_length=20, blank=True)
    email = models.EmailField(blank=True)
    url = models.URLField(blank=True)
    date_created = models.DateField(auto_now_add=True)
    date_updated = models.DateField(auto_now=True)

    class Meta:
        verbose_name = "Individual Other"
        verbose_name_plural = "Individual Others"

    def __str__(self):
        return f'{self.common_name} - {self.first_name} {self.last_name}'
    @property
    def to_json(self):
        return {
            "common_name": self.common_name,
            "first_name": self.first_name,
            "last_name": self.last_name,
            "credentials": self.credential,
            "organization_name": self.organization_name,
            "address_1": self.address_1,
            "address_2": self.address_2,
            "city": self.city,
            "state": self.state,
            "postal_code": self.postal_code,
            "phone_number": self.phone_number,
            "email": self.email,
            "url": self.url,
        }

    @property
    def full_name(self):
        return f'{self.first_name} {self.last_name}'
    
    def save(self, *args, **kwargs):
        self.url = f"{settings.HOSTNAME_URL}/.well-known/{self.common_name}"
        super().save(*args, **kwargs)

class MPI(models.Model):
    name_of_identifier = models.CharField(max_length=100)
    identifier = models.CharField
    date_of_birth = models.DateField(null=True, blank=True)
    state_code = models.CharField(max_length=2, unique=True, db_index=True)
    mpi_root_url = models.URLField(blank=True)
    description = models.CharField(max_length=255, blank=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True, related_name='mpi_user')
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True)
    date_created = models.DateField(auto_now_add=True)
    date_updated = models.DateField(auto_now=True)

    class Meta:
        verbose_name = "MPI"
        verbose_name_plural = "MPIs"

    def __str__(self):
        return f'{self.name_of_identifier}|{self.identifier}'



class PersonalIdentifier(models.Model):
    identifier = models.CharField(max_length=100, unique=True, db_index=True)
    description = models.CharField(max_length=255, blank=True)
    issuer = models.ForeignKey(Entity, on_delete=models.SET_NULL, null=True, blank=True)
    self_issued = models.BooleanField(default=False)
    digest = models.TextField(blank=True)

    class Meta:
        verbose_name = "Personal Identifier"
        verbose_name_plural = "Personal Identifiers"

    def __str__(self):
        return f'{self.issuer}-{self.identifier}'
    
    @property
    def sub(self):
        return f'{self.identifier}'

    @property
    def subject(self):
        return f'{self.identifier}'

class NPI1ToNPI2Mapping(models.Model):
    npi1 = models.ForeignKey(NPI1, on_delete=models.CASCADE)
    npi2 = models.ForeignKey(NPI2, on_delete=models.CASCADE)
    email = models.EmailField(blank=True)
    direct_secure_messaging_inbound_email = models.EmailField(blank=True)
    phone_number = models.CharField(max_length=20, blank=True)
    schedule = models.CharField(max_length=255, blank=True)
    date_created = models.DateField(auto_now_add=True)
    date_updated = models.DateField(auto_now=True)

    class Meta:
        verbose_name = "NPI1 to NPI2 Mapping"
        verbose_name_plural = "NPI1 to NPI2 Mappings"

    def __str__(self):
        return f'{self.npi1.npi} -> {self.npi2.npi}'


class NPI2ToPayerPlan(models.Model):
    npi2 = models.ForeignKey(NPI2, on_delete=models.CASCADE)
    payer_plan = models.ForeignKey(PayerPlan, on_delete=models.CASCADE)
    date_created = models.DateField(auto_now_add=True)
    date_updated = models.DateField(auto_now=True)

    class Meta:
        verbose_name = "NPI2 to Payer Plan Mapping"
        verbose_name_plural = "NPI2 to Payer Plan Mappings"

    def __str__(self):
        return f'{self.npi2.npi} -> {self.payer_plan.plan_id}'
    
class NPI1ToPayerPlan(models.Model):
    npi1 = models.ForeignKey(NPI1, on_delete=models.CASCADE)
    payer_plan = models.ForeignKey(PayerPlan, on_delete=models.CASCADE)
    date_created = models.DateField(auto_now_add=True)
    date_updated = models.DateField(auto_now=True)

    class Meta:
        verbose_name = "NPI1 to Payer Plan Mapping"
        verbose_name_plural = "NPI1 to Payer Plan Mappings"

    def __str__(self):
        return f'{self.npi1.npi} -> {self.payer_plan.plan_id}'


class HealthMap(models.Model):
    title = models.CharField(max_length=256)
    common_name = models.CharField(max_length=1024, db_index=True)
    logo_url = models.URLField(blank=True)
    root_url = models.URLField(blank=True)
    description = models.TextField()
    legal_business_entities = models.ManyToManyField(LegalBusinessEntity, blank=True)
    organizations_other = models.ManyToManyField(OrganizationOther, blank=True)
    npi1s = models.ManyToManyField(NPI1, blank=True)
    npi2s = models.ManyToManyField(NPI2, blank=True)
    individual_others = models.ManyToManyField(IndividualOther, blank=True)
    entities = models.ManyToManyField('self', blank=True)
    url = models.URLField(blank=True)
    direct_secure_messaging_inbound_email = models.EmailField(blank=True)
    logo = models.ImageField(upload_to='entity_logos/', blank=True, null=True)
    patient_portal_url = models.URLField(blank=True)
    patient_fhir_api_url = models.URLField(blank=True)
    provider_portal_url = models.URLField(blank=True)
    entity_fhir_api_url = models.URLField(blank=True)
    entity_bulk_fhir_api_url = models.URLField(blank=True)
    support_email = models.EmailField(blank=True)
    support_phone = models.CharField(max_length=32, blank=True)
    support_fax = models.CharField(max_length=32, blank=True)
    support_tty = models.CharField(max_length=32, blank=True)
    other_json_data = models.JSONField(blank=True, null=True)
    support_website_url = models.URLField(blank=True)
    date_created = models.DateField(auto_now_add=True)
    date_updated = models.DateField(auto_now=True)

    def __str__(self):
        return self.common_name

    @property
    def ori(self):
        return self.common_name
    
    @property
    def name(self):
        return self.title
    
    @property
    def to_json(self):
        return {
            "common_name": self.common_name,
            "title": self.title,
            "description": self.description,
            "entity_type": self.entity_type,
            "fein": self.fein,
            "url": self.url,
            "wellknown_url": self.wellknown_url,
            "direct_secure_messaging_inbound_email": self.direct_secure_messaging_inbound_email,
            "logo_url": self.logo_url,
            "patient_portal_url": self.patient_portal_url,
            "patient_fhir_api_url": self.patient_fhir_api_url,
            "provider_portal_url": self.provider_portal_url,
            "entity_fhir_api_url": self.entity_fhir_api_url,
            "entity_bulk_fhir_api_url": self.entity_bulk_fhir_api_url,
            "support_email": self.support_email,
            "support_phone": self.support_phone,
            "support_fax": self.support_fax,
            "support_tty": self.support_tty,
            "support_website_url": self.support_website_url,
            "other_json_data": self.other_json_data,
        }

    class Meta:
        verbose_name = "Health Map"
        verbose_name_plural = "Health Maps"
    