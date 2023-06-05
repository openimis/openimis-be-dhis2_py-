# DHIS2 metadata
# Copyright Patrick Delcoix <patrick@pmpd.eu>

from typing import Dict, List, Optional, Union, Tuple
from enum import Enum, IntEnum
from datetime import datetime, date
from uuid import uuid4
from pydantic import constr, BaseModel, ValidationError, validator, Field, AnyUrl, EmailStr
from dhis2.utils import *
from .dhis2Enum import FeatureType, ValueType
from .dhis2Type import uid, dateStr, datetimeStr, DHIS2Ref, DeltaDHIS2Ref, str50, str150, str230, str130, str255




class OrganisationUnit(MetadataSn):
    created: Optional[datetimeStr]
    lastUpdated: Optional[datetimeStr]
    description: Optional[str] # TBC
    openingDate: dateStr
    closedDate: Optional[dateStr]
    comment : Optional[str] # TBC
    featureType: Optional[FeatureType]  # NONE | MULTI_POLYGON | POLYGON | POINT | SYMBOL 
    coordinates: Optional[Tuple[float, float]]
    url: Optional[AnyUrl]
    contactPerson: Optional[str]
    address: Optional[str]
    email: Optional[EmailStr] # max 150
    phoneNumber: Optional[str150] # max 150
    parent: Optional[DHIS2Ref]




class OrganisationUnitGroup(MetadataSn):
    created: Optional[datetimeStr]
    lastUpdated: Optional[datetimeStr]
    description: Optional[str]
    organisationUnits:Union[List[DHIS2Ref],DeltaDHIS2Ref] = []
    # color
    # symbol

class OrganisationUnitGroupSet(Metadata):
    created: Optional[datetimeStr]
    lastUpdated: Optional[datetimeStr]
    description: Optional[str] # TBC
    organisationUnitGroups:Union[List[DHIS2Ref],DeltaDHIS2Ref] = []
    # datadimention
    # compulsory
    # include sub hiearchy

class OrganisationUnitGroupSetBundle(BaseModel):
    organisationUnitGroupSets:List[OrganisationUnitGroupSet]

class OrganisationUnitGroupBundle(BaseModel):
    organisationUnitGroups:List[OrganisationUnitGroup]

class OrganisationUnitBundle(BaseModel):
    organisationUnits:List[OrganisationUnit]

# OptionSet and options

class OptionSet(Metadata):
    valueType: ValueType
    options: List[DHIS2Ref]

class Option(BaseModel):
    id: Optional[uid]
    code: str50
    name: Union[float, int, dateStr, datetimeStr, str, DHIS2Ref, bool]
    # type, maybe other class of option are required
class OptionNumber(Option):
    name: float

class OptionInteger(Option):
    name: int

class OptionDate(Option):
    name: dateStr

class OptionDateTime(Option):
    name: datetimeStr

class OptionEmail(Option):
    name: EmailStr

class OptionText(Option):
    name: str130 # TBC

class OptionUid(Option): # for TEI, orgunit
    name: DHIS2Ref # TBC

class OptionBool(Option): # for YesNo YesOnly
    name: bool # TBC if not Emun

class OptionSetBundle(BaseModel):
    optionSets: List[OptionSet]

class OptionBundle(BaseModel):
    options: List[Option]

class Metadata(BaseModel):
    name: str230
    id: Optional[uid]
    code: Optional[str50]

class MetadataSn(Metadata):
    shortName: Optional[str50]


class Category(MetadataSn):
    pass
    
class CategoryBundle(BaseModel):
    categories: List[Category]
 
class CategoryCombo(MetadataSn):
    pass
 
class CategoryComboBundle(BaseModel):
    categoryCombos: List[Category]

 
class CategoryOption(MetadataSn):
    pass
 
 class CategoryOptionBundle(BaseModel):
    categoryOptions: List[Category]

