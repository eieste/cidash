from jsonschema import validate, Draft7Validator, validators

#def extend_with_default(validator_class):
#    validate_properties = validator_class.VALIDATORS["properties"]
#    def set_defaults(validator, properties, instance, schema):
#
#        for property, subschema in properties.items():
#            if "default" in subschema:
#                instance.setdefault(property, subschema["default"])
#
#        for error in validate_properties(
#            validator,
#            properties,
#            instance,
#            schema,
#        ):
#            yield error
#    return validators.extend(
#        validator_class,
#        {"properties": set_defaults},
#    )


def extend_with_default(validator_class):
    validate_properties = validator_class.VALIDATORS["properties"]

    def set_defaults(validator, properties, instance, schema):
        for property_, subschema in properties.items():
            if "default" in subschema and not isinstance(instance, list):
                instance.setdefault(property_, subschema["default"])

        for error in validate_properties(
            validator, properties, instance, schema,
        ):
            yield error

    return validators.extend(
        validator_class, {"properties": set_defaults},
    )


DefaultValidatingDraft7Validator = extend_with_default(Draft7Validator)
