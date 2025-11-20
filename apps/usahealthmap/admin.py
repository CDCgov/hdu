from django.contrib import admin
from .models import PublicKeyType, PublicKey, PrivateKey
from .models import (EntityType, Entity, LegalBusinessEntity, NPI2, OrganizationOther, 
                     Payer, PayerPlan, IndividualOther, NPI1, HealthMap, APIEndpointType, 
                     APIEndpoint, PersonalIdentifier)


@admin.register(PersonalIdentifier)
class PersonalIdentifierAdmin(admin.ModelAdmin):
    list_display = ('issuer', 'identifier', 'description')
    search_fields = ('issuer__common_name', 'identifier', )
    ordering = ('issuer__common_name',)

@admin.register(HealthMap)
class HealthMapAdmin(admin.ModelAdmin):
    list_display = ('title', 'common_name', 'date_created', 'date_updated')
    search_fields = ('title', 'common_name')
    ordering = ('-date_created',)

@admin.register(APIEndpointType)
class APIEndpointTypeAdmin(admin.ModelAdmin):
    list_display = ('code', 'description')
    search_fields = ('code', 'description')
@admin.register(APIEndpoint)
class APIEndpointAdmin(admin.ModelAdmin):
    list_display = ('title', 'api_type', 'description')
    search_fields = ('title', 'api_type',)
    ordering = ('-date_created',)

@admin.register(LegalBusinessEntity)
class LegalBusinessEntityAdmin(admin.ModelAdmin):
    list_display = ('name', 'organization_type', 'date_created', 'date_updated')
    search_fields = ('fein', 'name', )
    ordering = ('-date_created',)

@admin.register(NPI2)
class NPI2Admin(admin.ModelAdmin):
    list_display = ('code', 'name', 'postal_code', 'date_created', 'date_updated')
    search_fields = ('code', 'name', 'postal_code')
    list_filter = ('date_created',)
    ordering = ('-date_created',)

@admin.register(OrganizationOther)
class OrganizationOtherAdmin(admin.ModelAdmin):
    list_display = ('common_name', 'name', 'description')
    search_fields = ('common_name', 'name')
    ordering = ('common_name',)

@admin.register(IndividualOther)
class IndividualOtherAdmin(admin.ModelAdmin):
    list_display = ('common_name', 'first_name', 'last_name',)
    search_fields = ('common_name', 'first_name', 'last_name', )
    ordering = ('last_name', 'first_name')

@admin.register(NPI1)
class NPI1Admin(admin.ModelAdmin):
    list_display = ('npi', 'first_name', 'last_name', 'date_created', 'date_updated')
    search_fields = ('npi', 'first_name', 'last_name',)
    ordering = ('-date_created',)



@admin.register(EntityType)
class EntityTypeAdmin(admin.ModelAdmin):
    list_display = ('code', 'description')
    search_fields = ('code', 'description')


@admin.register(Payer)
class PayerAdmin(admin.ModelAdmin):
    list_display = ('name', 'legal_business_entity')
    search_fields = ('name', )
@admin.register(PayerPlan)
class PayerPlanAdmin(admin.ModelAdmin):
    list_display = ('plan_id',  'date_created', 'date_updated' )
    search_fields = ('plan_id', 'payer_name', )
    ordering = ('date_updated',)


@admin.register(Entity)
class EntityAdmin(admin.ModelAdmin):
    list_display = ('entity_type', 'subject', 'common_name', 'subject_alternative_name', 'digest', 'root_url', 'title', 'date_created', 'date_updated' )
    search_fields = ('subject', 'common_name', 'subject_alternative_name', 'digest',)
    list_filter = ('entity_type',)
    ordering = ('entity_type',)



@admin.register(PublicKeyType)
class PublicKeyTypeAdmin(admin.ModelAdmin):
    list_display = ('code', 'description')
    search_fields = ('code', 'description')

@admin.register(PublicKey)
class PublicKeyAdmin(admin.ModelAdmin):
    list_display = ('identifier', 'kid')
    search_fields = ['identifier', 'kid']



@admin.register(PrivateKey)
class PrivateKeyAdmin(admin.ModelAdmin):
    list_display = ('identifier', 'kid')
    search_fields = ['identifier', 'kid', ]






