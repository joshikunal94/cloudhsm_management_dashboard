import React, { useState } from "react";
import { PropertyFilter } from "@cloudscape-design/components";

const KeysPropertiesFilter = ({ onFilterChange }) => {
    const [query, setQuery] = useState({ filterText: '', tokens: [] })

    const handleFilterChange = ({ detail }) => {
        console.log("Filter changed", detail)
        setQuery(detail)
        if (onFilterChange) {
            onFilterChange(detail)
        }
    }

    const filteringProperties = [
        {
            key: 'label',
            propertyLabel: 'Label',
            groupValuesLabel: 'Label values',
            operators: ['=', '!=']
        },
        {
            key: 'key_class',
            propertyLabel: 'Class',
            groupValuesLabel: 'Class values',
            operators: ['=', '!=']
        },
        {
            key: 'key_type',
            propertyLabel: 'Type',
            groupValuesLabel: 'Type values',
            operators: ['=', '!=']
        },
        {
            key: 'key_id',
            propertyLabel: 'Key ID',
            groupValuesLabel: 'Key ID values',
            operators: ['=', '!=']
        },
        {
            key: 'token',
            propertyLabel: 'Token',
            groupValuesLabel: 'Token values',
            operators: ['=']
        },
        {
            key: 'private',
            propertyLabel: 'Private',
            groupValuesLabel: 'Private values',
            operators: ['=']
        },
        {
            key: 'sensitive',
            propertyLabel: 'Sensitive',
            groupValuesLabel: 'Sensitive values',
            operators: ['=']
        },
        {
            key: 'extractable',
            propertyLabel: 'Extractable',
            groupValuesLabel: 'Extractable values',
            operators: ['=']
        },
        {
            key: 'local',
            propertyLabel: 'Local',
            groupValuesLabel: 'Local values',
            operators: ['=']
        },
        {
            key: 'modifiable',
            propertyLabel: 'Modifiable',
            groupValuesLabel: 'Modifiable values',
            operators: ['=']
        },
        {
            key: 'destroyable',
            propertyLabel: 'Destroyable',
            groupValuesLabel: 'Destroyable values',
            operators: ['=']
        }
    ];
    
    const filteringOptions = [
        { propertyKey: 'key_class', value: 'PRIVATE_KEY'},
        { propertyKey: 'key_class', value: 'PUBLIC_KEY'},
        { propertyKey: 'key_class', value: 'SECRET_KEY'},
        { propertyKey: 'key_type', value: 'RSA'},
        { propertyKey: 'key_type', value: 'EC'},
        { propertyKey: 'key_type', value: 'AES'},
        { propertyKey: 'token', value: 'true'},
        { propertyKey: 'token', value: 'false'},
        { propertyKey: 'private', value: 'true'},
        { propertyKey: 'private', value: 'false'},
        { propertyKey: 'sensitive', value: 'true'},
        { propertyKey: 'sensitive', value: 'false'},
        { propertyKey: 'extractable', value: 'true'},
        { propertyKey: 'extractable', value: 'false'},
        { propertyKey: 'local', value: 'true'},
        { propertyKey: 'local', value: 'false'},
        { propertyKey: 'modifiable', value: 'true'},
        { propertyKey: 'modifiable', value: 'false'},
        { propertyKey: 'destroyable', value: 'true'},
        { propertyKey: 'destroyable', value: 'false'}
    ]

    return <PropertyFilter
        query={query}
        onChange={handleFilterChange}
        filteringProperties={filteringProperties}
        filteringOptions={filteringOptions}
        filteringPlaceholder="Filter keys"
        filteringAriaLabel="Filter keys"
        expandToViewport
        hideOperations
        i18nStrings={{
            clearFiltersText: "Clear filters",
            applyActionText: "Apply",
            cancelActionText: "Cancel"
        }}
    />   
}

export default KeysPropertiesFilter;